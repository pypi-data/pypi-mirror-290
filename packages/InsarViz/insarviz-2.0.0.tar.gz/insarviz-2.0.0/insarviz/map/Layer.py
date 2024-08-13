# -*- coding: utf-8 -*-

from typing import Any, Optional, overload, TYPE_CHECKING

import logging

import ctypes

from PyQt5.QtCore import Qt, pyqtSlot

from PyQt5.QtGui import QIcon, QPainter, QOpenGLContext, QOffscreenSurface

from OpenGL.GL import (
    GL_TEXTURE0, glUseProgram, glActiveTexture, glBindTexture, GL_TEXTURE_2D,
    glDrawElements, GL_TRIANGLES, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
    GL_UNSIGNED_INT, glBindVertexArray,
    GL_RGB, GL_RGB32F, GL_RGBA, GL_RGBA32F, GL_FLOAT, GL_RG32F, GL_RG,
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER,
    GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST,
    GL_PIXEL_UNPACK_BUFFER, GL_STREAM_DRAW,
    glGenTextures, glTexParameter, glGenerateMipmap,
    glGenBuffers, glBindBuffer, glBufferData,
    glTexImage2D, glDeleteBuffers, glDeleteTextures, glDeleteProgram,
    GL_TEXTURE_1D,
    GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE, GL_TEXTURE_WRAP_T,
    glEnable, GL_BLEND, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
)

from pyqtgraph.colormap import ColorMap

from OpenGL.constant import IntConstant

import numpy as np

import os

import rasterio

from rasterio.vrt import WarpedVRT

from insarviz.map.TreeModel import TreeItem, TreeModel

from insarviz.map.TreeItemAttribute import (
    TreeItemAttribute, TreeItemColormapAttribute, TreeItemFloatAttribute
)

from insarviz.map.gl_utils import set_uniform, create_shader, create_program

from insarviz.map.Shaders import (
    DATA_UNIT, PALETTE_UNIT, VERT_SHADER, PALETTE_SHADER, MAP_SHADER, GEOMAP_SHADER, ALPHA_SHADER
)

from insarviz.linalg import matrix

from insarviz.colormaps import my_colormaps, create_colormap_texture

from insarviz.Loader import Loader

from insarviz.ColormapWidget import ColormapWidget

if TYPE_CHECKING:
    from insarviz.map.MapModel import MapModel


logger = logging.getLogger(__name__)


class Layer(TreeItem):

    kind: str = "layer"  # description of the class, used in RemoveTreeItemCommand
    removable: bool = True
    renamable: bool = True
    # TODO look here https://github.com/qgis/QGIS/tree/master/images/themes/default
    icon: QIcon = QIcon()

    def __init__(self, name: str):
        super().__init__()
        # whether the layer is visible in MapView or not, also checkbox state in LayerView
        self.visible: bool = True
        self.name: str = name

    # see https://mypy.readthedocs.io/en/stable/more_types.html#function-overloading
    @overload
    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix) -> None: ...

    @overload
    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: QPainter, vao_id: int) -> None: ...

    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: Optional[QPainter] = None, vao_id: Optional[int] = None) -> None:
        """
        Shall be implemented by subclasses.
        Display the layer using either OpenGL commands or painter.

        Parameters
        ----------
        view_matrix : matrix.Matrix
            Transform world coordinates into view coordinates.
        projection_matrix : matrix.Matrix
            Transform view coordinates into clip coordinates (OpenGL only)
        painter : QPainter, optional
            QPainter provided by the view. If painter is given then vao_id must be given aswell.
        vao_id : int, optional
            OpenGL Vertex Array Object identifier, the VAO is a square mapped with a texture.
        """
        raise NotImplementedError

    def data(self, column: int, role: int) -> Any:
        if column == TreeModel.remove_column:
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self.name
        if role == Qt.CheckStateRole:
            return Qt.Checked if self.visible else Qt.Unchecked
        if role == Qt.DecorationRole:
            return self.icon
        return None

    def flags(self, flags: Qt.ItemFlags, column: int) -> Qt.ItemFlags:
        if column == 0:
            # enable visibility checkbox and drag&drop
            flags = flags | Qt.ItemIsUserCheckable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
            if self.renamable:
                # enable name edition
                flags = flags | Qt.ItemIsEditable
        elif column == TreeModel.remove_column:
            if self.removable:
                # enable the remove button
                flags = flags | Qt.ItemIsEditable
        return flags

    def set_data(self, value: Any, column: int, role: int) -> bool:
        if column != 0:
            return False
        if role == Qt.CheckStateRole:
            self.visible = True if value == Qt.Checked else False
            return True
        if role == Qt.EditRole and self.renamable:
            self.name = value
            return True
        return False

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = {}
        output["kind"] = self.kind
        output["name"] = self.name
        output["visible"] = self.visible
        return output


class OpenGLLayer(Layer):

    # QOpenGLContext shared with every other contexts, set by ts_viz.MainWindow.initUI
    context: Optional[QOpenGLContext] = None
    # QOffscreenSurface to use OpenGL commands, set by ts_viz.MainWindow.initUI
    offscreen_surface: Optional[QOffscreenSurface] = None

    def __init__(self, name: str):
        super().__init__(name)
        # dict of texture_unit:(texture_target, texture_id)
        self.textures: dict[int, tuple[int, int]] = {}
        self.alpha: float = 1.
        self.add_child(TreeItemFloatAttribute(self, "alpha", name="alpha", vmin=0., vmax=1.,
                                              tooltip="transparency (between 0 and 1)"))
        assert self.context is not None, "OpengGLLayer.init: no OpenGL shared context"
        assert self.context.isValid(), "OpenGLLayer.init: OpenGL shared context not valid"
        assert self.offscreen_surface is not None, "OpengGLLayer.init: no QOffscreenSurface"
        assert self.offscreen_surface.isValid(), "OpenGLLayer.init: QOffscreenSurface not valid"
        self.context.makeCurrent(self.offscreen_surface)
        self.program: int = self.build_program()
        self.context.doneCurrent()

    def build_program(self) -> int:
        """
        Shall be implemented by subclasses.
        Computes the OpenGL shader program used by the layer, possibly sets some constant uniforms
        to the program (such as texture unit for example) and then returns its id.
        A valid shared OpenGL context is supposed to already be current when this method is called.

        Note that texture unit shall be given as integer (without GL_TEXTURE0) with set_uniform.

        Returns
        -------
        program : int
            the OpenGL shader program id
        """
        # shall be implented by subclasses
        raise NotImplementedError

    @pyqtSlot(IntConstant, IntConstant, int)
    def set_texture(self, texture_unit: IntConstant, texture_target: IntConstant, tex_id: int) -> None:
        """
        Set (texture_target, tex_id) as value for key texture_unit in self.textures dictionnary.
        That information is used by self.show to bind the correct texture to the texture unit when
        displaying the layer.

        Parameters
        ----------
        texture_unit : int
            texture unit for glActiveTexture, shall be on the form GL_TEXTURE0 + ...
        texture_target : int
            texture target for glBindTexture (for example  GL_TEXTURE_1D or GL_TEXTURE_2D)
        tex_id : int
            texture id for glBindTexture (created with glGenTextures)
        """
        self.textures[texture_unit] = (texture_target, tex_id)

    def show(self, view_matrix: matrix.Matrix, projection_matrix: matrix.Matrix,
             painter: Optional[QPainter] = None, vao_id: Optional[int] = None,
             blend: bool = True) -> None:
        if painter is not None:
            painter.beginNativePainting()
            # a VAO is required because QPainter bound its own VAO so we need to bind back our own
            assert vao_id is not None, "OpenGLLayer: vao_id is required when using QPainter"
        if blend:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if vao_id is not None:
            glBindVertexArray(vao_id)
        # bind textures to texture units
        for texture_unit, (texture_target, texture_id) in self.textures.items():
            glActiveTexture(texture_unit)
            glBindTexture(texture_target, texture_id)
        glUseProgram(self.program)
        # set view and projection matrixes
        set_uniform(self.program, 'view_matrix', view_matrix)
        set_uniform(self.program, 'projection_matrix', projection_matrix)
        # set alpha value
        set_uniform(self.program, 'alpha', self.alpha)
        # draw the two triangles of the VAO that form a square
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        if vao_id is not None:
            glBindVertexArray(0)
        if painter is not None:
            painter.endNativePainting()

    def __del__(self):
        """
        Free textures and shader program from the VRAM when the layer is destroyed to prevent
        memory leaks.
        """
        self.context.makeCurrent(self.offscreen_surface)
        # delete the OpenGL textures
        for _, (_, texture_id) in self.textures.items():
            glDeleteTextures(1, [texture_id])
        # delete the OpenGL shaders program
        glDeleteProgram(self.program)
        self.context.doneCurrent()

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["alpha"] = self.alpha
        return output


class MainLayer(OpenGLLayer):

    removable: bool = False
    renamable: bool = False
    kind: str = "main layer"

    def __init__(self, map_model: "MapModel"):
        self.width: int = map_model.tex_width
        self.height: int = map_model.tex_height
        super().__init__("Main Layer")
        map_model.texture_changed.connect(self.set_texture)
        map_model.v0_v1_changed.connect(self.set_v0_v1)

    def build_program(self) -> int:
        program: int = create_program(
            create_shader(GL_VERTEX_SHADER, VERT_SHADER),
            create_shader(GL_FRAGMENT_SHADER, PALETTE_SHADER),
            create_shader(GL_FRAGMENT_SHADER, ALPHA_SHADER),
            create_shader(GL_FRAGMENT_SHADER, MAP_SHADER)
        )
        glUseProgram(program)
        model_matrix: matrix.Matrix = matrix.scale(self.width, self.height)
        set_uniform(program, 'model_matrix', model_matrix)
        set_uniform(program, 'values', DATA_UNIT)
        set_uniform(program, 'palette', PALETTE_UNIT)
        set_uniform(program, 'v0', 0.)
        set_uniform(program, 'v1', 1.)
        glUseProgram(0)
        return program

    def data(self, column: int, role: int) -> Any:
        if column == 0 and role == Qt.ToolTipRole:
            return "Main data layer, insar data cube"
        return super().data(column, role)

    # connected to MapModel.v0_v1_changed
    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        """Update v0 and v1."""
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.context.makeCurrent(self.offscreen_surface)
        glUseProgram(self.program)
        set_uniform(self.program, 'v0', float(v0))
        set_uniform(self.program, 'v1', float(v1))
        self.context.doneCurrent()

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "MainLayer":
        assert input_dict["kind"] == cls.kind
        layer = MainLayer(map_model)
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        return layer


class RasterLayer(OpenGLLayer):

    bandcounts_allowed: tuple = ()
    nb_band: int = 0

    def __init__(self, name: str, model: "MapModel", filepath: str):
        self.model_matrix: matrix.Matrix = matrix.scale(model.tex_width, model.tex_height)
        super().__init__(name)
        with rasterio.open(filepath) as file:
            assert model.loader.dataset is not None
            assert file.count in self.bandcounts_allowed, (f"{self.__class__} requires an image with "
                                                           f"{' or '.join(str(i) for i in self.bandcounts_allowed)} "
                                                           "bands")
            assert ((file.crs is not None and model.loader.dataset.crs is not None) or
                    (file.shape == model.loader.dataset.shape)), (f"{self.__class__} requires a ",
                                                                  "geolocalized image or an image "
                                                                  "of same shape than the dataset")
            assert self.context is not None
            assert self.context.isValid()
            assert self.offscreen_surface is not None
            assert self.offscreen_surface.isValid()
            self.filepath = filepath
            self.name = os.path.basename(filepath)
            self.add_child(TreeItemAttribute(self, "filepath", tooltip=filepath, editable=False))
            # warp the image if geolocated
            if (file.crs is not None and model.loader.dataset.crs is not None):
                with WarpedVRT(file, crs=model.loader.dataset.crs) as vrt:
                    img = np.empty((*vrt.shape, self.nb_band), dtype=np.float32)
                    band_max = min(file.count, self.nb_band)
                    data = vrt.read(vrt.indexes[:band_max], out_dtype=np.float32)
                    # transpose to change shape from (bands, rows, columns) to (rows, columns, bands)
                    img[:, :, :band_max] = np.transpose(data, [1, 2, 0])
                    # model matrix transforms coordinates inside the square (0,1) to coordinates in
                    # pixels relatively to the dataset
                    self.model_matrix = matrix.from_rasterio_Affine(
                        ~model.loader.dataset.transform
                        * vrt.transform
                        * rasterio.Affine.scale(*vrt.shape[::-1]))
                    self.context.makeCurrent(self.offscreen_surface)
                    glUseProgram(self.program)
                    set_uniform(self.program, 'model_matrix', self.model_matrix)
                    glUseProgram(0)
                    self.context.doneCurrent()
            else:
                img = np.empty((*file.shape, self.nb_band), dtype=np.float32)
                band_max = min(file.count, self.nb_band)
                data = file.read(file.indexes[:band_max], out_dtype=np.float32)
                # transpose to change shape from (bands, rows, columns) to (rows, columns, bands)
                img[:, :, :band_max] = np.transpose(data, [1, 2, 0])
            # if alpha band is missing build it from nodata
            if file.count == self.nb_band-1:
                img[:, :, self.nb_band-1] = 1.
                if all(x is not None for x in file.nodatavals):
                    img[:, :, self.nb_band-1][np.logical_or.reduce(
                        [img[:, :, i] == file.nodatavals[i] for i in range(self.nb_band-1)])] = 0.
                elif file.nodata is not None:
                    img[:, :, self.nb_band-1][np.logical_or.reduce(
                        [img[:, :, i] == file.nodata for i in range(self.nb_band-1)])] = 0.
            # transform from integer to float if needed
            for i, dtype in enumerate(file.dtypes):
                if np.dtype(dtype) == np.uint8:
                    img[:, :, i] = img[:, :, i] / 255
            # set the value of others band to 0 when alpha is 0
            img[:, :, :self.nb_band-1][img[:, :, self.nb_band-1] == 0] = 0.
            # set the value of alpha band to 1 when > 0
            img[:, :, self.nb_band-1][img[:, :, self.nb_band-1] > 0] = 1.
            # create the texture
            self.load_image(img)

    def load_image(self, img: np.ndarray):
        # shall be implented by subclasses
        raise NotImplementedError

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["filepath"] = os.path.relpath(self.filepath, start=filedir)
        return output


class Raster1BLayer(RasterLayer):

    icon: QIcon = QIcon()
    kind: str = "raster 1B layer"
    bandcounts_allowed = (1, 2)
    nb_band: int = 2
    outlier_threshold = Loader.outlier_threshold
    autorange_threshold = ColormapWidget.autorange_threshold

    def __init__(self, name: str, model: "MapModel", filepath: str):
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            Raster1BLayer.icon = QIcon('icons:raster1B.svg')
        self.colormap: ColorMap = my_colormaps[[c.name for c in my_colormaps].index('viridis')]
        self.colormap_v0: float = 0.  # minimum value for colorbar range (default 5 percentile)
        self.colormap_v1: float = 1.  # maximum value for colorbar range (default 95 percentile)
        super().__init__(name, model, filepath)
        self.set_colormap(self.colormap)
        self.add_child(TreeItemColormapAttribute(self, "colormap", tooltip="colormap"))

    def load_image(self, img: np.ndarray):
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        h, w, d = img.shape
        self.context.makeCurrent(self.offscreen_surface)
        glActiveTexture(GL_TEXTURE0+0)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        pixel_buffer = glGenBuffers(1)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pixel_buffer)
        float_size = ctypes.sizeof(ctypes.c_float)
        glBufferData(GL_PIXEL_UNPACK_BUFFER, w*h*d*float_size, img, GL_STREAM_DRAW)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RG32F, w, h, 0, GL_RG, GL_FLOAT, None)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)
        glDeleteBuffers(1, [pixel_buffer])
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.context.doneCurrent()
        assert texture_id != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0+DATA_UNIT, GL_TEXTURE_2D, texture_id)
        # compute histogram
        self.histogram = self.compute_histogram(img)
        # compute v0 v1
        self.set_v0_v1(*self.autorange_from_hist(*self.histogram))

    def compute_histogram(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        data = img[:, :, 0][img[:, :, 1] > 0]
        # build bins excluding the most extreme percentiles
        bins = np.histogram_bin_edges(data, bins="fd", range=np.percentile(data, [1, 99]))
        # add bins at the start and end for outliers
        bins = np.array([np.min(data), *bins, np.max(data)])
        return np.histogram(data, bins=bins)

    autorange_from_hist = ColormapWidget.autorange_from_hist

    def build_program(self) -> int:
        program: int = create_program(
            create_shader(GL_VERTEX_SHADER, VERT_SHADER),
            create_shader(GL_FRAGMENT_SHADER, PALETTE_SHADER),
            create_shader(GL_FRAGMENT_SHADER, ALPHA_SHADER),
            create_shader(GL_FRAGMENT_SHADER, MAP_SHADER)
        )
        glActiveTexture(GL_TEXTURE0)
        glUseProgram(program)
        set_uniform(program, 'model_matrix', self.model_matrix)
        set_uniform(program, 'values', DATA_UNIT)
        set_uniform(program, 'palette', PALETTE_UNIT)
        set_uniform(program, 'v0', self.colormap_v0)
        set_uniform(program, 'v1', self.colormap_v1)
        glUseProgram(0)
        return program

    @pyqtSlot(ColorMap)
    def set_colormap(self, colormap: ColorMap) -> None:
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.colormap = colormap
        self.context.makeCurrent(self.offscreen_surface)
        _, old_texture_id = self.textures.get(GL_TEXTURE0+PALETTE_UNIT, (0, 0))
        glDeleteTextures(1, [old_texture_id])
        colormap_tex_id = create_colormap_texture(colormap, GL_TEXTURE0+PALETTE_UNIT)
        self.context.doneCurrent()
        self.set_texture(GL_TEXTURE0+PALETTE_UNIT, GL_TEXTURE_1D, colormap_tex_id)

    @pyqtSlot(float, float)
    def set_v0_v1(self, v0: float, v1: float) -> None:
        self.colormap_v0 = v0
        self.colormap_v1 = v1
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.context.makeCurrent(self.offscreen_surface)
        glUseProgram(self.program)
        set_uniform(self.program, 'v0', self.colormap_v0)
        set_uniform(self.program, 'v1', self.colormap_v1)
        glUseProgram(0)
        self.context.doneCurrent()

    def to_dict(self, filedir: str) -> dict[str, Any]:
        output: dict[str, Any] = super().to_dict(filedir)
        output["colormap"] = self.colormap.name
        output["colormap_v0"] = self.colormap_v0
        output["colormap_v1"] = self.colormap_v1
        return output

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "Raster1BLayer":
        assert input_dict["kind"] == cls.kind
        assert "filepath" in input_dict
        name = input_dict.get("name", "raster1B layer")
        layer = Raster1BLayer(name, map_model, input_dict["filepath"])
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        if "colormap" in input_dict:
            try:
                colormap = my_colormaps[[c.name for c in my_colormaps].index(
                    input_dict["colormap"])]
                layer.set_colormap(colormap)
            except ValueError:
                pass
        if "colormap_v0" in input_dict and "colormap_v1" in input_dict:
            v0, v1 = input_dict["colormap_v0"], input_dict["colormap_v1"]
            if isinstance(v0, float) and isinstance(v1, float):
                layer.set_v0_v1(v0, v1)
            else:
                logger.warning(f"layer {name}: colormap_v0 and/or colormap_v1 are not float, thus"
                               " they are ignored")
        return layer


class RasterRGBLayer(RasterLayer):

    icon: QIcon = QIcon()
    kind: str = "raster RGB layer"
    bandcounts_allowed = (3, 4)
    nb_band: int = 4

    def __init__(self, name: str, model: "MapModel", filepath: str):
        super().__init__(name, model, filepath)
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            RasterRGBLayer.icon = QIcon('icons:rasterRGB.svg')

    def load_image(self, img: np.ndarray):
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        h, w, d = img.shape
        self.context.makeCurrent(self.offscreen_surface)
        glActiveTexture(GL_TEXTURE0+0)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        pixel_buffer = glGenBuffers(1)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pixel_buffer)
        float_size = ctypes.sizeof(ctypes.c_float)
        glBufferData(GL_PIXEL_UNPACK_BUFFER, w*h*d*float_size, img, GL_STREAM_DRAW)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, w, h, 0, GL_RGBA, GL_FLOAT, None)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)
        glDeleteBuffers(1, [pixel_buffer])
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.context.doneCurrent()
        assert texture_id != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0, GL_TEXTURE_2D, texture_id)

    def build_program(self) -> int:
        program: int = create_program(create_shader(GL_VERTEX_SHADER, VERT_SHADER),
                                      create_shader(GL_FRAGMENT_SHADER, ALPHA_SHADER),
                                      create_shader(GL_FRAGMENT_SHADER, GEOMAP_SHADER))
        glActiveTexture(GL_TEXTURE0)
        glUseProgram(program)
        set_uniform(program, 'geomap_texture', 0)
        set_uniform(program, 'model_matrix', self.model_matrix)
        glUseProgram(0)
        return program

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "RasterRGBLayer":
        assert input_dict["kind"] == cls.kind
        assert "filepath" in input_dict
        name = input_dict.get("name", "rasterRGB layer")
        layer = RasterRGBLayer(name, map_model, input_dict["filepath"])
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        return layer


class GeomapLayer(OpenGLLayer):

    icon: QIcon = QIcon()
    kind: str = "WMS layer"

    def __init__(self, name: str, model: "MapModel"):
        self.model_matrix: matrix.Matrix = matrix.scale(model.tex_width, model.tex_height)
        super().__init__(name)
        if self.icon.isNull():
            # cannot be initialized in the class declaration because:
            # "QIcon needs a QGuiApplication instance before the icon is created." see QIcon doc
            GeomapLayer.icon = QIcon('icons:WMS.svg')
        img = model.loader.load_geomap()
        # change img.shape from (bands, rows, columns) to (rows, columns, bands)
        img = np.transpose(img, [1, 2, 0])
        if img.dtype == "uint8":
            # TODO : give correct parameters for integer texture to glTexImage2D instead
            img = img.astype(np.float32)/255
        h, w, d = img.shape
        assert self.context is not None
        assert self.context.isValid()
        assert self.offscreen_surface is not None
        assert self.offscreen_surface.isValid()
        self.context.makeCurrent(self.offscreen_surface)
        glActiveTexture(GL_TEXTURE0+0)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        pixel_buffer = glGenBuffers(1)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pixel_buffer)
        float_size = ctypes.sizeof(ctypes.c_float)
        glBufferData(GL_PIXEL_UNPACK_BUFFER, w*h*d*float_size, img, GL_STREAM_DRAW)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, w, h, 0, GL_RGB, GL_FLOAT, None)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)
        glDeleteBuffers(1, [pixel_buffer])
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.context.doneCurrent()
        assert texture_id != 0, f"{self.name} layer: cannot load image texture in OpenGl"
        self.set_texture(GL_TEXTURE0, GL_TEXTURE_2D, texture_id)

    def build_program(self) -> int:
        program: int = create_program(create_shader(GL_VERTEX_SHADER, VERT_SHADER),
                                      create_shader(GL_FRAGMENT_SHADER, ALPHA_SHADER),
                                      create_shader(GL_FRAGMENT_SHADER, GEOMAP_SHADER))
        glActiveTexture(GL_TEXTURE0)
        glUseProgram(program)
        set_uniform(program, 'geomap_texture', 0)
        set_uniform(program, 'model_matrix', self.model_matrix)
        glUseProgram(0)
        return program

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any], map_model: "MapModel") -> "GeomapLayer":
        assert input_dict["kind"] == cls.kind
        name = input_dict.get("name", "geomap layer")
        layer = GeomapLayer(name, map_model)
        if "visible" in input_dict:
            layer.visible = input_dict["visible"]
        if "alpha" in input_dict:
            layer.alpha = input_dict["alpha"]
        return layer

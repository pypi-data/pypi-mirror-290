#!/usr/bin/env python3
""" Main module for insarviz time-series visualization tool.

Create the main window and manage links with other sub-windows and loading
data modules.
Contains the following class:
    * MainWindow

and function:
    * main
"""

from typing import Optional, Any

import logging

import os

import numpy as np

import datetime

import json

import rasterio.warp

from PyQt5.QtWidgets import (
    QSizePolicy, QApplication, QLabel, QWidget,
    QMainWindow, QFileDialog, QToolBar, QUndoStack,
    QDockWidget, QAction, QActionGroup,
    QVBoxLayout, QHBoxLayout, QSplitter, QMessageBox
)

from PyQt5.QtGui import (
    QPixmap, QIcon, QKeySequence, QSurfaceFormat, QOpenGLContext, QOffscreenSurface
)

from PyQt5.QtCore import (
    Qt, QCoreApplication,
    pyqtSlot, QDir
)

import pyqtgraph as pg
import pyqtgraph.exporters
from insarviz.exporters.myCSVExporter import myCSVExporter

from insarviz.Loader import Loader
from insarviz.BandSlider import BandSlider
from insarviz.ColormapWidget import ColormapWidget
from insarviz.map.MapModel import MapModel
from insarviz.map.MapView import MapView
from insarviz.map.MinimapView import MinimapView
from insarviz.plot.PlotModel import PlotModel
from insarviz.plot.TemporalPlotView import TemporalPlotWindow
from insarviz.plot.SpatialPlotView import SpatialPlotWindow
import insarviz.version as version

from insarviz.custom_widgets import IconDockWidget

from insarviz.utils import openUrl

from insarviz.map.Layer import OpenGLLayer, GeomapLayer, RasterRGBLayer, Raster1BLayer  # TODO TEST
from insarviz.map.LayerView import LayerView

logging.getLogger("rasterio").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    TODO Docstring for MainWindow.
    """

    def __init__(self, filepath: Optional[str] = None, config_dict=None):
        """
        :filepath: the file to load
        :config_dict: the configuration dictionary
        """
        super().__init__()
        self.config_dict = config_dict
        self.current_filepath: Optional[str] = filepath
        self.initUI()
        # replace csv exporter by custom csv exporter:
        pg.exporters.Exporter.Exporters.pop(
            pg.exporters.Exporter.Exporters.index(
                pyqtgraph.exporters.CSVExporter))
        myCSVExporter.register()

    def initUI(self) -> None:
        """
        initialize user interface

        :filepath: the file to load
        :returns: None

        """
        # various init:
        self.setWindowTitle("InsarViz")
        self.setMouseTracking(True)
        self.setDockNestingEnabled(True)
        self.undo_stack: QUndoStack = QUndoStack(self)

        # Loader:
        self.loader: Loader = Loader()

        # Models:
        context: QOpenGLContext = QOpenGLContext()
        context.setShareContext(QOpenGLContext.globalShareContext())
        context.create()
        if not context.isValid():
            QMessageBox.critical(self, "Insarviz", "OpenGL error: context is not valid")
            raise RuntimeError("Global OpenGL shared context cannot be created")
        offscreen_surface = QOffscreenSurface()
        offscreen_surface.setFormat(context.format())
        offscreen_surface.create()
        OpenGLLayer.context = context
        OpenGLLayer.offscreen_surface = offscreen_surface
        self.map_model = MapModel(self.loader, context, offscreen_surface)
        self.plot_model = PlotModel(self.loader)
        self.map_model.layer_model.selection_initialized.connect(self.plot_model.on_selection_init)
        self.map_model.closed.connect(self.plot_model.close)
        self.map_model.closed.connect(self.undo_stack.clear)
        self.map_model.layer_model.add_undo_command.connect(self.undo_stack.push)

        # Layer manager
        self.layer_model = self.map_model.layer_model
        self.layer_widget = LayerView(self.layer_model)
        # new geomap action
        self.new_geomap_action = QAction(QIcon('icons:WMS.svg'), "New Geomap", self)
        self.new_geomap_action.triggered.connect(lambda: self.map_model.layer_model.add_layer(
            GeomapLayer("test", self.map_model)))
        # new raster1B action
        self.new_raster1B_action = QAction(QIcon('icons:raster1B.svg'), "New Raster1B", self)
        self.new_raster1B_action.triggered.connect(self.new_raster1B)
        # new rasterRGB action
        self.new_rasterRGB_action = QAction(QIcon('icons:rasterRGB.svg'), "New RasterRGB", self)
        self.new_rasterRGB_action.triggered.connect(self.new_rasterRGB)
        # show all action
        self.layer_showall_action = QAction(QIcon('icons:eye_open.svg'), "Show all", self)
        self.layer_showall_action.setToolTip("Show all layers")
        self.layer_showall_action.triggered.connect(self.layer_model.show_all_layers)
        # hide all action
        self.layer_hideall_action = QAction(QIcon('icons:eye_closed.svg'), "Hide all", self)
        self.layer_hideall_action.setToolTip("Hide all layers")
        self.layer_hideall_action.triggered.connect(self.layer_model.hide_all_layers)
        # move up action
        self.layer_moveup_action = QAction(QIcon('icons:arrowup.png'), "Move Up", self)
        self.layer_moveup_action.setToolTip("Move up layer")
        self.layer_moveup_action.triggered.connect(lambda: self.layer_model.move_layer_up(
            self.layer_widget.proxy_model.mapToSource(
                self.layer_widget.selectionModel().currentIndex())))
        self.layer_model.current_movable_up.connect(self.layer_moveup_action.setEnabled)
        # move down action
        self.layer_movedown_action = QAction(QIcon('icons:arrowdown.png'), "Move Down", self)
        self.layer_movedown_action.setToolTip("Move down layer")
        self.layer_movedown_action.triggered.connect(lambda: self.layer_model.move_layer_down(
            self.layer_widget.proxy_model.mapToSource(
                self.layer_widget.selectionModel().currentIndex())))
        self.layer_model.current_movable_down.connect(self.layer_movedown_action.setEnabled)
        # remove action
        self.layer_remove_action = QAction(QIcon('icons:remove.png'), "Remove", self)
        self.layer_remove_action.setToolTip("Remove item")
        self.layer_remove_action.setShortcuts(QKeySequence.Delete)
        self.layer_remove_action.triggered.connect(lambda: self.layer_model.remove(
            self.layer_widget.proxy_model.mapToSource(
                self.layer_widget.selectionModel().currentIndex())))
        self.layer_model.current_removable.connect(self.layer_remove_action.setEnabled)
        # action group
        layer_action_group = QActionGroup(self)
        layer_action_group.addAction(self.layer_moveup_action)
        layer_action_group.addAction(self.layer_movedown_action)
        layer_action_group.addAction(self.layer_showall_action)
        layer_action_group.addAction(self.layer_hideall_action)
        layer_action_group.addAction(self.layer_remove_action)
        layer_action_group.addAction(self.new_geomap_action)
        layer_action_group.addAction(self.new_raster1B_action)
        layer_action_group.addAction(self.new_rasterRGB_action)
        layer_action_group.setExclusive(False)
        layer_action_group.setDisabled(True)
        self.map_model.closed.connect(lambda: layer_action_group.setDisabled(True))
        self.map_model.opened.connect(lambda: layer_action_group.setEnabled(True))
        # layout
        layer_layout = QVBoxLayout()
        layer_toolbar = QToolBar(self)
        layer_toolbar.addAction(self.layer_moveup_action)
        layer_toolbar.addAction(self.layer_movedown_action)
        layer_toolbar.addAction(self.layer_showall_action)
        layer_toolbar.addAction(self.layer_hideall_action)
        layer_toolbar.addAction(self.layer_remove_action)
        layer_layout.addWidget(layer_toolbar)
        layer_layout.addWidget(self.layer_widget)
        layer_manager_widget = QWidget()
        layer_manager_widget.setLayout(layer_layout)
        self.layer_dockwidget = QDockWidget('Layers', self)
        self.layer_dockwidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.layer_dockwidget.setWidget(layer_manager_widget)

        # Map:
        self.map_widget = MapView(self.map_model, self)
        self.map_widget.setMouseTracking(True)
        self.map_widget.pointer_changed.connect(self.plot_model.update_pointer)
        self.map_widget.interaction_changed.connect(self.on_mapview_interaction_changed)
        self.plot_model.updated_pointer_info.connect(self.map_widget.update_mouse_tooltip)

        # Minimap
        self.minimap_widget = MinimapView(self.map_model, self)
        self.minimap_widget.pan_map_view.connect(self.map_widget.pan)
        self.minimap_widget.zoom_map_view.connect(self.map_widget.zoom)
        self.minimap_widget.set_center_map_view.connect(self.map_widget.set_view_center)
        self.map_widget.viewport_matrix_changed.connect(
            self.minimap_widget.update_mapview_viewport_matrix)
        self.minimap_dock_widget = QDockWidget('Minimap', self)
        self.minimap_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.minimap_dock_widget.setWidget(self.minimap_widget)

        # Colormap
        self.colormap_widget = ColormapWidget(self)
        # connect signals to slots
        self.map_model.closed.connect(lambda: self.colormap_widget.setDisabled(True))
        self.map_model.opened.connect(lambda: self.colormap_widget.setEnabled(True))
        self.map_model.total_hist_changed.connect(self.colormap_widget.set_total_histogram)
        self.map_model.band_hist_changed.connect(self.colormap_widget.set_band_histogram)
        self.map_model.request_colormap.connect(self.colormap_widget.set_colormap)
        self.map_model.v0_v1_changed.connect(self.colormap_widget.set_v0_v1)
        self.loader.data_units_loaded.connect(self.colormap_widget.set_data_units)
        self.colormap_widget.colormap_changed.connect(self.map_model.set_colormap)
        self.colormap_widget.v0_v1_changed.connect(self.map_model.set_v0_v1)
        self.colormap_widget.compute_histograms.connect(self.loader.compute_histograms)

        # dates slider:
        self.band_slider = BandSlider(self.loader)
        self.band_slider.value_changed.connect(self.map_model.show_band)
        self.map_model.closed.connect(self.band_slider.on_close)
        self.loader.data_loaded.connect(self.band_slider.on_data_loaded)

        # plot windows:
        # temporal window
        self.temporal_plot_window = TemporalPlotWindow(self.plot_model)
        self.band_slider.value_changed.connect(
            self.temporal_plot_window.plot_widget.date_marker.on_slider_changed)
        self.temporal_plot_window.plot_widget.date_marker.pos_changed.connect(
            self.band_slider.set_value)
        self.temporal_plot_dock = IconDockWidget(
            "Temporal profile", self, QIcon('icons:temporal.svg'))
        self.temporal_plot_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.temporal_plot_dock.setWidget(self.temporal_plot_window)
        self.addDockWidget(Qt.RightDockWidgetArea, self.temporal_plot_dock)
        # spatial window
        self.spatial_plot_window = SpatialPlotWindow(self.plot_model)
        self.spatial_plot_dock = IconDockWidget(
            "Spatial profile", self, QIcon('icons:spatial.svg'))
        self.spatial_plot_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.spatial_plot_dock.setWidget(self.spatial_plot_window)
        self.addDockWidget(Qt.RightDockWidgetArea, self.spatial_plot_dock)
        # layout
        self.tabifyDockWidget(self.temporal_plot_dock, self.spatial_plot_dock)
        self.temporal_plot_dock.hide()
        self.spatial_plot_dock.hide()

        # Main layout:
        self.main_widget = QSplitter(Qt.Horizontal)
        self.main_widget.setChildrenCollapsible(False)
        self.map_band_slider_layout = QVBoxLayout()
        self.map_band_slider_layout.addWidget(self.band_slider)
        self.map_band_slider_layout.addWidget(self.map_widget, stretch=1)
        self.map_band_slider_widget = QWidget()
        self.map_band_slider_widget.setLayout(self.map_band_slider_layout)
        self.main_widget.addWidget(self.map_band_slider_widget)
        self.main_widget.addWidget(self.colormap_widget)
        self.setCentralWidget(self.main_widget)
        self.main_widget.resize(250, 250)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.layer_dockwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.minimap_dock_widget)

        # Status bar / footer
        # Logo & version
        self.logo_widget = QLabel(self)
        pix = QPixmap('icons:logo_insarviz.png')
        self.logo_widget.setPixmap(
            pix.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_text_widget = QLabel(f"InsarViz v.{version.__version__}", self)
        # logo_text_widget.setFont(QFont("Arial", 15, QFont.Bold))
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_widget)
        logo_layout.addWidget(logo_text_widget)
        logoandtext_widget = QWidget()
        logoandtext_widget.setLayout(logo_layout)
        self.statusBar().addPermanentWidget(logoandtext_widget)
        # Point info
        self.info_widget = QLabel('x=  , y=  ,z=  ')
        self.info_widget.setMargin(3)
        self.plot_model.updated_pointer_info.connect(self.update_cursor_info)
        self.statusBar().addWidget(self.info_widget)

        # selection toolbar
        self.plotting_toolbar = QToolBar("Selection toolbar")
        self.plotting_toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.inter_action = QAction("Interactive", self)
        self.inter_action.setToolTip("Interactive (Alt+1)")
        self.inter_action.setIcon(QIcon('icons:cursor.png'))
        self.inter_action.triggered.connect(lambda x:
                                            self.map_widget.set_interaction(MapView.INTERACTIVE)
                                            if x else None)
        self.inter_action.setCheckable(True)
        self.inter_action.trigger()
        self.inter_action.setShortcut('Alt+1')

        self.points_action = QAction("Points", self)
        self.points_action.setToolTip("Points (Alt+2)")
        self.points_action.setIcon(QIcon('icons:points.png'))
        self.points_action.setIconText("Points")
        self.points_action.setCheckable(True)
        self.points_action.toggled.connect(lambda x: self.map_widget.set_interaction(MapView.POINTS)
                                           if x else None)
        self.points_action.setShortcut('Alt+2')

        self.prof_action = QAction("Profile", self)
        self.prof_action.setToolTip("Profile (Alt+3)")
        self.prof_action.setIcon(QIcon('icons:profile.png'))
        self.prof_action.setIconText("Profile")
        self.prof_action.setCheckable(True)
        self.prof_action.toggled.connect(lambda x: self.map_widget.set_interaction(MapView.PROFILE)
                                         if x else None)
        self.prof_action.setShortcut('Alt+3')

        self.ref_action = QAction("Reference", self)
        self.ref_action.setToolTip("Reference (Alt+4)")
        self.ref_action.setIcon(QIcon('icons:ref.png'))
        self.ref_action.setIconText("Reference")
        self.ref_action.setCheckable(True)
        self.ref_action.toggled.connect(lambda x: self.map_widget.set_interaction(MapView.REF)
                                        if x else None)
        self.ref_action.setShortcut('Alt+4')

        # action group so that only one tool can be selected at the same time
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        self.action_group.addAction(self.inter_action)
        self.action_group.addAction(self.points_action)
        self.action_group.addAction(self.prof_action)
        self.action_group.addAction(self.ref_action)
        self.action_group.setDisabled(True)
        self.map_model.closed.connect(lambda: self.action_group.setDisabled(True))
        self.map_model.opened.connect(lambda: self.action_group.setEnabled(True))
        # spacers to center buttons:
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plotting_toolbar.addWidget(spacer)
        self.plotting_toolbar.addAction(self.inter_action)
        self.plotting_toolbar.addAction(self.points_action)
        self.plotting_toolbar.addAction(self.prof_action)
        self.plotting_toolbar.addAction(self.ref_action)
        self.plotting_toolbar.addWidget(spacer2)
        self.addToolBar(self.plotting_toolbar)

        # Menu
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # File Menu
        file_menu = menubar.addMenu('File')
        open_action = QAction("Open data cube or project", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.on_button_clicked_open)

        save_map_action = QAction("Save project", self)
        save_map_action.triggered.connect(self.on_button_clicked_save)
        save_figs_action = QAction("Save all figures", self)
        save_figs_action.setShortcut('Ctrl+S')
        save_figs_action.triggered.connect(self.on_button_clicked_save_figures)
        save_action_group = QActionGroup(self)
        save_action_group.addAction(save_map_action)
        save_action_group.addAction(save_figs_action)
        save_action_group.setExclusive(False)
        save_action_group.setDisabled(True)
        self.map_model.closed.connect(lambda: save_action_group.setDisabled(True))
        self.map_model.opened.connect(lambda: save_action_group.setEnabled(True))

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.on_button_clicked_quit)
        quit_action.setShortcut(QKeySequence.Quit)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_map_action)
        file_menu.addAction(save_figs_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        # Edit Menu
        edit_menu = menubar.addMenu('Edit')
        undo_action = self.undo_stack.createUndoAction(self, "Undo")
        undo_action.setIcon(QIcon("icons:undo.svg"))
        undo_action.setShortcuts(QKeySequence.Undo)

        redo_action = self.undo_stack.createRedoAction(self, "Redo")
        redo_action.setIcon(QIcon("icons:redo.svg"))
        redo_action.setShortcuts(QKeySequence.Redo)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Layer Menu
        layer_menu = menubar.addMenu('Layer')
        layer_menu.addAction(self.layer_moveup_action)
        layer_menu.addAction(self.layer_movedown_action)
        layer_menu.addAction(self.layer_showall_action)
        layer_menu.addAction(self.layer_hideall_action)
        layer_menu.addAction(self.layer_remove_action)
        layer_menu.addSeparator()
        layer_menu.addAction(self.new_geomap_action)
        layer_menu.addAction(self.new_raster1B_action)
        layer_menu.addAction(self.new_rasterRGB_action)

        # View Menu
        view_menu = menubar.addMenu('View')
        self.plot_act = QAction("Plotting", self)
        self.plot_act.setCheckable(True)
        self.plot_act.setChecked(False)
        self.plot_act.setEnabled(False)
        self.plot_act.toggled.connect(self.show_plot_window)
        self.plot_act.setShortcut('Ctrl+P')
        view_menu.addAction(self.plot_act)

        self.minimap_action = QAction("Minimap", self)
        self.minimap_action.setCheckable(True)
        self.minimap_action.setChecked(True)
        self.minimap_action.toggled.connect(self.minimap_dock_widget.setVisible)
        self.minimap_dock_widget.visibilityChanged.connect(
            lambda _: self.minimap_action.setChecked(self.minimap_dock_widget.isVisible()))
        view_menu.addAction(self.minimap_action)

        self.flip_h_action = QAction("Flip Horizontally", self)
        self.flip_h_action.setToolTip("Flip map horizontally")
        self.flip_h_action.setCheckable(True)
        self.flip_h_action.setChecked(False)
        self.flip_h_action.toggled.connect(self.map_model.set_flip_h)
        self.flip_v_action = QAction("Flip Vertically", self)
        self.flip_v_action.setToolTip("Flip map vertically")
        self.flip_v_action.setCheckable(True)
        self.flip_v_action.setChecked(False)
        self.flip_v_action.toggled.connect(self.map_model.set_flip_v)
        flip_group = QActionGroup(self)
        flip_group.addAction(self.flip_h_action)
        flip_group.addAction(self.flip_v_action)
        flip_group.setExclusive(False)
        flip_group.setDisabled(True)
        self.map_model.closed.connect(lambda: flip_group.setDisabled(True))
        self.map_model.opened.connect(lambda: flip_group.setEnabled(True))
        view_menu.addSeparator()
        view_menu.addAction(self.flip_h_action)
        view_menu.addAction(self.flip_v_action)

        # Help Menu
        help_menu = menubar.addMenu('Help')
        help_action = QAction("Documentation", self)
        help_action.triggered.connect(openUrl)
        help_action.setShortcut(QKeySequence.HelpContents)
        help_menu.addAction(help_action)

        # show main window and minimap, focus on mainwindow
        self.show()
        self.showMaximized()
        self.activateWindow()

        # loading directly if file specified upon app launch:
        logger.debug(f"current_filepath = {self.current_filepath}")
        if self.current_filepath is not None:
            self.load_data(self.current_filepath)

    def load_data(self, filepath: str) -> bool:
        self.map_model.close()
        logger.info(f"loading {filepath}")
        _, extension = os.path.splitext(filepath)
        if extension == ".json":
            input_dict: dict[str, Any]
            with open(filepath, "r", encoding="utf-8") as file:
                input_dict = json.load(file)
            try:
                logger.info(f"{filepath} is an insarviz project version {input_dict['insarviz']}")
            except KeyError:
                logger.warning(f"{filepath} is not an insarviz project")
                self.current_filepath = None
                return False
            try:
                self.loader.open(input_dict["dataset_path"])
            except rasterio.errors.RasterioIOError:
                logger.debug(f"{filepath} is not an absolute path nor an url, trying relative path")
                try:
                    filedir = os.path.dirname(filepath)
                    dataset_path = os.path.join(filedir, input_dict["dataset_path"])
                    self.loader.open(dataset_path)
                except rasterio.errors.RasterioIOError:
                    logger.warning(f"File {input_dict['dataset_path']} does not exists / cannot be \
                        opened")
                    self.current_filepath = None
                    return False
            if not self.map_model.from_dict(input_dict, filepath):
                logger.warning(
                    f"{filepath} is an insarviz project but its structure is not correct")
                self.undo_stack.clear()
                self.current_filepath = None
                return False
        else:
            try:
                self.loader.open(filepath)
            except rasterio.errors.RasterioIOError:
                logger.warning(f"gdal cannot open {filepath}")
                self.current_filepath = None
                return False
            self.map_model.create_base_layers()
        logger.info(f"{filepath} successfully loaded")
        # enable plot button in menu:
        self.plot_act.setEnabled(True)
        self.undo_stack.clear()
        self.map_model.opened.emit()
        if self.loader.dataset.crs is None:
            self.new_geomap_action.setDisabled(True)
        else:
            self.new_geomap_action.setEnabled(True)
        self.band_slider.set_value(self.map_model.i)
        self.band_slider.setEnabled(True)
        return True

    @pyqtSlot(int)
    def on_mapview_interaction_changed(self, value: int) -> None:
        if value == MapView.INTERACTIVE:
            self.inter_action.setChecked(True)
        elif value == MapView.POINTS:
            self.points_action.setChecked(True)
        elif value == MapView.PROFILE:
            self.prof_action.setChecked(True)
        elif value == MapView.REF:
            self.ref_action.setChecked(True)

    @pyqtSlot(tuple, np.ndarray)
    def update_cursor_info(self, info: tuple, _: np.ndarray) -> None:
        """
        update point information (x, y, value) in Informations widget as
        cursor hovers over Map

        Parameters
        ----------
        coord : tuple (x, y, date, value)
            values of the point currently hovered over in MapView.
        """
        if info == ():
            self.info_widget.setText("")
        else:
            assert self.loader.dataset is not None
            x, y, date, value = info
            if isinstance(date, int):
                date = f"band #{date}"
            elif isinstance(date, datetime.datetime):
                date = date.date()
            text = f"x:{x:5d}, y:{y:5d}, val:{value:7.3f}, date:{date}"
            if self.loader.dataset.crs is not None:
                x_coord, y_coord = self.loader.dataset.xy(y, x)
                long, lat = rasterio.warp.transform(self.loader.dataset.crs,
                                                    rasterio.crs.CRS.from_epsg(4326),
                                                    [x_coord], [y_coord])
                text = text + f", lat:{lat[0]:7.3f}, long:{long[0]:7.3f}"
            self.info_widget.setText(text)

    def show_plot_window(self, checked: bool) -> None:
        if checked:
            self.temporal_plot_dock.show()
            self.spatial_plot_dock.show()
        else:
            self.temporal_plot_dock.hide()
            self.spatial_plot_dock.hide()

    def closeEvent(self, event) -> None:
        self.map_model.close()
        super().closeEvent(event)

    def on_button_clicked_quit(self) -> None:
        print('\n *** Thank you for using InsarViz, see you soon! *** \n')
        QApplication.quit()

    def new_rasterRGB(self) -> None:
        # the second return value of QFileDialog.getOpenFileName is the filter selected by user
        filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        if filepath:
            self.map_model.layer_model.add_layer(RasterRGBLayer("test", self.map_model, filepath))

    def new_raster1B(self) -> None:
        # the second return value of QFileDialog.getOpenFileName is the filter selected by user
        filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        if filepath:
            self.map_model.layer_model.add_layer(Raster1BLayer("test", self.map_model, filepath))

    def on_button_clicked_open(self) -> None:
        # the second return value of QFileDialog.getOpenFileName is the filter selected by user
        self.current_filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        if self.current_filepath:
            self.load_data(self.current_filepath)

    def on_button_clicked_save(self) -> None:
        """
        TODO
        Open dialog window to save map view to image file filepath.
        By default, also save corresponding colorbar to filepath_colorbar
        and minimap view to filepath_general_map (same format).
        """
        filter_string = "Insarviz project (*.json)"
        # the second return value of QFileDialog.getOpenFileName is the filter selected by user
        filepath, _ = QFileDialog.getSaveFileName(self, "Save insarviz project to ...",
                                                  filter=filter_string)
        if filepath:
            _, extension = os.path.splitext(filepath)
            if extension == "":
                filepath = os.path.join(filepath, ".json")
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(self.map_model.to_dict(filepath), file, indent=4)

    def on_button_clicked_save_figures(self) -> None:
        """
        Open dialog window to save all figures (map view, minimap view,
        colorbar and plots) to individual image files in a common directory
        """
        saveall_dirpath, _ = QFileDialog.getSaveFileName(
            self,
            'Save all figures to new directory...',
            "results",
            ".tiff ;; .png ;; .jpg",
            options=QFileDialog.ShowDirsOnly)
        if saveall_dirpath:
            if not os.path.exists(saveall_dirpath):
                os.makedirs(saveall_dirpath)
                saveall_dirname = saveall_dirpath.split('/')[-1]

                # save map view:
                self.map_widget.grabFramebuffer().save(
                    os.path.join(saveall_dirpath,
                                 saveall_dirname + '_map' + _))
                # save minimap view:
                self.minimap_widget.grabFramebuffer().save(
                    os.path.join(saveall_dirpath,
                                 saveall_dirname + '_general_map' + _))
                # save colorbar:
                cbar_name = saveall_dirname + '_colorbar' + _
                exporter = pg.exporters.ImageExporter(self.colormap_widget.sceneObj)
                exporter.export(os.path.join(saveall_dirpath, cbar_name))
                # if applicable save plots:
                if self.plot_act.isChecked():
                    tplot_name = saveall_dirname + '_temporal_plot' + _
                    self.temporal_plot_window.plot_widget.grab().save(
                        os.path.join(saveall_dirpath, tplot_name))
                    splot_name = saveall_dirname + '_spatial_plot' + _
                    self.spatial_plot_window.plot_widget.grab().save(
                        os.path.join(saveall_dirpath, splot_name))
                print('figures saved to directory', saveall_dirpath, '(format:', _+')')


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="insar timeseries visualisation")
    parser.add_argument("-v", type=int, default=3,
                        help=("set logging level:"
                              "0 critical, 1 error, 2 warning,"
                              "3 info, 4 debug, default=info"))
    parser.add_argument("-i", type=str, default=None, help="input filepath")
    parser.add_argument("-p", type=str, default=None,
                        help="directory that contains user defined plugins")
    args = parser.parse_args()
    logging_translate = [logging.CRITICAL,
                         logging.ERROR,
                         logging.WARNING,
                         logging.INFO,
                         logging.DEBUG]
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging_translate[args.v])
    config = None
    if args.p:
        config = {"plugin_directory": args.p}
        logger.info(f"adding {args.p} as plugin_directory")
    # OpenGL widgets share context even belonging in different windows
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    # set OpenGL profile
    opengl_format: QSurfaceFormat = QSurfaceFormat.defaultFormat()
    opengl_format.setMajorVersion(4)
    opengl_format.setProfile(QSurfaceFormat.CoreProfile)
    opengl_format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
    QSurfaceFormat.setDefaultFormat(opengl_format)
    # set pyqtgraph options
    pg.setConfigOption("background", 'w')
    pg.setConfigOption("foreground", 'k')
    # add icons directory to Qt paths
    script_dir: str = os.path.dirname(os.path.realpath(__file__))  # directory of ts_viz.py
    icons_dir: str = script_dir + os.path.sep + "icons" + os.path.sep
    QDir.addSearchPath('icons', icons_dir)
    # create application
    app: QApplication = QApplication([])
    MainWindow(filepath=args.i, config_dict=config)
    app.exec_()


if __name__ == '__main__':
    main()

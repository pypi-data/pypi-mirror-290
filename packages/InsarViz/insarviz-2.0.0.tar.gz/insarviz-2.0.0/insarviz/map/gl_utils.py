""" utils for OpenGL-based stuff (used for display of Map and Minimap)
"""
# imports ###################################################################

import ctypes
import numpy as np

from OpenGL.GL import (
    GL_TRUE,
    glGetString, GL_VERSION,
    glCreateShader, glShaderSource, glCompileShader,
    glCreateProgram, glAttachShader, glLinkProgram,
    glGetShaderiv, glGetShaderInfoLog,
    glGetProgramiv, glGetProgramInfoLog,
    glGetUniformLocation,
    GL_COMPILE_STATUS, GL_LINK_STATUS,
    glUniform1fv, glUniform2fv, glUniform3fv, glUniform4fv,
    glUniform1iv, glUniformMatrix3fv, glUniformMatrix4fv,
    glGenTextures, glBindTexture,
    glTexParameter, glTexImage2D, glGenerateMipmap,
    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
    GL_NEAREST, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR,
    GL_RED, GL_R32F, GL_RG, GL_RG32F, GL_RGB, GL_RGB32F, GL_RGBA,  GL_RGBA32F,
    glActiveTexture, GL_TEXTURE0, GL_FLOAT,
)


# utils #####################################################################

def get_opengl_version():
    """
    return opengl version.

    """
    version = glGetString(GL_VERSION).decode()
    version = version.split()[0]
    version = map(int, version.split("."))
    return tuple(version)


def create_shader(shader_type, source, **kwargs):
    """
    compile a shader.

    """
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader


def create_program(*shaders):
    """
    link a program.

    """
    program = glCreateProgram()
    for shader in shaders:
        glAttachShader(program, shader)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))
    return program


_c_types = {
    float:      ctypes.c_float,
    np.float32: ctypes.c_float,
    np.float64: ctypes.c_float,
    int:        ctypes.c_int,
    bool:       ctypes.c_int,
}

_Uniforms = {
    (1, ctypes.c_float): glUniform1fv,
    (2, ctypes.c_float): glUniform2fv,
    (3, ctypes.c_float): glUniform3fv,
    (4, ctypes.c_float): glUniform4fv,
    (9, ctypes.c_float): lambda location, n, values:
        glUniformMatrix3fv(location, n, GL_TRUE, values),
    (16, ctypes.c_float): lambda location, n, values:
        glUniformMatrix4fv(location, n, GL_TRUE, values),
    (1, ctypes.c_int):   glUniform1iv,
}


def set_uniform(program, uniform, *values):
    """
    dispatch uniform setting according to value type.

    """
    v0, n = values[0], len(values)
    if isinstance(v0, (tuple, list)):
        if isinstance(v0[0], (tuple, list)):
            # matrix case
            l, t = len(v0)*len(v0[0]), _c_types[type(v0[0][0])]
            values = (t * (l*n))(*(x for value in values for u in value for x in u))
        else:
            # vector case
            l, t = len(v0), _c_types[type(v0[0])]
            values = (t * (l*n))(*(u for value in values for u in value))
    else:
        l, t = 1, _c_types[type(v0)]
        values = (t * n)(*values)
    _Uniforms[l, t](glGetUniformLocation(program, uniform), n, values)


def load_texture(img, texture_id=0, texture_unit=GL_TEXTURE0):
    # TODO remove it
    """
    Load img as texture_unit OpenGl texture and return its texture_id

    Parameters
    ----------
    img : numpy array of shape (bands, rows, columns) or (rows, columns)
          such as a raster outputed by rasterio (i.e. (d, h, w) or (h, w))
          img.dtype must be "float32" or "uint8"

    texture_id : int
                 texture_id where img will be loaded
                 (if 0 then a new id will be generated, default)

    texture_unit : int
                   the texture unit where img will be loaded

    Returns
    -------
    texture_id: int
                identifier of the texture loaded by OpenGl

    Note
    ----
    OpenGl requires img to be in shape (rows, columns, bands)=(h,w,d)
    the first element being the lower left corner of the image
    https://registry.khronos.org/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml
    while rasterio rasters are (bands, rows, columns)=(d,h,w)
    the first element being the upper left corner of the image
    https://rasterio.readthedocs.io/en/latest/topics/image_processing.html
    """
    if img.dtype == "uint8":
        # TODO : give correct parameters for integer texture to glTexImage2D instead
        img = img.astype(np.float32)/255
    assert img.dtype == "float32", "img.dtype must be uint8 or float32"
    # if img.shape=(rows, columns) then add a empty bands axis
    if len(img.shape) == 2:
        img = img.reshape((1, img.shape[0], img.shape[1]))
    # change img.shape from (bands, rows, columns) to (rows, columns, bands)
    img = np.transpose(img, [1, 2, 0])
    # inverse the rows axis so that the first element is the lower left corner
    # img = img[::-1, :, :]
    h, w, d = img.shape
    if d == 1:
        internal_format = GL_R32F
        pixel_format = GL_RED
    elif d == 2:
        internal_format = GL_RG32F
        pixel_format = GL_RG
    elif d == 3:
        internal_format = GL_RGB32F
        pixel_format = GL_RGB
    elif d == 4:
        internal_format = GL_RGBA32F
        pixel_format = GL_RGBA
    else:
        raise ValueError(f"img must be of dimension at most 4, img.shape={img.shape}")
    if texture_id == 0:
        texture_id = glGenTextures(1)
    glActiveTexture(texture_unit)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameter(GL_TEXTURE_2D,
                   GL_TEXTURE_MAG_FILTER,
                   GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D,
                   GL_TEXTURE_MIN_FILTER,
                   GL_LINEAR_MIPMAP_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D,
        0, internal_format,
        w, h, 0,
        pixel_format,
        GL_FLOAT,
        img)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id


# exports ###################################################################

__all__ = [
    'get_opengl_version',
    'create_shader',
    'create_program',
    'set_uniform',
]

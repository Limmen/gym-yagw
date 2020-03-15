"""
Some OpenGL utility functions for drawing various shapes using the OpenGL primitive API
"""

import pyglet.gl as gl
import pyglet

def draw_label(text, x, y, font_size, color, font_name='Times New Roman'):
    label = pyglet.text.Label(text,
                          font_name=font_name,
                          font_size=font_size,
                          x=x, y=y,
                          anchor_x='center', anchor_y='center',
                          color=color)
    label.draw()

def draw_and_fill_rect(x, y, width, height, color):
    """
    Draws and fills a rectangle

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color to fill the rectangle with [R,G,B] scaled between [0,1]
    :return: None
    """
    __rect(x, y, width, height, color, fill=True)

def draw_rect_border(x, y, width, height, color):
    """
    Draws a rectangle with a border

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color of the border [R,G,B] scaled between [0,1]
    :return: None
    """
    __rect(x,y,width,height,color)

def __rect(x, y, width, height, color, fill=False):
    """
    Draws a rectangle

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :param color: RGB color of the rectangle [R,G,B] scaled between [0,1]
    :param fill: whether to fill the rectangle or just stroke it
    :return: None
    """
    # Set the color in the OpenGL Context (State)
    gl.glColor3f(color[0], color[1], color[2])
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
    # Configure rectangle (fill or not)
    if fill:
        # Delimits the vertices of a primitive or group of primitives
        gl.glBegin(gl.GL_POLYGON)

    else:
        # Delimits the vertices of a primitive or group of primitives
        gl.glBegin(gl.GL_LINES)

    # Draw the vertices of the rectangle
    __rect_vertices(x, y, width, height)
    # Delimits the vertices of a primitive or group of primitives
    gl.glEnd()

def __rect_vertices(x, y, width, height):
    """
    Uses the OpenGL API to create vertices to form a rectangle of a primitive

    :param x: the x coordinate of the lower-left  corner of the rectangle
    :param y: the y coordinate of the lower-left  corner of the rectangle
    :param width: the width of the rectangle
    :param height: the height of the rectangle
    :return: None
    """
    gl.glVertex2f(x, y)  # coordinate A
    gl.glVertex2f(x, y + height)  # coordinate B and line AB
    gl.glVertex2f(x, y + height)  # coordinate B
    gl.glVertex2f(x + width, y + height)  # coordinate C and line BC
    gl.glVertex2f(x + width, y + height)  # coordinate C
    gl.glVertex2f(x + width, y)  # coordinate D and line CD
    gl.glVertex2f(x + width, y)  # coordinate D
    gl.glVertex2f(x, y)  # coordinate A and line DA
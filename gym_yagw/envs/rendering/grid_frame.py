import pyglet
from gym_yagw.envs.rendering.grid import Grid
from gym_yagw.envs.rendering.agent import Agent
from gym_yagw.envs.rendering import constants
from gym_yagw.envs.rendering.render_util import draw_and_fill_rect, draw_label

class GridFrame(pyglet.window.Window):
    """
    A class representing the OpenGL/Pyglet Frame of a Gridworld
    By subclassing pyglet.window.Window, event handlers can be defined simply by overriding functions, e.g.
    event handler for on_draw is defined by overriding the on_draw function.
    """

    def __init__(self, height=1000, width = 800, rect_size = constants.GRIDWORLD.RECT_SIZE,
                 bg_color = constants.GRIDWORLD.WHITE, border_color = constants.GRIDWORLD.BLACK,
                 avatar_filename = constants.GRIDWORLD.AVATAR_FILENAME,
                 resources_dir = constants.GRIDWORLD.RESOURCES_DIR, agent_start_x = None, agent_start_y = None,
                 agent_scale = 0.2, caption="GridWorld", goal_state_x = None, goal_state_y = None, manual = True
                 ):
        """
        Gridframe constructor, initializes frame state and creates the window.

        :param height: height of the window
        :param width: width of the window
        :param rect_size: size of each cell in the grid
        :param bg_color: the color of the background of the grid
        :param border_color: the color of the border of the grid
        :param avatar_filename: name of the file-avatar to use for the agent
        :param resources_dir: the directory where resources are put (e.g. images)
        :param agent_start_x: the agent starting position (column index)
        :param agent_start_y: the agent starting position (row index)
        :param agent_scale: the scale of the agent avatar
        :param caption: caption of the frame
        :param manual: whether to setup the grid for manual play with keyboard
        """
        super(GridFrame, self).__init__(height=height, width=width, caption=caption) # call constructor of parent class
        self.bg_color = bg_color
        self.border_color = border_color
        self.rect_size = rect_size
        assert self.rect_size > 0
        assert self.rect_size < (self.height - constants.GRIDWORLD.PANEL_HEIGHT)
        assert self.rect_size < self.width
        self.num_rows = (self.height - constants.GRIDWORLD.PANEL_HEIGHT) // self.rect_size
        self.num_cols = self.width//self.rect_size
        self.num_cells = self.num_rows*self.num_cols
        if goal_state_x is not None and goal_state_y is not None:
            self.goal_state_x, self.goal_state_y = agent_start_x, agent_start_y
        else:
            self.goal_state_x, self.goal_state_y = self.num_cols-1, 0
        self.grid = Grid(self.rect_size, self.num_rows, self.num_cols, self.goal_state_x, self.goal_state_y)
        self.resources_dir = resources_dir
        self.setup_resources_path()
        self.manual = manual
        if agent_start_y is not None and agent_start_x is not None:
            x,y = agent_start_x, agent_start_y
        else:
            x,y = 0, self.num_rows
        self.agent = Agent(avatar_filename, x,y, self.rect_size, self.num_cols, self.num_rows,
                           self.goal_state_y, self.goal_state_x, scale=agent_scale)

    def setup_resources_path(self):
        """
        Setup path to resources (e.g. images)

        :return: None
        """
        pyglet.resource.path = [self.resources_dir]
        pyglet.resource.reindex()

    def on_draw(self):
        """
        Event handler for on_draw event. OpenGL does not remember what was rendered on the previous frame so
        we redraw each frame every time. This method is typically called many times per second.

        Draws the GridWorld Frame

        :return: None
        """

        # Clear the window
        self.clear()


        # Sets the background
        draw_and_fill_rect(0, 0, self.width, self.height, self.bg_color)

        # Draw the panel labels
        draw_label("R: ", constants.GRIDWORLD.PANEL_LEFT_MARGIN, self.height - constants.GRIDWORLD.PANEL_TOP_MARGIN,
                   constants.GRIDWORLD.PANEL_FONT_SIZE, constants.GRIDWORLD.BLACK_ALPHA)
        draw_label("t: ", constants.GRIDWORLD.PANEL_LEFT_MARGIN, self.height - constants.GRIDWORLD.PANEL_TOP_MARGIN * 2,
                   constants.GRIDWORLD.PANEL_FONT_SIZE, constants.GRIDWORLD.BLACK_ALPHA)
        draw_label(str(self.agent.reward), constants.GRIDWORLD.PANEL_LEFT_MARGIN * 2, self.height - constants.GRIDWORLD.PANEL_TOP_MARGIN,
                   constants.GRIDWORLD.PANEL_FONT_SIZE, constants.GRIDWORLD.BLACK_ALPHA)
        draw_label(str(self.agent.step), constants.GRIDWORLD.PANEL_LEFT_MARGIN * 2,
                   self.height - constants.GRIDWORLD.PANEL_TOP_MARGIN * 2,
                   constants.GRIDWORLD.PANEL_FONT_SIZE, constants.GRIDWORLD.BLACK_ALPHA)

        # Draws the cells of the grid
        for i in range(self.grid.num_rows):
            for j in range(self.grid.num_cols):
                self.grid.grid[i][j].draw(i, j, self.border_color)

        # Draw agent
        self.agent.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Event handler for on_key_press event.
        The user can move the agent with key presses.

        :param symbol: the symbol of the keypress
        :param modifiers: _
        :return: None
        """
        if self.manual:
            if symbol == pyglet.window.key.LEFT:
                self.agent.move_left()
            elif symbol == pyglet.window.key.RIGHT:
                self.agent.move_right()
            elif symbol == pyglet.window.key.UP:
                self.agent.move_up()
            elif symbol == pyglet.window.key.DOWN:
                self.agent.move_down()
            elif symbol == pyglet.window.key.SPACE:
                pass


    def update(self, dt):
        """
        Event handler for the update-event (timer-based typically), used to update the state of the grid.

        :param dt: the number of seconds since the function was last called
        :return: None
        """
        self.agent.update()

    def set_state(self, state):
        """
        Updates the frame with a given system-state.

        :param state: the state
        :return: None
        """
        self.agent.set_state(state)
        self.agent.update()

    def reset(self):
        self.agent.reset()

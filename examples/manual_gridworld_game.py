"""
Runner for the Gridworld GUI Manual Game
"""
from gym_yagw.envs.rendering.viewer import Viewer
from gym_yagw.envs.rendering import constants

if __name__ == '__main__':
    viewer = Viewer(width=300, height=400, rect_size=50, bg_color=constants.GRIDWORLD.WHITE, manual=True)
    viewer.manual_start()
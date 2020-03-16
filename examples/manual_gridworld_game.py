"""
Runner for the Gridworld GUI Manual Game
"""
from gym_yagw.envs.rendering.viewer import Viewer

if __name__ == '__main__':
    viewer = Viewer(width=300, height=400, rect_size=50, manual=True)
    viewer.manual_start()
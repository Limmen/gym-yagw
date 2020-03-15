from gym.envs.registration import register

register(
    id='yagw-v1',
    entry_point='gym_yagw.envs:YagwEnv',
)
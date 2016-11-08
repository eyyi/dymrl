from gym.envs.registration import register

print("register dymola inverted pendulum env")

register(
    id='DymolaInvertedPendulumEnv-v0',
    entry_point='dymrl.envs:DymolaInvertedPendulumEnv',
    timestep_limit=200,
    reward_threshold = 195,
)
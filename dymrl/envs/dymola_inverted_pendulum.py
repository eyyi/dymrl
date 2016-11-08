"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c
Use https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py as template
"""

import logging
import math
import numpy as np
from gym import spaces
from dymrl.envs import dymola_env

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DymolaInvertedPendulumEnv(dymola_env.DymolaEnv):
    NINETY_DEGREE_IN_RAD = (90/180)*math.pi
    TWELVE_DEGREE_IN_RAD = (12/180.0)*math.pi

    def __init__(self):
        self.theta_threshold_radians = self.TWELVE_DEGREE_IN_RAD
        self.x_threshold = 2.4
        dymola_env.DymolaEnv.__init__(self, 'inverted_pendulum/Pendel_Komponenten_Pendulum.fmu')

        self.force_magnitude = 10.0
        self.restart_simulation = True

        self.config = {
            'action': {'u': 10},
            'state': ['s', 'v', 'phi1', 'w'],
            'initial_parameters': {'m_trolley': 1, 'm_load': 0.1, 'phi1': self.NINETY_DEGREE_IN_RAD}
        }

        self.viewer = None
        # Just need to initialize the relevant attributes
        self._configure()

    def _configure(self, display=None):
        self.display = display

    def _get_action_space(self):
        return spaces.Discrete(2)

    def _get_observation_space(self):
        high = np.array([self.x_threshold, np.inf, self.theta_threshold_radians, np.inf])
        return spaces.Box(-high, high)

    def _step(self, action):
        force = self.force_magnitude if action == 1 else -self.force_magnitude
        self.state = self.do_simulation(force, self.restart_simulation)

        done = self._is_inside_threshold()

        if not done:
            reward = 1.0
            self.restart_simulation = False
        elif self.steps_beyond_done is None:
            logger.debug("Pole just fell")
            self.steps_beyond_done = 0
            self.restart_simulation = True
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logging.warning(
                    """You are calling 'step()' even though this environment has already returned done = True.
                    You should always call 'reset()' once you receive 'done = True' -- any further steps are
                    undefined behavior.""")
            self.steps_beyond_done += 1
            self.restart_simulation = True
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def _reset(self):
        self.steps_beyond_done = None
        self.restart_simulation = True
        self.state = np.random.uniform(low=-0.05, high=0.05, size=(4,))
        return np.array(self.state)

    def _is_inside_threshold(self):
        x, x_dot, theta, theta_dot = self.state
        logger.debug("x: {0}, x_dot: {1}, theat: {2}, theta_dot: {3}".format(x, x_dot, theta, theta_dot))

        theta = self._transform_theta(theta)

        if x < -self.x_threshold  or x > self.x_threshold:
            done = True
        elif theta < -self.theta_threshold_radians or theta > self.theta_threshold_radians:
            done = True
        else:
            done = False

        return done

    def _transform_theta(self, theta):
        if theta > 0:
            theta -= self.NINETY_DEGREE_IN_RAD
        else:
            theta += self.NINETY_DEGREE_IN_RAD

        return theta

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold * 2
        scale = screen_width / world_width
        carty = 100  # TOP OF CART
        polewidth = 10.0
        polelen = scale * 1.0
        cartwidth = 50.0
        cartheight = 30.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height, display=self.display)
            l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
            axleoffset = cartheight / 4.0
            cart = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(cart)
            l, r, t, b = -polewidth / 2, polewidth / 2, polelen - polewidth / 2, -polewidth / 2
            pole = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            pole.set_color(.8, .6, .4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth / 2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(.5, .5, .8)
            self.viewer.add_geom(self.axle)
            self.track = rendering.Line((0, carty), (screen_width, carty))
            self.track.set_color(0, 0, 0)
            self.viewer.add_geom(self.track)

        x = self.state
        cartx = x[0] * scale + screen_width / 2.0  # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)

        theta_ = x[2]

        if theta_ > 0:
            theta_ -= 1.5707963267948966
        else:
            theta_ += 1.5707963267948966

        self.poletrans.set_rotation(-theta_)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

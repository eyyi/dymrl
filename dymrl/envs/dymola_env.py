import datetime
import logging
import os

import gym
from pyfmi import load_fmu

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DymolaEnv(gym.Env):
    """
    Superclass for all Dymola environments.
    Simulate a dymola model with FMU CS2
    Link to pyfmi library: http://www.jmodelica.org/assimulo_home/pyfmi_1.0/##
    """

    def __init__(self, model_path):
        if model_path.startswith("/"):
            full_path = model_path
        else:
            full_path = os.path.join(os.path.dirname(__file__), "assets", model_path)
        if not os.path.exists(full_path):
            raise IOError("File %s does not exist" % full_path)

        self.model_name = full_path.split(os.path.sep)[-1]

        self.model = None
        self.result = None
        self.FMU_state = None

        self.tau = 0.02
        self.start = 0
        self.stop = 0

        self.action_space = self._get_action_space()
        self.observation_space = self._get_observation_space()

        self.model = load_fmu(full_path, kind='CS', log_file_name=self._get_log_file_name())

        self.config = {
            'action': {'u': 10},
            'state': ['s', 'v', 'phi1', 'w']
        }

        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50
        }

    def _render(self):
        raise NotImplementedError

    def _reset(self):
        raise NotImplementedError

    def _step(self, action):
        raise NotImplementedError

    def _get_action_space(self):
        raise NotImplementedError

    def _get_observation_space(self):
        raise NotImplementedError

    def _get_log_file_name(self):
        log_date = datetime.datetime.utcnow()
        log_file_name = "{0}-{1}-{2}_{3}.txt".format(log_date.year, log_date.month, log_date.day, self.model_name)
        return log_file_name

    def _set_init_parameter(self):
        if 'initial_parameters' in self.config:
            self.model.set(list(self.config['initial_parameters']), list(self.config['initial_parameters'].values()))

    def _restart_simulation(self):
        """
        Resets the Modellica model to its original state
        """
        logger.debug("restart simulation")
        self.model.reset()
        self.start = 0
        self.stop = self.tau

    def _continue_simulation(self):
        logger.debug("continue simulation")
        self.start = self.stop
        self.stop += self.tau

    def do_simulation(self, action, restart_simulation):
        logger.debug("simulate")

        if restart_simulation:
            self._restart_simulation()
        else:
            self._continue_simulation()

        opts = self.model.simulate_options()
        opts['ncp'] = 50

        logger.debug("action: {0}".format(list(self.config['action'])[0]))

        self.model.set(list(self.config['action'])[0], action)
        self.result = self.model.simulate(start_time=self.start, final_time=self.stop, options=opts)

        state = self._get_state()

        return state

    def _get_state(self):
        """
        Get the final value of states
        :return: states as tuple in ascending order (s, v, phi1, w)
        """
        sorted_states = self.config['state']
        return tuple([self.result.final(k) for k in sorted_states])

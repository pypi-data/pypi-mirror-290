import logging
import math
import os
import pickle
import sys
import warnings
from argparse import ArgumentParser
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from numpy.random import RandomState

from rlai.core import Monitor
from rlai.meta import rl_text
from rlai.policy_gradient.policies.continuous_action import ContinuousActionPolicy
from rlai.utils import load_class, get_base_argument_parser


@rl_text(chapter='Training and Running Agents', page=1)
def run(
        args: List[str]
) -> List[Monitor]:
    """
    Run an agent within an environment.

    :param args: Arguments.
    :return: List of run monitors.
    """

    parser = get_argument_parser_for_run()

    parsed_args, unparsed_args = parser.parse_known_args(args)

    # set logging level
    if parsed_args.log is not None:
        logging.getLogger().setLevel(parsed_args.log)
    del parsed_args.log

    if parsed_args.random_seed is None:
        warnings.warn(
            'No random seed provided to the trainer. Results will not be replicable. Consider passing --random-seed '
            'argument.'
        )
        random_state = RandomState()
    else:
        random_state = RandomState(parsed_args.random_seed)

    # init environment
    environment_class = load_class(parsed_args.environment)
    environment, unparsed_args = environment_class.init_from_arguments(
        args=unparsed_args,
        random_state=random_state
    )

    # init agent from file if it's a path
    if os.path.exists(os.path.expanduser(parsed_args.agent)):
        with open(os.path.expanduser(parsed_args.agent), 'rb') as f:
            agents = [pickle.load(f)]

    # otherwise, parse arguments for agent.
    else:
        agent_class = load_class(parsed_args.agent)
        agents, unparsed_args = agent_class.init_from_arguments(
            args=unparsed_args,
            random_state=random_state,
            environment=environment
        )

    # no unparsed arguments should remain
    if len(unparsed_args) > 0:
        raise ValueError(f'Unparsed arguments remain:  {unparsed_args}')

    # set up plotting
    pdf = None
    reward_ax = cum_reward_ax = optimal_action_ax = None
    if parsed_args.plot:

        if parsed_args.pdf_save_path:
            pdf = PdfPages(parsed_args.pdf_save_path)

        _, axs = plt.subplots(2, 1, sharex='all', figsize=(6, 9))

        assert isinstance(axs, np.ndarray)

        reward_ax = axs[0]
        cum_reward_ax = reward_ax.twinx()
        optimal_action_ax = axs[1]

    # run each agent in the environment
    monitors = []
    for agent in agents:

        logging.info(f'Running {agent} agent in {environment} environment.')

        # manually set the environment on continuous-action policies, as they require a reference but do not pickle it.
        if hasattr(agent, 'pi') and isinstance(agent.pi, ContinuousActionPolicy):
            agent.pi.environment = environment

        monitor = Monitor()
        monitors.append(monitor)

        num_runs_per_print = math.ceil(parsed_args.n_runs * 0.05)
        for r in range(parsed_args.n_runs):

            state = environment.reset_for_new_run(agent)
            agent.reset_for_new_run(state)
            monitor.reset_for_new_run()

            environment.run(
                agent=agent,
                monitor=monitor
            )

            num_runs_finished = r + 1
            if (num_runs_finished % num_runs_per_print) == 0:
                percent_done = 100 * (num_runs_finished / parsed_args.n_runs)
                logging.info(
                    f'{percent_done:.0f}% complete (finished {num_runs_finished} of {parsed_args.n_runs} runs).'
                )

        environment.close()

        if parsed_args.plot:

            assert reward_ax is not None
            assert cum_reward_ax is not None
            assert optimal_action_ax is not None

            reward_ax.plot([
                monitor.t_average_reward[t].get_value()
                for t in sorted(monitor.t_average_reward)
            ], linewidth=1, label=agent.name)

            cum_reward_ax.plot([
                monitor.t_average_cumulative_reward[t].get_value()
                for t in sorted(monitor.t_average_cumulative_reward)
            ], linewidth=1, linestyle='--', label=agent.name)

            optimal_action_ax.plot([
                monitor.t_count_optimal_action[t] / parsed_args.n_runs
                for t in sorted(monitor.t_count_optimal_action)
            ], linewidth=1, label=agent.name)

    # finish plotting
    if parsed_args.plot:

        assert reward_ax is not None
        assert cum_reward_ax is not None
        assert optimal_action_ax is not None

        if parsed_args.figure_name is not None:
            reward_ax.set_title(parsed_args.figure_name)

        reward_ax.set_xlabel('Time step')
        reward_ax.set_ylabel(f'Per-step reward (averaged over {parsed_args.n_runs} run(s))')
        reward_ax.grid()
        reward_ax.legend()
        cum_reward_ax.set_ylabel(f'Cumulative reward (averaged over {parsed_args.n_runs} run(s))')
        cum_reward_ax.legend(loc='lower right')

        optimal_action_ax.set_xlabel('Time step')
        optimal_action_ax.set_ylabel('% optimal action selected')
        optimal_action_ax.grid()
        optimal_action_ax.legend()

        plt.tight_layout()

        if pdf is None:
            plt.show(block=False)
        else:
            pdf.savefig()

        plt.close()

    return monitors


def get_argument_parser_for_run() -> ArgumentParser:
    """
    Get argument parser for the run function.

    :return: Argument parser.
    """

    parser = get_base_argument_parser(
        prog='rlai run',
        description=(
            'Run an agent within an environment. This does not support learning (e.g., monte carlo or temporal '
            'difference). See trainer.py for such methods.'
        )
    )

    parser.add_argument(
        '--n-runs',
        type=int,
        help='Number of runs.'
    )

    parser.add_argument(
        '--pdf-save-path',
        type=str,
        help='Path where a PDF of all plots is to be saved.'
    )

    parser.add_argument(
        '--figure-name',
        type=str,
        help='Name for figure that is generated.'
    )

    parser.add_argument(
        '--environment',
        type=str,
        help='Fully-qualified type name of environment.'
    )

    parser.add_argument(
        '--agent',
        type=str,
        help='Either (1) the fully-qualified type name of agent, or (2) a path to a pickled agent.'
    )

    parser.add_argument(
        '--random-seed',
        type=int,
        help='Random seed. Omit to generate an arbitrary random seed.'
    )

    parser.add_argument(
        '--plot',
        action='store_true',
        help='Pass this flag to plot rewards.'
    )

    return parser


if __name__ == '__main__':  # pragma no cover
    run(sys.argv[1:])

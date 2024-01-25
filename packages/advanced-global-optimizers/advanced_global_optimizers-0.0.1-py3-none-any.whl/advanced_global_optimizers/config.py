import time
import argparse


def get_options(args=None):

    parser = argparse.ArgumentParser(description="DE_PPO")

    # Overall settings
    parser.add_argument('--seed', type=int, default=123, help='random seed to use')
    parser.add_argument('--norm_ub', default=1.)
    parser.add_argument('--norm_lb', default=0.)
    parser.add_argument('--repeat', default=1)
    parser.add_argument('--batchsize', default=32)
    parser.add_argument('--precision', default=[1e-8, 1e-4, 1e-2])
    parser.add_argument('--tolerance', default=[0.0001, 0.01, 1.])
    parser.add_argument('--store_path', default='output/')
    parser.add_argument('--benchmark_path', default='problem_no_constraint_seed10.pkl')
    # parser.add_argument('--benchmark_path', default='constrained_problem_s67.pkl')

    opts = parser.parse_args(args)
    opts.run_time = time.strftime("%Y%m%dT%H%M%S")
    # opts.run_name = "{}_{}".format(opts.run_name, opts.run_time)

    return opts
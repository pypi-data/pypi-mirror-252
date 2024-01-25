import numpy as np
from pypop7.optimizers.bo.lamcts import LAMCTS as lamcts
import time
from .config import get_options

class LAMCTS:
    def __init__(self, param):
        self.config = get_options()
        # self.n_individuals = 100
        # self.c_e = 0.01
        # self.leaf_size = 40
        self.n_individuals = param['n_individuals']
        self.c_e = param['c_e']
        self.leaf_size = param['leaf_size']

    def evaluate(self, problem, x):
        x = np.array(x)
        x = (x - self.config.norm_lb) / (self.config.norm_ub - self.config.norm_lb)
        x = np.clip(x, 0., 1.)
        x = x * (problem.ub - problem.lb) + problem.lb
        return problem.eval(x)
    
    def optimize(self, problem):
        st_time = time.time()
        # original_stdout = sys.stdout
        # sys.stdout = open(os.devnull, 'w')

        def black_box_function(x):
            return self.evaluate(problem, x)
        p = {'fitness_function': black_box_function,  # cost function
            'ndim_problem': problem.dim,  # dimension
            'lower_boundary': self.config.norm_lb*np.ones((problem.dim,)),  # search boundary
            'upper_boundary': self.config.norm_ub*np.ones((problem.dim,))}
        options = {
           'max_function_evaluations': problem.maxFEs,  # 1 hours (terminate when the actual runtime exceeds it)
           'seed_rng': 0,  # seed of random number generation (which must be explicitly set for repeatability)
           'n_individuals': self.n_individuals,
           'c_e': self.c_e,
           'leaf_size': self.leaf_size,
           }
        optimizer = lamcts(p, options)  # initialize the optimizer
        res = optimizer.optimize()  # run its (time-consuming) search process
        del optimizer

        # sys.stdout.close()
        # sys.stdout = original_stdout

        ed_time = time.time()
        return {'x': res['best_so_far_x'], 'fun': res['best_so_far_y'], 'nfev_rec': 'unmeasurable', 'runtime': ed_time - st_time, 'nfev': problem.maxFEs}

from evosax import SAMR_GA
import jax
import numpy as np
from .config import get_options
import time



class SAMRGA():
    def __init__(self, param):
        self.config = get_options()
        self.popsize=param["popsize"]
        self.elite_ratio=param["elite_ratio"]
        self.sigma_init=param["sigma_init"]
        self.sigma_meta=param["sigma_meta"]
        self.sigma_best_limit=param["sigma_best_limit"]
    def init(self, problem, ):
        rng = jax.random.PRNGKey(seed=1)
        self.strategy = SAMR_GA(popsize=self.popsize,
                          num_dims=problem.dim,
                          elite_ratio=self.elite_ratio, 
                          sigma_init=self.sigma_init, 
                          sigma_meta=self.sigma_meta,
                          )
        es_params = self.strategy.default_params
        es_params = es_params.replace(init_max=self.config.norm_ub, init_min=self.config.norm_lb,
                                      clip_max=self.config.norm_ub, clip_min=self.config.norm_lb,
                                      sigma_best_limit=self.sigma_best_limit)
        state = self.strategy.initialize(rng, es_params)
        return rng, state, es_params
    def evaluate(self, problem, x):
        x = (x - self.config.norm_lb) / (self.config.norm_ub - self.config.norm_lb)
        x = x * (problem.ub - problem.lb) + problem.lb
        return problem.eval(x)
    def optimize(self, problem):
        st_time = time.time()
        rng, state, es_params = self.init(problem)
        fes = 0
        FEs_rec = {}
        for p in self.config.precision:
            FEs_rec[p] = -1
        while fes < problem.maxFEs:
            rng, rng_gen, rng_eval = jax.random.split(rng, 3)
            x, state = self.strategy.ask(rng_gen, state, es_params)
            fitness = self.evaluate(problem, x)
            fes += fitness.shape[0]
            state = self.strategy.tell(x, fitness, state, es_params)
            for p in self.config.precision:
                if np.min(fitness) < p and FEs_rec[p] < 0:
                    FEs_rec[p] = fes
                    break
        best_member, best_fitness = state.best_member, state.best_fitness
        del state
        del rng
        del es_params
        del self.strategy

        ed_time = time.time()
        return {'x': best_member, 'fun': best_fitness, 'nfev_rec': FEs_rec, 'runtime': ed_time - st_time, 'nfev': fes}

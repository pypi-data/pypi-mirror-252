from evosax import SimAnneal
import jax, time
import numpy as np
from .config import get_options
class Sim_Anneal():
    def __init__(self, param):
        self.config = get_options()
        self.popsize=param["popsize"]
        self.sigma_init=param["sigma_init"]
        self.sigma_decay=param["sigma_decay"]
        self.sigma_limit=param["sigma_limit"]
        self.temp_init=param["temp_init"]
        self.temp_limit=param["temp_limit"]
        self.temp_decay=param["temp_decay"]
        self.boltzmann_const=param["boltzmann_const"]
    def init(self, problem, ):
        rng = jax.random.PRNGKey(seed=1)
        # Assign parameter settings
        self.strategy = SimAnneal(popsize=self.popsize,
                        num_dims=problem.dim,
                        sigma_init=self.sigma_init, 
                        sigma_decay=self.sigma_decay, 
                        sigma_limit=self.sigma_limit,
                        )
        es_params = self.strategy.default_params
        es_params = es_params.replace(init_max=self.config.norm_ub, init_min=self.config.norm_lb,
                                      clip_max=self.config.norm_ub, clip_min=self.config.norm_lb,
                                      temp_init=self.temp_init, temp_limit=self.temp_limit, 
                                      temp_decay=self.temp_decay, boltzmann_const=self.boltzmann_const,
                                      )
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


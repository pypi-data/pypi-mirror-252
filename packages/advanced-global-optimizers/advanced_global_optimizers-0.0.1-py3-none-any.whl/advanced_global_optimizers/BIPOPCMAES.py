from evosax import BIPOP_CMA_ES
import jax
import numpy as np
from .config import get_options


class BIPOPCMAES():
    def __init__(self, param) -> None:
        self.config = get_options()
        self.popsize=param["popsize"]
        self.elite_ratio=param["elite_ratio"]
        self.sigma_init=param["sigma_init"]
        self.mean_decay=param["mean_decay"]
        self.min_num_gens=param["min_num_gens"]
        self.popsize_multiplier=param["popsize_multiplier"]
    def init(self, problem, ):
        rng = jax.random.PRNGKey(seed=1)
        self.strategy = BIPOP_CMA_ES(popsize=self.popsize,
                          num_dims=problem.dim,
                          elite_ratio=self.elite_ratio, 
                          sigma_init=self.sigma_init, 
                          mean_decay=self.mean_decay,
                          )
        es_params = self.strategy.default_params
        strategy_params = es_params.strategy_params.replace(init_max=self.config.norm_ub, init_min=self.config.norm_lb,
                                                            clip_max=self.config.norm_ub, clip_min=self.config.norm_lb)
        restart_params = es_params.restart_params.replace(min_num_gens=self.min_num_gens, popsize_multiplier=self.popsize_multiplier)
        es_params = es_params.replace(strategy_params=strategy_params, restart_params=restart_params)
        state = self.strategy.initialize(rng, es_params)
        return rng, state, es_params
    def evaluate(self, problem, x):
        x = (x - self.config.norm_lb) / (self.config.norm_ub - self.config.norm_lb)
        x = x * (problem.ub - problem.lb) + problem.lb
        return problem.eval(x)
    def optimize(self, problem):
        rng, state, es_params = self.init(problem)
        fes = 0
        FEs_rec = {}
        for p in self.config.precision:
            FEs_rec[p] = -1
        # if problem.maxFEs / param["popsize"] >= 500:
        #     return {'gbest_solution': np.zeros(problem.dim), 'gbest': 1e15, 'FEs_rec': FEs_rec}

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

        best_member, best_fitness = state.strategy_state.best_member, state.strategy_state.best_fitness
        del state
        del rng
        del es_params
        del self.strategy
        

        return {'gbest_solution': best_member, 'gbest': best_fitness, 'FEs_rec': FEs_rec}

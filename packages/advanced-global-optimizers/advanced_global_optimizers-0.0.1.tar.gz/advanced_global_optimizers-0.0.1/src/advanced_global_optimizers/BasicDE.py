import numpy as np
from .config import get_options
from .DE_base import DEtool
import time

class basic_DE(DEtool):
    def __init__(self, param):
        self.config = get_options()
        self.popsize = param['popsize']
        self.F = param['F']
        self.Cr = param['Cr']
        self.mutation = param['mutation']
        self.bounds = param['bound']

    def optimize(self,
                    problem,
                    ):
        # Initialize population
        st_time = time.time()
        dim = problem.dim
        NP = self.popsize
        population = np.random.rand(NP, dim) * (self.config.norm_ub - self.config.norm_lb) + self.config.norm_lb
        cost = self.evaluate(population, problem)
        gbest = np.min(cost)
        gbest_solution = population[np.argmin(cost)]
        FEs = NP
        FEs_rec = {}
        for p in self.config.precision:
            FEs_rec[p] = -1
        while FEs < problem.maxFEs:
            Fs = self.F
            Crs = self.Cr
            trail = eval("self."+self.mutation)(population, gbest_solution, Fs)
            trail = self.binomial(population, trail, Crs)
            trail = self.bound(trail, self.bounds)

            new_cost = self.evaluate(trail, problem)
            replace_id = np.where(new_cost < cost)[0]

            population[replace_id] = trail[replace_id]
            cost[replace_id] = new_cost[replace_id]
            FEs += NP

            if gbest > np.min(cost):
                gbest = np.min(cost)
                gbest_solution = population[np.argmin(cost)]
            for p in self.config.precision:
                if gbest < p and FEs_rec[p] < 0:
                    FEs_rec[p] = FEs
                    break

        ed_time = time.time()
        return {'x': gbest_solution, 'fun': gbest, 'nfev_rec': FEs_rec, 'runtime': ed_time - st_time, 'nfev': FEs}
    

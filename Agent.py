from random import choice
from numpy import exp
from math import sqrt
from copy import copy


class _Agent:
    '''Agent Baseclass'''
    def __init__(self, id):
        self.id = id

class RandomAgent(_Agent):      #agent_params takes the following form.. {}
    '''Agent Baseclass'''
    def __init__(self, id):
        self.id = id

    def choose(self, action_set, stated_problem):
        '''Given actions available and state info, returns choice from action set.'''
        return choice(action_set)

    def collect_payoff(self, payoff):
        '''Agent take their payoff and update their choice performance forecasts.'''
        pass

class CaseBasedAgent(_Agent):   #agent_params takes the following form.. {'aspiration': _, 'action_bandwidth':_, sim_weight_action:_,'state_space_params':{'var1':{'weight':_, 'missing':_}, 'var1':{'weight':_, 'missing':_}, ...}
    '''Agent case based reasoning class with bandwidth action sim.'''
    def __init__(self, id, aspiration, sim_weight_action, action_bandwidth, state_space_params):
        self.id = id
        self.aspiration = aspiration
        self.action_bandwidth = action_bandwidth
        self.sim_weight_action = sim_weight_action
        self.state_space_params = state_space_params
        self.memory = []        #a list of cases (dictionaries), of the following form.. [{'circumstance': {}, 'action':_, 'result':_}, ...]
        self.action_attractions = {}

    def reset_attractions(self, action_set):
        '''Establishes and resets attractions for new calcs each period.'''
        for a in action_set:
            self.action_attractions[a] = 0

    def update_attractions(self, case, action_set, stated_problem):
        '''Returns vector of action_attractions case will contribute.'''
        #1. establish range of actions which whose estimates will be affected by this experience (case):
        min_affected = max(case.get('action') - self.action_bandwidth, min(action_set))
        max_affected = min(case.get('action') + self.action_bandwidth, max(action_set))
        #2. Calculate part of similarity contributed by dimensions of the stated problem:
        sim_tally = 0
        for problem_dimension, state_val in stated_problem.items():
            if problem_dimension in self.state_space_params:
                if (state_val) and (case['circumstance'][problem_dimension] is not None):
                    sim_tally += self.state_space_params[problem_dimension]['weight']*((case['circumstance'][problem_dimension] - state_val)**2)
                else:
                    sim_tally += self.state_space_params[problem_dimension]['missing_sim']
            else:
                print(f'ERROR - Missing dimension of stated problem in agent state space params: {problem_dimension}')
        for act in action_set:
            if act >= min_affected and act <= max_affected:
                #3. Calculate part of similarity contributed by the action similarity:
                sim_action = self.sim_weight_action*((case['action'] - act)**2)
                sim_score = exp(-sqrt(sim_tally + sim_action))
                #4. Calculate CBU for that action and add it into our action attractions
                self.action_attractions[act] += sim_score*(case.get('result') - self.aspiration)

    def choose(self, action_set, stated_problem):
        '''Given actions available and state info, returns choice from action set.'''
        #1. Reset attractions to prepare for new calcs:
        self.reset_attractions(action_set)
        #2. Update action estimates by processing each case in memory:
        for case in self.memory:
            self.update_attractions(case, action_set, stated_problem)
        #3. Make choice:
        max_cbu = max(self.action_attractions.values())
        period_choice = choice([act for act, cbu in self.action_attractions.items() if cbu == max_cbu])
        #4. Save and return choice:
        self.period_stated_problem = stated_problem
        self.period_choice = period_choice
        return period_choice

    def collect_payoff(self, payoff):
        '''Agent take their payoff and update their choice performance forecasts.'''
        #Stores experience to memory
        self.memory.append({'circumstance': copy(self.period_stated_problem), 'action': self.period_choice, 'result': payoff})
        if self.id == 0:
            print(self.action_attractions)
            print(self.memory)
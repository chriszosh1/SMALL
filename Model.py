from Enums import Pairings
from random import shuffle
from copy import copy

class Model:
    '''A model to facilitate agents playing a repeated stage game.'''
    def __init__(self, agent_count: int,
                 pairing_type: Pairings,    #NOTE: If CUSTOM_FIXED, give list of lists of shape: custom_pairings = [[Group1 ids], [Group2 ids],...]
                                            #      If CUSTOM_BY_ROUND, give a list of the lists above, where each position is a round
                 agent_vars: dict,          #NOTE: agent_vars passes a dict of shape {'agent_type': class, agent_params: {}}
                 game_vars: dict,           #NOTE: game_vars passes a dict of shape {'stage_game': class, game_params: {}}
                 output_vars: dict,         #NOTE: output_vars passes a dict of shape {'model_level_output': bool, 'tag': str}
                 run: int = 0,             #For output storage purposes
                 verbose: bool = False,
                 custom_pairing: list = []
                 ):
        #Model variables:
        self.period = 0
        self.run = run
        self.agent_count = agent_count
        self.pairing_type = pairing_type      
        self.custom_pairings = custom_pairing
        self.period_pairing = None
        self.verbose = verbose
        #Setting up our stage game:
        self.game_params = game_vars.get('game_params')
        self.stage_game = game_vars.get('stage_game')(**self.game_params)
        #Making our agents:
        self.agent_params = agent_vars.get('agent_params')
        self.agents = {i : agent_vars.get('agent_type')(id = i, **self.agent_params) for i in range(agent_count)}
        self.agent_ids = [i for i in range(self.agent_count)]
        #Giving agents lags (history) if any:
        initial_lags = self.stage_game.return_outcome_info()
        for a in self.agents.values():
            a._store_lags(initial_lags)

        #Prepping storing our model output:
        self.output_vars = output_vars
        if self.output_vars.get('model_level_output', False):
            if self.run == 0:
                self.file = open(f'{self.output_vars.get("file_tag", "")}_data.txt','w')
                self.file.write('run,period,agent_id,choice,round_payoff,cumulative_payoff\n')
            else:
                self.file = open(f'{self.output_vars.get("file_tag", "")}_data.txt','a')

    def update_round_pairings(self) -> list:
        '''Establishes what the round pairings will be this round.'''
        if self.pairing_type == Pairings.N_PLAYER:
            return [self.agent_ids]
        elif self.pairing_type == Pairings.RANDOM:
            if self.agent_count % 2 == 0:
                #1. Mix up the order of all the ids
                random_order_ids =copy(self.agent_ids)
                shuffle(random_order_ids)
                #2. Chop up the shuffled id list into list of player pairs
                pairs = []
                for i in range(0, len(random_order_ids), 2):
                    pairs.append(random_order_ids[i:i+2])
                return pairs
            else:
                print('ERROR: An odd number of agents cannot be paired up!')
        elif self.pairing_type == Pairings.CUSTOM_FIXED:
            return self.custom_pairings
        elif self.pairing_type == Pairings.CUSTOM_BY_PERIOD:
            return self.custom_pairings[self.period]
        else:
            print('ERROR: Invalid pairing_type!')

    def collect_actions(self, stated_problem: dict, game_group_ids: list) -> dict:
        '''Asks the agents to make their choices and returns them.'''
        period_choices = {}
        for aid in game_group_ids:
            a = self.agents[aid]
            period_choices[aid] = a.choose(self.stage_game.return_action_set(), stated_problem)
        return period_choices
    
    def distribute_payoffs(self, payoffs: float, outcome_info:dict) -> None:
        '''Gives payoffs and result info to the agents.'''
        for aid in payoffs.keys():
            self.agents[aid].collect_payoff(payoffs.get(aid), outcome_info)

    def store_output(self, id_list) -> None:
        '''Writes output to a text file.'''
        for aid in id_list:
            a = self.agents[aid]
            self.file.write(f'{self.run},{self.period},{aid},{a.period_choice},{a.round_payoff},{a.cumulative_payoff}\n')

    def step(self):
        '''Asks the agents to play one iteration of the stage game.'''
        #0. Update pairings if necessary...
        self.period_pairing = self.update_round_pairings()
        if self.verbose:
            print(f'\n---Period {self.period}---')
            print(f'Pairings: {self.period_pairing}')
        #... then for each pairing/group:
        for game_group_ids in self.period_pairing:
            #1. Present the problem to the agents:
            stated_problem = self.stage_game.return_state_info(t=self.period)
            #2. Ask agents to make a choice:
            period_choices = self.collect_actions(stated_problem, game_group_ids)
            #3. Process the decisions to calculate payoffs:
            payoffs = self.stage_game.tabulate_game(period_choices)
            #4. Give agents their payoffs and outcome info:
            outcome_info = self.stage_game.return_outcome_info()
            self.distribute_payoffs(payoffs, outcome_info)
            #5. Printing/Storing output:
            if self.output_vars.get('model_level_output', False):
                self.store_output(game_group_ids)
        if self.verbose:
            pc = {aid: a.period_choice for aid, a in self.agents.items()}
            rpo = {aid: a.round_payoff for aid, a in self.agents.items()}
            print(f'period choices: {pc}')
            print(f'payoffs: {rpo}')
        #6. Bookkeeping for next iteration:
        self.stage_game.bookkeeping()                        
        self.period += 1

    def run_model(self, step_count: int) -> None:
        '''Model steps steps number of times.'''
        for s in range(step_count):
            self.step()
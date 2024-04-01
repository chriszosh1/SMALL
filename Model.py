class Model:
    '''A model to facilitate agents playing a repeated stage game.'''
    def __init__(self, agent_count,
                 agent_vars,          #NOTE: agent_vars passes a dict of shape {'agent_type': class, agent_params: {}}
                 game_vars,           #NOTE: game_vars passes a dict of shape {'stage_game': class, game_params: {}}
                 output_vars,         #NOTE: output_vars passes a dict of shape {'model_level_output': bool, 'tag': str}
                 run = 0,             #For output storage purposes
                 verbose = False,
                 ):
        #Model variables:
        self.period = 0
        self.run = run
        self.agent_count = agent_count
        self.verbose = verbose
        #Setting up our stage game:
        self.game_params = game_vars.get('game_params')
        self.stage_game = game_vars.get('stage_game')(**self.game_params)
        #Making our agents:
        self.agent_params = agent_vars.get('agent_params')
        self.agents = {i : agent_vars.get('agent_type')(id = i, **self.agent_params) for i in range(agent_count)}
        #Prepping storing our model output:
        self.output_vars = output_vars
        if self.output_vars.get('model_level_output', False):
            if self.run == 0:
                self.file = open(f'{self.output_vars.get("file_tag", "")}_data.txt','w')
                self.file.write('run,period,agent_id,choice,round_payoff,cumulative_payoff\n')
            else:
                self.file = open(f'{self.output_vars.get("file_tag", "")}_data.txt','a')

    def collect_actions(self, stated_problem):
        '''Asks the agents to make their choices and returns them.'''
        period_choices = {}
        for aid, a in self.agents.items():
            period_choices[aid] = a.choose(self.stage_game.return_action_set(), stated_problem)
        return period_choices
    
    def distribute_payoffs(self, payoffs):
        '''Gives payoffs to the agents.'''
        for aid, a in self.agents.items():
            a.collect_payoff(payoffs.get(aid))

    def store_output(self):
        '''Writes output to a text file.'''
        for aid, a in self.agents.items():
            self.file.write(f'{self.run},{self.period},{aid},{a.period_choice},{a.round_payoff},{a.cumulative_payoff}\n')

    def step(self):
        '''Asks the agents to play one iteration of the stage game.'''
        if self.verbose:
            print(f'---Period {self.period}---')
        #1. Present the problem to the agents:
        stated_problem = self.stage_game.return_state_info(t=self.period)
        #2. Ask agents to make a choice:
        period_choices = self.collect_actions(stated_problem)
        #3. Process the decisions to calculate payoffs:
        payoffs = self.stage_game.tabulate_game(period_choices)
        #4. Give agents their payoffs:
        self.distribute_payoffs(payoffs)
        #5. Printing/Storing output:
        if self.output_vars.get('model_level_output', False):
            self.store_output()
        if self.verbose:
            print(f'stated_problem: {stated_problem}')
            print(f'period_choices: {period_choices}')
            print(f'period_target: {self.stage_game.period_target}')
            print(f'payoffs: {payoffs}')
        #6. Bookkeeping for next iteration:
        self.stage_game.bookkeeping()                        
        self.period += 1

    def run_model(self, step_count):
        '''Model steps steps number of times.'''
        for s in range(step_count):
            self.step()
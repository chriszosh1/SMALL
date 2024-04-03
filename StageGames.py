from copy import copy

class _StageGame:
    '''Base class for games.'''
    def __init__(self, groupsize = None, pairings = None):
        self.action_set = None
        self.groupsize = groupsize
        self.pairings = pairings

    def return_action_set(self):
        '''Returns action set.'''
        return self.action_set      #NOTE: This is supported only for numerical (integer) actions right now in CBR, due to bandwidth def.

class BeautyContestGame(_StageGame):
    '''An implementation of the beauty contest game (Keynes 1936 / Alain Ledoux 1981).'''
    def __init__(self, target_scalar, prize, max_choice, groupsize = None, pairings = None):
        super().__init__(groupsize, pairings)
        self.action_set = [c for c in range(max_choice+1)]
        self.target_scalar = target_scalar
        self.prize = prize
        #Accounting vars:
        self.period_target = None
        self.target_lag = None

    def return_state_info(self, t):
        '''Returns state of the world to agents: period and last period's target.'''
        return {'period': t, 'target_lag': self.target_lag}

    def tabulate_game(self, period_choices):
        '''Calculates the agent payoffs and game state using agent choices, then return them.'''
        #1. Calculate the target value:
        self.period_target = sum(period_choices.values()) * self.target_scalar / len(period_choices)
        #2. Find agents who chose the closest target:
        min_dist = float('inf')
        winners = []
        for aid, chosen in period_choices.items():
            distance = abs(chosen - self.period_target)
            if distance < min_dist:
                min_dist = distance
                winners = [aid]
            elif distance == min_dist:
                winners.append(aid)
        #3. Calculate agent payoffs:
        winner_payoff = self.prize / len(winners)
        payoffs = {}
        for aid in period_choices.keys():
            if aid in winners:
                payoffs[aid] = winner_payoff
            else:
                payoffs[aid] = 0
        return payoffs
    
    def bookkeeping(self):
        '''Gets ready for next period.'''
        self.target_lag = self.period_target

class Symmetric2x2(_StageGame):
    '''A general 2x2 game implementation, which looks as follows:\n
        0   1  \n
    0 |A,A|D,C|\n
    1 |C,D|B,B|\n
    With A = payoff_table[0][0],\n
         B = payoff_table[1][1],\n
         C = payoff_table[1][0],\n
         D = payoff_table[0][1]\n
    '''
    def __init__(self, payoff_table, pairings = None, groupsize = None):
        super().__init__(groupsize, pairings)
        self.action_set = [0,1]
        self.payoff_table = payoff_table    #NOTE: This is a dict of the form {0:{0:float, 1:float}, 1:{0:float, 1:float}}
        #Accounting vars
        self.period_choice_freq = None
        self.choice_freq_lag = None

    def return_state_info(self, t):
        '''Returns state of the world to agents: period and last period's frequency of choosing each action.'''
        return {'period': t, 'coop_rate_lag': self.choice_freq_lag}

    def tabulate_game(self, period_choices):
        '''Calculates the agent payoffs and game state using agent choices, then return them.'''
        #1. Getting frequencies of each action:
        freq_0 = sum(1 for act in period_choices.values() if act == 0)
        freq_1 = sum(1 for act in period_choices.values() if act == 1)
        self.period_choice_freq = {0:freq_0, 1:freq_1}
        #2. Calculate average payoff for players choosing either action:
        player_count = len(period_choices)
        payoff_0 = ((freq_0-1)*self.payoff_table[0][0] + (freq_1)*self.payoff_table[0][1]) / player_count
        payoff_1 = ((freq_0)*self.payoff_table[1][0] + (freq_1-1)*self.payoff_table[1][1]) / player_count
        #3. Awarding players their payoff:
        payoffs = {}
        for aid, act in period_choices.items():
            if act == 0:
                payoffs[aid] = payoff_0
            elif act == 1:
                payoffs[aid] = payoff_1
            else:
                payoffs[aid] = None
                print('ERROR: Invalid agent action!')
        return payoffs
    
    def bookkeeping(self):
        '''Gets ready for next period.'''
        self.choice_freq_lag = copy(self.period_choice_freq)

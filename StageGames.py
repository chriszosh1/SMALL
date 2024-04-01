class _StageGame:
    '''Base class for games.'''
    def __init__(self):
        self.action_set = None

    def return_action_set(self):
        '''Returns action set.'''
        return self.action_set      #NOTE: This is supported only for numerical (integer) actions right now in CBR, due to bandwidth def.

class BeautyContestGame(_StageGame):
    '''An implementation of the beauty contest game (Keynes 1936 / Alain Ledoux 1981).'''
    def __init__(self, target_scalar, prize, max_choice):
        self.action_set = [c for c in range(max_choice+1)]
        self.target_scalar = target_scalar
        self.prize = prize
        #Accounting/printing vars:
        self.period_target = None
        self.target_lag = None

    def return_state_info(self, t):
        '''Returns state of the world and other relevant info.'''
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

from Model import Model
from StageGames import BeautyContestGame
from Agent import RandomAgent, CaseBasedAgent

game_vars = {'stage_game': BeautyContestGame, 'game_params': {'target_scalar': .5, 'prize': 20, 'max_choice':100}}
#agent_vars = {'agent_type': RandomAgent, 'agent_params': {}}
agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
                                                             'state_space_params':{'period':{'weight':1},
                                                                                   'target_lag':{'weight':1, 'missing_sim':0}}
                                                             }
                                                             }

test_model = Model(agent_count = 5, agent_vars = agent_vars, game_vars = game_vars, verbose = True)
for i in range(3):
    test_model.step()
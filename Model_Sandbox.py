from Model import Model
from StageGames import BeautyContestGame
from Agent import RandomAgent, CaseBasedAgent, SimpleReinforcementLearning_ER95

steps = 3
agent_count = 6
group_size = 3  #Allows for smaller groups of the players to play games (eg. =2 means players are in pairs)
game_vars = {'stage_game': BeautyContestGame, 'game_params': {'target_scalar': .5, 'prize': 20, 'max_choice':100}}
#agent_vars = {'agent_type': RandomAgent, 'agent_params': {}}
agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
                                                             'state_space_params':{'period':{'weight':1},
                                                                                   'target_lag':{'weight':1, 'missing_sim':0}}
                                                             }
                                                             }
output_vars = {'model_level_output': True, 'file_tag': 'test'}

test_model = Model(agent_count = agent_count, agent_vars = agent_vars,
                   game_vars = game_vars, output_vars = output_vars, verbose = False)
test_model.run_model(step_count = steps)
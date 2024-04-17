from Model import Model
from StageGames import BeautyContestGame
from Agent import RandomAgent, CaseBasedAgent, SimpleReinforcementLearning_ER95
from Enums import Pairings

steps = 3
agent_count = 6
game_vars = {'stage_game': BeautyContestGame, 'game_params': {'target_scalar': .5, 'prize': 20, 'max_choice':100}}

#agent_vars = {'agent_type': RandomAgent, 'agent_params': {}} #RANDOM AGENT
#agent_vars = {'agent_type': SimpleReinforcementLearning_ER95, 'agent_params': {'prior_strengths':2, 'reinforcement_strength':.5}} #RL95 Agent
agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
                                                             'state_space_params':{'period':{'weight':1},
                                                                                   'target':{'weight':1, 'missing_sim':0}}
                                                             }
                                                             }

#cp = [[0,1,2,3],[4,5]] #Fixed Custom
cp = [[[0,1],[2,3],[4,5]], [[0,1,2,3,4,5]], [[0,1],[2,3],[4,5]]]

output_vars = {'model_level_output': True, 'file_tag': 'test'}

test_model = Model(agent_count = agent_count, agent_vars = agent_vars,
                   game_vars = game_vars, output_vars = output_vars, verbose = True,
                   pairing_type=Pairings.CUSTOM_BY_PERIOD, custom_pairing=cp)
test_model.run_model(step_count = steps)
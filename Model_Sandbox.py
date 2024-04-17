from Model import Model
from StageGames import BeautyContestGame, Symmetric2x2
from Agent import RandomAgent, CaseBasedAgent, SimpleReinforcementLearning_ER95
from Enums import Pairings

steps = 3
agent_count = 6
output_vars = {'model_level_output': True, 'file_tag': 'test'}

#-------Stage Game Specification Examples------------:
#game_vars = {'stage_game': BeautyContestGame, 'game_params': {'target_scalar': .5, 'prize': 20, 'max_choice':100}} #BCG
game_vars = {'stage_game': Symmetric2x2, 'game_params': {'payoff_table': {0:{0:10, 1:30}, 1:{0:5, 1:25}}}} #the PD-CC09, where 0 is defect

#-------Agent Variable Specification Examples------------:
#agent_vars = {'agent_type': RandomAgent, 'agent_params': {}} #RANDOM AGENT
#agent_vars = {'agent_type': SimpleReinforcementLearning_ER95, 'agent_params': {'prior_strengths':2, 'reinforcement_strength':.5}} #RL95 Agent
#agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
#                                                             'state_space_params':{'period':{'weight':1},
#                                                                                   'target':{'weight':1, 'missing_sim':0}}
#                                                             }} #CBDT for BCG
agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
                                                             'state_space_params':{'period':{'weight':1},
                                                                                   'coop_rate':{'weight':1, 'missing_sim':0}}
                                                             }} #CBDT for Symmetric 2x2

#-------Custom Pairing Specification Examples------------:
#cp = [] #No custom - for RANDOM or N_PLAYER
#cp = [[0,1,2,3],[4,5]] #CUSTOM_FIXED
cp = [[[0,1],[2,3],[4,5]], [[0,1,2,3,4,5]], [[0,1],[2,3],[4,5]]] #CUSTOM_PER_PERIOD


test_model = Model(agent_count = agent_count, agent_vars = agent_vars,
                   game_vars = game_vars, output_vars = output_vars, verbose = True,
                   pairing_type=Pairings.CUSTOM_BY_PERIOD, custom_pairing=cp)
test_model.run_model(step_count = steps)
from Model import Model
from StageGames import BeautyContestGame
from Agent import RandomAgent, CaseBasedAgent
from Collect_Runs import collect_runs


steps = 3
runs = 3
agent_count = 5
game_vars = {'stage_game': BeautyContestGame, 'game_params': {'target_scalar': .5, 'prize': 20, 'max_choice':100}}
agent_vars = {'agent_type': CaseBasedAgent, 'agent_params': {'aspiration': 2, 'action_bandwidth': 4, 'sim_weight_action': 1,
                                                             'state_space_params':{'period':{'weight':1},
                                                                                   'target_lag':{'weight':1, 'missing_sim':0}}
                                                             }
                                                             }
output_vars = {'model_level_output': True, 'file_tag': 'collected_model_output'}
model_args = {'agent_count':agent_count, 'game_vars':game_vars, 'agent_vars': agent_vars, 'output_vars': output_vars}


results =  collect_runs(Model, runs = runs, steps = steps, model_args = model_args)
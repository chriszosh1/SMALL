from Model import Model


def collect_runs(model_class, runs, steps, model_args, output_file_name = 'model_output'):
    '''Creates models runs times and collects data from each.'''
    
    for r in range(runs):
        temp_model = model_class(**model_args)
        temp_model.run_model(step_count = steps)

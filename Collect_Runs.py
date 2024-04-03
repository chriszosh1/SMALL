from Model import Model


def collect_runs(model_class, runs, steps, model_args):
    '''Creates models runs times and collects data from each.'''
    for r in range(runs):
        temp_model = model_class(run = r, **model_args)
        temp_model.run_model(step_count = steps)

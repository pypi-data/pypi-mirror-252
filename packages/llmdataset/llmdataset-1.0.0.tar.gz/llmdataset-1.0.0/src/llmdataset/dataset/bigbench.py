from .base import base_data_split

def bigbench_split(dataset, data_type, keys_list):
    all_dataset, num_data = base_data_split(dataset, data_type, keys_list)
    data_list = [[example['inputs'], example['targets'], example['multiple_choice_targets'], example['multiple_choice_scores']] for example in all_dataset]
    return data_list, num_data

from .base import base_data_split

def aquarat_split(dataset, data_type, keys_list):
    all_dataset, num_data = base_data_split(dataset, data_type, keys_list)
    data_list = [[example['question'], example['options'], example['rationale'], example['correct']] for example in all_dataset]
    return data_list, num_data

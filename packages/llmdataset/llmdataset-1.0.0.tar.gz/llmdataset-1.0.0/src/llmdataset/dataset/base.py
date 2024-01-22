from datasets import load_dataset, concatenate_datasets

def base_load_dataset(dataset_name, subset):
    try:
        dataset = load_dataset(dataset_name, subset)
        keys_list = list(dataset.keys())
        count_list = []
        for i in range(len(keys_list)):
            num_dataset = len(dataset[keys_list[i]])
            count_list.append(num_dataset)
        return keys_list, count_list, dataset

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def base_data_split(dataset, data_type, keys_list):
    if data_type == 'all':
        concat_data_list = []
        for i in range(len(keys_list)):
            all_dataset = dataset[keys_list[i]]
            concat_data_list.append(all_dataset)
        all_dataset = concatenate_datasets(concat_data_list)
        num_data = len(all_dataset)
    else:
        all_dataset = dataset[data_type]
        num_data = len(all_dataset)

    return all_dataset, num_data

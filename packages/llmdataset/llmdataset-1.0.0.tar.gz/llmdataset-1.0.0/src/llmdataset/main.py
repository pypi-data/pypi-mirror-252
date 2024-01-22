from .dataset.gsm8k import gsm8k_split
from .dataset.multiarith import multiarith_split
from .dataset.bigbenchhard import bbh_split
from .dataset.gsmhard import gsmhard_split
from .dataset.wikitablequestions import wikitq_split
from .dataset.strategyqa import strategyqa_split
from .dataset.arc import arc_split
from .dataset.bigbench import bigbench_split
from .dataset.aquarat import aquarat_split
from .dataset.gpqa import gpqa_split
from .dataset.svamp import svamp_split
from .dataset.csqa import csqa_split
import random
from .dataset.base import base_load_dataset

class LLMdataset:
    def __init__(
        self,
        dataset_name = None,
        subset = None
        ):
        self.dataset_name = dataset_name
        self.subset = subset
        self.keys_list, count_list, self.dataset = base_load_dataset(self.dataset_name, self.subset)
        print(f"Data types:{self.keys_list}")
        print(f"Number of data:{count_list}")


    def _split_dataset(self, data_type):
        if self.dataset_name == 'gsm8k':
            data_list, num_data = gsm8k_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "ChilleD/MultiArith":
            data_list, num_data = multiarith_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "lukaemon/bbh":
            data_list, num_data = bbh_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "reasoning-machines/gsm-hard":
            data_list, num_data = gsmhard_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "wikitablequestions":
            data_list, num_data = wikitq_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "ChilleD/StrategyQA":
            data_list, num_data = strategyqa_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "allenai/ai2_arc":
            data_list, num_data = arc_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "tasksource/bigbench":
            data_list, num_data = bigbench_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "aqua_rat":
            data_list, num_data = aquarat_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "Idavidrein/gpqa":
            data_list, num_data = gpqa_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "ChilleD/SVAMP":
            data_list, num_data = svamp_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        elif self.dataset_name == "tau/commonsense_qa":
            data_list, num_data = csqa_split(self.dataset, data_type, self.keys_list)
            return data_list, num_data
        else:
            raise ValueError(f"Unsupported dataset name: {self.dataset_name}")


    def dataloader(self, data_type=None, batch_size=1, seed=None, max_data=5):
        self.data_list, self.num_data = self._split_dataset(data_type)

        if seed is not None:
            random.seed(seed)

        if max_data is not None and max_data > self.num_data:
            raise ValueError(f"max_data ({max_data}) cannot be greater than the size of the dataset ({self.num_data}).")

        if max_data is not None:
            data_list = random.sample(self.data_list, max_data)
        else:
            data_list = self.dataset[:max_data]

        for i in range(0, len(data_list), batch_size):
            yield data_list[i:i + batch_size]



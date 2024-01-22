# LLM dataset

## How to use
- install
    - https://pypi.org/project/llmdataset/
```
pip install llmdataset
```
- setting
```python
dataloader = llmdataset.dataloader(
    data_type='train',
    batch_size=4,
    seed=3655,
    max_data=5
    )
```
- execution
```
for i in dataloader:
    print('------')
    print(i)
```

## Useful dataset
- GSM8K
    - https://huggingface.co/datasets/gsm8k
```python
llmdataset = main.LLMdataset(dataset_name="gsm8k", subset='main')
```
- MultiArith
    - https://huggingface.co/datasets/ChilleD/MultiArith
```python
llmdataset = main.LLMdataset(dataset_name="ChilleD/MultiArith")
```

- Big Bench
    - https://huggingface.co/datasets/bigbench
```python
llmdataset = main.LLMdataset(dataset_name="tasksource/bigbench", subset = "abstract_narrative_understanding")
```

- Big Bench Hard
    - https://huggingface.co/datasets/lukaemon/bbh
```python
llmdataset = main.LLMdataset(dataset_name="reasoning-machines/gsm-hard", subset="boolean_expressions")
```

- GSM Hard
    - https://huggingface.co/datasets/reasoning-machines/gsm-hard
```python
llmdataset = main.LLMdataset(dataset_name="reasoning-machines/gsm-hard")
```

- wikitablequestions
    - https://huggingface.co/datasets/wikitablequestions?row=0
```python
llmdataset = main.LLMdataset(dataset_name="wikitablequestions")
```

- StrategyQA
    - https://huggingface.co/datasets/ChilleD/StrategyQA?row=0
```python
llmdataset = main.LLMdataset(dataset_name="ChilleD/StrategyQA")
```

- ARC
    - https://huggingface.co/datasets/allenai/ai2_arc
```python
llmdataset = main.LLMdataset(dataset_name="allenai/ai2_arc", subset = "ARC-Challenge")
```

- AQuA-RAT
    - https://huggingface.co/datasets/aqua_rat/viewer/raw
```python
llmdataset = main.LLMdataset(dataset_name="aqua_rat", subset = "raw")
```

- GPQA
    - https://huggingface.co/datasets/Idavidrein/gpqa
```python
llmdataset = main.LLMdataset(dataset_name="Idavidrein/gpqa", subset = "gpqa_diamond")
```

- SVAP
    - https://huggingface.co/datasets/ChilleD/SVAMP?row=0
```python
llmdataset = main.LLMdataset(dataset_name="ChilleD/SVAMP")
```

- CommonsenseQA
    - https://huggingface.co/datasets/tau/commonsense_qa
```python
llmdataset = main.LLMdataset(dataset_name="tau/commonsense_qa")
```

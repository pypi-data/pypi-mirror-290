# Benchmarking and Rethinking Multiplex Graphs
Multiplex graphs, which represent complex real-world relationships, have recently garnered significant research interest. However, contemporary methods exhibit variations in implementations and settings, lacking a unified benchmark for fair comparison. Additionally, existing multiplex graph datasets suffer from small-scale issues and a lack of representative features. Furthermore, current evaluation metrics are restricted to node classification and clustering tasks, lacking evaluations on edge-level tasks. These obstacles impede the further development of the multiplex graph learning community.
To address these issues, we first conducted a fair comparison based on existing settings, finding that current methods are approaching performance saturation on existing datasets with minimal differences; and simple end-to-end models sometimes achieve better results.
Subsequently, we proposed a unified multiplex graph benchmark called MGB. MGB includes ten baseline models with unified implementations, formalizes seven existing datasets, introduces four new datasets with text attributes, and proposes two novel edge-level evaluation tasks.
Experiments on MGB revealed that the performance of existing methods significantly diminishes on new challenging datasets and tasks. Additional results suggest that models with global attention and stronger expressive power in end-to-end solutions hold promise for future work.
The data and code are publicly available at [https://anonymous.4open.science/r/multiplex-F150].

## Environment
You can simply set the running enviroment by running 
```
conda install --yes --file requirements.txt
```


## Data Preprocess
To ensure a unified and reproducible fair comparison, we have uploaded all datasets at [Dataset](https://drive.google.com/file/d/1LsJPsfr5tB2zK8ELlATxomJn687ToohX/view?usp=drive_link).
Simply place the datasets in the `./data/` folder under the MGB code directory for automatic execution.

## Run by Examples
```
bash main.sh ${gpu} ${model_name} ${dataset_name}
```

## Pip Usage
You can also download our code using pip package by running the following
```
pip install xxx
```
Currently, we only support ...


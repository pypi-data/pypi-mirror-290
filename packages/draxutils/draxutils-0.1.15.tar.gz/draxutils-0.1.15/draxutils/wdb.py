import wandb
import numpy as np
from PIL import Image
import multiprocessing as mp
from tqdm import tqdm
from typing import List, Optional, Any, Dict
import torch

def convert_tensors_to_numpy(item):
    """
    Recursively converts all PyTorch tensors in the given item to NumPy arrays.

    Args:
    item: A single item or a dictionary/list/tuple containing items to be converted.

    Returns:
    The item with all PyTorch tensors converted to NumPy arrays.
    """
    if isinstance(item, torch.Tensor):
        return item.detach().cpu().numpy()
    elif isinstance(item, dict):
        return {k: convert_tensors_to_numpy(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [convert_tensors_to_numpy(v) for v in item]
    elif isinstance(item, tuple):
        return tuple(convert_tensors_to_numpy(v) for v in item)
    else:
        return item

def item_to_wandb_row(item: Dict[str, Any], keys: Optional[List[str]] = None) -> List[Any]:
    """
    Convert a single dataset item to a row suitable for a W&B Table.

    :param item: A single item from a HuggingFace dataset
    :param keys: Optional list of keys to include and their order. If None, all keys are included.
    :return: A list representing a row for a W&B Table
    """
    if keys is None:
        keys = item.keys()

    row = []
    for key in keys:
        value = item.get(key)
        if isinstance(value, Image.Image):
            value = wandb.Image(np.array(value))
        # Add more type conversions here if needed
        row.append(value)

    return row

def dataset_to_wandb_table(dataset, keys: Optional[List[str]] = None, num_proc: int = 1) -> wandb.Table:
    """
    Convert a HuggingFace dataset to a W&B Table using multiprocessing.

    :param dataset: A HuggingFace dataset
    :param keys: Optional list of keys to include and their order. If None, all keys are included.
    :param num_proc: Number of processes to use for multiprocessing
    :return: A wandb.Table object
    """
    columns = keys if keys is not None else dataset.column_names

    with mp.Manager() as manager:
        shared_list = manager.list()

        def process_item(item):
            shared_list.append(item_to_wandb_row(item, keys))

        with tqdm(total=len(dataset), desc="Processing items") as pbar:
            def update(*a):
                pbar.update()

            with mp.Pool(num_proc) as pool:
                for _ in pool.imap_unordered(process_item, dataset, chunksize=100):
                    update()

        wdb_data = list(shared_list)

    return wandb.Table(data=wdb_data, columns=columns)

# Example usage:
# import wandb
# from datasets import load_dataset
#
# # Initialize W&B run
# run = wandb.init(project="your_project", name="your_run")
#
# # Load your HuggingFace dataset
# dataset = load_dataset("your_dataset")["train"]
#
# # Convert to W&B Table
# table = dataset_to_wandb_table(dataset, num_proc=32)
#
# # Log the table to W&B
# run.log({"dataset_preview": table})
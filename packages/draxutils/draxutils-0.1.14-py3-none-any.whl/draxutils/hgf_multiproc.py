import datasets
from multiprocessing import Manager
def map_add_list(ds: datasets.Dataset, map_fn, num_proc):
    with Manager() as manager:
        shared_list = manager.list([None] * len(ds))

        # Process data using map function
        print("Processing data...")
        ds.map(
            lambda x, idx: map_fn(x, idx, shared_list),
            with_indices=True,
            num_proc=num_proc,
            desc="Processing items"
        )

        # Convert shared_list to a regular list
        all_data = list(shared_list)
    return all_data
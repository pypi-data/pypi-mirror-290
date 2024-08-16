from typing import Union, Callable, Iterable, Tuple, Any
from weakref import proxy
import numpy as np
from torch.utils.data import Dataset
from .utils import get_combined_transform


class AugmentationIndexMapping:
    def __init__(self, value = np.empty((0, 2), dtype=int)):
        self.value = np.asarray(value)
        if len(self.value.shape) != 2 or self.value.shape[1] != 2:
            raise ValueError(f"'value' is expected to have a shape of '(n, 2)', but accepted '{self.value.shape}'")
    
    def __len__(self):
        return len(self.value)
    
    def get_mapped_index(self, index) -> int:
        return self.value[index, 0]
    
    def get_mapped_boolean(self, index) -> bool:
        return bool(self.value[index, 1])


class Augmenter:
    def __init__(self, transform: Union[Callable[..., Tuple[Any, ...]], Iterable[Callable[[Any], Any]], None], multiplier: int = 1):   
        self.transform = get_combined_transform(transform)
        self.dataset = None
        self.multiplier = multiplier
    
    def augment(self, *args):
        args_length = len(args)
        if args_length == 1:
            if self.transform is None:
                return args[0]
            else:
                return self.transform(*args)[0]
        elif args_length > 1:
            if self.transform is None:
                return args
            else:
                return self.transform(*args)

    def attach_dataset(self, dataset: Dataset):
        self.dataset = proxy(dataset)
        self.index_mapping = self.initialize_index_mapping()

    def detach_dataset(self):
        self.dataset = None

    def initialize_index_mapping(self) -> AugmentationIndexMapping:
        length = len(self.dataset)
        indexes = np.arange(length, dtype=int)[:, None]
        index_mapping = np.broadcast_to(indexes, (length, 2)).copy()
        index_mapping[:, 1] = 1
        index_mapping = np.broadcast_to(index_mapping[None, :], (self.multiplier, length, 2)).copy()
        index_mapping[0, :, 1] = 0
        index_mapping = index_mapping.reshape(-1, 2)
        return AugmentationIndexMapping(index_mapping)
    
    def map_to_index(self, index):
        return self.index_mapping.get_mapped_index(index)
    
    def is_augmentee(self, index):
        return self.index_mapping.get_mapped_boolean(index)
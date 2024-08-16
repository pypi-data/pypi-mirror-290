from typing import Union, Callable, Iterable, Tuple, Any
from torch.utils.data import Dataset
from .augmenter import Augmenter
from .augmentation_scheduler import AugmentationScheduler
from .utils import get_combined_transform


class AugmentationDataset(Dataset):
    def __init__(
        self,
        dataset: Dataset,
        augmenter: Augmenter,
        scheduler: AugmentationScheduler = AugmentationScheduler(),
        transform: Union[Callable[..., Tuple[Any, ...]], Iterable[Callable[[Any], Any]], None] = None
    ):
        self.dataset = dataset
        self.augmenter = augmenter
        self.scheduler = scheduler
        self.transform = get_combined_transform(transform)
        self.augmenter.attach_dataset(self.dataset)

    def __del__(self):
        self.augmenter.detach_dataset()
    
    def __len__(self):
        return len(self.augmenter.index_mapping)
    
    def __getitem__(self, index):
        with self.scheduler:
            mapped_index = self.augmenter.map_to_index(index)
            current_item = self.dataset[mapped_index]
            if self.augmenter.is_augmentee(index):
                if not isinstance(current_item, tuple):
                    current_item = (current_item,)
                current_item = self.augmenter.augment(*current_item)
            if self.transform is not None:
                if not isinstance(current_item, tuple):
                    current_item = (current_item,)
                current_item = self.transform(*current_item)
                if len(current_item) == 1:
                    current_item = current_item[0]
        return current_item
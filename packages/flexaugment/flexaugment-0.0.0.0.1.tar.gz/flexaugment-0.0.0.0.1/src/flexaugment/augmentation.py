from typing import Union, Callable, Iterable, Tuple, Any
from torch.utils.data import Dataset
from .augmenter import Augmenter
from .augmentation_scheduler import AugmentationScheduler
from .augmentation_dataset import AugmentationDataset


class Augmentation:
    def __init__(
        self,
        augmenter: Augmenter,
        scheduler: AugmentationScheduler = AugmentationScheduler(),
        transform: Union[Callable[..., Tuple[Any, ...]], Iterable[Callable[[Any], Any]], None] = None
    ):
        self.augmenter = augmenter
        self.scheduler = scheduler
        self.transform = transform
    
    def wrap(self, dataset) -> AugmentationDataset:
        return AugmentationDataset(dataset, self.augmenter, self.scheduler, self.transform)
    
    def prepare(self, *args) -> Union[Dataset, Tuple[Dataset, ...]]:
        args_length = len(args)
        if args_length == 1:
            if isinstance(args[0], Dataset):
                return self.wrap(args[0])
            else:
                return args[0]
        elif args_length > 1:
            return (arg if not isinstance(arg, Dataset) else self.wrap(arg) for arg in args)
    
    def step(self, *args):
        return self.scheduler.step(*args)
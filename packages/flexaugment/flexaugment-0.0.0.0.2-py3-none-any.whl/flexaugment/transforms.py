from typing import Any
import torch


class SharingRandomTransform:
    def __init__(self, transform):
        self.transform = transform
    
    def __call__(self, *args: Any):
        if self.transform is None:
            return args
        else:
            rng_state = torch.get_rng_state()
            called = self.transform(*args)
            self.__last_changed_rng_state = torch.get_rng_state()
            torch.set_rng_state(rng_state)
            return called
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.transform is not None:
            torch.set_rng_state(self.__last_changed_rng_state)
        return False
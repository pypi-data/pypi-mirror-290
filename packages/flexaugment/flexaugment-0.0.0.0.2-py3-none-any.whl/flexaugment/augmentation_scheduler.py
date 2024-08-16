import torch


class AugmentationScheduler:
    def __init__(self):
        pass

    def step(self, *args):
        pass

    def pre_get(self):
        pass

    def post_get(self):
        pass
    
    def __enter__(self):
        return self.pre_get()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.post_get()


class OriginalRandomStateScheduler(AugmentationScheduler):
    '''
    This scheduler stores the original random state.
    '''
    def pre_get(self):
        self.__original_rng_state = torch.get_rng_state()

    def post_get(self):
        torch.set_rng_state(self.__original_rng_state)


class RetainedRandomStateScheduler(OriginalRandomStateScheduler):
    '''
    This scheduler retains the ramdom state.
    '''
    def __init__(self, retention: int = None):
        self.retention = retention
        self.pre_get = self.__before_get_item_at_first

    def pre_get(self):
        pass

    def post_get(self):
        self.__transform_rng_state = torch.get_rng_state()
        super().post_get()

    def step(self, *args):
        super().pre_get()
        self.pre_get = self.__before_get_item_after_iteration_finish
    
    def __before_get_item_after_iteration_finish(self):
        self.pre_get = self.__before_get_item_normally
    
    def __before_get_item_normally(self):
        super().pre_get()
        torch.set_rng_state(self.__transform_rng_state)

    def __before_get_item_at_first(self):
        super().pre_get()
        self.pre_get = self.__before_get_item_normally

    def __getstate__(self):
        state: dict = {}
        state.update(self.__dict__)
        from .utils import save_state_from_names
        state = save_state_from_names(state, __class__.pre_get.__name__)
        return state
    
    def __setstate__(self, state):
        from .utils import restore_state_from_names
        state = restore_state_from_names(self, state, __class__.pre_get.__name__)
        self.__dict__.update(state)


class PeriodRetentionScheduler(RetainedRandomStateScheduler):
    '''
    This scheduler make the random state immutable for a given epochs period,
    after that the random state will change.
    '''
    def __init__(self, retention_period_num: int = 0):
        super().__init__(retention_period_num)
        self.step = self.__update_period_at_first

    def step(self):
        pass
    
    @property
    def retention_period_num(self):
        return self.retention
    
    @retention_period_num.setter
    def retention_period_num(self, value):
        self.retention = value

    def __update_period_normally(self):
        super().step()
        torch.set_rng_state(self.__initial_period_rng_state)
        if self.__delta_period < self.retention - 1:
            self.__delta_period += 1
        else:
            self.step = self.__update_period_at_first

    def __update_period_at_first(self):
        self.__delta_period = 1
        self.__initial_period_rng_state = torch.get_rng_state()
        self.step = self.__update_period_normally

    def __getstate__(self):
        state = super().__getstate__()
        from .utils import save_state_from_names
        state = save_state_from_names(state, __class__.step.__name__)
        return state
    
    def __setstate__(self, state):
        super().__setstate__(state)
        from .utils import restore_state_from_names
        state = restore_state_from_names(self, state, __class__.step.__name__)
        self.__dict__.update(state)


class LossAwaredScheduler(RetainedRandomStateScheduler):
    '''
    This scheduler keep the random state the same when the loss difference is huge,
    if the difference is less than the given tolerance, the random state will change.
    '''
    def __init__(self, tolerance: float = 1e-2):
        super().__init__(tolerance)
        self.step = self.__update_step_period_at_first

    def step(self, loss):
        pass
    
    @property
    def tolerance(self):
        return self.retention
    
    @tolerance.setter
    def tolerance(self, value):
        self.retention = value

    def __update_step_period_normally(self, loss):
        super().step()
        torch.set_rng_state(self.__initial_epoch_rng_state)
        if abs(self.__last_loss - loss) > self.retention:
            self.__last_loss = loss
        else:
            self.step = self.__update_step_period_at_first

    def __update_step_period_at_first(self, loss):
        self.__last_loss = loss
        self.__initial_epoch_rng_state = torch.get_rng_state()
        self.step = self.__update_step_period_normally
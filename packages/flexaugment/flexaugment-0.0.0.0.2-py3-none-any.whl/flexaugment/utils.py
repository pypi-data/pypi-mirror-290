from typing import Union, Callable, Iterable, Tuple, Any
from torchvision.transforms import transforms, autoaugment


def _getitem(iterable, index):
    try:
        return iterable[index]
    except IndexError:
        return None


def _callfunc(func, arg):
    if func is None:
        return arg
    else:
        return func(arg)


def get_combined_transform(transform: Union[Callable[..., Tuple[Any, ...]], Iterable[Callable[[Any], Any]], None]):
    if isinstance(transform, Iterable):
        def transform_func(*args):
            return (_callfunc(_getitem(transform, i), arg) for i, arg in enumerate(args))
        return transform_func
    else:        
        return transform


def save_state_from_names(state, *names):
    for name in names:
        state[name] = state[name].__name__
    return state


def restore_state_from_names(obj, state, *names):
    from types import MethodType
    for name in names:
        for current_type in type(obj).__mro__:
            step_func = current_type.__dict__.get(f"_{current_type.__name__}{state[name]}")
            if step_func is not None:
                break
        state[name] = MethodType(step_func, obj)
    return state
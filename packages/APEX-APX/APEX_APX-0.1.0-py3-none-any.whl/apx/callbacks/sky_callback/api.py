"""ApxCallback APIs to benchmark an iterative task on cloud resources.

ApxCallback measures averaged time taken by each 'step', and extrapolates it to
the makespan of the task. The APIs provide:
- `init` function to initialize the callback.
- Three equivalent ways to measure the time taken by each step.

Example:
    1. Use `apx_callback.init` to initialize the callback.
       Optionally, specify the total number of steps that the task will take.
    ```python
        apx_callback.init(total_steps=num_epochs * len(train_dataloader))
    ```

    2. Mark the start and end of each step with ApxCallback APIs.
       Select one of the three equivalent methods.

    1) Wrap your iterable (e.g., dataloader) with `step_iterator`.
    ```python
    from apx_callback import step_iterator

    for batch in step_iterator(train_dataloader):
        ...
    ```

    2) Wrap your loop body with `apx_callback.step`.
    ```python
    for i in range(num_steps):
        with apx_callback.step():
            ...
    ```

    3) Call `apx_callback.step_begin` and `apx_callback.step_end`
       at the beginning and end of each step.
    ```python
    for i in range(num_steps):
        apx_callback.step_begin()
        ...
        apx_callback.step_end()
    ```
"""
import collections
import contextlib
from typing import Optional

from apx_callback import base
from apx_callback import utils

_DISABLE_CALLBACK = utils.DISABLE_CALLBACK
_apx_callback = None
_initialized = False


def init(global_rank: int = 0,
         log_dir: Optional[str] = None,
         total_steps: Optional[int] = None) -> None:
    """Initializes ApxCallback.

    NOTE: This function is not thread-safe. Only one thread per process should
        call this function.
    NOTE: Do not use this function when using framework-integrated ApxCallback
        APIs (e.g., ApxKerasCallback).

    Args:
        global_rank: global rank of the calling process. In non-distributed tasks,
            the rank should be 0. In distributed tasks, only one process should
            have rank 0. Check your framework API to query the global rank
            (e.g., torch.distributed.get_rank() or hvd.rank()).
        log_dir: A directory to store the logs.
        total_steps: A total number of steps. If None, ApxCallback will not
            estimate the total time to complete the task.
    """
    if _DISABLE_CALLBACK:
        return

    global _initialized
    if _initialized:
        raise RuntimeError('apx_callback is already initialized. '
                           'Please call `apx_callback.init` only once.')

    global _apx_callback
    if global_rank == 0:
        _apx_callback = base.BaseCallback(log_dir=log_dir,
                                          total_steps=total_steps)
    # Processes with non-zero ranks should also set this flag.
    _initialized = True


def step_begin() -> None:
    """Marks the beginning of a step.

    NOTE: This function is not thread-safe. Only one thread per process should
        call this function.
    """
    if _DISABLE_CALLBACK:
        return
    if not _initialized:
        raise RuntimeError(
            'apx_callback is not initialized. '
            'Please call `apx_callback.init` before using apx_callback.')
    if _apx_callback is not None:
        # Only rank-0 process will execute below.
        _apx_callback.on_step_begin()


def step_end() -> None:
    """Marks the end of a step.

    NOTE: This function is not thread-safe. Only one thread per process should
        call this function.
    """
    if _DISABLE_CALLBACK:
        return
    if not _initialized:
        raise RuntimeError(
            'apx_callback is not initialized. '
            'Please call `apx_callback.init` before using apx_callback.')
    if _apx_callback is not None:
        # Only rank-0 process will execute below.
        _apx_callback.on_step_end()


@contextlib.contextmanager
def step():
    """Marks the beginning and end of a step.

    NOTE: This function is not thread-safe. Only one thread per process should
        call this function.
    """
    step_begin()
    yield
    step_end()


class step_iterator:
    """Wraps an iterable with ApxCallback APIs.

    NOTE: This class is not thread-safe. Only one thread per process should
        create/use this class.
    """

    def __init__(self, iterable: collections.abc.Iterable) -> None:
        self._iterable = iterable
        if _DISABLE_CALLBACK:
            return
        if not _initialized:
            raise RuntimeError(
                'apx_callback is not initialized. '
                'Please call `apx_callback.init` before using apx_callback.')

    def __iter__(self):
        # Inlining instance variables as locals for speed optimization.
        # Refer to: https://github.com/tqdm/tqdm/blob/4f208e72552c4d916aa4fe6a955349ee8b2ed353/tqdm/std.py#L1177  # pylint: disable=line-too-long
        iterable = self._iterable
        if _DISABLE_CALLBACK or _apx_callback is None:
            for obj in iterable:
                yield obj
        else:
            # Only rank-0 process will execute below.
            for obj in iterable:
                _apx_callback.on_step_begin()
                yield obj
                _apx_callback.on_step_end()

from typing import Any
from collections.abc import Callable
import time


def retry(
    func: Callable[[], Any],
    exceptions: tuple[type[Exception], ...],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
    if max_attempts < 1:
        raise ValueError("max_attempts deve ser maior ou igual a 1.")

    if delay < 0:
        raise ValueError("delay não pode ser negativo.")

    for attempt in range(1, max_attempts + 1):
        try:
            return func()

        except exceptions:
            if attempt == max_attempts:
                raise

            wait_time = delay * (2 ** (attempt - 1))

            time.sleep(wait_time)

    raise RuntimeError("Retry não conseguiu executar a função.")

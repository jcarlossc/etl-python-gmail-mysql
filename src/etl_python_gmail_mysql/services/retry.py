import time
from collections.abc import Callable
from typing import Any


def retry(
    func: Callable[[], Any],
    exceptions: tuple[type[Exception], ...],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
    """
    Executa uma função novamente em caso de exceções recuperáveis.

    Utiliza exponential backoff para aumentar progressivamente
    o intervalo entre as tentativas.

    Args:
        func: Função sem argumentos que será executada.
        exceptions: Tupla contendo as exceções que permitem
            uma nova tentativa.
        max_attempts: Número máximo de tentativas.
        delay: Tempo inicial, em segundos, antes de uma nova
            tentativa. O intervalo é duplicado a cada falha.

    Returns:
        Resultado retornado pela função quando a execução
        for concluída com sucesso.

    Raises:
        ValueError: Se max_attempts for menor que 1 ou
            delay for negativo.
        Exception: Propaga a última exceção quando todas
            as tentativas forem malsucedidas.

    Example:
        >>> retry(
        ...     lambda: "sucesso",
        ...     exceptions=(ConnectionError,),
        ... )
        'sucesso'
    """

    # Valida a quantidade mínima de tentativas.
    if max_attempts < 1:
        raise ValueError("max_attempts deve ser maior ou igual a 1.")

    # Não permite tempo de espera negativo.
    if delay < 0:
        raise ValueError("delay não pode ser negativo.")

    for attempt in range(1, max_attempts + 1):
        try:
            # Executa a operação.
            return func()

        except exceptions:
            # Na última tentativa, não há motivo para esperar.
            # A exceção original será propagada.
            if attempt == max_attempts:
                raise

            # Exponential backoff:
            # delay=1 → 1s, 2s, 4s, 8s...
            wait_time = delay * (2 ** (attempt - 1))

            time.sleep(wait_time)

    # Este ponto não deve ser alcançado.
    raise RuntimeError("Retry não conseguiu executar a função.")

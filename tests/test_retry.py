import pytest

from etl_python_gmail_mysql.services.retry import retry


def test_retry_success_first_attempt():
    """Deve retornar o resultado sem realizar novas tentativas."""

    attempts = 0

    def operation():
        nonlocal attempts

        attempts += 1

        return "sucesso"

    result = retry(
        operation,
        exceptions=(ConnectionError,),
    )

    assert result == "sucesso"
    assert attempts == 1


def test_retry_success_after_failures(monkeypatch):
    """Deve repetir a operação até obter sucesso."""

    attempts = 0
    sleep_times = []

    def operation():
        nonlocal attempts

        attempts += 1

        if attempts < 3:
            raise ConnectionError("Falha temporária.")

        return "sucesso"

    def fake_sleep(seconds):
        sleep_times.append(seconds)

    monkeypatch.setattr(
        "etl_python_gmail_mysql.services.retry.time.sleep",
        fake_sleep,
    )

    result = retry(
        operation,
        exceptions=(ConnectionError,),
        max_attempts=3,
        delay=1,
    )

    assert result == "sucesso"
    assert attempts == 3
    assert sleep_times == [1, 2]


def test_retry_raises_after_max_attempts(monkeypatch):
    """Deve propagar a exceção após atingir o limite de tentativas."""

    attempts = 0
    sleep_times = []

    def operation():
        nonlocal attempts

        attempts += 1

        raise ConnectionError("Serviço indisponível.")

    def fake_sleep(seconds):
        sleep_times.append(seconds)

    monkeypatch.setattr(
        "etl_python_gmail_mysql.services.retry.time.sleep",
        fake_sleep,
    )

    with pytest.raises(
        ConnectionError,
        match="Serviço indisponível.",
    ):
        retry(
            operation,
            exceptions=(ConnectionError,),
            max_attempts=3,
            delay=1,
        )

    assert attempts == 3
    assert sleep_times == [1, 2]


def test_retry_does_not_catch_unexpected_exception():
    """Deve propagar imediatamente uma exceção não configurada."""

    attempts = 0

    def operation():
        nonlocal attempts

        attempts += 1

        raise ValueError("Erro de validação.")

    with pytest.raises(
        ValueError,
        match="Erro de validação.",
    ):
        retry(
            operation,
            exceptions=(ConnectionError,),
        )

    assert attempts == 1


def test_retry_exponential_backoff(monkeypatch):
    """Deve aumentar progressivamente o tempo entre as tentativas."""

    sleep_times = []

    def operation():
        raise ConnectionError("Falha.")

    def fake_sleep(seconds):
        sleep_times.append(seconds)

    monkeypatch.setattr(
        "etl_python_gmail_mysql.services.retry.time.sleep",
        fake_sleep,
    )

    with pytest.raises(ConnectionError):
        retry(
            operation,
            exceptions=(ConnectionError,),
            max_attempts=4,
            delay=1,
        )

    assert sleep_times == [1, 2, 4]


def test_retry_invalid_max_attempts():
    """Deve rejeitar quantidade inválida de tentativas."""

    with pytest.raises(
        ValueError,
        match="max_attempts",
    ):
        retry(
            lambda: "sucesso",
            exceptions=(ConnectionError,),
            max_attempts=0,
        )


def test_retry_negative_delay():
    """Deve rejeitar um tempo de espera negativo."""

    with pytest.raises(
        ValueError,
        match="delay",
    ):
        retry(
            lambda: "sucesso",
            exceptions=(ConnectionError,),
            delay=-1,
        )

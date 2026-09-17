import logging

import etl_python_gmail_mysql.main as main_module


def test_main_success(monkeypatch, caplog):
    """
    Testa a execução bem-sucedida da função main().

    Verifica se o pipeline é executado e se as mensagens
    de início e finalização são registradas.
    """

    pipeline_called = False

    def fake_get_run_pipeline():
        nonlocal pipeline_called
        pipeline_called = True

    monkeypatch.setattr(
        main_module,
        "get_run_pipeline",
        fake_get_run_pipeline,
    )

    with caplog.at_level(logging.INFO):
        main_module.main()

    assert pipeline_called is True

    assert "Iniciando aplicação." in caplog.text
    assert "Aplicação finalizada com sucesso." in caplog.text

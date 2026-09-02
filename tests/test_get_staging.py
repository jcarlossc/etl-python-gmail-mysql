from pathlib import Path

from etl_python_gmail_mysql.staging.get_staging import (
    move_to_staging,
)


def test_move_files_to_staging_copia_csv_e_xlsx(
    tmp_path: Path,
) -> None:
    """
    Testa a cópia de arquivos CSV e XLSX para o staging.
    """

    # Cria o diretório de downloads.
    download_dir = tmp_path / "downloads"
    download_dir.mkdir()

    # Define o diretório de staging.
    staging_dir = tmp_path / "staging"

    # Cria arquivos de teste.
    csv_file = download_dir / "vendas.csv"
    xlsx_file = download_dir / "clientes.xlsx"

    csv_file.write_text(
        "id,nome\n1,Carlos\n",
        encoding="utf-8",
    )

    xlsx_file.write_bytes(
        b"conteudo-xlsx",
    )

    # Executa a função.
    result = move_to_staging(
        download_dir=download_dir,
        staging_dir=staging_dir,
    )

    # Verifica os contadores.
    assert result == {
        "csv": 1,
        "xlsx": 1,
    }

    # Verifica se os arquivos foram copiados.
    assert (staging_dir / "csv" / "vendas.csv").exists()
    assert (staging_dir / "xlsx" / "clientes.xlsx").exists()


def test_move_files_to_staging_ignora_extensao_nao_suportada(
    tmp_path: Path,
) -> None:
    """
    Testa se arquivos com extensões não suportadas são ignorados.
    """

    download_dir = tmp_path / "downloads"
    download_dir.mkdir()

    staging_dir = tmp_path / "staging"

    # Cria um arquivo que não deve ser copiado.
    txt_file = download_dir / "arquivo.txt"
    txt_file.write_text(
        "teste",
        encoding="utf-8",
    )

    result = move_to_staging(
        download_dir=download_dir,
        staging_dir=staging_dir,
    )

    assert result == {
        "csv": 0,
        "xlsx": 0,
    }

    assert not (staging_dir / "csv" / "arquivo.txt").exists()
    assert not (staging_dir / "xlsx" / "arquivo.txt").exists()

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from loguru import logger  # noqa: E402
from logs.set_logger import setup_logger  # noqa: E402

import pandas as pd  # noqa: E402
from pandas import DataFrame  # noqa: E402

K = 1000

# ===== LOG ===== #
LOG_FILE = ROOT_DIR / "logs"
LOG_NAME = "data_log"

setup_logger(log_file_path=LOG_FILE, log_name=LOG_NAME, overwrite=True)

logger.info("=" * 50)
logger.info("Log inicializado.")
###################

DATA_PATH = ROOT_DIR / "ml_model_workspace" / "data"

# ===== CONFIG DO PANDAS ===== #
# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", 100)  # serve pra mostrar até 100 linhas antes de ocultar
# pd.set_option("display.width", 1000)
################################


def data_normalizer(df: DataFrame, arquivo: str, tipo: list) -> DataFrame:
    """Normaliza uma base de dados se necessário."""

    logger.info(f"Normalizando a base do arquivo '{arquivo}'.")

    if tipo == "DEMOGRAFIA":
        df.columns = ["MUNICIPIO", "POPULACAO", "AREA", "DENSIDADE"]
    elif tipo == "CONDICAO_DE_VIDA":
        pass
    elif tipo == "EMPREGABILIDADE":
        pass
    elif tipo == "SEGURANCA":
        pass
    else:
        logger.warning(
            f"O tipo '{tipo}' não é compatível com o arquivo '{arquivo}'.",
            "Pulando processamento e retornando base não normalizada",
        )

        return df

    print(df.columns.tolist())

    print(df.head())

    # if df["POPULACAO"] > 100 * K:
    #     df["POPULACAO"] = df["POPULACAO"] / 100 * K

    df_normalizado = df

    logger.info("Normalização concluida com sucesso.")

    return df_normalizado


def get_data() -> dict:
    """Extrai os dados da pasta 'data' do projeto"""

    logger.info("Iniciando extração de dados.")

    tipos = ["SEGURANCA", "EMPREGABILIDADE", "CONDICAO_DE_VIDA", "DEMOGRAFIA"]

    dfs = {tipo: [] for tipo in tipos}

    df_list = []
    for arquivo in DATA_PATH.rglob("*"):
        arquivo = str(arquivo)
        arquivo_upper = arquivo.upper()

        if arquivo.endswith(".md"):
            continue

        if arquivo_upper.endswith(".CSV"):
            df = pd.read_csv(arquivo, sep=";", encoding="latin-1", header=None)
            # o header permite que eu consiga redefinir o nome das colunas
        elif arquivo_upper.endswith("XLSX"):
            df = pd.read_excel(arquivo, skiprows=4, header=None)
            # o skiprows pula X linhas da tabela
        else:
            logger.warning(f"Tipo do arquivo {arquivo} é inválido. Pulando processamento do arquivo.")

            continue

        for tipo in tipos:
            if tipo in arquivo_upper:
                df_normalizado = data_normalizer(df, arquivo, tipo)
                df_list.append(df_normalizado)

                logger.info(f"DataFrame do arquivo '{arquivo}' criado.")

                dfs[tipo] = pd.concat(df_list, ignore_index=True)
                # ignore_index=True pra tentar evitar que os índices repitam no final
                logger.info(f"Colocando o DataFrame do arquivo '{arquivo}' no tipo '{tipo}'.")

    return dfs


def main():
    dict = get_data()

    tipos = ["SEGURANCA", "EMPREGABILIDADE", "CONDICAO_DE_VIDA", "DEMOGRAFIA"]

    for tipo in tipos:
        print(f"Bases de '{tipo}': ")

        print(dict[tipo])

        print("=" * 50)


if __name__ == "__main__":
    main()

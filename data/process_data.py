import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from utils.time_utils import time_count  # noqa: E402

from loguru import logger  # noqa: E402
from logs.set_logger import setup_logger  # noqa: E402

import pandas as pd  # noqa: E402
from pandas import DataFrame  # noqa: E402
from pandas import Series  # noqa: E402

# ===== LOG ===== #
LOG_FILE = ROOT_DIR / "logs"
LOG_NAME = "data_log"

setup_logger(log_file_path=LOG_FILE, log_name=LOG_NAME, overwrite=True)

logger.info("=" * 32)
logger.info("LOG INICIALIZED.")
###################

DATA_PATH = ROOT_DIR / "data/raw"
PROCESSED_PATH = ROOT_DIR / "data/processed"

TYPES = ["DEMOGRAPHY", "LIFE_CONDITION", "EMPREGABILITY", "SECURITY", "FEMICIDE"]


def print_log_type(type: str):
    logger.info(f"TYPE: {type.upper()}")


def check_type(obj_check, type_map: dict, mode: str, *args, **kwargs):
    """
    Checks 'obj_check' against the keys in 'type_map'.

    Returns the associated value if a match is found and its type.
    """

    for key, func in type_map.items():
        if mode == "EXACTLY" and obj_check == key:
            return key, (func(*args, **kwargs) if callable(func) else func)
        elif mode == "CONTAINS" and key in obj_check:
            return key, (func(*args, **kwargs) if callable(func) else func)

    return None, None


def padronize_df_column_string(df: DataFrame, column: str) -> Series:
    """
    Padronize strings from a especific column of a DataFrame.

    Returns a column padronized.

    1. normalize("NFKD") => separates the accent from the letter (e.g., 'é' turns into 'e' + '´').
    2. encode("ascii", errors="ignore") => keeps only ASCII characters (throws out '´' and 'ç', keeping just 'c').
    3. decode("utf-8") => transforms the bytes back into normal text.
    """

    return (
        df[column]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
        .str.replace(" ", "_")
    )


def normalize_demography(df: DataFrame) -> DataFrame:
    """
    Normalize DEMOGRAPHY type database.
    """

    print_log_type("DEMOGRAPHY")

    df = df[["munic", "ano", "pop_munic"]]

    df = df.rename(columns={"munic": "municipio", "pop_munic": "populacao"})

    df["municipio"] = padronize_df_column_string(df, "municipio")

    return df


def normalize_life_condition(df: DataFrame) -> DataFrame:
    """
    Normalize LIFE CONDITION type database.

    Maps encoded columns to their readable meanings using the ATLAS dictionary.
    """

    print_log_type("LIFE_CONDITION")

    df = df.rename(columns={"Territorialidades": "municipio"})
    df = df.dropna(subset=["municipio"])
    df = df[~df["municipio"].str.contains("Fontes:", na=False)]

    df["municipio"] = df["municipio"].str.replace(r"\s+\([A-Z]{2}\)$", "", regex=True)
    df["municipio"] = padronize_df_column_string(df, "municipio")

    mantain_columns = [
        c for c in df.columns if "Desagregação" not in c
    ]  # filtra fora as colunas de "Desagregação" (brancos, negros, etc) para poupar memória
    df = df[mantain_columns]

    new_columns = {}
    for col in df.columns:
        if col != "municipio":
            # extrai o ano (os últimos 4 caracteres) e o nome do indicador (o resto da string)
            # |
            # V
            year = col[-4:]
            indicator_name = col[:-4].strip()
            new_columns[col] = f"{indicator_name}_{year}"

    df = df.rename(columns=new_columns)

    indicators = list(set([c[:-5] for c in df.columns if c != "municipio"]))

    df_long = pd.wide_to_long(df, stubnames=indicators, i="municipio", j="ano", sep="_").reset_index()

    mapa_nomes = {
        "Índice de Gini": "gini",
        "IDHM": "idhm",
        "Renda per capita": "rdpc",
        "Taxa de analfabetismo - 18 anos ou mais de idade": "taxa_analfabetismo_18mais",
        "Esperança de vida ao nascer": "esperanca_de_vida_ao_nascer",
        "Mortalidade infantil": "mortalidade_ate_1_ano_de_idade",
        "% da população em domicílios com água encanada": "pop_agua_encanada",
        "% de pessoas em domicílios urbanos com coleta de lixo": "pop_com_coleta_de_lixo",
        "% da população que vive em domicílios com banheiro e água encanada": "pop_agua_e_esgoto_inadequado",
    }

    df_long = df_long.rename(columns=mapa_nomes)

    final_columns = [
        "municipio",
        "ano",
        "idhm",
        "gini",
        "rdpc",
        "taxa_desocup_18mais",
        "esperanca_de_vida_ao_nascer",
        "mortalidade_ate_1_ano_de_idade",
        "pop_agua_encanada",
        "pop_com_coleta_de_lixo",
        "pop_agua_e_esgoto_inadequado",
        "taxa_analfabetismo_18mais",
    ]

    present_columns = [
        col for col in final_columns if col in df_long.columns
    ]  # previne que o código quebre se um indicador não tiver sido exportado do site

    return df_long[present_columns]


def normalize_empregability(df: DataFrame) -> DataFrame:
    """
    Normalize EMPREGABILITY type database.

    Reads the average income table, fills missing municipality names, extracts the "Total" category, and formats it for merging.
    """

    print_log_type("EMPREGABILITY")

    df.columns = [
        "municipio",
        "categoria_emprego",
        "rendimento_total",
        "rendimento_homens",
        "rendimento_mulheres",
    ]

    df["municipio"] = df["municipio"].ffill()  # pega o nome da cidade e vai copiando para as células 'NaN' logo abaixo

    df = df[
        df["categoria_emprego"] == "Total"
    ].copy()  # filtra apenas o bloco de "Total" (ignorando as quebras por tipo de emprego)

    df = df[
        df["municipio"] != "Rio de Janeiro"
    ]  # remove a linha do Estado (que não tem " (RJ)") para não confundir com a Cidade

    df["municipio"] = df["municipio"].str.replace(
        " (RJ)", "", regex=False
    )  # remove o sufixo " (RJ)" de todas as cidades (ex: "Macaé (RJ)" vira "Macaé")

    df["municipio"] = padronize_df_column_string(df, "municipio")

    df["ano"] = 2022

    return df[["municipio", "ano", "rendimento_total", "rendimento_homens", "rendimento_mulheres"]]


def normalize_security(df: DataFrame) -> DataFrame:
    """
    Normalize SECURITY type database.

    Converts Brazilian comma decimals to floats and aggregates monthly rates into annual rates per 100k inhabitants.
    """

    print_log_type("SECURITY")

    crime_columns = df.columns[3:-1]  # pega o nome de todas as colunas de crimes (ignora ano, mes, mes_ano e fase)

    # |
    # V converte a vírgula para ponto e transforma em número (float) para o modelo de machine learning
    for col in crime_columns:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

    anual_df = df.groupby("ano")[crime_columns].sum().reset_index()  # agrupa os dados por ANO e SOMA as taxas mensais
    # (se em jan teve 2 roubos/100k e em fev teve 3/100k, o ano teve 5 roubos/100k)

    anual_df = anual_df.round(2)

    # como essa base é do estado todo, é melhor criar uma coluna para não
    # misturar com as bases de município depois na hora do merge.
    anual_df["municipio"] = "estado_do_rio_de_janeiro"

    return anual_df


def normalize_femicide(femi_df: DataFrame, demo_df: DataFrame) -> DataFrame:
    """
    Normalize FEMICIDE type database.
    """
    print_log_type("FEMICIDE")

    femi_df.columns = [
        "cips",
        "aisp",
        "risp",
        "municipio",
        "mes",
        "ano",
        "vitimas_feminicidio",
        "tentativa_feminicidio",
        "fase",
    ]

    femi_df["ano"] = pd.to_numeric(femi_df["ano"], errors="coerce")
    femi_df["vitimas_feminicidio"] = pd.to_numeric(femi_df["vitimas_feminicidio"], errors="coerce")
    femi_df = femi_df.dropna(subset=["ano", "vitimas_feminicidio"])

    femi_df["municipio"] = padronize_df_column_string(femi_df, "municipio")

    femi_df["ano"] = femi_df["ano"].astype(int)
    demo_df["ano"] = demo_df["ano"].astype(int)

    ano_max_demo = demo_df["ano"].max()  # Descobre que é 2022
    ano_max_femi = femi_df["ano"].max()  # Descobre que é 2026

    if ano_max_femi > ano_max_demo:
        demo_ultimo_ano = demo_df[demo_df["ano"] == ano_max_demo].copy()

        anos_extras = []

        for ano_novo in range(ano_max_demo + 1, ano_max_femi + 1):
            temp_df = demo_ultimo_ano.copy()
            temp_df["ano"] = ano_novo
            anos_extras.append(temp_df)

        demo_df = pd.concat([demo_df] + anos_extras, ignore_index=True)

    agrup_femi_df = femi_df.groupby(["municipio", "ano"]).agg({"vitimas_feminicidio": "sum"}).reset_index()

    crossed_df = pd.merge(agrup_femi_df, demo_df, on=["municipio", "ano"], how="inner")

    crossed_df["taxa_feminicidio_100k"] = (crossed_df["vitimas_feminicidio"] / crossed_df["populacao"]) * 100000
    crossed_df["taxa_feminicidio_100k"] = crossed_df["taxa_feminicidio_100k"].round(2)

    return crossed_df


@time_count
def data_normalize(df: DataFrame, file: str, type: str, **kwargs) -> DataFrame:
    """
    Normalize a database if needed.
    """

    logger.info(f"Normalizing the database of the file: '{file}'.")

    normalize_rules = {
        "DEMOGRAPHY": normalize_demography,
        "LIFE_CONDITION": normalize_life_condition,
        "EMPREGABILITY": normalize_empregability,
        "SECURITY": normalize_security,
        "FEMICIDE": normalize_femicide,
    }

    matched_type, return_value = check_type(type, normalize_rules, "EXACTLY", df, **kwargs)

    if matched_type:
        df_normalized = return_value
    else:
        logger.warning(
            f"'{matched_type}' type is incompatible with the '{file}' file.",
            "Skipping the proccess and returning database not normalized.",
        )

        return df

    logger.info("Normalization complete.")
    logger.info(f"'{matched_type}' DataFrame normalized.")

    return df_normalized


def get_data_demography(file: str) -> DataFrame:
    """
    Get data for DEMOGRAPHY type.
    """

    df = pd.read_csv(file, sep=";", encoding="latin-1")

    return df


def get_data_life_condition(file: str) -> DataFrame:
    """
    Get data for LIFE CONDITION type.
    """

    df = pd.read_excel(file, engine="openpyxl")

    return df


def get_data_empregability(file: str) -> DataFrame:
    """
    Get data for EMPREGABILITY type.
    """

    df = pd.read_excel(file, skiprows=4, header=None, engine="openpyxl")

    return df


def get_data_security(file: str) -> DataFrame:
    """
    Get data for SECURITY type.
    """

    df = pd.read_csv(
        file, sep=";", decimal=",", encoding="latin-1"
    )  # o header permite que eu consiga redefinir o nome das colunas

    return df


def get_data_femicide(file: str) -> DataFrame:
    """
    Get data for FEMICIDE type.
    """

    df = pd.read_csv(file, sep=";", encoding="latin-1", header=None)

    return df


@time_count
def get_data() -> dict:
    """
    Extract data from the 'data' folder of the project.
    """

    logger.info("Starting data extraction.")

    data_rules = {
        "DEMOGRAPHY": get_data_demography,
        "LIFE_CONDITION": get_data_life_condition,
        "EMPREGABILITY": get_data_empregability,
        "SECURITY": get_data_security,
        "FEMICIDE": get_data_femicide,
    }

    dfs = {type: [] for type in TYPES}
    files_map = {}

    for file in DATA_PATH.rglob("*"):
        if file.is_dir() or file.suffix == ".md":
            continue

        file_str = str(file)
        file_upper = file_str.upper()

        matched_type, return_value = check_type(file_upper, data_rules, "CONTAINS", file_str)

        if matched_type:
            dfs[matched_type] = return_value
            files_map[matched_type] = file_str
        else:
            logger.warning(f"Type of {file_str} is invalid. Skipping file process.")

            continue

    for matched_type, raw_df in dfs.items():
        if isinstance(raw_df, list) and len(raw_df) == 0:
            continue

        file_str = files_map[matched_type]

        if matched_type == "FEMICIDE":
            normalized_df = data_normalize(raw_df, file_str, matched_type, demo_df=dfs["DEMOGRAPHY"])
        else:
            normalized_df = data_normalize(raw_df, file_str, matched_type)

        dfs[matched_type] = normalized_df

        logger.info(f"File's '{file_str}' DataFrame created and put in '{matched_type}' type.")

    logger.info("Data extraction complete.")

    return dfs


@time_count
def save_data(dfs: dict):
    """
    Saves the normalized DataFrames into the processed data folder.
    """

    logger.info("Starting data export to processed folder.")

    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    for type_key, df in dfs.items():
        if df is None or (isinstance(df, list) and len(df) == 0):
            logger.warning(f"No data to save for '{type_key}'. Skipping.")
            continue

        file_name = f"{type_key.lower()}_normalized.csv"
        output_path = PROCESSED_PATH / file_name

        df.to_csv(output_path, index=False, sep=";", encoding="utf-8")

        logger.info(f"Successfully saved '{type_key}' DataFrame to: {file_name}")

    logger.info("Data export complete.")


def process_data():
    dfs = get_data()
    save_data(dfs)


if __name__ == "__main__":
    process_data()

#!/bin/bash

############################################
# ETL PIPELINE - LIVING STANDARD SIMULATION
############################################

echo "=========================================="
echo "          Starting Data Pipeline          "
echo "=========================================="

cd "$(dirname "$0")/.."
export PYTHONPATH=$(pwd)

##### ENVIRONMENT CHECK #####
echo "[0/2] Checking environment dependencies..."
source environment/check_env.sh

# se o script do ambiente falhar (retornar uma saída "não-zero")
if [ $? -ne 0 ]; then
    echo "ERROR: Aborting ETL process because the environment could not be activated."
    exit 1
fi
###################################

##### PROCESSED LAYER #####
echo "[1/2] Processing raw files..."
python data/process_data.py

if [ $? -ne 0 ]; then
    echo "ERROR: Data extraction failed. Aborting ETL."
    exit 1
fi
############################

##### REFINED LAYER #####
echo "[2/2] Generating master table..."
python data/build_final_data.py

if [ $? -ne 0 ]; then
    echo "ERROR: Data consolidation failed. Aborting ETL."
    exit 1
fi
##########################

echo "=========================================="
echo "      Pipeline completed successfully     "
echo "=========================================="
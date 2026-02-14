#!/bin/bash

TARGET_ENV="liv-stan-simulation"

if [ "$CONDA_DEFAULT_ENV" = "$TARGET_ENV" ]; then
    echo "Ambiente '$TARGET_ENV' já está ativo."
else
    echo "Ativando ambiente '$TARGET_ENV'..."

    source ~/miniconda3/etc/profile.d/conda.sh
    
    conda activate $TARGET_ENV
    
    if [ $? -eq 0 ]; then
        echo "Ambiente ativado."
    else
        echo "Erro ao ativar o ambiente. Verifique se o nome está correto."
    fi
fi
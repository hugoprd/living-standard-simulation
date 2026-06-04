#!/bin/bash

TARGET_ENV="liv-stan-simulation"

if [ "$CONDA_DEFAULT_ENV" = "$TARGET_ENV" ]; then
    echo "Environment '$TARGET_ENV' is already active."
    return 0
else
    echo "Activating environment '$TARGET_ENV'..."

    source ~/miniconda3/etc/profile.d/conda.sh
    
    conda activate $TARGET_ENV
    
    if [ $? -eq 0 ]; then
        echo "Environment activated successfully."
        return 0
    else
        echo "ERROR: Failed to activate the environment. Please check if the name is correct."
        return 1
    fi
fi
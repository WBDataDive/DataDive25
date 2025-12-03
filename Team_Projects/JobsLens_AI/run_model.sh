#!/bin/bash

# Setup script for running the AI Jobs forecasting model
# Usage: bash Team_Projects/JobsLens_AI/run_model.sh

echo "================================================"
echo "JobsLens AI - Model Setup and Execution"
echo "================================================"

# Navigate to project root
cd "$(dirname "$0")/../.."

# Check if venv exists
if [ ! -d "Team_Projects/JobsLens_AI/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv Team_Projects/JobsLens_AI/venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source Team_Projects/JobsLens_AI/venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r Team_Projects/JobsLens_AI/requirements.txt

# Run the model
echo ""
echo "================================================"
echo "Running AI Jobs Forecasting Model"
echo "================================================"
python Team_Projects/JobsLens_AI/src/model_ai_jobs.py

# Deactivate virtual environment
deactivate

echo ""
echo "================================================"
echo "Model execution complete!"
echo "================================================"

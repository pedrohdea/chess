#!/bin/bash

echo "Organizando imports com isort..."
isort . --profile black

echo "Formatando código com black..."
black .

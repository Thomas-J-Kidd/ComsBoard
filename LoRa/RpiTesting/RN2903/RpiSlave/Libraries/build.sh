#!/bin/bash

# CREATE DISTRIBUTION
read -p "Do you want to build the distribution? (Y/N) " input

if [[ "$input" =~ ^[Yy]$ ]]; then
    echo "BUILDING"
    python3 setup.py sdist
fi

# INSTALL DISTRIBUTION
read -p "Do you want to install the distribution? (Y/N) " input

if [[ "$input" =~ ^[Yy]$ ]]; then
    echo "INSTALLING"
    pip install .
fi

# DELETE DISTRIBUTION BUILD
read -p "Do you want to delete the distribution builds? (Y/N) " input

if [[ "$input" =~ ^[Yy]$ ]]; then
    echo "DELETING DISTRIBUTION BUILDS"
    rm -rf build dist myLibs.egg-info
fi

# UNINSTALL DISTRIBUTION
read -p "Do you want to uninstall the distribution from the system? (Y/N) " input

if [[ "$input" =~ ^[Yy]$ ]]; then
    echo "UNINSTALLING"
    pip uninstall myLibs
fi


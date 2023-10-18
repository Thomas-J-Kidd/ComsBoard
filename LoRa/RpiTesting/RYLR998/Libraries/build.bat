@echo off

REM CREATE DISTRIBUTION
set /p input="Do you want to build the distribution? (Y/N)"

if /i "%input%"=="Y" (
    echo "BUILDING"
    python setup.py sdist
)

REM INSTALL DISTRIBUTION
set /p input="Do you want to install the distribution? (Y/N)"

if /i "%input%"=="Y" (
    echo "INSTALLING"
    pip install .
)

REM DELETE DISTRIBUTION BUILD
set /p input="Do you want to delete the distribution builds? (Y/N)"

if /i "%input%"=="Y" (
    echo "DELETING DISTRIBUTION BUILDS"
    rd /S /Q build
    rd /S /Q dist
    rd /S /Q myLibs.egg-info
)

REM UNISTALL DISTRIBUTION
set /p input="Do you want to unistall the distribution from the system? (Y/N)"

if /i "%input%"=="Y" (
    echo "UNINSTALLING"
    pip uninstall myLibs
) 
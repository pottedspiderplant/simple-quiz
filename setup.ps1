# A way to install dependencies from a requirements.txt
# that contains pinned versions and hashes,
# using only built-in tools (pip and venv).

# Usage:
#
# ./setup.ps1
#
# - Will create the virtual environment if it doesn't exist, activate it and install
#   packages from requirements.txt. The virtual environment will be located in your
#   profile, under .virtualenvs, similar to what other package managers use, so you can
#   move this python script folder without breaking your venv. If the environment already
#   exists, it will try to install the packages, in case they were missed last time.
#
# ./setup.ps1 -Redo
#
# - Deletes the virtual environment, then repeats the steps above.
#
# ./setup.ps1 -Delete
#
# - Deletes the virtual environment.
#
# ./setup.ps1 -Activate
#
# - Activates the virtual environment.

[CmdletBinding()]

Param (
    [switch] $Redo,
    [switch] $Delete,
    [switch] $Activate
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = "Stop"


# Settings
$projectName = "simple-quiz"

$requirements = "requirements.txt"


# Logic
$venvPath = "$home\.virtualenvs\$projectName"

if (($Redo -or $Delete) -and (Test-Path $venvPath)) {
    try {
        Get-Command deactivate | Out-Null

        Write-Host "Deactivating virtual environment"

        deactivate
    } catch {}

    Write-Host "Deleting virtual environment"

    Remove-Item -Path $venvPath
}

if ($Delete) {
    return
}

if (!(Test-Path $venvPath)) {
    Write-Host "Creating virtual environment"

    New-Item -ItemType Directory -Path $venvPath | Out-Null

    py -m venv $venvPath

    if ($lastexitcode -ne 0) {
        throw "Error during virtual environment creation"
    }
}

Write-Host "Activating virtual environment"

& $venvPath\Scripts\activate.ps1

if ($Activate) {
    return
}

Write-Host "Installing packages in virtual environment"

py -m pip install -r $PSScriptRoot\$requirements

if ($lastexitcode -ne 0) {
    throw "Error during package installation"
}

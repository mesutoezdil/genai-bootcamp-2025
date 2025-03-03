##########################################################################
# PowerShell Script: Update SSH Configuration
#
# This script appends a new configuration block for a specified host to the
# SSH configuration file located at $env:USERPROFILE\.ssh\config. It is
# designed to ensure the necessary directory exists and provides informative
# messages during execution.
#
# Prerequisites:
#   - Ensure that the following variables are set prior to running the script:
#       $hostname     : The alias or hostname for the SSH entry.
#       $user         : The username to log in as.
#       $identityfile : The full path to the SSH private key file.
#
# Example variable initialization:
#   $hostname = "example.com"
#   $user = "ubuntu"
#   $identityfile = "C:\Users\YourUser\.ssh\id_rsa"
##########################################################################

# Define the SSH configuration entry using a here-string for readability.
$sshConfigEntry = @"
# SSH configuration for host $hostname
Host ${hostname}
  HostName ${hostname}
  User ${user}
  IdentityFile ${identityfile}
"@

# Define the path to the SSH configuration file.
$sshConfigPath = Join-Path -Path $env:USERPROFILE -ChildPath ".ssh\config"

# Ensure the .ssh directory exists; create it if it does not.
$sshDirectory = Split-Path -Path $sshConfigPath -Parent
if (-not (Test-Path -Path $sshDirectory)) {
    Write-Output "SSH directory not found. Creating directory: $sshDirectory"
    New-Item -ItemType Directory -Path $sshDirectory -Force | Out-Null
}

# Append the configuration entry to the SSH config file.
try {
    Add-Content -Path $sshConfigPath -Value $sshConfigEntry
    Write-Output "Successfully added the SSH configuration for host '$hostname' to '$sshConfigPath'."
} catch {
    Write-Error "Error: Failed to update SSH configuration. Details: $_"
}

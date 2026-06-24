if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Root (administrator) required!"
    exit 1
}

$exportFile = "$PSScriptRoot\secpol.txt"

secedit /export /cfg $exportFile > $null

if (Test-Path $exportFile) {
    Write-Output "The current security policy has been successfully exported to file: $exportFile"
} else {
    Write-Error "Failed to export security policy"
}

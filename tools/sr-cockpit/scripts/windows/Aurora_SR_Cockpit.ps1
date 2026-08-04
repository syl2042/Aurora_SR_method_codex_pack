$ErrorActionPreference = "Stop"

$RemoteHost = $env:AURORA_SR_COCKPIT_SSH_HOST
$RemoteUser = if ($env:AURORA_SR_COCKPIT_SSH_USER) { $env:AURORA_SR_COCKPIT_SSH_USER } else { "ubuntu" }
$RemotePort = if ($env:AURORA_SR_COCKPIT_REMOTE_PORT) { [int]$env:AURORA_SR_COCKPIT_REMOTE_PORT } else { 18787 }
$PreferredLocalPorts = @(18787, 18887)
$SshKey = if ($env:AURORA_SR_COCKPIT_SSH_KEY) { $env:AURORA_SR_COCKPIT_SSH_KEY } else { Join-Path $env:USERPROFILE ".ssh\id_rsa" }

function Write-Section($Text) {
  Write-Host ""
  Write-Host "== $Text ==" -ForegroundColor Cyan
}

function Test-HttpHealth($Port) {
  try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/api/health" -TimeoutSec 2
    return ($response.ok -eq $true)
  } catch {
    return $false
  }
}

function Test-LocalTcp($Port) {
  try {
    return (Test-NetConnection 127.0.0.1 -Port $Port -InformationLevel Quiet)
  } catch {
    return $false
  }
}

function Get-FreeLocalPort {
  foreach ($port in $PreferredLocalPorts) {
    if (Test-HttpHealth $port) {
      return @{ Port = $port; AlreadyReady = $true }
    }
  }

  foreach ($port in $PreferredLocalPorts) {
    if (-not (Test-LocalTcp $port)) {
      return @{ Port = $port; AlreadyReady = $false }
    }
  }

  return $null
}

Write-Section "Aurora SR Cockpit"
Write-Host "Serveur distant : $RemoteUser@$RemoteHost"
Write-Host "Port distant    : $RemotePort"
Write-Host "Cle SSH         : $SshKey"

if (-not $RemoteHost) {
  Write-Host ""
  Write-Host "ERREUR: hote SSH non configure." -ForegroundColor Red
  Write-Host "Definis AURORA_SR_COCKPIT_SSH_HOST, par exemple :"
  Write-Host 'setx AURORA_SR_COCKPIT_SSH_HOST "mon-serveur.example.com"'
  Write-Host 'setx AURORA_SR_COCKPIT_SSH_KEY "%USERPROFILE%\.ssh\ma_cle"'
  exit 1
}

if (-not (Test-Path $SshKey)) {
  Write-Host ""
  Write-Host "ERREUR: cle SSH introuvable." -ForegroundColor Red
  Write-Host $SshKey
  exit 1
}

$ssh = Get-Command ssh.exe -ErrorAction SilentlyContinue
if (-not $ssh) {
  Write-Host ""
  Write-Host "ERREUR: ssh.exe introuvable dans le PATH Windows." -ForegroundColor Red
  Write-Host "Installe OpenSSH Client Windows ou lance le tunnel depuis MobaXterm."
  exit 1
}

$portChoice = Get-FreeLocalPort
if (-not $portChoice) {
  Write-Host ""
  Write-Host "ERREUR: les ports locaux 18787 et 18887 sont deja occupes." -ForegroundColor Red
  Write-Host "Processus detectes :"
  Get-NetTCPConnection -LocalPort $PreferredLocalPorts -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, State, OwningProcess |
    Format-Table -AutoSize
  exit 1
}

$LocalPort = [int]$portChoice.Port
$Url = "http://127.0.0.1:$LocalPort/"

if ($portChoice.AlreadyReady) {
  Write-Section "Tunnel deja actif"
  Write-Host "L'interface repond deja sur $Url"
  Start-Process $Url
  exit 0
}

Write-Section "Ouverture du tunnel"
Write-Host "Local  : 127.0.0.1:$LocalPort"
Write-Host "Distant: 127.0.0.1:$RemotePort"
Write-Host ""
Write-Host "Une deuxieme fenetre PowerShell va rester ouverte pour le tunnel SSH."
Write-Host "Ne la ferme pas tant que tu utilises l'interface."

$sshCommand = @"
Write-Host 'Tunnel Aurora SR Cockpit' -ForegroundColor Cyan
Write-Host 'Local  : http://127.0.0.1:$LocalPort'
Write-Host 'Distant: $RemoteUser@$RemoteHost -> 127.0.0.1:$RemotePort'
Write-Host ''
& ssh.exe -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -i "$SshKey" -L "$LocalPort`:127.0.0.1:$RemotePort" "$RemoteUser@$RemoteHost"
Write-Host ''
Write-Host 'Le tunnel SSH est ferme ou a echoue.' -ForegroundColor Yellow
Read-Host 'Appuie sur Entree pour fermer cette fenetre'
"@

$encodedCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($sshCommand))
Start-Process powershell.exe -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", $encodedCommand) | Out-Null

Write-Section "Attente de l'interface"
$ready = $false
for ($i = 1; $i -le 20; $i++) {
  Start-Sleep -Seconds 1
  if (Test-HttpHealth $LocalPort) {
    $ready = $true
    break
  }
  Write-Host "Tentative $i/20..."
}

if (-not $ready) {
  Write-Host ""
  Write-Host "ERREUR: le tunnel n'a pas rendu l'interface disponible." -ForegroundColor Red
  Write-Host "URL testee: $Url"
  Write-Host ""
  Write-Host "A verifier dans la fenetre du tunnel SSH :"
  Write-Host "- Permission denied"
  Write-Host "- administratively prohibited"
  Write-Host "- bind: Address already in use"
  Write-Host "- Connection timed out"
  Write-Host ""
  Write-Host "Etat local du port $LocalPort :"
  Get-NetTCPConnection -LocalPort $LocalPort -ErrorAction SilentlyContinue |
    Select-Object LocalAddress, LocalPort, State, OwningProcess |
    Format-Table -AutoSize
  exit 1
}

Write-Section "Interface prete"
Write-Host $Url
Start-Process $Url

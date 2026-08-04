# Aurora SR Cockpit

Dashboard personnel read-only pour suivre les projets SR Method presents sous `/home/ubuntu/apps`.

## Demarrage

```bash
cd /home/ubuntu/apps/Aurora_Codex_Pack/tools/sr-cockpit
npm install
npm run build
npm start -- --host 127.0.0.1 --port 18787
```

L'application ecoute uniquement en local serveur :

```text
http://127.0.0.1:18787
```

## Connexion MobaXterm

Dans la session SSH OVH :

- `Advanced SSH settings`
- `Port forwarding` / `SSH tunnels`
- local port : `18787`
- remote server : `127.0.0.1`
- remote port : `18787`

Depuis Windows :

```text
http://localhost:18787
```

## Connexion Windows directe

Les scripts prets a poser sur le Bureau Windows sont dans :

```text
tools/sr-cockpit/scripts/windows/Aurora_SR_Cockpit.cmd
tools/sr-cockpit/scripts/windows/Aurora_SR_Cockpit.ps1
```

Ils ouvrent un tunnel SSH vers `127.0.0.1:18787` cote serveur, puis ouvrent l'interface locale dans le navigateur. Le script PowerShell teste d'abord `18787`, puis `18887` si le premier port local est deja utilise.

Configuration minimale cote Windows :

```powershell
setx AURORA_SR_COCKPIT_SSH_HOST "mon-serveur.example.com"
setx AURORA_SR_COCKPIT_SSH_USER "ubuntu"
setx AURORA_SR_COCKPIT_SSH_KEY "%USERPROFILE%\.ssh\ma_cle"
```

Ouvrir ensuite une nouvelle fenetre PowerShell ou double-cliquer sur `Aurora_SR_Cockpit.cmd`.

## Service systemd optionnel

Pour garder le cockpit actif cote serveur :

```bash
cd /home/ubuntu/apps/Aurora_Codex_Pack/tools/sr-cockpit
npm install
npm run build
bash scripts/linux/install-systemd-service.sh
systemctl status aurora-sr-cockpit
```

Le service reste lie a `127.0.0.1:18787`; il n'expose pas l'interface publiquement.

## Donnees lues

- tous les dossiers de `/home/ubuntu/apps`
- `docs/codex/SR_PACK_VERSION.json`
- `docs/codex/SR_LOTS.yaml`
- `docs/codex/SR_PASSES.yaml`
- `docs/codex/SR_INBOX.yaml`
- `docs/codex/tasks/*/sr_contract.json`
- `docs/codex/tasks/*/loop_contract.json`
- Git branch / dirty
- process Codex ouverts via `/proc/<pid>/cwd`

Le MVP ne modifie aucun projet scanne.

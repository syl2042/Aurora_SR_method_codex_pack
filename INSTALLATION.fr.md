# Installation

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Le parcours recommande est **prompt Codex d'abord**. Les scripts Python sont des outils techniques que Codex peut lancer apres inspection.

## Installer dans un projet cible

1. Cloner ce repository.
2. Ouvrir Codex dans le projet cible.
3. Coller [prompts/fr/00_install_codex_environment.md](prompts/fr/00_install_codex_environment.md).
4. Laisser Codex installer, verifier et produire le rapport.

Fallback technique :

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

## Mettre a jour

Dans le projet cible, coller [prompts/fr/05_upgrade_codex_environment.md](prompts/fr/05_upgrade_codex_environment.md). Codex doit auditer, preserver les fichiers projet, proposer le plan, puis seulement appliquer l'upgrade.

## Verifier

Coller [prompts/fr/06_verify_sr_installation.md](prompts/fr/06_verify_sr_installation.md).

## Demarrer une session

Coller [prompts/fr/01_start_sr_session.md](prompts/fr/01_start_sr_session.md). Pour les agents IA runtime, utiliser [prompts/fr/15_define_runtime_agents.md](prompts/fr/15_define_runtime_agents.md).

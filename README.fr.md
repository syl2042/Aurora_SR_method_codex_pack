# Aurora SR Method Codex Pack

[English](README.md) |
[Francais](README.fr.md) |
[Deutsch](README.de.md) |
[Portugues](README.pt.md) |
[Espanol](README.es.md)

[Mettre une etoile au repo](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) |
[Documentation](https://docs.auroramind.fr/docs/SR_Method) |
[Installer avec Codex](INSTALLATION.fr.md) |
[Mettre a jour](prompts/fr/05_upgrade_codex_environment.md) |
[Verifier](prompts/fr/06_verify_sr_installation.md)

## Ce que c'est

Aurora SR Method Codex Pack est un package source public pour installer une methode de travail Codex gouvernee dans des projets logiciels.

SR signifie **Specification Runtime**. La methode donne a Codex un cadre local au projet : regles de bootstrap, memoire de tache, evidence gates, repo maps, prompts controles, scripts de validation et skills methode reutilisables.

```text
Cloner le pack -> Coller un prompt Codex -> Installer la SR Method -> Verifier -> Demarrer un developpement gouverne
```

## Pourquoi l'utiliser

La SR Method s'adresse aux developpeurs qui veulent que Codex travaille comme un coequipier projet discipline, pas comme un simple generateur de code ponctuel.

Elle transforme une demande large en session de developpement cadree, avec perimetre explicite, memoire de tache ecrite, decisions fondees sur des preuves, gates de validation et handoff propre.

Gains principaux pour le developpeur :

- **Demarrage plus rapide** : Codex lit le depot, detecte la stack et installe un cadre de travail local au projet.
- **Moins de perte de contexte** : memoire de tache, etat courant, constats, decisions et verifications sont ecrits dans le projet.
- **Travail autonome plus sur** : Codex avance par lots bornes, verifie les preuves avant modification et garde la validation humaine explicite.
- **Meilleure continuite** : une autre session Codex ou un autre developpeur peut reprendre depuis l'etat ecrit.
- **Reviews plus claires** : les changements sont relies au perimetre, aux hypotheses, aux fichiers touches, aux verifications et aux risques restants.
- **Methode reutilisable** : le meme cadre peut etre installe sur plusieurs projets tout en s'adaptant a chaque depot.
- **Workflow prompt-first** : le developpeur pilote Codex avec des prompts prets a copier-coller ; les scripts restent des details d'execution.

En pratique, le pack reduit le cout d'utilisation de Codex sur du vrai travail projet : moins de changements flous, moins de contraintes oubliees, une validation plus claire et de meilleurs handoffs.

## Politique de langue

Le coeur de la SR Method reste maintenu en anglais comme langue technique canonique.

Les fichiers d'entree developpeur sont disponibles en plusieurs langues pour faciliter l'adoption : README, guides d'installation et prompts Codex a copier-coller.

Un projet installe peut demander a Codex d'echanger avec l'utilisateur en francais. La methode technique reste canonique en anglais.

## Demarrage rapide

1. Cloner ce repository.
2. Ouvrir Codex dans le projet cible.
3. Coller le prompt d'installation en francais.
4. Laisser Codex inspecter, installer, verifier et presenter le rapport.

Prompts principaux :

| Action | Prompt |
| --- | --- |
| Installer | [00](prompts/fr/00_install_codex_environment.md) |
| Demarrer une session | [01](prompts/fr/01_start_sr_session.md) |
| Mettre a jour | [05](prompts/fr/05_upgrade_codex_environment.md) |
| Verifier | [06](prompts/fr/06_verify_sr_installation.md) |
| Definir des agents runtime | [15](prompts/fr/15_define_runtime_agents.md) |

Les commandes Python restent des outils techniques ou de secours. Le parcours recommande est d'abord de passer par Codex et les prompts.

## Contenu public

```text
core/             coeur methode et templates en anglais canonique
prompts/          prompts racine et entrees multilingues
scripts/          installation, audit et validation
skills-method/    skills methode Codex reutilisables
blueprints/       templates de lots, inbox, tasks et skills
profiles/         profils generiques
project-skills/   emplacement pour les skills locales projet
adr/              template ADR
```

Le repository public ne publie pas les fichiers d'etat projet, tasks historiques, `.docx`, handoffs locaux, chemins client ou donnees projet.

## Licence

MIT License. Voir [LICENSE](LICENSE).

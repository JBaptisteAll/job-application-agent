# job-application-agent

[English](README.md) | **Français**

Génère des CV et des lettres de motivation adaptés à chaque offre d'emploi à partir d'une archive LinkedIn, avec relecture humaine.

## Installation pour le développement

Ce dépôt utilise [pre-commit](https://pre-commit.com) pour lancer des vérifications avant chaque commit : mise en forme, analyse du code, détection de secrets, et blocage des fichiers volumineux ou contenant des données personnelles.

Prérequis : Git et [uv](https://docs.astral.sh/uv/).

1. Installez pre-commit :

   ```
   uv tool install pre-commit
   ```

2. Activez les hooks dans votre copie du dépôt :

   ```
   pre-commit install
   ```

3. Vérifiez que tous les fichiers passent les contrôles :

   ```
   pre-commit run --all-files
   ```

Dès lors, un commit qui échoue à une vérification est bloqué. Corrigez le problème signalé, relancez `git add`, puis refaites le commit.

## Lancer les tests

1. Installez le projet et ses dépendances de développement :

   ```
   uv sync
   ```

2. Lancez les tests :

   ```
   uv run pytest
   ```

Le modèle de CV est `src/job_application_agent/templates/cv_template.docx`. Il peut être modifié dans Word : tapez chaque balise `{{ ... }}` ou `{% ... %}` d'un seul trait, sans changer sa mise en forme au milieu, puis lancez les tests pour vérifier que toutes les balises fonctionnent encore.

## Contribuer

Les contributions sont les bienvenues. Lisez [CONTRIBUTING.md](CONTRIBUTING.md) (en anglais) avant d'ouvrir une pull request, et [SECURITY.md](SECURITY.md) pour signaler une vulnérabilité.

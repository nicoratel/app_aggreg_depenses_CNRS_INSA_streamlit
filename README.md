# Synthèse des dépenses CNRS et INSA

Application Streamlit pour générer une synthèse des dépenses CNRS et INSA par code NACRE.

## Description

Cet utilitaire crée un fichier contenant 2 colonnes :
- Code NACRE
- Montant total HT associé au Code NACRE pour des crédits ayant comme origine le CNRS et l'INSA

## Utilisation

1. Téléversez le fichier GESLAB - CNRS (format .ods)
2. Téléversez le fichier INSA (format .ods)
3. Cliquez sur "Générer le fichier"
4. Téléchargez le fichier de résultats au format TSV

## Déploiement sur Streamlit Community Cloud

### Prérequis
- Un compte GitHub
- Un compte Streamlit Community Cloud (gratuit)

### Étapes
1. Créez un dépôt GitHub avec les fichiers suivants :
   - `app_streamlit.py`
   - `requirements.txt`
   - `README.md` (optionnel)

2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)

3. Cliquez sur "New app" et sélectionnez votre dépôt GitHub

4. Configurez :
   - Repository : `votre-username/votre-repo`
   - Branch : `main` (ou `master`)
   - Main file path : `app_streamlit.py`

5. Cliquez sur "Deploy"

## Format des fichiers

- **Entrée** : Fichiers .ods (LibreOffice/OpenOffice)
- **Sortie** : Fichier .tsv (tab-separated values)

## Licence

Usage interne CNRS/INSA

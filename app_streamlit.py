import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Synthèse des dépenses CNRS et INSA",
    page_icon="📊",
    layout="wide"
)

# Titre et description
st.title("📊 Synthèse des dépenses CNRS et INSA")

st.markdown("""
### Description

Cet utilitaire a pour objectif de créer un fichier contenant 2 colonnes:
- **Code NACRE**
- **Montant total HT** associé au Code NACRE pour des crédits ayant comme origine le CNRS et l'INSA

Cet outil prend comme fichier d'entrée les fichiers produits par les outils de gestion du CNRS et de l'INSA. 
L'outil récupère et additionne les dépenses par code NACRE dans chaque fichier, et les enregistre dans le fichier de sortie.

**Format des fichiers:**
- Fichiers d'entrée: format .ods (LibreOffice)
- Fichier de sortie: format .txt ou .tsv (tab separated)
""")

st.divider()

# Fonction de traitement
def process_files(cnrs_file, insa_file):
    """Traite les fichiers CNRS et INSA et retourne le résultat"""
    
    # Traitement du fichier CNRS
    cnrsfile = pd.read_excel(cnrs_file, engine='odf', skiprows=3)
    codes_cnrs = cnrsfile["Unnamed: 0"]
    sommes_cnrs = cnrsfile["Unnamed: 20"]
    
    # Stocker les données CNRS dans un dictionnaire
    cnrs_dict = {}
    i = 1
    for code in codes_cnrs[1:]:
        cnrs_dict.update({str(code): float(sommes_cnrs[i])})
        i += 1
    # Supprimer les clés et valeurs NaN
    cnrs_dict = {k: v for k, v in cnrs_dict.items() if pd.Series(v).notna().all()}
    
    # Traitement du fichier INSA
    insafile = pd.read_excel(insa_file, engine='odf')
    
    codes_insa_object = insafile["Code achat"]
    
    codes_insa = []
    for code in codes_insa_object:
        code_nacre = str(code)
        code_nacre.replace(".", "")
        codes_insa.append(code_nacre)
    
    sommes_insa = insafile["Montant budgétaire répartition"]
    
    # Stocker les données INSA dans un dictionnaire
    insa_dict = {}
    i = 1
    insa_dict.update({str(codes_insa[0]): float(format(sommes_insa[0], '.2f'))})
    for code in codes_insa[1:]:
        if code in insa_dict:
            insa_dict[code] += float(format(sommes_insa[i], '.2f'))
        else:
            insa_dict.update({str(code): float(sommes_insa[i])})
        i += 1
    # Supprimer les clés et valeurs NaN
    insa_dict = {k: v for k, v in insa_dict.items() if pd.Series(v).notna().all()}
    
    # Fusionner les dictionnaires et additionner les contributions
    res = cnrs_dict.copy()
    for key in insa_dict:
        if key in cnrs_dict:
            res[key] += insa_dict[key]
        else:
            res.update({key: insa_dict[key]})
    
    # Préparer les résultats
    res_codes = []
    res_sommes = []
    for k in sorted(res):
        res_codes.append(k)
        res_sommes.append(res[k])
    
    return res_codes, res_sommes, cnrs_dict, insa_dict

# Interface utilisateur
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Fichier GESLAB - CNRS")
    cnrs_file = st.file_uploader(
        "Sélectionner le fichier CNRS (format .ods)",
        type=['ods'],
        key='cnrs'
    )

with col2:
    st.subheader("📁 Fichier INSA")
    insa_file = st.file_uploader(
        "Sélectionner le fichier INSA (format .ods)",
        type=['ods'],
        key='insa'
    )

st.divider()

# Bouton de traitement
if st.button("🚀 Générer le fichier", type="primary", use_container_width=True):
    if cnrs_file is None or insa_file is None:
        st.error("⚠️ Veuillez sélectionner les deux fichiers (CNRS et INSA) avant de continuer.")
    else:
        with st.spinner('Traitement en cours...'):
            try:
                # Traiter les fichiers
                res_codes, res_sommes, cnrs_dict, insa_dict = process_files(cnrs_file, insa_file)
                
                # Créer le contenu du fichier de sortie
                line2write = 'Code NACRES\tMontant\n'
                for i in range(len(res_codes)):
                    line2write += f'{res_codes[i]}\t{res_sommes[i]:.2f}\n'
                
                # Afficher les résultats
                st.success("✅ Fichier généré avec succès!")
                
                # Statistiques
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Codes CNRS", len(cnrs_dict))
                with col2:
                    st.metric("Codes INSA", len(insa_dict))
                with col3:
                    st.metric("Codes Total", len(res_codes))
                with col4:
                    st.metric("Montant Total", f"{sum(res_sommes):.2f} €")
                
                # Créer un DataFrame pour l'affichage
                df_results = pd.DataFrame({
                    'Code NACRE': res_codes,
                    'Montant (€)': [f'{x:.2f}' for x in res_sommes]
                })
                
                # Afficher le tableau
                st.subheader("📋 Résultats")
                st.dataframe(df_results, use_container_width=True, height=400)
                
                # Bouton de téléchargement
                st.download_button(
                    label="💾 Télécharger le fichier TSV",
                    data=line2write,
                    file_name="bilan_achats.tsv",
                    mime="text/tab-separated-values"
                )
                
            except Exception as e:
                st.error(f"❌ Erreur lors du traitement: {str(e)}")
                st.exception(e)

st.divider()

# Footer
st.markdown("""
---
*Application de synthèse des dépenses CNRS et INSA*
""")

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from difflib import SequenceMatcher

# Configuration de la page
st.set_page_config(layout="wide", page_title="Dashboard IP Patent Litigation")

# Titre principal
st.title("Dashboard d'Analyse de Propriété Intellectuelle")
st.markdown("*Analyse des profils et entreprises dans le domaine de la propriété intellectuelle*")

# Fonction pour normaliser les job titles
def normalize_job_title(title):
    """Normalise les job titles pour regrouper les variantes similaires"""
    if not isinstance(title, str) or title == 'Unknown':
        return 'Unknown'

    title = title.lower().strip()

    # Regroupements spécifiques
    if 'patent attorney' in title or 'patent counsel' in title:
        return 'Patent Attorney/Counsel'
    elif 'ip attorney' in title or 'ip counsel' in title:
        return 'IP Attorney/Counsel'
    elif 'patent agent' in title:
        return 'Patent Agent'
    elif 'ip manager' in title or 'intellectual property manager' in title:
        return 'IP Manager'
    elif 'patent engineer' in title:
        return 'Patent Engineer'
    elif 'ip paralegal' in title or 'patent paralegal' in title:
        return 'IP/Patent Paralegal'
    elif 'general counsel' in title:
        return 'General Counsel'
    elif 'legal counsel' in title:
        return 'Legal Counsel'
    elif 'ip director' in title or 'director of ip' in title or 'director ip' in title:
        return 'IP Director'
    elif 'patent examiner' in title:
        return 'Patent Examiner'
    else:
        return title.title()

# Chargement des données
@st.cache_data
def load_data():
    # Charger le CSV avec gestion des types mixtes
    df = pd.read_csv('data/TAM_Corporations_IP_Patent_Litigation.csv', low_memory=False)

    # Nettoyer les noms de colonnes (remplacer les sauts de ligne et les espaces)
    df.columns = [c.replace('\n', ' ').strip() for c in df.columns]

    # Les colonnes réelles du CSV sont déjà correctes, on fait juste un mapping pour simplifier
    column_mapping = {
        'Titre': 'JobTitle',
        'Taille de l\'entreprise': 'Headcount',  # Nombre d'employés (numérique)
        'Size': 'CompanySize',  # Catégorie de taille (Enterprise, Medium, etc.)
        'Secteurs d\'activité': 'Industry',
        'Lieu': 'Location'
    }

    # Renommer les colonnes
    df.rename(columns=column_mapping, inplace=True)

    # Convertir Headcount en numérique (au cas où il y aurait des valeurs non numériques)
    if 'Headcount' in df.columns:
        df['Headcount'] = pd.to_numeric(df['Headcount'], errors='coerce')

    # Normaliser les job titles
    if 'JobTitle' in df.columns:
        df['JobTitleNormalized'] = df['JobTitle'].apply(normalize_job_title)

    # Extraction du pays à partir de la colonne Location
    if 'Location' in df.columns:
        df['Country'] = df['Location'].apply(lambda x: extract_country(x) if isinstance(x, str) else "Unknown")
    else:
        df['Country'] = 'Unknown'

    # Corriger la colonne Region : remplacer "Region" et "Unknown" par "NA"
    if 'Region' in df.columns:
        df['Region'] = df['Region'].replace({'Region': 'NA', 'Unknown': 'NA'})
        # S'assurer que seuls EU et NA existent
        df.loc[~df['Region'].isin(['EU', 'NA']), 'Region'] = 'NA'

    # Calculer le Tiering basé sur le nombre de profils IP par entreprise
    if 'Entreprise' in df.columns:
        # Compter le nombre de profils par entreprise
        company_profile_counts = df.groupby('Entreprise').size().reset_index(name='IP_Count')

        # Définir le tiering
        def assign_tier(count):
            if count > 30:
                return 'T1'
            elif count >= 5:
                return 'T2'
            else:
                return 'T3'

        company_profile_counts['Tier'] = company_profile_counts['IP_Count'].apply(assign_tier)

        # Fusionner avec le dataframe principal
        df = df.merge(company_profile_counts[['Entreprise', 'Tier', 'IP_Count']], on='Entreprise', how='left')
        df['Tier'] = df['Tier'].fillna('Unknown')

    # Gestion des valeurs manquantes
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(0)

    return df

def extract_country(location_str):
    """Extraire le pays à partir de la chaîne de localisation"""
    if not isinstance(location_str, str):
        return "Unknown"

    # Diviser par la virgule et prendre le dernier élément (généralement le pays)
    parts = location_str.split(',')
    if len(parts) > 0:
        country = parts[-1].strip()
        return country
    return "Unknown"

# Charger les données
try:
    df = load_data()
    st.sidebar.success("Données chargées avec succès!")
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

# Vérifier les colonnes disponibles
available_columns = df.columns.tolist()
st.sidebar.info(f"Dataset chargé avec {len(df)} lignes et {len(df.columns)} colonnes")

# Sidebar avec mode de visualisation
st.sidebar.title("Mode de visualisation")
view_mode = st.sidebar.radio(
    "Sélectionnez le mode:",
    ["Vue Simple", "Mode Comparaison"]
)

if view_mode == "Vue Simple":
    # Filtres classiques
    st.sidebar.title("Filtres")

    # Filtre pour Region/Continent
    if 'Region' in df.columns:
        regions = sorted(df['Region'].unique().tolist())
        if len(regions) > 0:
            selected_regions = st.sidebar.multiselect("Région/Continent", regions, default=[])

            if selected_regions:
                df_filtered = df[df['Region'].isin(selected_regions)]
            else:
                df_filtered = df
        else:
            df_filtered = df
    else:
        df_filtered = df
        st.sidebar.warning("Le filtre Région n'est pas disponible")

    # Filtre pour Entreprise
    if 'Entreprise' in df_filtered.columns:
        companies = sorted(df_filtered['Entreprise'].unique().tolist())
        if len(companies) > 0:
            selected_companies = st.sidebar.multiselect("Entreprise", companies, default=[])

            if selected_companies:
                df_filtered = df_filtered[df_filtered['Entreprise'].isin(selected_companies)]
    else:
        st.sidebar.warning("Le filtre Entreprise n'est pas disponible")

    # Filtres pour Industry (Top 10 + Other)
    if 'Industry' in df_filtered.columns:
        industry_counts = df_filtered['Industry'].value_counts()
        top_industries = industry_counts.nlargest(10).index.tolist()
        all_industries = top_industries + ['Other']
        selected_industries = st.sidebar.multiselect("Industries", all_industries, default=[])

        if selected_industries:
            if 'Other' in selected_industries:
                other_industries = [ind for ind in df_filtered['Industry'].unique() if ind not in top_industries]
                filter_industries = [ind for ind in selected_industries if ind != 'Other'] + other_industries
                df_filtered = df_filtered[df_filtered['Industry'].isin(filter_industries)]
            else:
                df_filtered = df_filtered[df_filtered['Industry'].isin(selected_industries)]
    else:
        st.sidebar.warning("Le filtre Industries n'est pas disponible")

    # Filtre pour Company Size
    if 'CompanySize' in df_filtered.columns:
        company_sizes = sorted(df_filtered['CompanySize'].unique().tolist())
        if len(company_sizes) > 0:
            selected_sizes = st.sidebar.multiselect("Taille de l'entreprise", company_sizes, default=[])

            if selected_sizes:
                df_filtered = df_filtered[df_filtered['CompanySize'].isin(selected_sizes)]
    else:
        st.sidebar.warning("Le filtre Taille de l'entreprise n'est pas disponible")

    # Filtre pour Country
    if 'Country' in df_filtered.columns:
        countries = sorted(df_filtered['Country'].unique().tolist())
        if len(countries) > 0:
            selected_countries = st.sidebar.multiselect("Pays", countries, default=[])

            if selected_countries:
                df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries)]
    else:
        st.sidebar.warning("Le filtre Pays n'est pas disponible")

    # Filtre pour Seniority
    if 'Seniority' in df_filtered.columns:
        seniority_levels = sorted(df_filtered['Seniority'].unique().tolist())
        if len(seniority_levels) > 0:
            selected_seniority = st.sidebar.multiselect("Niveau d'ancienneté", seniority_levels, default=[])

            if selected_seniority:
                df_filtered = df_filtered[df_filtered['Seniority'].isin(selected_seniority)]
    else:
        st.sidebar.warning("Le filtre Niveau d'ancienneté n'est pas disponible")

    # Filtre pour Tiering
    if 'Tier' in df_filtered.columns:
        tiers = ['T1', 'T2', 'T3']
        available_tiers = [t for t in tiers if t in df_filtered['Tier'].unique()]
        if len(available_tiers) > 0:
            selected_tiers = st.sidebar.multiselect(
                "Tiering des entreprises",
                available_tiers,
                default=[],
                help="T1: >30 profils IP | T2: 5-30 profils IP | T3: 0-5 profils IP"
            )

            if selected_tiers:
                df_filtered = df_filtered[df_filtered['Tier'].isin(selected_tiers)]
    else:
        st.sidebar.warning("Le filtre Tiering n'est pas disponible")

    # Pas de comparaison
    df_compare = None
    comparison_mode = False

else:
    # Mode Comparaison
    st.sidebar.title("Comparaison")

    # Sélectionner le type de comparaison
    comparison_type = st.sidebar.selectbox(
        "Type de comparaison:",
        ["Région vs Région", "Entreprise vs Entreprise", "Pays vs Pays", "Tiering vs Tiering", "Custom"]
    )

    col1, col2 = st.sidebar.columns(2)

    if comparison_type == "Région vs Région":
        if 'Region' in df.columns:
            regions = sorted(df['Region'].unique().tolist())
            with col1:
                st.markdown("**Groupe 1**")
                region1 = st.selectbox("Région 1", regions, key="region1")
                df_filtered = df[df['Region'] == region1]
            with col2:
                st.markdown("**Groupe 2**")
                region2 = st.selectbox("Région 2", regions, key="region2")
                df_compare = df[df['Region'] == region2]
        else:
            st.sidebar.error("Colonne Region non disponible")
            df_filtered = df
            df_compare = None

    elif comparison_type == "Entreprise vs Entreprise":
        if 'Entreprise' in df.columns:
            companies = sorted(df['Entreprise'].unique().tolist())
            with col1:
                st.markdown("**Groupe 1**")
                company1 = st.selectbox("Entreprise 1", companies, key="company1")
                df_filtered = df[df['Entreprise'] == company1]
            with col2:
                st.markdown("**Groupe 2**")
                company2 = st.selectbox("Entreprise 2", companies, key="company2")
                df_compare = df[df['Entreprise'] == company2]
        else:
            st.sidebar.error("Colonne Entreprise non disponible")
            df_filtered = df
            df_compare = None

    elif comparison_type == "Pays vs Pays":
        if 'Country' in df.columns:
            countries = sorted(df['Country'].unique().tolist())
            with col1:
                st.markdown("**Groupe 1**")
                country1 = st.selectbox("Pays 1", countries, key="country1")
                df_filtered = df[df['Country'] == country1]
            with col2:
                st.markdown("**Groupe 2**")
                country2 = st.selectbox("Pays 2", countries, key="country2")
                df_compare = df[df['Country'] == country2]
        else:
            st.sidebar.error("Colonne Country non disponible")
            df_filtered = df
            df_compare = None

    elif comparison_type == "Tiering vs Tiering":
        if 'Tier' in df.columns:
            tiers = ['T1', 'T2', 'T3']
            available_tiers = [t for t in tiers if t in df['Tier'].unique()]
            with col1:
                st.markdown("**Groupe 1**")
                tier1 = st.selectbox("Tier 1", available_tiers, key="tier1", help="T1: >30 profils IP | T2: 5-30 profils IP | T3: 0-5 profils IP")
                df_filtered = df[df['Tier'] == tier1]
            with col2:
                st.markdown("**Groupe 2**")
                tier2 = st.selectbox("Tier 2", available_tiers, key="tier2", help="T1: >30 profils IP | T2: 5-30 profils IP | T3: 0-5 profils IP")
                df_compare = df[df['Tier'] == tier2]
        else:
            st.sidebar.error("Colonne Tier non disponible")
            df_filtered = df
            df_compare = None

    else:  # Custom
        with col1:
            st.markdown("**Groupe 1**")
            custom_filter_type1 = st.selectbox("Filtrer par", ["Region", "Entreprise", "Country", "Tier"], key="custom1_type")
            if custom_filter_type1 == "Region" and 'Region' in df.columns:
                custom_val1 = st.selectbox("Valeur", sorted(df['Region'].unique()), key="custom1_val")
                df_filtered = df[df['Region'] == custom_val1]
            elif custom_filter_type1 == "Entreprise" and 'Entreprise' in df.columns:
                custom_val1 = st.selectbox("Valeur", sorted(df['Entreprise'].unique()), key="custom1_val")
                df_filtered = df[df['Entreprise'] == custom_val1]
            elif custom_filter_type1 == "Country" and 'Country' in df.columns:
                custom_val1 = st.selectbox("Valeur", sorted(df['Country'].unique()), key="custom1_val")
                df_filtered = df[df['Country'] == custom_val1]
            elif custom_filter_type1 == "Tier" and 'Tier' in df.columns:
                custom_val1 = st.selectbox("Valeur", ['T1', 'T2', 'T3'], key="custom1_val")
                df_filtered = df[df['Tier'] == custom_val1]

        with col2:
            st.markdown("**Groupe 2**")
            custom_filter_type2 = st.selectbox("Filtrer par", ["Region", "Entreprise", "Country", "Tier"], key="custom2_type")
            if custom_filter_type2 == "Region" and 'Region' in df.columns:
                custom_val2 = st.selectbox("Valeur", sorted(df['Region'].unique()), key="custom2_val")
                df_compare = df[df['Region'] == custom_val2]
            elif custom_filter_type2 == "Entreprise" and 'Entreprise' in df.columns:
                custom_val2 = st.selectbox("Valeur", sorted(df['Entreprise'].unique()), key="custom2_val")
                df_compare = df[df['Entreprise'] == custom_val2]
            elif custom_filter_type2 == "Country" and 'Country' in df.columns:
                custom_val2 = st.selectbox("Valeur", sorted(df['Country'].unique()), key="custom2_val")
                df_compare = df[df['Country'] == custom_val2]
            elif custom_filter_type2 == "Tier" and 'Tier' in df.columns:
                custom_val2 = st.selectbox("Valeur", ['T1', 'T2', 'T3'], key="custom2_val")
                df_compare = df[df['Tier'] == custom_val2]

    comparison_mode = True

# Afficher les colonnes disponibles pour le débogage si nécessaire
with st.sidebar.expander("Colonnes disponibles"):
    st.write(df.columns.tolist())

# KPIs en haut de page
st.subheader("Indicateurs Clés de Performance")

if comparison_mode and df_compare is not None:
    # Mode comparaison - afficher les KPIs côte à côte
    col_group1, col_group2 = st.columns(2)

    with col_group1:
        st.markdown("### Groupe 1")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

        with kpi_col1:
            total_profiles = len(df_filtered)
            st.metric(label="Profils", value=f"{total_profiles:,}")

        with kpi_col2:
            if 'Entreprise' in df_filtered.columns:
                unique_companies = df_filtered['Entreprise'].nunique()
            else:
                unique_companies = "N/A"
            st.metric(label="Entreprises", value=f"{unique_companies:,}" if isinstance(unique_companies, int) else unique_companies)

        with kpi_col3:
            if 'Industry' in df_filtered.columns and len(df_filtered) > 0:
                top_industry = df_filtered['Industry'].value_counts().idxmax()
                st.metric(label="Top Industrie", value=f"{top_industry[:20]}...")
            else:
                st.metric(label="Top Industrie", value="N/A")

        with kpi_col4:
            if 'Seniority' in df_filtered.columns and len(df_filtered) > 0:
                senior_count = df_filtered[df_filtered['Seniority'] == 'Senior'].shape[0]
                senior_percentage = (senior_count / total_profiles) * 100 if total_profiles > 0 else 0
                st.metric(label="% Seniors", value=f"{senior_percentage:.1f}%")
            else:
                st.metric(label="% Seniors", value="N/A")

    with col_group2:
        st.markdown("### Groupe 2")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

        with kpi_col1:
            total_profiles2 = len(df_compare)
            st.metric(label="Profils", value=f"{total_profiles2:,}")

        with kpi_col2:
            if 'Entreprise' in df_compare.columns:
                unique_companies2 = df_compare['Entreprise'].nunique()
            else:
                unique_companies2 = "N/A"
            st.metric(label="Entreprises", value=f"{unique_companies2:,}" if isinstance(unique_companies2, int) else unique_companies2)

        with kpi_col3:
            if 'Industry' in df_compare.columns and len(df_compare) > 0:
                top_industry2 = df_compare['Industry'].value_counts().idxmax()
                st.metric(label="Top Industrie", value=f"{top_industry2[:20]}...")
            else:
                st.metric(label="Top Industrie", value="N/A")

        with kpi_col4:
            if 'Seniority' in df_compare.columns and len(df_compare) > 0:
                senior_count2 = df_compare[df_compare['Seniority'] == 'Senior'].shape[0]
                senior_percentage2 = (senior_count2 / total_profiles2) * 100 if total_profiles2 > 0 else 0
                st.metric(label="% Seniors", value=f"{senior_percentage2:.1f}%")
            else:
                st.metric(label="% Seniors", value="N/A")

else:
    # Mode simple - afficher les KPIs normalement
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        total_profiles = len(df_filtered)
        st.metric(label="Nombre de profils", value=f"{total_profiles:,}")

    with kpi_col2:
        if 'Entreprise' in df_filtered.columns:
            unique_companies = df_filtered['Entreprise'].nunique()
        else:
            alternative_columns = [col for col in df_filtered.columns if 'entreprise' in col.lower() or 'company' in col.lower()]
            if alternative_columns:
                unique_companies = df_filtered[alternative_columns[0]].nunique()
            else:
                unique_companies = "N/A"
        st.metric(label="Entreprises uniques", value=f"{unique_companies:,}" if isinstance(unique_companies, int) else unique_companies)

    with kpi_col3:
        if 'Industry' in df_filtered.columns and len(df_filtered) > 0:
            top_industry = df_filtered['Industry'].value_counts().idxmax()
            top_industry_count = df_filtered['Industry'].value_counts().max()
            top_industry_percentage = (top_industry_count / total_profiles) * 100
            st.metric(label="Top Industrie", value=f"{top_industry}", delta=f"{top_industry_percentage:.1f}%")
        else:
            st.metric(label="Top Industrie", value="N/A")

    with kpi_col4:
        if 'Seniority' in df_filtered.columns and len(df_filtered) > 0:
            senior_count = df_filtered[df_filtered['Seniority'] == 'Senior'].shape[0]
            senior_percentage = (senior_count / total_profiles) * 100 if total_profiles > 0 else 0
            st.metric(label="% de Seniors", value=f"{senior_percentage:.1f}%")
        else:
            st.metric(label="% de Seniors", value="N/A")

# Création des onglets
tab1, tab2, tab3 = st.tabs(["Global & Company Overview", "IP Strategy & Density", "Talent & Seniority"])

# Onglet 1: Global & Company Overview
with tab1:
    st.header("Vue d'ensemble globale et des entreprises")

    if comparison_mode and df_compare is not None:
        st.info("Mode comparaison activé - Les graphiques affichent les deux groupes côte à côte")

    # Créer une colonne pour chaque graphique
    col1, col2 = st.columns(2)

    with col1:
        # Graphique 1: Top 10 Industries représentées
        if 'Industry' in df_filtered.columns:
            if comparison_mode and df_compare is not None:
                # Mode comparaison
                industry_counts1 = df_filtered['Industry'].value_counts().nlargest(10)
                industry_counts2 = df_compare['Industry'].value_counts().nlargest(10)

                # Combiner les top industries des deux groupes
                all_industries = set(industry_counts1.index.tolist() + industry_counts2.index.tolist())

                # Créer un dataframe pour la comparaison
                comparison_data = []
                for ind in all_industries:
                    pct1 = (industry_counts1.get(ind, 0) / len(df_filtered)) * 100
                    pct2 = (industry_counts2.get(ind, 0) / len(df_compare)) * 100
                    comparison_data.append({'Industry': ind, 'Groupe 1': pct1, 'Groupe 2': pct2})

                comp_df = pd.DataFrame(comparison_data).sort_values('Groupe 1', ascending=False).head(10)

                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    y=comp_df['Industry'],
                    x=comp_df['Groupe 1'],
                    name='Groupe 1',
                    orientation='h',
                    marker=dict(color='#4e8df5')
                ))
                fig1.add_trace(go.Bar(
                    y=comp_df['Industry'],
                    x=comp_df['Groupe 2'],
                    name='Groupe 2',
                    orientation='h',
                    marker=dict(color='#f58d4e')
                ))

                fig1.update_layout(
                    title='Top 10 Industries - Comparaison',
                    xaxis_title='Pourcentage (%)',
                    yaxis_title='Industrie',
                    barmode='group',
                    height=500
                )
            else:
                # Mode simple
                industry_counts = df_filtered['Industry'].value_counts().nlargest(10)
                total_companies = len(df_filtered)
                industry_percentages = (industry_counts / total_companies) * 100

                fig1 = px.bar(
                    x=industry_percentages.values,
                    y=industry_percentages.index,
                    orientation='h',
                    labels={'x': 'Pourcentage (%)', 'y': 'Industrie'},
                    title='Top 10 Industries Représentées',
                    text=[f"{val:.1f}%" for val in industry_percentages.values],
                    color_discrete_sequence=['#4e8df5']
                )
                fig1.update_layout(height=500)
                fig1.update_traces(textposition='outside')

            fig1.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Données d'industries non disponibles")

    with col2:
        # Graphique 2: Répartition des tailles d'entreprises
        if 'CompanySize' in df_filtered.columns:
            if comparison_mode and df_compare is not None:
                # Mode comparaison
                size_counts1 = df_filtered['CompanySize'].value_counts()
                size_counts2 = df_compare['CompanySize'].value_counts()

                all_sizes = set(size_counts1.index.tolist() + size_counts2.index.tolist())

                comparison_data = []
                for size in all_sizes:
                    comparison_data.append({
                        'Size': size,
                        'Groupe 1': size_counts1.get(size, 0),
                        'Groupe 2': size_counts2.get(size, 0)
                    })

                comp_df = pd.DataFrame(comparison_data)

                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=comp_df['Size'],
                    y=comp_df['Groupe 1'],
                    name='Groupe 1',
                    marker=dict(color='#4e8df5')
                ))
                fig2.add_trace(go.Bar(
                    x=comp_df['Size'],
                    y=comp_df['Groupe 2'],
                    name='Groupe 2',
                    marker=dict(color='#f58d4e')
                ))

                fig2.update_layout(
                    title='Répartition des tailles d\'entreprises - Comparaison',
                    xaxis_title='Taille de l\'entreprise',
                    yaxis_title='Nombre',
                    barmode='group',
                    height=500
                )
            else:
                # Mode simple
                company_size_counts = df_filtered['CompanySize'].value_counts()

                fig2 = px.bar(
                    x=company_size_counts.index,
                    y=company_size_counts.values,
                    labels={'x': 'Taille de l\'entreprise', 'y': 'Nombre'},
                    title='Répartition des tailles d\'entreprises',
                    text=company_size_counts.values,
                    color_discrete_sequence=['#4e8df5']
                )
                fig2.update_layout(height=500)
                fig2.update_traces(textposition='outside')

            fig2.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Données de taille d'entreprise non disponibles")

    # Graphique 3: Distribution du Tiering
    if 'Tier' in df_filtered.columns:
        col_tier1, col_tier2 = st.columns(2)

        with col_tier1:
            if comparison_mode and df_compare is not None:
                # Mode comparaison
                tier_counts1 = df_filtered['Tier'].value_counts().reindex(['T1', 'T2', 'T3'], fill_value=0)
                tier_counts2 = df_compare['Tier'].value_counts().reindex(['T1', 'T2', 'T3'], fill_value=0)

                # Compter les entreprises uniques par tier
                tier_companies1 = df_filtered.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)
                tier_companies2 = df_compare.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)

                comparison_data = []
                for tier in ['T1', 'T2', 'T3']:
                    comparison_data.append({
                        'Tier': tier,
                        'Groupe 1': tier_companies1.get(tier, 0),
                        'Groupe 2': tier_companies2.get(tier, 0)
                    })

                comp_df = pd.DataFrame(comparison_data)

                fig_tier = go.Figure()
                fig_tier.add_trace(go.Bar(
                    x=comp_df['Tier'],
                    y=comp_df['Groupe 1'],
                    name='Groupe 1',
                    marker=dict(color='#4e8df5'),
                    text=comp_df['Groupe 1'],
                    textposition='outside'
                ))
                fig_tier.add_trace(go.Bar(
                    x=comp_df['Tier'],
                    y=comp_df['Groupe 2'],
                    name='Groupe 2',
                    marker=dict(color='#f58d4e'),
                    text=comp_df['Groupe 2'],
                    textposition='outside'
                ))

                fig_tier.update_layout(
                    title='Distribution des Entreprises par Tiering - Comparaison',
                    xaxis_title='Tier',
                    yaxis_title="Nombre d'entreprises",
                    barmode='group',
                    height=400
                )
            else:
                # Mode simple - compter les entreprises par tier
                tier_companies = df_filtered.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)

                fig_tier = px.bar(
                    x=tier_companies.index,
                    y=tier_companies.values,
                    labels={'x': 'Tier', 'y': "Nombre d'entreprises"},
                    title='Distribution des Entreprises par Tiering',
                    text=tier_companies.values,
                    color_discrete_sequence=['#4e8df5']
                )
                fig_tier.update_layout(height=400)
                fig_tier.update_traces(textposition='outside')

            fig_tier.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig_tier, use_container_width=True)

            # Légende
            st.caption("**T1**: >30 profils IP | **T2**: 5-30 profils IP | **T3**: 0-5 profils IP")

        with col_tier2:
            # Afficher les statistiques détaillées
            st.subheader("Statistiques Tiering")

            if comparison_mode and df_compare is not None:
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1:
                    st.markdown("**Groupe 1**")
                    tier_companies1 = df_filtered.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)
                    for tier in ['T1', 'T2', 'T3']:
                        st.metric(f"{tier}", f"{tier_companies1.get(tier, 0)} entreprises")

                with col_stat2:
                    st.markdown("**Groupe 2**")
                    tier_companies2 = df_compare.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)
                    for tier in ['T1', 'T2', 'T3']:
                        st.metric(f"{tier}", f"{tier_companies2.get(tier, 0)} entreprises")
            else:
                tier_companies = df_filtered.groupby('Tier')['Entreprise'].nunique().reindex(['T1', 'T2', 'T3'], fill_value=0)
                total_companies = tier_companies.sum()

                for tier in ['T1', 'T2', 'T3']:
                    count = tier_companies.get(tier, 0)
                    pct = (count / total_companies * 100) if total_companies > 0 else 0
                    st.metric(f"{tier}", f"{count} entreprises", f"{pct:.1f}%")

    # Graphique 4: Top 10 des pays/locations
    if 'Country' in df_filtered.columns:
        if comparison_mode and df_compare is not None:
            # Mode comparaison
            country_counts1 = df_filtered['Country'].value_counts().nlargest(10)
            country_counts2 = df_compare['Country'].value_counts().nlargest(10)

            all_countries = set(country_counts1.index.tolist() + country_counts2.index.tolist())

            comparison_data = []
            for country in all_countries:
                comparison_data.append({
                    'Country': country,
                    'Groupe 1': country_counts1.get(country, 0),
                    'Groupe 2': country_counts2.get(country, 0)
                })

            comp_df = pd.DataFrame(comparison_data).sort_values('Groupe 1', ascending=False).head(10)

            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                x=comp_df['Country'],
                y=comp_df['Groupe 1'],
                name='Groupe 1',
                marker=dict(color='#4e8df5')
            ))
            fig4.add_trace(go.Bar(
                x=comp_df['Country'],
                y=comp_df['Groupe 2'],
                name='Groupe 2',
                marker=dict(color='#f58d4e')
            ))

            fig4.update_layout(
                title='Top 10 des Pays des Talents - Comparaison',
                xaxis_title='Pays',
                yaxis_title='Nombre',
                barmode='group',
                height=500
            )
        else:
            # Mode simple
            country_counts = df_filtered['Country'].value_counts().nlargest(10)

            fig4 = px.bar(
                x=country_counts.index,
                y=country_counts.values,
                labels={'x': 'Pays', 'y': 'Nombre'},
                title='Top 10 des Pays des Talents',
                text=country_counts.values,
                color_discrete_sequence=['#4e8df5']
            )
            fig4.update_layout(height=500)
            fig4.update_traces(textposition='outside')

        fig4.update_layout(font=dict(color='#000000'))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("Données de pays non disponibles")

# Onglet 2: IP Strategy & Density
with tab2:
    st.header("Stratégie IP & Densité")

    # Calcul de la Densité IP pour chaque entreprise
    if 'Entreprise' in df_filtered.columns and 'Headcount' in df_filtered.columns:
        # Créer un dataframe avec le nombre de profils par entreprise
        company_profile_counts = df_filtered.groupby('Entreprise').size().reset_index(name='ProfileCount')

        # Fusionner avec les données de headcount (taille de l'entreprise)
        company_headcount = df_filtered.groupby('Entreprise')['Headcount'].first().reset_index()
        company_data = pd.merge(company_profile_counts, company_headcount, on='Entreprise')

        # Calculer la densité IP (en %)
        company_data['IP_Density'] = (company_data['ProfileCount'] / company_data['Headcount']) * 100

        # Filtrer les valeurs invalides
        company_data = company_data[company_data['IP_Density'].notna()]
        company_data = company_data[company_data['IP_Density'] != np.inf]
        company_data = company_data[company_data['IP_Density'] > 0]

        # Filtrer les valeurs extrêmes pour une meilleure visualisation
        company_data_filtered = company_data[company_data['IP_Density'] < 2.5]

        # Statistiques de la densité IP
        ip_density_stats = {
            'Min': company_data['IP_Density'].min(),
            'Max': company_data['IP_Density'].max(),
            'Median': company_data['IP_Density'].median(),
            'Mean': company_data['IP_Density'].mean()
        }

        col1, col2 = st.columns([3, 1])

        with col1:
            # Graphique 5: Distribution de la densité IP (Boxplot)
            fig5 = px.box(
                company_data_filtered,
                y='IP_Density',
                points='all',
                hover_data=['Entreprise', 'ProfileCount', 'Headcount'],
                labels={'IP_Density': 'Densité IP (%)'},
                title='Distribution de la Densité IP (Profiles/Headcount)',
                color_discrete_sequence=['#4e8df5']
            )

            fig5.update_layout(height=500, font=dict(color='#000000'))
            fig5.update_yaxes(range=[0, 0.5])  # Limite par défaut pour une meilleure visualisation

            st.plotly_chart(fig5, use_container_width=True)

            st.caption("*Note: Le graphique est zoomé sur [0, 0.5%] pour meilleure visibilité. Utilisez les outils de zoom pour voir plus de détails.*")

        with col2:
            # Afficher les statistiques
            st.subheader("Statistiques de Densité IP")
            for stat_name, stat_value in ip_density_stats.items():
                if np.isfinite(stat_value):
                    st.metric(label=stat_name, value=f"{stat_value:.4f}%")
                else:
                    st.metric(label=stat_name, value="N/A")
    else:
        st.warning("Données d'entreprises ou de headcount non disponibles pour calculer la densité IP")

    # Graphique 6: "Average Workflow Composition"
    if 'Workflow' in df_filtered.columns and 'Entreprise' in df_filtered.columns:
        # Filtrer uniquement les workflows souhaités
        valid_workflows = ['Patent Litigation', 'Patent Preparation & Prosecution', 'Both']
        df_workflow = df_filtered[df_filtered['Workflow'].isin(valid_workflows)]

        if len(df_workflow) > 0:
            if comparison_mode and df_compare is not None:
                # Mode comparaison
                df_workflow2 = df_compare[df_compare['Workflow'].isin(valid_workflows)]

                # Calculer la composition de workflow pour chaque groupe
                workflow_counts1 = df_workflow['Workflow'].value_counts()
                workflow_pct1 = (workflow_counts1 / len(df_workflow)) * 100

                workflow_counts2 = df_workflow2['Workflow'].value_counts()
                workflow_pct2 = (workflow_counts2 / len(df_workflow2)) * 100

                # Créer un dataframe pour le graphique
                comparison_data = []
                for wf in valid_workflows:
                    comparison_data.append({
                        'Workflow': wf,
                        'Groupe 1': workflow_pct1.get(wf, 0),
                        'Groupe 2': workflow_pct2.get(wf, 0)
                    })

                comp_df = pd.DataFrame(comparison_data)

                fig6 = go.Figure()
                fig6.add_trace(go.Bar(
                    x=comp_df['Workflow'],
                    y=comp_df['Groupe 1'],
                    name='Groupe 1',
                    marker=dict(color='#4e8df5'),
                    text=[f"{val:.1f}%" for val in comp_df['Groupe 1']],
                    textposition='outside'
                ))
                fig6.add_trace(go.Bar(
                    x=comp_df['Workflow'],
                    y=comp_df['Groupe 2'],
                    name='Groupe 2',
                    marker=dict(color='#f58d4e'),
                    text=[f"{val:.1f}%" for val in comp_df['Groupe 2']],
                    textposition='outside'
                ))

                fig6.update_layout(
                    title='Composition des Workflows - Comparaison',
                    xaxis_title='Type de workflow',
                    yaxis_title='Pourcentage (%)',
                    barmode='group',
                    height=500
                )
            else:
                # Mode simple
                # Calculer la composition de workflow pour chaque entreprise
                enterprise_workflows = pd.crosstab(
                    df_workflow['Entreprise'],
                    df_workflow['Workflow']
                )

                # Calculer les pourcentages par entreprise
                enterprise_workflows_pct = enterprise_workflows.div(enterprise_workflows.sum(axis=1), axis=0) * 100

                # Calculer la moyenne des pourcentages (Mean of Means)
                avg_workflow_pct = enterprise_workflows_pct.mean()

                # Créer un dataframe pour le graphique
                avg_workflow_df = pd.DataFrame({
                    'Workflow': avg_workflow_pct.index,
                    'Percentage': avg_workflow_pct.values
                })

                fig6 = px.bar(
                    avg_workflow_df,
                    x='Workflow',
                    y='Percentage',
                    text=[f"{val:.1f}%" for val in avg_workflow_df['Percentage']],
                    title='Composition moyenne des Workflows par entreprise',
                    labels={'Percentage': 'Pourcentage moyen (%)', 'Workflow': 'Type de workflow'},
                    color_discrete_sequence=['#4e8df5']
                )

                fig6.update_layout(height=500)
                fig6.update_traces(textposition='outside')

            fig6.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig6, use_container_width=True)

            if not comparison_mode:
                st.info("Ce graphique représente la moyenne des pourcentages de chaque type de workflow par entreprise (Mean of Means).")
        else:
            st.warning("Aucune donnée de workflow valide disponible")
    else:
        st.warning("Données de workflow non disponibles")

# Onglet 3: Talent & Seniority
with tab3:
    st.header("Talent & Séniorité")

    # Graphique 7: Répartition des niveaux de Séniorité
    col1, col2 = st.columns(2)

    with col1:
        if 'Seniority' in df_filtered.columns:
            if comparison_mode and df_compare is not None:
                # Mode comparaison - utiliser des pie charts côte à côte
                seniority_counts1 = df_filtered['Seniority'].value_counts()
                seniority_pct1 = (seniority_counts1 / len(df_filtered)) * 100

                seniority_counts2 = df_compare['Seniority'].value_counts()
                seniority_pct2 = (seniority_counts2 / len(df_compare)) * 100

                fig7 = make_subplots(
                    rows=1, cols=2,
                    specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=("Groupe 1", "Groupe 2")
                )

                fig7.add_trace(go.Pie(
                    labels=seniority_counts1.index,
                    values=seniority_counts1.values,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Pastel)
                ), row=1, col=1)

                fig7.add_trace(go.Pie(
                    labels=seniority_counts2.index,
                    values=seniority_counts2.values,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Pastel)
                ), row=1, col=2)

                fig7.update_layout(
                    title_text='Répartition des niveaux de Séniorité - Comparaison',
                    height=500
                )
            else:
                # Mode simple - Pie chart avec pourcentages
                seniority_counts = df_filtered['Seniority'].value_counts()

                fig7 = go.Figure(data=[go.Pie(
                    labels=seniority_counts.index,
                    values=seniority_counts.values,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Pastel)
                )])

                fig7.update_layout(
                    title='Répartition des niveaux de Séniorité',
                    height=500
                )

            fig7.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.warning("Données de séniorité non disponibles")

    with col2:
        # Graphique 8: Top 10 des Job Titles les plus fréquents (normalisés)
        if 'JobTitleNormalized' in df_filtered.columns:
            if comparison_mode and df_compare is not None:
                # Mode comparaison
                job_counts1 = df_filtered['JobTitleNormalized'].value_counts().nlargest(10)
                job_counts2 = df_compare['JobTitleNormalized'].value_counts().nlargest(10)

                all_jobs = set(job_counts1.index.tolist() + job_counts2.index.tolist())

                comparison_data = []
                for job in all_jobs:
                    comparison_data.append({
                        'Job': job,
                        'Groupe 1': job_counts1.get(job, 0),
                        'Groupe 2': job_counts2.get(job, 0)
                    })

                comp_df = pd.DataFrame(comparison_data).sort_values('Groupe 1', ascending=False).head(10)

                fig8 = go.Figure()
                fig8.add_trace(go.Bar(
                    y=comp_df['Job'],
                    x=comp_df['Groupe 1'],
                    name='Groupe 1',
                    orientation='h',
                    marker=dict(color='#4e8df5')
                ))
                fig8.add_trace(go.Bar(
                    y=comp_df['Job'],
                    x=comp_df['Groupe 2'],
                    name='Groupe 2',
                    orientation='h',
                    marker=dict(color='#f58d4e')
                ))

                fig8.update_layout(
                    title='Top 10 des Titres de Postes - Comparaison',
                    xaxis_title='Nombre',
                    yaxis_title='',
                    barmode='group',
                    height=500
                )
            else:
                # Mode simple
                job_title_counts = df_filtered['JobTitleNormalized'].value_counts().nlargest(10)

                fig8 = px.bar(
                    x=job_title_counts.values,
                    y=job_title_counts.index,
                    orientation='h',
                    labels={'x': 'Nombre', 'y': ''},
                    title='Top 10 des Titres de Postes (normalisés)',
                    text=job_title_counts.values,
                    color_discrete_sequence=['#4e8df5']
                )

                fig8.update_layout(height=500)
                fig8.update_traces(textposition='outside')

            fig8.update_layout(font=dict(color='#000000'))
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.warning("Données de titre de poste non disponibles")

    # Graphique 9: Séniorité par Persona
    if 'Seniority' in df_filtered.columns and 'Persona' in df_filtered.columns:
        if comparison_mode and df_compare is not None:
            # Mode comparaison
            st.subheader("Répartition de Séniorité par Persona")

            col_comp1, col_comp2 = st.columns(2)

            with col_comp1:
                st.markdown("**Groupe 1**")
                seniority_persona1 = pd.crosstab(df_filtered['Persona'], df_filtered['Seniority'])
                seniority_persona_pct1 = seniority_persona1.div(seniority_persona1.sum(axis=1), axis=0) * 100

                seniority_persona_df1 = seniority_persona_pct1.reset_index().melt(
                    id_vars=['Persona'],
                    var_name='Seniority_Level',
                    value_name='Percentage'
                )

                fig9_1 = px.bar(
                    seniority_persona_df1,
                    x='Persona',
                    y='Percentage',
                    color='Seniority_Level',
                    title='',
                    labels={'Percentage': '%', 'Persona': ''},
                    text=seniority_persona_df1['Percentage'].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) and x > 0 else ''),
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                fig9_1.update_layout(height=600, barmode='stack', showlegend=True, font=dict(color='#000000'))
                st.plotly_chart(fig9_1, use_container_width=True)

            with col_comp2:
                st.markdown("**Groupe 2**")
                seniority_persona2 = pd.crosstab(df_compare['Persona'], df_compare['Seniority'])
                seniority_persona_pct2 = seniority_persona2.div(seniority_persona2.sum(axis=1), axis=0) * 100

                seniority_persona_df2 = seniority_persona_pct2.reset_index().melt(
                    id_vars=['Persona'],
                    var_name='Seniority_Level',
                    value_name='Percentage'
                )

                fig9_2 = px.bar(
                    seniority_persona_df2,
                    x='Persona',
                    y='Percentage',
                    color='Seniority_Level',
                    title='',
                    labels={'Percentage': '%', 'Persona': ''},
                    text=seniority_persona_df2['Percentage'].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) and x > 0 else ''),
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                fig9_2.update_layout(height=600, barmode='stack', showlegend=True, font=dict(color='#000000'))
                st.plotly_chart(fig9_2, use_container_width=True)
        else:
            # Mode simple
            # Créer un tableau croisé de Seniority par Persona
            seniority_persona = pd.crosstab(df_filtered['Persona'], df_filtered['Seniority'])

            # Normaliser pour avoir des pourcentages par Persona
            seniority_persona_pct = seniority_persona.div(seniority_persona.sum(axis=1), axis=0) * 100

            # Préparer les données pour le graphique
            seniority_persona_df = seniority_persona_pct.reset_index().melt(
                id_vars=['Persona'],
                var_name='Seniority_Level',
                value_name='Percentage'
            )

            fig9 = px.bar(
                seniority_persona_df,
                x='Persona',
                y='Percentage',
                color='Seniority_Level',
                title='Répartition de Séniorité par Persona',
                labels={'Percentage': 'Pourcentage (%)', 'Persona': '', 'Seniority_Level': 'Niveau'},
                text=seniority_persona_df['Percentage'].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) and x > 0 else ''),
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig9.update_layout(height=600, barmode='stack', font=dict(color='#000000'))

            st.plotly_chart(fig9, use_container_width=True)

        # Ajouter des insights
        st.info("Ce graphique montre comment les niveaux de séniorité sont répartis dans différents rôles, permettant d'identifier si certains rôles ont tendance à être occupés par des profils plus seniors ou juniors.")
    else:
        st.warning("Données de séniorité ou persona non disponibles")

# Ajout du bouton pour télécharger les données filtrées
st.header("Télécharger les données filtrées")
st.write("Cliquez sur le bouton ci-dessous pour télécharger les données actuellement filtrées au format CSV.")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(df_filtered)
st.download_button(
    label="📥 Télécharger en CSV",
    data=csv_data,
    file_name="ip_patent_litigation_filtered.csv",
    mime="text/csv",
)

# Pied de page
st.markdown("---")
st.markdown("*Dashboard créé avec Streamlit et Plotly pour l'analyse des données de propriété intellectuelle*")

# Optimisations de la mise en page pour une meilleure expérience utilisateur
st.markdown("""
<style>
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
        color: #000000;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8df5;
        color: white !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #6ea3f7;
        color: white;
    }

    /* Métriques */
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stMetric label {
        color: #000000 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #000000 !important;
    }

    /* Bouton de téléchargement */
    .stDownloadButton button {
        background-color: #4e8df5 !important;
        color: white !important;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }
    .stDownloadButton button:hover {
        background-color: #3d7de0 !important;
    }

    /* Texte sur fond noir - le rendre plus clair */
    .stApp {
        color: #ffffff;
    }

    /* Headers et titres sur fond sombre */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* Texte dans les sections principales */
    .main .block-container {
        color: #ffffff;
    }

    /* Texte des paragraphes */
    p {
        color: #e0e0e0 !important;
    }

    /* Texte dans les infos/warnings/captions */
    .stAlert, .stInfo, .stWarning, .stCaption {
        color: #000000 !important;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Labels des filtres dans sidebar */
    .stSelectbox label, .stMultiSelect label, .stRadio label {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

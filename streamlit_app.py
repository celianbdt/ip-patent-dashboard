import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page
st.set_page_config(
    layout="wide",
    page_title="Dashboard IP - TAM Analysis",
    page_icon="⬡",
    initial_sidebar_state="expanded"
)

# Custom CSS pour un design DeepIP-inspired (bleu foncé, violet, orange)
st.markdown("""
<style>
    /* Reset et base - Style DeepIP */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0d1117 100%);
    }

    /* Titres */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Paragraphes et texte */
    p, span, label {
        color: #b4b4b4 !important;
    }

    /* Sidebar - Style DeepIP */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141421 0%, #0d0d15 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* Expander dans sidebar */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.1) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(99, 102, 241, 0.2) !important;
    }

    /* Onglets - Style DeepIP */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        color: #b4b4b4 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(99, 102, 241, 0.15) !important;
        border-color: #6366f1 !important;
        color: #ffffff !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    }

    /* Forcer le texte dans les onglets */
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) p,
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) span,
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) div {
        color: #b4b4b4 !important;
    }

    /* Texte blanc dans l'onglet sélectionné */
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div {
        color: #ffffff !important;
    }

    /* Métriques - Style DeepIP */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stMetric"] label {
        color: #9ca3af !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }

    /* Multiselect et selectbox - texte noir sur blanc */
    .stMultiSelect, .stSelectbox {
        color: #000000 !important;
    }

    .stMultiSelect [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #e0e0e0 !important;
        color: #1a1a2e !important;
    }

    /* Placeholder text en noir */
    .stMultiSelect [data-baseweb="select"] input,
    .stSelectbox [data-baseweb="select"] input,
    .stMultiSelect [data-baseweb="select"] [data-baseweb="input"] input,
    .stSelectbox [data-baseweb="select"] [data-baseweb="input"] input {
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
    }

    .stMultiSelect [data-baseweb="select"] input::placeholder,
    .stSelectbox [data-baseweb="select"] input::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
        opacity: 1 !important;
    }

    /* Texte dans le select */
    .stMultiSelect [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] span,
    .stMultiSelect [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] div {
        color: #1a1a2e !important;
    }

    .stMultiSelect [data-baseweb="tag"],
    .stSelectbox [data-baseweb="tag"] {
        background-color: #6366f1 !important;
        color: #ffffff !important;
    }

    .stMultiSelect [data-baseweb="tag"] span,
    .stSelectbox [data-baseweb="tag"] span {
        color: #ffffff !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }

    .stRadio label {
        color: #ffffff !important;
    }

    /* Bouton de téléchargement */
    .stDownloadButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* Info et warnings */
    .stAlert {
        background-color: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* Caption */
    .stCaption {
        color: #9ca3af !important;
    }

    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Success message sidebar */
    [data-testid="stSidebar"] .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }

    /* Info message sidebar */
    [data-testid="stSidebar"] .stInfo {
        background-color: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal avec style
st.markdown("# Dashboard IP - Analyse TAM")
st.markdown("*Analyse des profils et entreprises dans le domaine de la propriété intellectuelle*")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data/Merged TAM with Brevets.csv', low_memory=False)

    # Nettoyer les noms de colonnes
    df.columns = [c.replace('\n', ' ').strip() for c in df.columns]

    # Mapping des colonnes pour faciliter l'utilisation
    column_mapping = {
        'Titre': 'JobTitle',
        'Taille de l\'entreprise': 'Headcount',
        'Size': 'CompanySize',
        'Secteurs d\'activité': 'Industry',
        'Lieu': 'Location',
        'Region (2)': 'Region',
        'Brevets des 3 dernières années': 'Patents_Recent',
        'Total Brevets': 'Patents_Total',
        'Nombre_IP_Pro': 'IP_Team_Size'
    }

    df.rename(columns=column_mapping, inplace=True)

    # Convertir Headcount en numérique
    if 'Headcount' in df.columns:
        df['Headcount'] = pd.to_numeric(df['Headcount'], errors='coerce')

    # Convertir les colonnes numériques
    if 'IP_Team_Size' in df.columns:
        df['IP_Team_Size'] = pd.to_numeric(df['IP_Team_Size'], errors='coerce').fillna(0).astype(int)
    if 'Patents_Recent' in df.columns:
        df['Patents_Recent'] = pd.to_numeric(df['Patents_Recent'], errors='coerce')
    if 'Patents_Total' in df.columns:
        df['Patents_Total'] = pd.to_numeric(df['Patents_Total'], errors='coerce')

    # Extraire le pays de la location
    if 'Location' in df.columns:
        df['Country'] = df['Location'].apply(lambda x: x.split(',')[-1].strip() if isinstance(x, str) and ',' in x else (x if isinstance(x, str) else "Unknown"))
    else:
        df['Country'] = 'Unknown'

    # Normaliser les valeurs de Region - Les vides sont NA (North America)
    if 'Region' in df.columns:
        df['Region'] = df['Region'].fillna('NA')
        df['Region'] = df['Region'].replace({'': 'NA', 'Error processing request': 'NA'})

    # S'assurer que Tier existe et est propre
    if 'Tier' in df.columns:
        df['Tier'] = df['Tier'].fillna('Unknown')
        # Normaliser les valeurs de tier
        tier_mapping = {
            'Tier 1': 'T1', 'Tier1': 'T1', 'T1': 'T1',
            'Tier 2': 'T2', 'Tier2': 'T2', 'T2': 'T2',
            'Tier 3': 'T3', 'Tier3': 'T3', 'T3': 'T3'
        }
        df['Tier'] = df['Tier'].replace(tier_mapping)

    # Gestion des valeurs manquantes
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(0)

    return df

# Charger les données
try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

# === SIDEBAR - FILTRES AVEC INCLUDE/EXCLUDE PAR FILTRE ===
st.sidebar.markdown("## Filtres")
st.sidebar.caption("+ Inclure | - Exclure")

# Fonction helper pour créer un filtre avec mode include/exclude
def create_filter_with_exclude(label, column, help_text=None):
    """Crée un filtre avec possibilité d'inclure ou exclure"""
    include_list = []
    exclude_list = []

    if column in df.columns:
        values = sorted([v for v in df[column].unique() if v != 'Unknown' and pd.notna(v)])

        with st.sidebar.expander(f"{label}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**+ Inclure**")
                include_list = st.multiselect(
                    f"Inclure {label}",
                    values,
                    default=[],
                    key=f"include_{column}",
                    label_visibility="collapsed"
                )
            with col2:
                st.markdown("**- Exclure**")
                # Exclure seulement les valeurs non incluses
                available_for_exclude = [v for v in values if v not in include_list]
                exclude_list = st.multiselect(
                    f"Exclure {label}",
                    available_for_exclude,
                    default=[],
                    key=f"exclude_{column}",
                    label_visibility="collapsed"
                )
            if help_text:
                st.caption(help_text)

    return include_list, exclude_list

# Filtre Tier
include_tiers, exclude_tiers = create_filter_with_exclude(
    "Tiering", "Tier",
    "T1: >30 profils IP | T2: 5-30 | T3: <5"
)

# Filtre Région
include_regions, exclude_regions = create_filter_with_exclude(
    "Région", "Region"
)

# Filtre Industry
include_industries, exclude_industries = create_filter_with_exclude(
    "Industrie", "Industry"
)

# Filtre Company Size
include_sizes, exclude_sizes = create_filter_with_exclude(
    "Taille entreprise", "CompanySize"
)

# Filtre Seniority
include_seniorities, exclude_seniorities = create_filter_with_exclude(
    "Séniorité", "Seniority"
)

# Filtre Persona
include_personas, exclude_personas = create_filter_with_exclude(
    "Persona", "Persona"
)

# === DÉFINITION TIERING PERSONNALISÉ ===
st.sidebar.markdown("---")
st.sidebar.markdown("## Tiering Personnalisé")
st.sidebar.caption("Définissez vos propres critères de tiering")

# Valeurs par défaut pour le tiering
with st.sidebar.expander("Définir les Tiers", expanded=False):
    st.markdown("**Critères : Personnes IP + Brevets 3 ans**")

    # TIER 1
    st.markdown("**TIER 1** (Grands comptes)")
    col_t1a, col_t1b = st.columns(2)
    with col_t1a:
        t1_ip_min = st.number_input("IP min", value=30, min_value=0, key="t1_ip_min")
        t1_patents_min = st.number_input("Brevets 3a min", value=0, min_value=0, key="t1_pat_min")
    with col_t1b:
        t1_ip_max = st.number_input("IP max", value=9999, min_value=0, key="t1_ip_max")
        t1_patents_max = st.number_input("Brevets 3a max", value=999999, min_value=0, key="t1_pat_max")

    st.markdown("---")

    # TIER 2
    st.markdown("**TIER 2** (Moyens comptes)")
    col_t2a, col_t2b = st.columns(2)
    with col_t2a:
        t2_ip_min = st.number_input("IP min", value=5, min_value=0, key="t2_ip_min")
        t2_patents_min = st.number_input("Brevets 3a min", value=0, min_value=0, key="t2_pat_min")
    with col_t2b:
        t2_ip_max = st.number_input("IP max", value=29, min_value=0, key="t2_ip_max")
        t2_patents_max = st.number_input("Brevets 3a max", value=999999, min_value=0, key="t2_pat_max")

    st.markdown("---")

    # TIER 3
    st.markdown("**TIER 3** (Petits comptes)")
    col_t3a, col_t3b = st.columns(2)
    with col_t3a:
        t3_ip_min = st.number_input("IP min", value=0, min_value=0, key="t3_ip_min")
        t3_patents_min = st.number_input("Brevets 3a min", value=0, min_value=0, key="t3_pat_min")
    with col_t3b:
        t3_ip_max = st.number_input("IP max", value=4, min_value=0, key="t3_ip_max")
        t3_patents_max = st.number_input("Brevets 3a max", value=999999, min_value=0, key="t3_pat_max")

# Calculer le tiering personnalisé
def calculate_custom_tier(row):
    ip_count = row.get('IP_Team_Size', 0) or 0
    patents_3y = row.get('Patents_Recent', 0) or 0

    # T1 : vérifie les conditions
    if (t1_ip_min <= ip_count <= t1_ip_max) and (t1_patents_min <= patents_3y <= t1_patents_max):
        return 'T1'
    # T2
    elif (t2_ip_min <= ip_count <= t2_ip_max) and (t2_patents_min <= patents_3y <= t2_patents_max):
        return 'T2'
    # T3
    elif (t3_ip_min <= ip_count <= t3_ip_max) and (t3_patents_min <= patents_3y <= t3_patents_max):
        return 'T3'
    else:
        return 'Non classé'

# Appliquer le tiering personnalisé
df['Custom_Tier'] = df.apply(calculate_custom_tier, axis=1)

# Appliquer les filtres
df_filtered = df.copy()

# Appliquer INCLUSIONS (si sélectionnées)
if include_tiers:
    df_filtered = df_filtered[df_filtered['Tier'].isin(include_tiers)]
if include_regions:
    df_filtered = df_filtered[df_filtered['Region'].isin(include_regions)]
if include_industries and 'Industry' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['Industry'].isin(include_industries)]
if include_sizes:
    df_filtered = df_filtered[df_filtered['CompanySize'].isin(include_sizes)]
if include_seniorities:
    df_filtered = df_filtered[df_filtered['Seniority'].isin(include_seniorities)]
if include_personas:
    df_filtered = df_filtered[df_filtered['Persona'].isin(include_personas)]

# Appliquer EXCLUSIONS
if exclude_tiers:
    df_filtered = df_filtered[~df_filtered['Tier'].isin(exclude_tiers)]
if exclude_regions:
    df_filtered = df_filtered[~df_filtered['Region'].isin(exclude_regions)]
if exclude_industries and 'Industry' in df_filtered.columns:
    df_filtered = df_filtered[~df_filtered['Industry'].isin(exclude_industries)]
if exclude_sizes:
    df_filtered = df_filtered[~df_filtered['CompanySize'].isin(exclude_sizes)]
if exclude_seniorities:
    df_filtered = df_filtered[~df_filtered['Seniority'].isin(exclude_seniorities)]
if exclude_personas:
    df_filtered = df_filtered[~df_filtered['Persona'].isin(exclude_personas)]

# Résumé des filtres actifs
st.sidebar.markdown("---")
active_filters = []
if include_tiers:
    active_filters.append(f"+ Tier: {', '.join(include_tiers)}")
if exclude_tiers:
    active_filters.append(f"- Tier: {', '.join(exclude_tiers)}")
if include_regions:
    active_filters.append(f"+ Région: {', '.join(include_regions)}")
if exclude_regions:
    active_filters.append(f"- Région: {', '.join(exclude_regions)}")
if include_industries:
    active_filters.append(f"+ Industrie: {len(include_industries)} sélectionnées")
if exclude_industries:
    active_filters.append(f"- Industrie: {len(exclude_industries)} exclues")

if active_filters:
    st.sidebar.markdown("**Filtres actifs:**")
    for f in active_filters[:5]:  # Max 5 affichés
        st.sidebar.caption(f)
    if len(active_filters) > 5:
        st.sidebar.caption(f"... et {len(active_filters) - 5} autres")

# Créer un dataframe au niveau entreprise (1 ligne par account)
if 'Entreprise' in df_filtered.columns:
    # Définir les colonnes d'agrégation
    agg_dict = {
        'Tier': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
        'Custom_Tier': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Non classé',
        'Region': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
        'Industry': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
        'CompanySize': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
    }

    # Ajouter les colonnes patents si elles existent (prendre la première valeur - c'est par entreprise)
    if 'IP_Team_Size' in df_filtered.columns:
        agg_dict['IP_Team_Size'] = 'first'
    if 'Patents_Recent' in df_filtered.columns:
        agg_dict['Patents_Recent'] = 'first'
    if 'Patents_Total' in df_filtered.columns:
        agg_dict['Patents_Total'] = 'first'

    df_companies = df_filtered.groupby('Entreprise').agg(agg_dict).reset_index()
    df_companies['Profile_Count'] = df_filtered.groupby('Entreprise').size().values
    total_accounts = len(df_companies)

    # Calculer les totaux de brevets (sans duplication)
    total_patents_recent = df_companies['Patents_Recent'].sum() if 'Patents_Recent' in df_companies.columns else 0
    total_patents = df_companies['Patents_Total'].sum() if 'Patents_Total' in df_companies.columns else 0
    accounts_with_patents = df_companies['Patents_Total'].notna().sum() if 'Patents_Total' in df_companies.columns else 0
else:
    df_companies = pd.DataFrame()
    total_accounts = 0
    total_patents_recent = 0
    total_patents = 0
    accounts_with_patents = 0

total_profiles = len(df_filtered)

st.sidebar.info(f"**{total_accounts:,}** accounts | **{total_profiles:,}** profils")

# === KPIs EN HAUT ===
st.markdown("### Indicateurs Clés (Tiering Personnalisé)")

# Première ligne : Accounts, Profils, Brevets, Non classé
kpi_row1_col1, kpi_row1_col2, kpi_row1_col3, kpi_row1_col4 = st.columns(4)

with kpi_row1_col1:
    st.metric("ACCOUNTS", f"{total_accounts:,}")

with kpi_row1_col2:
    st.metric("PROFILS", f"{total_profiles:,}")

with kpi_row1_col3:
    if total_patents > 0:
        st.metric("BREVETS TOTAL", f"{int(total_patents):,}", f"{accounts_with_patents} accounts")
    else:
        st.metric("BREVETS TOTAL", "N/A")

with kpi_row1_col4:
    if 'Custom_Tier' in df_companies.columns and total_accounts > 0:
        unclassified = len(df_companies[df_companies['Custom_Tier'] == 'Non classé'])
        st.metric("NON CLASSÉ", f"{unclassified:,}", f"{unclassified/total_accounts*100:.1f}%")

# Deuxième ligne : Tier 1, Tier 2, Tier 3
kpi_row2_col1, kpi_row2_col2, kpi_row2_col3 = st.columns(3)

with kpi_row2_col1:
    if 'Custom_Tier' in df_companies.columns and total_accounts > 0:
        t1_accounts = len(df_companies[df_companies['Custom_Tier'] == 'T1'])
        t1_pct = (t1_accounts / total_accounts * 100)
        st.metric("TIER 1", f"{t1_accounts:,}", f"{t1_pct:.1f}%")

with kpi_row2_col2:
    if 'Custom_Tier' in df_companies.columns and total_accounts > 0:
        t2_accounts = len(df_companies[df_companies['Custom_Tier'] == 'T2'])
        t2_pct = (t2_accounts / total_accounts * 100)
        st.metric("TIER 2", f"{t2_accounts:,}", f"{t2_pct:.1f}%")

with kpi_row2_col3:
    if 'Custom_Tier' in df_companies.columns and total_accounts > 0:
        t3_accounts = len(df_companies[df_companies['Custom_Tier'] == 'T3'])
        t3_pct = (t3_accounts / total_accounts * 100)
        st.metric("TIER 3", f"{t3_accounts:,}", f"{t3_pct:.1f}%")

st.markdown("---")

# === ONGLETS PRINCIPAUX ===
tab1, tab2, tab3 = st.tabs(["Vue Globale", "Stratégie IP", "Talent & Séniorité"])

# Palette de couleurs DeepIP (indigo, violet, orange)
colors_gradient = ['#6366f1', '#8b5cf6', '#a855f7', '#f97316', '#fb923c', '#38bdf8']
colors_main = '#6366f1'  # Indigo
colors_secondary = '#8b5cf6'  # Violet
colors_accent = '#f97316'  # Orange

# Configuration commune pour les graphiques Plotly - Police sans-serif
chart_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff', family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
    title_font=dict(size=18, color='#ffffff', family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Inter, -apple-system, BlinkMacSystemFont, sans-serif')
    ),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        linecolor='rgba(255,255,255,0.2)',
        tickfont=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif')
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        linecolor='rgba(255,255,255,0.2)',
        tickfont=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif')
    )
)

# === ONGLET 1: VUE GLOBALE (basé sur les ACCOUNTS) ===
with tab1:
    st.caption("Toutes les statistiques sont basées sur le nombre d'entreprises (accounts), pas sur les profils individuels.")

    col1, col2 = st.columns(2)

    with col1:
        # Distribution par Tier PERSONNALISÉ (basé sur les accounts)
        if 'Custom_Tier' in df_companies.columns and len(df_companies) > 0:
            tier_counts = df_companies['Custom_Tier'].value_counts()
            tier_order = ['T1', 'T2', 'T3', 'Non classé']
            tier_counts = tier_counts.reindex([t for t in tier_order if t in tier_counts.index])

            fig_tier = go.Figure(data=[go.Pie(
                labels=tier_counts.index,
                values=tier_counts.values,
                hole=0.5,
                marker=dict(colors=['#6366f1', '#8b5cf6', '#f97316', '#64748b']),
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Inter, sans-serif'),
                hovertemplate='<b>%{label}</b><br>Accounts: %{value:,}<br>Pourcentage: %{percent}<extra></extra>'
            )])

            fig_tier.update_layout(
                title='Distribution par Tiering Personnalisé',
                **chart_layout,
                height=400,
                showlegend=True,
                annotations=[dict(
                    text=f'{total_accounts:,}',
                    x=0.5, y=0.5,
                    font_size=24, font_color='white',
                    showarrow=False
                )]
            )
            st.plotly_chart(fig_tier, use_container_width=True)
            st.caption("**T1**: >30 profils IP | **T2**: 5-30 | **T3**: <5")

    with col2:
        # Distribution par Région (basé sur les accounts)
        if 'Region' in df_companies.columns and len(df_companies) > 0:
            region_counts = df_companies['Region'].value_counts().head(5)
            region_pcts = (region_counts / total_accounts * 100).round(1)

            fig_region = go.Figure(data=[go.Bar(
                x=region_counts.index,
                y=region_counts.values,
                marker=dict(
                    color=region_counts.values,
                    colorscale=[[0, '#6366f1'], [1, '#8b5cf6']],
                    showscale=False
                ),
                text=[f'{v:,} ({p}%)' for v, p in zip(region_counts.values, region_pcts.values)],
                textposition='outside',
                textfont=dict(color='white', size=12, family='Inter, sans-serif')
            )])

            fig_region.update_layout(
                title='Distribution par Région (Accounts)',
                xaxis_title='',
                yaxis_title='Nombre d\'accounts',
                **chart_layout,
                height=400
            )
            st.plotly_chart(fig_region, use_container_width=True)

    # Deuxième ligne
    col3, col4 = st.columns(2)

    with col3:
        # Top 10 Industries (basé sur les accounts)
        if 'Industry' in df_companies.columns and len(df_companies) > 0:
            industry_counts = df_companies['Industry'].value_counts().nlargest(10)
            industry_pcts = (industry_counts / total_accounts * 100).round(1)

            fig_industry = go.Figure(data=[go.Bar(
                y=industry_counts.index[::-1],
                x=industry_counts.values[::-1],
                orientation='h',
                marker=dict(
                    color=list(range(len(industry_counts))),
                    colorscale=[[0, '#8b5cf6'], [1, '#6366f1']],
                    showscale=False
                ),
                text=[f'{v:,} ({p}%)' for v, p in zip(industry_counts.values[::-1], industry_pcts.values[::-1])],
                textposition='outside',
                textfont=dict(color='white', size=11, family='Inter, sans-serif')
            )])

            fig_industry.update_layout(
                title='Top 10 Industries (Accounts)',
                xaxis_title='Nombre d\'accounts',
                yaxis_title='',
                **chart_layout,
                height=500
            )
            st.plotly_chart(fig_industry, use_container_width=True)

    with col4:
        # Distribution par taille d'entreprise (basé sur les accounts)
        if 'CompanySize' in df_companies.columns and len(df_companies) > 0:
            size_counts = df_companies['CompanySize'].value_counts()

            # Ordre logique des tailles
            size_order = ['Small', 'Medium', 'Large', 'Enterprise']
            size_counts = size_counts.reindex([s for s in size_order if s in size_counts.index])
            size_pcts = (size_counts / total_accounts * 100).round(1)

            fig_size = go.Figure(data=[go.Bar(
                x=size_counts.index,
                y=size_counts.values,
                marker=dict(
                    color=['#4facfe', '#00f2fe', '#6366f1', '#8b5cf6'][:len(size_counts)],
                    showscale=False
                ),
                text=[f'{v:,} ({p}%)' for v, p in zip(size_counts.values, size_pcts.values)],
                textposition='outside',
                textfont=dict(color='white', size=12, family='Inter, sans-serif')
            )])

            fig_size.update_layout(
                title='Distribution par Taille (Accounts)',
                xaxis_title='',
                yaxis_title='Nombre d\'accounts',
                **chart_layout,
                height=500
            )
            st.plotly_chart(fig_size, use_container_width=True)

    # Top 15 Entreprises par nombre de profils IP
    if 'Entreprise' in df_filtered.columns:
        st.markdown("### Top 15 Accounts par taille d'équipe IP")

        company_counts = df_filtered['Entreprise'].value_counts().nlargest(15)

        fig_companies = go.Figure(data=[go.Bar(
            x=company_counts.index,
            y=company_counts.values,
            marker=dict(
                color=company_counts.values,
                colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#f97316']],
                showscale=False
            ),
            text=company_counts.values,
            textposition='outside',
            textfont=dict(color='white', size=12, family='Inter, sans-serif')
        )])

        fig_companies.update_layout(
            xaxis_title='',
            yaxis_title='Nombre de profils IP',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
            title_font=dict(size=18, color='#ffffff', family='Inter, -apple-system, BlinkMacSystemFont, sans-serif'),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff')),
            height=400,
            xaxis=dict(tickangle=45, gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.2)', tickfont=dict(family='Inter, sans-serif')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.2)', tickfont=dict(family='Inter, sans-serif'))
        )
        st.plotly_chart(fig_companies, use_container_width=True)
        st.caption("Ce graphique montre le nombre de profils IP par entreprise (pas les accounts).")

# === ONGLET 2: STRATÉGIE IP (basé sur les ACCOUNTS) ===
with tab2:
    st.caption("Statistiques basées sur les accounts (entreprises uniques).")

    # Ajouter Workflow et Persona au df_companies si pas déjà fait
    if 'Entreprise' in df_filtered.columns and len(df_companies) > 0:
        if 'Workflow' not in df_companies.columns and 'Workflow' in df_filtered.columns:
            workflow_by_company = df_filtered.groupby('Entreprise')['Workflow'].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown')
            df_companies = df_companies.merge(workflow_by_company.reset_index(), on='Entreprise', how='left')
        if 'Persona' not in df_companies.columns and 'Persona' in df_filtered.columns:
            persona_by_company = df_filtered.groupby('Entreprise')['Persona'].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown')
            df_companies = df_companies.merge(persona_by_company.reset_index(), on='Entreprise', how='left')

    col1, col2 = st.columns(2)

    with col1:
        # Distribution Workflow (basé sur les accounts)
        if 'Workflow' in df_companies.columns and len(df_companies) > 0:
            workflow_counts = df_companies['Workflow'].value_counts()

            fig_workflow = go.Figure(data=[go.Pie(
                labels=workflow_counts.index,
                values=workflow_counts.values,
                hole=0.4,
                marker=dict(colors=['#6366f1', '#8b5cf6', '#f97316', '#fb923c']),
                textinfo='label+percent',
                textfont=dict(size=12, color='white', family='Inter, sans-serif'),
                hovertemplate='<b>%{label}</b><br>Accounts: %{value:,}<br>%{percent}<extra></extra>'
            )])

            fig_workflow.update_layout(
                title='Répartition par Workflow (Accounts)',
                **chart_layout,
                height=400
            )
            st.plotly_chart(fig_workflow, use_container_width=True)

    with col2:
        # Distribution Persona (basé sur les accounts)
        if 'Persona' in df_companies.columns and len(df_companies) > 0:
            persona_counts = df_companies['Persona'].value_counts()

            fig_persona = go.Figure(data=[go.Pie(
                labels=persona_counts.index,
                values=persona_counts.values,
                hole=0.4,
                marker=dict(colors=['#4facfe', '#00f2fe', '#6366f1', '#8b5cf6', '#f97316']),
                textinfo='label+percent',
                textfont=dict(size=12, color='white', family='Inter, sans-serif'),
                hovertemplate='<b>%{label}</b><br>Accounts: %{value:,}<br>%{percent}<extra></extra>'
            )])

            fig_persona.update_layout(
                title='Répartition par Persona (Accounts)',
                **chart_layout,
                height=400
            )
            st.plotly_chart(fig_persona, use_container_width=True)

    # Tier vs Workflow (basé sur les accounts)
    if 'Custom_Tier' in df_companies.columns and 'Workflow' in df_companies.columns and len(df_companies) > 0:
        st.markdown("### Tiering Personnalisé vs Workflow (Accounts)")

        tier_workflow = pd.crosstab(df_companies['Custom_Tier'], df_companies['Workflow'])
        tier_order = ['T1', 'T2', 'T3', 'Non classé']
        tier_workflow = tier_workflow.reindex([t for t in tier_order if t in tier_workflow.index])

        fig_tier_workflow = go.Figure()

        colors_workflow = ['#6366f1', '#8b5cf6', '#f97316', '#fb923c']
        for i, workflow in enumerate(tier_workflow.columns):
            fig_tier_workflow.add_trace(go.Bar(
                name=workflow,
                x=tier_workflow.index,
                y=tier_workflow[workflow],
                marker_color=colors_workflow[i % len(colors_workflow)],
                text=tier_workflow[workflow],
                textposition='auto',
                textfont=dict(color='white', family='Inter, sans-serif')
            ))

        fig_tier_workflow.update_layout(
            barmode='group',
            xaxis_title='Tier',
            yaxis_title='Nombre d\'accounts',
            **chart_layout,
            height=400
        )
        st.plotly_chart(fig_tier_workflow, use_container_width=True)

    # IP Density si possible
    if 'Entreprise' in df_filtered.columns and 'Headcount' in df_filtered.columns:
        st.markdown("### Densité IP par Entreprise")

        company_stats = df_filtered.groupby('Entreprise').agg({
            'Headcount': 'first',
            'Custom_Tier': 'first'
        }).reset_index()
        company_stats.rename(columns={'Custom_Tier': 'Tier'}, inplace=True)

        profile_counts = df_filtered.groupby('Entreprise').size().reset_index(name='IP_Profiles')
        company_stats = company_stats.merge(profile_counts, on='Entreprise')

        # Calculer la densité
        company_stats['IP_Density'] = (company_stats['IP_Profiles'] / company_stats['Headcount']) * 100
        company_stats = company_stats[company_stats['IP_Density'].notna() & (company_stats['IP_Density'] < 5)]

        if len(company_stats) > 0:
            fig_density = px.box(
                company_stats,
                x='Tier',
                y='IP_Density',
                color='Tier',
                color_discrete_map={'T1': '#6366f1', 'T2': '#8b5cf6', 'T3': '#f97316'},
                points='all',
                hover_data=['Entreprise', 'IP_Profiles', 'Headcount']
            )

            fig_density.update_layout(
                title='Distribution de la Densité IP par Tier',
                xaxis_title='Tier',
                yaxis_title='Densité IP (%)',
                **chart_layout,
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_density, use_container_width=True)

    # === SECTION BREVETS ===
    st.markdown("---")
    st.markdown("### Analyse des Brevets")

    # Filtrer les accounts avec des brevets (>0) - ne pas compter ceux sans données
    if 'Patents_Total' in df_companies.columns:
        df_with_patents = df_companies[df_companies['Patents_Total'] > 0].copy()
        accounts_with_patents_count = len(df_with_patents)

        if accounts_with_patents_count > 0:
            # KPIs Brevets
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)

            with col_p1:
                avg_total = df_with_patents['Patents_Total'].mean()
                st.metric("MOY. BREVETS TOTAL", f"{avg_total:,.0f}")

            with col_p2:
                avg_recent = df_with_patents['Patents_Recent'].mean() if 'Patents_Recent' in df_with_patents.columns else 0
                st.metric("MOY. BREVETS 3 ANS", f"{avg_recent:,.0f}")

            with col_p3:
                median_total = df_with_patents['Patents_Total'].median()
                st.metric("MÉDIANE BREVETS", f"{median_total:,.0f}")

            with col_p4:
                st.metric("ACCOUNTS AVEC BREVETS", f"{accounts_with_patents_count:,}",
                         f"{accounts_with_patents_count/total_accounts*100:.1f}%")

            st.caption(f"Statistiques calculées uniquement sur les {accounts_with_patents_count:,} accounts ayant des données de brevets (brevets > 0).")

            # Graphiques brevets
            col_b1, col_b2 = st.columns(2)

            with col_b1:
                # Distribution des brevets totaux par Tier
                if 'Custom_Tier' in df_with_patents.columns:
                    tier_patents = df_with_patents.groupby('Custom_Tier').agg({
                        'Patents_Total': 'mean',
                        'Patents_Recent': 'mean'
                    }).reindex(['T1', 'T2', 'T3']).dropna()

                    fig_patents_tier = go.Figure()
                    fig_patents_tier.add_trace(go.Bar(
                        name='Brevets Total (moy)',
                        x=tier_patents.index,
                        y=tier_patents['Patents_Total'],
                        marker_color='#6366f1',
                        text=[f'{v:,.0f}' for v in tier_patents['Patents_Total']],
                        textposition='outside',
                        textfont=dict(color='white', family='Inter, sans-serif')
                    ))
                    fig_patents_tier.add_trace(go.Bar(
                        name='Brevets 3 ans (moy)',
                        x=tier_patents.index,
                        y=tier_patents['Patents_Recent'],
                        marker_color='#f97316',
                        text=[f'{v:,.0f}' for v in tier_patents['Patents_Recent']],
                        textposition='outside',
                        textfont=dict(color='white', family='Inter, sans-serif')
                    ))

                    fig_patents_tier.update_layout(
                        title='Moyenne Brevets par Tier',
                        barmode='group',
                        xaxis_title='Tier',
                        yaxis_title='Nombre moyen de brevets',
                        **chart_layout,
                        height=400
                    )
                    st.plotly_chart(fig_patents_tier, use_container_width=True)

            with col_b2:
                # Distribution (box plot) des brevets
                fig_box = px.box(
                    df_with_patents,
                    x='Custom_Tier',
                    y='Patents_Total',
                    color='Custom_Tier',
                    color_discrete_map={'T1': '#6366f1', 'T2': '#8b5cf6', 'T3': '#f97316', 'Non classé': '#64748b'},
                    hover_data=['Entreprise']
                )

                fig_box.update_layout(
                    title='Distribution Brevets Total par Tier',
                    xaxis_title='Tier',
                    yaxis_title='Nombre de brevets',
                    **chart_layout,
                    height=400,
                    showlegend=False
                )
                # Limiter l'axe Y pour meilleure lisibilité
                fig_box.update_yaxes(range=[0, df_with_patents['Patents_Total'].quantile(0.95)])
                st.plotly_chart(fig_box, use_container_width=True)

            # Top 10 entreprises par brevets
            top_patent_companies = df_with_patents.nlargest(10, 'Patents_Total')[['Entreprise', 'Patents_Total', 'Patents_Recent', 'Custom_Tier']]

            fig_top_patents = go.Figure(data=[go.Bar(
                y=top_patent_companies['Entreprise'][::-1],
                x=top_patent_companies['Patents_Total'][::-1],
                orientation='h',
                marker=dict(
                    color=top_patent_companies['Patents_Total'][::-1],
                    colorscale=[[0, '#6366f1'], [1, '#f97316']],
                    showscale=False
                ),
                text=[f'{v:,.0f}' for v in top_patent_companies['Patents_Total'][::-1]],
                textposition='outside',
                textfont=dict(color='white', size=11, family='Inter, sans-serif')
            )])

            fig_top_patents.update_layout(
                title='Top 10 Accounts par Nombre de Brevets',
                xaxis_title='Nombre total de brevets',
                yaxis_title='',
                **chart_layout,
                height=450
            )
            st.plotly_chart(fig_top_patents, use_container_width=True)
        else:
            st.info("Aucun account avec des données de brevets dans la sélection actuelle.")

# === ONGLET 3: TALENT & SÉNIORITÉ ===
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        # Distribution Seniority
        if 'Seniority' in df_filtered.columns:
            seniority_counts = df_filtered['Seniority'].value_counts()

            # Ordre logique
            sen_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Executive']
            seniority_counts = seniority_counts.reindex([s for s in sen_order if s in seniority_counts.index])

            fig_seniority = go.Figure(data=[go.Pie(
                labels=seniority_counts.index,
                values=seniority_counts.values,
                hole=0.5,
                marker=dict(colors=['#4facfe', '#00f2fe', '#6366f1', '#8b5cf6', '#f97316']),
                textinfo='label+percent',
                textfont=dict(size=13, color='white'),
                hovertemplate='<b>%{label}</b><br>Profils: %{value:,}<br>%{percent}<extra></extra>'
            )])

            fig_seniority.update_layout(
                title='Répartition par Séniorité',
                **chart_layout,
                height=400
            )
            st.plotly_chart(fig_seniority, use_container_width=True)

    with col2:
        # Top Job Titles
        if 'JobTitle' in df_filtered.columns:
            job_counts = df_filtered['JobTitle'].value_counts().nlargest(10)

            fig_jobs = go.Figure(data=[go.Bar(
                y=job_counts.index[::-1],
                x=job_counts.values[::-1],
                orientation='h',
                marker=dict(
                    color=list(range(len(job_counts))),
                    colorscale=[[0, '#8b5cf6'], [1, '#6366f1']],
                    showscale=False
                ),
                text=job_counts.values[::-1],
                textposition='outside',
                textfont=dict(color='white', size=11)
            )])

            fig_jobs.update_layout(
                title='Top 10 Titres de Poste',
                xaxis_title='Nombre',
                yaxis_title='',
                **chart_layout,
                height=400
            )
            st.plotly_chart(fig_jobs, use_container_width=True)

    # Seniority par Tier
    if 'Seniority' in df_filtered.columns and 'Custom_Tier' in df_filtered.columns:

        tier_seniority = pd.crosstab(df_filtered['Custom_Tier'], df_filtered['Seniority'], normalize='index') * 100
        tier_order = ['T1', 'T2', 'T3', 'Non classé']
        tier_seniority = tier_seniority.reindex([t for t in tier_order if t in tier_seniority.index])

        sen_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Executive']
        tier_seniority = tier_seniority[[s for s in sen_order if s in tier_seniority.columns]]

        fig_tier_sen = go.Figure()

        colors_sen = ['#4facfe', '#00f2fe', '#6366f1', '#8b5cf6', '#f97316']
        for i, sen in enumerate(tier_seniority.columns):
            fig_tier_sen.add_trace(go.Bar(
                name=sen,
                x=tier_seniority.index,
                y=tier_seniority[sen],
                marker_color=colors_sen[i % len(colors_sen)],
                text=[f'{v:.1f}%' for v in tier_seniority[sen]],
                textposition='auto',
                textfont=dict(color='white', size=11)
            ))

        fig_tier_sen.update_layout(
            title='Séniorité par Tiering',
            barmode='stack',
            xaxis_title='Tier',
            yaxis_title='Pourcentage (%)',
            **chart_layout,
            height=400
        )
        st.plotly_chart(fig_tier_sen, use_container_width=True)

    # Seniority par Persona
    if 'Seniority' in df_filtered.columns and 'Persona' in df_filtered.columns:
        persona_seniority = pd.crosstab(df_filtered['Persona'], df_filtered['Seniority'], normalize='index') * 100

        sen_order = ['Entry', 'Junior', 'Mid', 'Senior', 'Executive']
        persona_seniority = persona_seniority[[s for s in sen_order if s in persona_seniority.columns]]

        fig_persona_sen = go.Figure()

        colors_sen = ['#4facfe', '#00f2fe', '#6366f1', '#8b5cf6', '#f97316']
        for i, sen in enumerate(persona_seniority.columns):
            fig_persona_sen.add_trace(go.Bar(
                name=sen,
                x=persona_seniority.index,
                y=persona_seniority[sen],
                marker_color=colors_sen[i % len(colors_sen)],
                text=[f'{v:.1f}%' for v in persona_seniority[sen]],
                textposition='auto',
                textfont=dict(color='white', size=10)
            ))

        fig_persona_sen.update_layout(
            title='Séniorité par Persona',
            barmode='stack',
            xaxis_title='Persona',
            yaxis_title='Pourcentage (%)',
            **chart_layout,
            height=400
        )
        st.plotly_chart(fig_persona_sen, use_container_width=True)

# === TÉLÉCHARGEMENT ===
st.markdown("---")
st.markdown("### Exporter les données")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])

with col_dl1:
    csv_data = convert_df_to_csv(df_filtered)
    st.download_button(
        label="Télécharger CSV",
        data=csv_data,
        file_name="tam_filtered_export.csv",
        mime="text/csv",
    )

with col_dl2:
    st.info(f"**{len(df_filtered):,}** lignes à exporter")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>"
    "Dashboard IP - Analyse TAM | Créé avec Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)

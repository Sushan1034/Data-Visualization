import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Page Config
st.set_page_config(
    page_title="EV & Charging Infrastructure Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Sidebar Width CSS
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        width: 380px !important; # Set a fixed width to prevent text wrapping
    }
</style>
""", unsafe_allow_html=True)


# ISO-2 to ISO-3 mapping for Choropleth maps
iso_map = {
    'AD': 'AND', 'AE': 'ARE', 'AF': 'AFG', 'AG': 'ATG', 'AL': 'ALB', 'AM': 'ARM', 'AO': 'AGO', 'AR': 'ARG', 
    'AT': 'AUT', 'AU': 'AUS', 'AZ': 'AZE', 'BA': 'BIH', 'BB': 'BRB', 'BD': 'BGD', 'BE': 'BEL', 'BF': 'BFA', 
    'BG': 'BGR', 'BH': 'BHR', 'BI': 'BDI', 'BJ': 'BEN', 'BN': 'BRN', 'BO': 'BOL', 'BR': 'BRA', 'BS': 'BHS', 
    'BT': 'BTN', 'BW': 'BWA', 'BY': 'BLR', 'BZ': 'BLZ', 'CA': 'CAN', 'CD': 'COD', 'CF': 'CAF', 'CG': 'COG', 
    'CH': 'CHE', 'CI': 'CIV', 'CL': 'CHL', 'CM': 'CMR', 'CN': 'CHN', 'CO': 'COL', 'CR': 'CRI', 'CU': 'CUB', 
    'CV': 'CPV', 'CY': 'CYP', 'CZ': 'CZE', 'DE': 'DEU', 'DJ': 'DJI', 'DK': 'DNK', 'DM': 'DMA', 'DO': 'DOM', 
    'DZ': 'DZA', 'EC': 'ECU', 'EE': 'EST', 'EG': 'EGY', 'ER': 'ERI', 'ES': 'ESP', 'ET': 'ETH', 'FI': 'FIN', 
    'FJ': 'FJI', 'FR': 'FRA', 'GA': 'GAB', 'GB': 'GBR', 'GD': 'GRD', 'GE': 'GEO', 'GH': 'GHA', 'GM': 'GMB', 
    'GN': 'GIN', 'GQ': 'GNQ', 'GR': 'GRC', 'GT': 'GTM', 'GW': 'GNB', 'GY': 'GUY', 'HN': 'HND', 'HR': 'HRV', 
    'HT': 'HTI', 'HU': 'HUN', 'ID': 'IDN', 'IE': 'IRL', 'IL': 'ISR', 'IN': 'IND', 'IQ': 'IRQ', 'IR': 'IRN', 
    'IS': 'ISL', 'IT': 'ITA', 'JM': 'JAM', 'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KG': 'KGZ', 'KH': 'KHM', 
    'KI': 'KIR', 'KM': 'COM', 'KN': 'KNA', 'KP': 'PRK', 'KR': 'KOR', 'KW': 'KWT', 'KZ': 'KAZ', 'LA': 'LAO', 
    'LB': 'LBN', 'LC': 'LCA', 'LI': 'LIE', 'LK': 'LKA', 'LR': 'LBR', 'LS': 'LSO', 'LT': 'LTU', 'LU': 'LUX', 
    'LV': 'LVA', 'LY': 'LBY', 'MA': 'MAR', 'MC': 'MCO', 'MD': 'MDA', 'ME': 'MNE', 'MG': 'MDG', 'MH': 'MHL', 
    'MK': 'MKD', 'ML': 'MLI', 'MM': 'MMR', 'MN': 'MNG', 'MR': 'MRT', 'MT': 'MLT', 'MU': 'Mauritius', 'MV': 'MDV', 
    'MW': 'MWI', 'MX': 'MEX', 'MY': 'MYS', 'MZ': 'MOZ', 'NA': 'NAM', 'NE': 'NER', 'NG': 'NGA', 'NI': 'NIC', 
    'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL', 'NR': 'NRU', 'NZ': 'NZL', 'OM': 'OMN', 'PA': 'PAN', 'PE': 'PER', 
    'PG': 'PNG', 'PH': 'PHL', 'PK': 'PAK', 'PL': 'POL', 'PT': 'PRT', 'PW': 'PLW', 'PY': 'PRY', 'QA': 'QAT', 
    'RO': 'ROU', 'RS': 'SRB', 'RU': 'RUS', 'RW': 'RWA', 'SA': 'SAU', 'SB': 'SLB', 'SC': 'SYC', 'SD': 'SDN', 
    'SE': 'SWE', 'SG': 'SGP', 'SI': 'SVN', 'SK': 'SVK', 'SL': 'SLE', 'SN': 'SEN', 'SO': 'SOM', 'SR': 'SUR', 
    'SS': 'SSD', 'ST': 'STP', 'SV': 'SLV', 'SY': 'SYR', 'SZ': 'SWZ', 'TD': 'TCD', 'TG': 'TGO', 'TH': 'THA', 
    'TJ': 'TJK', 'TL': 'TLS', 'TM': 'TKM', 'TN': 'TUN', 'TO': 'TON', 'TR': 'TUR', 'TT': 'TTO', 'TV': 'TUV', 
    'TW': 'TWN', 'TZ': 'TZA', 'UA': 'UKR', 'UG': 'UGA', 'US': 'USA', 'UY': 'URY', 'UZ': 'UZB', 'VC': 'VCT', 
    'VE': 'VEN', 'VN': 'VNM', 'VU': 'VUT', 'WS': 'WSM', 'YE': 'YEM', 'ZA': 'ZAF', 'ZM': 'ZMB', 'ZW': 'ZWE'
}

# ISO-2 to Full Name mapping for sidebar filters
country_name_map = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AG': 'Antigua and Barbuda', 
    'AL': 'Albania', 'AM': 'Armenia', 'AO': 'Angola', 'AR': 'Argentina', 'AT': 'Austria', 'AU': 'Australia', 
    'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'BD': 'Bangladesh', 'BE': 'Belgium', 
    'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BN': 'Brunei', 
    'BO': 'Bolivia', 'BR': 'Brazil', 'BS': 'Bahamas', 'BT': 'Bhutan', 'BW': 'Botswana', 'BY': 'Belarus', 
    'BZ': 'Belize', 'CA': 'Canada', 'CD': 'Congo (DRC)', 'CF': 'Central African Republic', 'CG': 'Congo (Republic)', 
    'CH': 'Switzerland', 'CI': 'Ivory Coast', 'CL': 'Chile', 'CM': 'Cameroon', 'CN': 'China', 'CO': 'Colombia', 
    'CR': 'Costa Rica', 'CU': 'Cuba', 'CV': 'Cape Verde', 'CY': 'Cyprus', 'CZ': 'Czech Republic', 'DE': 'Germany', 
    'DJ': 'Djibouti', 'DK': 'Denmark', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'DZ': 'Algeria', 
    'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'ER': 'Eritrea', 'ES': 'Spain', 'ET': 'Ethiopia', 
    'FI': 'Finland', 'FJ': 'Fiji', 'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom', 'GD': 'Grenada', 
    'GE': 'Georgia', 'GH': 'Ghana', 'GM': 'Gambia', 'GN': 'Guinea', 'GQ': 'Equatorial Guinea', 'GR': 'Greece', 
    'GT': 'Guatemala', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HN': 'Honduras', 'HR': 'Croatia', 'HT': 'Haiti', 
    'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq', 
    'IR': 'Iran', 'IS': 'Iceland', 'IT': 'Italy', 'JM': 'Jamaica', 'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya', 
    'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KI': 'Kiribati', 'KM': 'Comoros', 'KN': 'Saint Kitts and Nevis', 
    'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LA': 'Laos', 'LB': 'Lebanon', 
    'LC': 'Saint Lucia', 'LI': 'Liechtenstein', 'LK': 'Sri Lanka', 'LR': 'Liberia', 'LS': 'Lesotho', 
    'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco', 'MC': 'Monaco', 
    'MD': 'Moldova', 'ME': 'Montenegro', 'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia', 
    'ML': 'Mali', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MR': 'Mauritania', 'MT': 'Malta', 'MU': 'Mauritius', 
    'MV': 'Maldives', 'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NA': 'Namibia', 
    'NE': 'Niger', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NP': 'Nepal', 
    'NR': 'Nauru', 'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama', 'PE': 'Peru', 'PG': 'Papua New Guinea', 
    'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PT': 'Portugal', 'PW': 'Palau', 'PY': 'Paraguay', 
    'QA': 'Qatar', 'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russia', 'RW': 'Rwanda', 'SA': 'Saudi Arabia', 
    'SB': 'Solomon Islands', 'SC': 'Seychelles', 'SD': 'Sudan', 'SE': 'Sweden', 'SG': 'Singapore', 
    'SI': 'Slovenia', 'SK': 'Slovakia', 'SL': 'Sierra Leone', 'SN': 'Senegal', 'SO': 'Somalia', 'SR': 'Suriname', 
    'SS': 'South Sudan', 'ST': 'Sao Tome and Principe', 'SV': 'El Salvador', 'SY': 'Syria', 'SZ': 'Eswatini', 
    'TD': 'Chad', 'TG': 'Togo', 'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 
    'TN': 'Tunisia', 'TO': 'Tonga', 'TR': 'Turkey', 'TT': 'Trinidad and Tobago', 'TV': 'Tuvalu', 'TW': 'Taiwan', 
    'TZ': 'Tanzania', 'UA': 'Ukraine', 'UG': 'Uganda', 'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 
    'VC': 'Saint Vincent and the Grenadines', 'VE': 'Venezuela', 'VN': 'Vietnam', 'VU': 'Vanuatu', 
    'WS': 'Samoa', 'YE': 'Yemen', 'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'
}

# Custom Styling (CSS) for premium aesthetics and global font consistency
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Font & Background */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #f8fafc !important;
    }

    /* Sidebar Styling - Clean and Minimal */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    /* Remove unnecessary top padding in sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1rem !important;
        gap: 0.5rem !important;
    }

    /* Logo Styling */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2rem;
        padding: 0.5rem;
    }
    .logo-icon {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        color: white;
        font-size: 1.5rem;
    }
    .logo-text {
        font-weight: 800;
        font-size: 1.1rem;
        line-height: 1.1;
        color: #1e293b;
        letter-spacing: -0.02em;
    }    /* Sidebar Section Headers */
    .section-header {
        font-size: 0.85rem !important; /* Increased font size */
        font-weight: 900 !important; /* Extra bold */
        text-transform: uppercase !important;
        letter-spacing: 0.14em !important; /* Improved spacing */
        color: #1e293b !important; /* Darker, more prominent color */
        margin: 2.5rem 0 1rem 0.6rem !important;
        padding-bottom: 8px;
        border-bottom: 2px solid #f1f5f9;
        font-family: 'Inter', sans-serif !important;
    }

    /* Navigation Item Styling (Radio buttons) */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        padding-top: 0.2rem !important;
        gap: 6px !important;
    }
    
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] > label {
        padding: 0.7rem 1rem !important;
        border-radius: 12px !important;
        background: transparent !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        border: 1px solid transparent !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        white-space: nowrap !important; /* Prevent text wrapping */
        min-width: 100% !important;
    }

    /* Hide the radio circles - More robust selectors */
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetLabel"] + div,
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-testid="stMarkdownContainer"] {
        margin-left: 0 !important;
    }

    /* Selected State */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] > label[data-selected="true"] {
        background-color: #f0fdf4 !important;
        color: #059669 !important;
        border: 1px solid #bdfbd7 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.1) !important;
    }

    /* Hover State */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] > label:hover:not([data-selected="true"]) {
        background-color: #10b981 !important; /* Solid emerald green background */
        color: #ffffff !important; /* White text for clarity on green background */
        transform: translateX(6px); /* Dynamic sliding transition */
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2) !important;
    }

    /* Global Widget Polish */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        background-color: #ffffff !important;
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    
    /* Multiselect spacing */
    div[data-testid="stMultiSelect"] {
        margin-bottom: 0.75rem !important;
    }

    /* Global Typography Enforcement - Optimized to skip icons */
    *, html, body, div, span, p, label {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Ensure Icons keep their glyph fonts */
    [data-testid="stIcon"], .material-icons, icon-font, i {
        font-family: inherit !important; /* Let Streamlit's default icon fonts take precedence */
    }
    /* KPI Card - Modern White Theme */
    .kpi-container {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        padding: 1.5rem !important;
        background-color: #ffffff !important;
        border-radius: 16px !important;
        border-top: 4px solid #10b981 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        margin-bottom: 1rem !important;
        gap: 1.5rem !important;
        width: 100% !important;
        min-height: 160px !important; /* Standardized height for all KPI cards */
        justify-content: flex-start !important;
    }
    .kpi-container:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Icon Container - Large & Recognizable Emojis or Images */
    .kpi-icon-container {
        min-width: 64px !important;
        height: 64px !important;
        background-color: #f0fdf4 !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 2.2rem !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
        overflow: hidden !important;
    }

    .kpi-icon-container img {
        width: 42px !important;
        height: 42px !important;
        object-fit: contain !important;
    }

    /* Content Area */
    .kpi-content {
        display: flex !important;
        flex-direction: column !important;
        text-align: left !important;
    }

    .kpi-label {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #64748b !important;
        margin-bottom: 4px !important;
    }

    .kpi-value {
        font-size: 2rem !important; /* Bold and big */
        font-weight: 900 !important;
        color: #0f172a !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    .kpi-insight {
        font-size: 0.7rem !important;
        color: #94a3b8 !important;
        margin-top: 6px !important;
    }

    .stPlotlyChart {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    stations_df = pd.read_csv("charging_station.csv")
    models_df = pd.read_csv("ev_models_updated.csv")
    stations_df['iso_alpha'] = stations_df['country_code'].map(iso_map)
    models_df['iso_alpha'] = models_df['origin_country'].map(iso_map)
    return stations_df, models_df

try:
    stations_df, models_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}"); st.stop()

# --- SIDEBAR NAVIGATION ---
# Syncing multiple radios for a flat navigation feel
if "active_page" not in st.session_state:
    st.session_state.active_page = "📊 Dashboard Overview"

with st.sidebar:
    # Stylized Logo
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">⚡</div>
            <div class="logo-text">EV INFRASTRUCTURE<br><span style="font-size: 0.8rem; font-weight: 500; color: #64748b;">Analytics suite</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section: Filters
    st.markdown('<div class="section-header">FILTERS</div>', unsafe_allow_html=True)
    all_countries = sorted(list(set(stations_df['country_code'].dropna().unique()) | set(models_df['origin_country'].dropna().unique())))
    selected_countries = st.multiselect("Countries", options=all_countries, format_func=lambda x: country_name_map.get(x, x), placeholder="All Countries", label_visibility="collapsed")
    all_models = sorted(models_df['model'].unique())
    selected_models = st.multiselect("Models", options=all_models, placeholder="All Models", label_visibility="collapsed")

    # Section: Visualization
    st.markdown('<div class="section-header">VISUALIZATION</div>', unsafe_allow_html=True)
    viz_options = [
        "📈 Market Trends", "🏆 Infrastructure Leaders", "🔗 Power Correlation", 
        "🔋 Power vs Ports", "🥧 Infrastructure Mix", "🏭 Manufacturing Hubs"
    ]
    
    # Section: Advanced Analytics
    separator = "ADVANCED ANALYTICS"
    adv_options = ["📊 Dashboard Overview", "🧩 MultiFacet Analytics", "🗺️ Geospatial Intelligence"]
    
    # Section: Sustainability
    sust_separator = "SUSTAINABILITY"
    sust_options = ["🍀 SDGs Alignment"]

    # Combine into one clean serial list
    all_options = viz_options + [separator] + adv_options + [sust_separator] + sust_options
    
    try:
        curr_idx = all_options.index(st.session_state.active_page)
    except:
        curr_idx = 7 # Default to Overview (which is index 7)

    # One radio is best for "serial form" - no absolute positioning hacks used anymore
    page = st.radio("Navigation", all_options, index=curr_idx, label_visibility="collapsed")
    
    # Selection Guard: If they click the separators, revert to previous page
    if page in [separator, sust_separator]:
        st.rerun() # Revert to the state-cached page
    else:
        st.session_state.active_page = page

    # Style the separators to look like real section headers
    st.markdown(f"""
        <style>
            /* TARGET THE SEPARATORS (ADVANCED ANALYTICS and SUSTAINABILITY) */
            div[role="radiogroup"] > label:nth-child(7), 
            div[role="radiogroup"] > label:nth-child(11) {{
                pointer-events: none !important;
                background-color: transparent !important;
                border: none !important;
                box-shadow: none !important;
                margin-top: 1.5rem !important;
                margin-bottom: 0.5rem !important;
                padding: 0.5rem 0.5rem !important;
                cursor: default !important;
            }}
            /* Completely hide the radio circles for the separators */
            div[role="radiogroup"] > label:nth-child(7) > div:first-child,
            div[role="radiogroup"] > label:nth-child(11) > div:first-child {{
                display: none !important;
            }}
            div[role="radiogroup"] > label:nth-child(7) div[data-testid="stMarkdownContainer"] p,
            div[role="radiogroup"] > label:nth-child(11) div[data-testid="stMarkdownContainer"] p {{
                font-size: 0.85rem !important; /* Matched to section-header */
                font-weight: 900 !important; /* Extra bold */
                color: #1e293b !important;
                letter-spacing: 0.14em !important;
                text-transform: uppercase !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        </style>
    """, unsafe_allow_html=True)


# --- DATA FILTERING LOGIC ---
filtered_stations = stations_df.copy()
filtered_models = models_df.copy()

if selected_countries:
    filtered_stations = filtered_stations[filtered_stations['country_code'].isin(selected_countries)]
    filtered_models = filtered_models[filtered_models['origin_country'].isin(selected_countries)]

if selected_models:
    filtered_models = filtered_models[filtered_models['model'].isin(selected_models)]

# Define common chart layout updates
def apply_layout(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin={"l": 40, "r": 30, "t": 60, "b": 40},
        font={"family": "Inter, sans-serif", "size": 11, "color": "#2c3e50"},
        title_font={"family": "Inter, sans-serif", "size": 16, "weight": "bold", "color": "#1e293b"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"family": "Inter, sans-serif", "color": "#475569"}},
    )
    # Explicitly force axis and colorbar colors to dark
    fig.update_xaxes(
        title_font={"family": "Inter, sans-serif", "color": "#64748b"},
        tickfont={"family": "Inter, sans-serif", "color": "#64748b"},
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0"
    )
    fig.update_yaxes(
        title_font={"family": "Inter, sans-serif", "color": "#64748b"},
        tickfont={"family": "Inter, sans-serif", "color": "#64748b"},
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0"
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            tickfont=dict(family="Inter, sans-serif", color="#64748b"),
            title_font=dict(family="Inter, sans-serif", color="#64748b")
        )
    )
    return fig


# --- SHARED UI COMPONENTS ---
def render_kpis():
    # Asset: Custom Battery Icon (Base64)
    FAST_CHARGING_ICON = "data:image/png;base64,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S77O9l3S/pXvep/fP69P9Xp/+vL7f+z+2p+fRv9P7Xq93v9/vSbe/35Nf/07f7/fS82i9v5vS+3Snu33p7i/6P9399X+u97/T//u+vtd7Py8v73Opef76f7fX6/+fP/67Pv2Z+nf6Xv/+vv9/+N/p7v/Zfk8vv8v7Xun+p7tfum/0Xve+n/9j3f/Zfk+vd/u56fS56PP67/Hn6S99P72eT88rvU9PH+n59f6+93vS8+t90v3Q++P/oX895D3kP+bfTf8f+n+u59Pv3efv+9S/n/v/6v/+D/nH+5/+Gfq99HvS8+jn9E/u7+GfTM9Bnz7pvu/fSzf9mX1/R/8Of6Zuz8PnPv0Z+vPoOf29/D38Pfxz6fdKn8fTM+p9/Of1vK87P0/P997vof8OfT/9fS/p75Nuz3tfz/s6/Xv6e/p76T6979O7X9vteU/6N/v7pfdrp59eXm7aL+/fSvffTf+fOf0v3X+l59Lnt+fS59Hz6fPr8+nz6/Poer/v7/X+rOdz7+H1un7Zfp/vP/Nz0v3S/fB8vffze59v7+f79e6/X/q+fr+9L30/fS/9f/X69PXeT/9dv6fen76H/jv9O/y5fC/9Gf7/+ndKn8Pfp/v5fu/T7u/+v9K/y+t9X3+X/9/+Pv376PdI97t/t/++9Prp3X/fT9OfY+fp/t/0eejn6X0/3X/88/R++rz0efS83vt59Xvpfvp+eu/n6Xfp7+rv/tNfIn+n+7/++P+97vIduu+7T7fHofR76D/mOfT8un7N99Pf6fep7/f376Tvx59Ln0vf6/6f/p96j776Pv2y7pLutO50f68L+R6lv9X+FvpL7e+hn6Wf7er76Xv9v/vz63npz6Hn0eeXp/v3qXm/9HPo5/L/7ffU59D90XOf+p/Xn/n/9+r76vup96XfS78/vS79ufy59Ofqz/A6ve8v1S9dP9N7pufVv6Pfv8/96f7T7366/s117//vfve8f4a+j+576b7Tz6P3Wve/07p+nf4O+Xf6Z/rn6Wf6/fT9XOn+ov+Xfof/fT873Z76Z+i/0f/v/vf7Tne6vff99fN77/9Yv9/+ff5vof+O/6b6PfV3+/9M75Gerv78/ln6mf7Tf9f9Z/7T77Y7v6u/9U9L5f/pX7o+p/s7Xd96un6eP8fPST+n3v06Tf/p5/XzPe3X83R6X+n/7f9Yf7e/Z9I60+ntTnf7/+e3u/2eXvfTP9fP90r3W7rb/0/9vPr199f/e9/+f++97v+h76PfU///fu/9Hz9Gv9vVz3T9/v8P/Rz/F93v99Xf999P98fX/Xv98/+t9z2v99/zPv0+SffX/ffpZ7n7mN736OfX+3vfZ09/p/+Gvofuez87Te/7/495Hv0Z/p/r//3p/p/6d3if1/8vnef10+v13p7f3+v/7v+bvp/+jOn+TvfvU/O5/Xz9/un+Zp9u30tPe+l9T+9O947Xn6mfoY+tP0OfV3/GZ6n5ffoz9GfqZ/tH/6v/h/6d/v74OfX7fKbfX7r/S+c5/e/9PvXn6P++H9Of9dmG0u17Xm+fR/dP7+u8PrfPe7XfR/d9fP6p/u7//B98H/2Zvp8+j//v/lvp/u/++z+2+zfT/e/59D6O/q8ZtP6G9v/Vf/u9+vN76L7nZ7v/Xv6Xf2x3e/X9evm56X36r/6/vTf9+/m56Xm9/v77PfR+Xp+vUvP5ve+v9X7/uT57pOfT/dP9P7330u8jz+vveP+8Xun36+fX+7W/p5fT76uX97L+9vYefP6Xf9f748f3u5f+kX9XL6c/W76uX36O9PfU9/R79vU7/PP0X3yffR+8n3y/fR+8v30/vX9fX/yffR+8f3xfve793v6Mfov/o9/T99P71fP9Z/8v3y/vI98X71u/Rz6mfo59XPq5+jn9Pfy5/Dn0O97//zP9PvUeW/pf9Pv9/v9/f9/f9vX+9RzzXPOe8v7yHvt/fD+8X7ve8S7ye/N68vvS6ufT6/N683vye/N68X+v55fzlZ7v9Gvlvz/fU+m3/v199n/9+/r/lX+5/9p++v/qv/mf7v/rf6f/u/+5/r/fT7+HP5TfS7/Wf+05/rv68/3G9n39Xv5++l/799Lz0S+/ne/r30/v5Xv5c+tfTX+Gfqz+X/vX0/fS8+mfoZ+vve3u9L/+c/t9/P6bve/8M/R76vfR76PfS783Pq38Of7v6+f3v6ef5Pf7v9/XPo//mO//9/P36ffpZ+rX9N/9uX+rfS79PX5+/lz6PPY6n/p3+mfpd9Lveq/9v/u6+l953P19PfyZ/Gfpf+7P9P99L7X9M/z68T+X6/f7u/p7+X76fvo5/m/eXvpe+v9+Ln0e/V78XvS7+Xvp/vT86X7tPPrPvef6Zfpz6Sffz6nfp9/z9D66z+5T57TPlvn62/V35Xfhd6Hfp76XvS//3/df6tf+XfpefH6/N78Pvt+Hfqd9p32vS/S/T/6/vU/un+nP1Z/j7/XP9Xv/fv5e+XP5e+XP48/lz6Wfp/+3P4e+R75X+97+/rZfs99H+mfqZ+jn+bP4s/m/6ffS/9Ofy59DP0e/77/j/6Zfo96Hf9/u/7u96T3XedC76bvpO+n76Xvp5+un6ePreeS+v55L69H9H9H3mZ+un6fPoZ+uz66frs+jn6HPoc+uz66Pqc+jP1efW88t9eT+rOen+nn6HPrc+uz66PqZ+mz66foc+uz6LPpc+hz6XPpc+hz6HPps+mz6bPo8+gz6HPps+nz6bPr5+vn6ePqc+lz6+fr5+nn6LPrc+ln6LPr5+nz6HPoc+vn6/Pqc+vP1efX88nzynX86m59Xnyu/K78bvxe9L78Xvy+9N70vPl+9R70vvXc+l55XnV+dH52Pnt+eXp5rnX+vX6+fV58nzx/vI+8f7mffI+8f7mfvIe8l7yXvpe+l76Ofp5+nn6eL97Sfp5+p96znhPdN50vvS88p9eX+pT6m9pL2lvaS9pb2kvaS9pb2kPaT9nP2U/Zz9nP2Y/Zz9nP2Y/Zz9nP7ZdtF2/8Y8P/OfM94z3XedP9P/V/3S/dH9N/9P90P9TP1M/Uf9Z/1P/Vf9V/5Z/ln+bP4s/lz+PP58/jn8c/j38XPy+fL58vnz+ffx9/L38efx5/Hn8O/V/9X/Vf9TfV/1Z9Vv9Z9X/V39Z/WP9r/Wf1X9Vf1n9Vf1X9V/9Z/1P9Nf5p/sz9mf6p+qz+vP6/+j+mP6p+rz6v6sv6TfpP+s/6T+qP6b/qf+q/ps+iz6HPps+mz6m/pz6u/p76s+qz6bPqs+iz6m/qr+qv6r/n/9b/mP6o/p/+s/rL+k/qj+rv6m/rL+lv6T+mP6Pfpd+j36ffpd9D36PfpZ+p30Pfwz9L/+v/rv/rv9uX+n/7f9T/dP9Mf0x/U/9Wf9p/Vn/Wf1Y/Wz9bf1v/W79bP1f9U/1N9Xf1X9Tf1v9Xf9n/ZP85/zn9M/2T/OP+c/p/+z/7P/k/zj/OP9c/1z/XP/sf+T/bP9uX7sv2f7s/2T/NP80/yT/OP9c/2T/JP8//v9+/X+9n+/fS/fBf8F/wn+C/3r/uv9a/17/Xv/tf+3/p/+v/r/+7/rv+y/pf+H/7f9V/9v/Zf87/Tf9T/86/0r/m7+7rqXuk+eD15Lfld6F7pnuv+6H7reut66Xrou+l76Pvo/+n+6P7qPuf+y77X/9uX+Xvpe+v96bnoee+p77Hvp9+T74vvl+vT99L30vfl96XfS99P30fvR/9H/0f/p/+n+6f7p/pj8mPyY/p/+j/mf6Y/pj6mPqf+p/6n+6P7p/uj+mP7f/t/+3/rf+t/2X9t/2/7L+l/7f9v/279H/0v/S79Lv0vfT99H30vfh99P30ffT99P30ffT99f70fvT86Xzpfuj57PXstex17TXuPe691nXWtdE10XXRd9D30PfS99H30vfR99H30/fS99Lr0mvTa6NroOuja6dro/ug66Hroeug66XroOun66froOur66froeul76fvp++l76fvp++l76fvpe+l66Xrp+un66Xrp+un66Xro+ul76fvpeun66Prpeun66LrpOun66Drpeul66frpeul66Prp+ul66TrpOur66frp+un66fvp++l76Xvpuun66vrp++l76fvp++h66Hrpeul66brpeuk66TroOul66Prp++l66Hvoeuh66Lrp+un66Xrp+uh66Hvoeul66Hrp+un66Xvp++j76fvk+uP7Y/qj+qP6p/qj+nP6Y/pj+mf6p/v/+f98P7xfu97wbvRe9L78XvT+9Lz0PPc89z33Pe887zzvXf9v/7f9Wv6f/O793v3f7/+3r6Hnn9efp53lneOd473nveO9473mvead493rvue95r3vveud877zvfS79Xvye/L78vvy+/L78vPy8/Lz8vPy8/Lz8vfy9/L78vvy+/L78rvyu/K78vvze/Pr5e+l76XPpden16PnldeR15XPk8+T35fvk++X75Pvk++X75fvj++P74/vj++L74vvje+P75Pvk++T74/vm+fb99j32Pfa99r32/fb99X30vfS89Pz0PPYy/Pr9ev18/Xz9fP18/Xz9vP18/bz9fP18/bz9vP58/nz+vP68/nz+fP58/nz+vP68/nz+XP5c+rz6vPq8+lz6vPr9ev18/Xz9XP18/Xz+fP58/lz6XPq8/Pr9PP18/nz+fP68+r06fXp9en06vTo9e71vPX89fP18PXp9ev18/Xz9vX09vX09vX29ff19PX09PX09PX09fP19PX39vf3+fT59Pn1efV69Xp9ev16fXr9en16fXp9fH18fXx9PH08vTz9fr0evV69Xr1evV69Xr1evV69Xr1evV69Xr1+vV69Xr1evV69Xr1evV29Xb1dvT29Xb19vX09vT29fb1dvV2/PZ85nzmfOZ85nzmfOZ85nznfPd873z3fO9873znfOd87zznPOe89zznPPe897z3vPe887z3fPe897z3vPe897z3vPe897z3vPe873zveS95L3kveS97L3sPe497nvue9753vfe997H3ve+973vve+973vfe973nveed573vve+dz3vfe9773vfe973vPe897z3vPe9773vfe973vve973vve973vfe973vve973vve973vve973vfe973vfe973vve973vve973vve973vve973vfe973vfe973vve973vve+973vve973vve973vve973vve973vve973vve973vve973vve973vve9/f////X4uwQSPtCBAAAAABJRU5ErkJggg=="
    # KPI COLORS (Emerald/Teal Palette)
    kpi_gradients = [
        "linear-gradient(135deg, #065f46 0%, #10b981 100%)",
        "linear-gradient(135deg, #059669 0%, #34d399 100%)",
        "linear-gradient(135deg, #0d9488 0%, #2dd4bf 100%)",
        "linear-gradient(135deg, #0f766e 0%, #5eead4 100%)"
    ]

    # 1. Charging Demand Pressure Index
    total_battery = filtered_models['battery_capacity_kWh'].sum()
    total_power = filtered_stations['power_kw'].sum()
    demand_pressure = (total_battery * 10000 / total_power) if total_power > 0 else 0
    
    # 2. Fast Charging Availability Score
    fast_stations_count = filtered_stations[filtered_stations['power_kw'] >= 50].shape[0]
    total_stations_count = len(filtered_stations)
    fast_charging_score = (fast_stations_count / total_stations_count * 100) if total_stations_count > 0 else 0
    
    # 3. Average Charging Time Compatibility
    avg_battery = filtered_models['battery_capacity_kWh'].mean() if not filtered_models.empty else 0
    avg_power = filtered_stations['power_kw'].mean() if not filtered_stations.empty else 0
    compatibility_score = avg_battery / avg_power if avg_power > 0 else 0
    
    # 4. Range Support Sufficiency Index
    avg_ev_range = 400 
    range_support_index = total_stations_count / avg_ev_range
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi_metrics = [
        ("🔋", "Charging Demand Pressure", f"{demand_pressure:.2f}"),
        ("⚡", "Fast Charging Availability", f"{fast_charging_score:.1f}%"),
        ("🤝", "Charging Compatibility", f"{compatibility_score:.2f}"),
        ("🌱", "Range Support Sufficiency", f"{range_support_index:.3f}")
    ]
    
    cols = [kpi1, kpi2, kpi3, kpi4]
    for i, (icon, label, value) in enumerate(kpi_metrics):
        with cols[i]:
            # Detect if icon is a data URI or emoji
            if icon.startswith("data:image"):
                icon_html = f'<img src="{icon}" alt="icon">'
            else:
                icon_html = icon
                
            st.markdown(f"""
                <div class="kpi-container">
                    <div class="kpi-icon-container">{icon_html}</div>
                    <div class="kpi-content">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# --- PAGE ROUTING ---


def display_dashboard():
    render_kpis()
    st.title("Electric Vehicle Infrastructure Overview")
    st.markdown("<br>", unsafe_allow_html=True)
    # ROW 1
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        if not filtered_models.empty:
            trend_data = filtered_models.groupby('first_year').size().reset_index(name='count')
            fig1 = px.line(trend_data, x='first_year', y='count', title="EV Market Entrance Trend", markers=True, line_shape='spline', color_discrete_sequence=['#10b981'])
            st.plotly_chart(apply_layout(fig1), use_container_width=True)
    with row1_col2:
        if not filtered_stations.empty:
            top_countries = filtered_stations['country_code'].value_counts().head(10).reset_index()
            top_countries.columns = ['Country', 'Stations Count']
            fig2 = px.bar(top_countries, x='Stations Count', y='Country', orientation='h', title="Top 10 Infrastructure Leaders", color='Stations Count', color_continuous_scale='Emrld')
            st.plotly_chart(apply_layout(fig2), use_container_width=True)
    with row1_col3:
        if not filtered_stations.empty:
            corr = filtered_stations[['ports', 'power_kw', 'latitude', 'longitude']].corr()
            fig3 = px.imshow(corr, text_auto=".2f", title="Port vs Power Correlation", color_continuous_scale='YlGn', aspect="auto")
            st.plotly_chart(apply_layout(fig3), use_container_width=True)

    # ROW 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        if not filtered_stations.empty:
            scatter_data = filtered_stations[filtered_stations['power_kw'] > 0].sample(min(len(filtered_stations), 5000))
            fig4 = px.scatter(scatter_data, x='ports', y='power_kw', color='power_class', log_y=True, title="Power Output vs Port Capacity", color_discrete_sequence=['#064e3b', '#065f46', '#059669', '#34d399', '#6ee7b7', '#a7f3d0'])
            st.plotly_chart(apply_layout(fig4), use_container_width=True)
    with row2_col2:
        if not filtered_stations.empty:
            power_dist = filtered_stations['power_class'].value_counts().reset_index()
            power_dist.columns = ['Power Class', 'Count']
            fig5 = px.pie(power_dist, values='Count', names='Power Class', title="Charging Infrastructure Mix", hole=0.5, color_discrete_sequence=['#d1fae5', '#a7f3d0', '#6ee7b7', '#34d399', '#10b981'])
            fig5.update_traces(textinfo='percent')
            st.plotly_chart(apply_layout(fig5), width="stretch")
    with row2_col3:
        if not filtered_models.empty:
            model_dist = filtered_models['origin_country'].value_counts().reset_index()
            model_dist.columns = ['Country', 'EV Models']
            model_dist = model_dist.sort_values('EV Models', ascending=False)
            left = model_dist.iloc[1::2]
            right = model_dist.iloc[0::2]
            model_dist = pd.concat([left.iloc[::-1], right]).reset_index(drop=True)
            fig6 = px.bar(model_dist, x='Country', y='EV Models', title="Manufacturing Hubs", color='EV Models', color_continuous_scale='Greens')
            fig6.update_layout(bargap=0.01)
            st.plotly_chart(apply_layout(fig6), use_container_width=True)

def display_specific_viz(selected_viz):
    render_kpis()
    st.title(selected_viz)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if selected_viz == "📈 Market Trends":
        if not filtered_models.empty:
            trend_data = filtered_models.groupby('first_year').size().reset_index(name='count')
            fig = px.line(trend_data, x='first_year', y='count', title="EV Market Entrance Trend (Detailed View)", markers=True, line_shape='spline', color_discrete_sequence=['#10b981'])
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)

    elif selected_viz == "🏆 Infrastructure Leaders":
        if not filtered_stations.empty:
            top_countries = filtered_stations['country_code'].value_counts().head(15).reset_index()
            top_countries.columns = ['Country', 'Stations Count']
            fig = px.bar(top_countries, x='Stations Count', y='Country', orientation='h', title="Top 15 Infrastructure Leaders", color='Stations Count', color_continuous_scale='Emrld', text_auto='.2s')
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)

    elif selected_viz == "🔗 Power Correlation":
        if not filtered_stations.empty:
            corr = filtered_stations[['ports', 'power_kw', 'latitude', 'longitude']].corr()
            fig = px.imshow(corr, text_auto=".2f", title="Expanded Port vs Power Correlation", color_continuous_scale='YlGn')
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)

    elif selected_viz == "🔋 Power vs Ports":
        if not filtered_stations.empty:
            scatter_data = filtered_stations[filtered_stations['power_kw'] > 0].sample(min(len(filtered_stations), 10000))
            fig = px.scatter(scatter_data, x='ports', y='power_kw', color='power_class', log_y=True, title="Power vs Ports Deep Dive", color_discrete_sequence=['#064e3b', '#065f46', '#059669', '#34d399', '#6ee7b7', '#a7f3d0'], size='ports', opacity=0.7)
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)

    elif selected_viz == "🥧 Infrastructure Mix":
        if not filtered_stations.empty:
            power_dist = filtered_stations['power_class'].value_counts().reset_index()
            power_dist.columns = ['Power Class', 'Count']
            fig = px.pie(power_dist, values='Count', names='Power Class', title="Charging Infrastructure Mix (Global Share)", hole=0.4, color_discrete_sequence=['#d1fae5', '#a7f3d0', '#6ee7b7', '#34d399', '#10b981'])
            fig.update_traces(textinfo='percent', pull=[0.1, 0, 0, 0, 0])
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)

    elif selected_viz == "🏭 Manufacturing Hubs":
        if not filtered_models.empty:
            model_dist = filtered_models['origin_country'].value_counts().reset_index()
            model_dist.columns = ['Country', 'EV Models']
            model_dist = model_dist.sort_values('EV Models', ascending=False)
            left = model_dist.iloc[1::2]
            right = model_dist.iloc[0::2]
            model_dist = pd.concat([left.iloc[::-1], right]).reset_index(drop=True)
            fig = px.bar(model_dist, x='Country', y='EV Models', title="Manufacturing Hubs (Inverse-U Profile)", color='EV Models', color_continuous_scale='Greens', text_auto=True)
            fig.update_layout(bargap=0.01)
            st.plotly_chart(apply_layout(fig, height=600), use_container_width=True)


def display_multifacet():
    render_kpis()
    st.title("MultiFacet Analytics")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not filtered_stations.empty:
        # Exclude UNKNOWN and AC_L2 as requested for cleaner focus
        excluded = ['UNKNOWN', 'AC_L2_(7.5-21kW)']
        facet_stations = filtered_stations[~filtered_stations['power_class'].isin(excluded)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            dist_data = facet_stations.groupby(['power_class', 'is_fast_dc'])['ports'].sum().reset_index(name='Total Ports')
            dist_data = dist_data.sort_values('Total Ports', ascending=False)
            
            fig1 = px.bar(dist_data, x="power_class", y="Total Ports", color="is_fast_dc", 
                         title="Infrastructure Capacity (Ports)",
                         labels={'power_class': 'Power Category', 'Total Ports': 'Total Ports', 'is_fast_dc': 'Fast DC'},
                         color_discrete_map={True: "#059669", False: "#a7f3d0"}, 
                         opacity=0.9, barmode="group", text_auto='.2s')
            
            # Explicitly manage margin for alignment
            fig1.update_layout(margin={"l": 60, "r": 20, "t": 60, "b": 80}, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
            st.plotly_chart(apply_layout(fig1, height=600), width="stretch")
            
        with col2:
            top_countries = facet_stations['country_code'].value_counts().nlargest(10).index
            region_data = facet_stations[facet_stations['country_code'].isin(top_countries)]
            region_data = region_data.groupby(['country_code', 'power_class']).size().reset_index(name='Stations')
            
            fig2 = px.bar(region_data, x="country_code", y="Stations", color="power_class", 
                         title="Regional Intensity (Top 10 Countries)",
                         labels={'country_code': 'Country', 'Stations': 'Station Count', 'power_class': 'Power Category'},
                         color_discrete_sequence=['#064e3b', '#059669', '#34d399', '#6ee7b7', '#a7f3d0'], 
                         opacity=0.9, barmode="stack", text_auto='.2s')
            
            fig2.update_layout(margin={"l": 60, "r": 20, "t": 60, "b": 80}, showlegend=True)
            st.plotly_chart(apply_layout(fig2, height=600), width="stretch")
            
    

# --- GEOSPATIAL PAGE ---

def display_geospatial():
    render_kpis()
    st.title("Geospatial Intelligence")
    
    map_types = [
        "Infrastructure Density (Choropleth)",
        "EV Model Origins (Choropleth)",
        "Market Evolution (Animated Growth)"
    ]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_map = st.selectbox("Select Map Perspective", map_types)
    st.markdown("<br>", unsafe_allow_html=True)

    if selected_map == "Infrastructure Density (Choropleth)":
        if not filtered_stations.empty:
            density_data = filtered_stations.groupby('iso_alpha').size().reset_index(name='Count')
            fig = px.choropleth(density_data, locations="iso_alpha", color="Count",
                                hover_name="iso_alpha", color_continuous_scale="Greens",
                                title="Global Charging Infrastructure Density")
            st.plotly_chart(apply_layout(fig, height=800), width="stretch")
        else:
            st.info("No data for Density Map.")

    elif selected_map == "EV Model Origins (Choropleth)":
        if not filtered_models.empty:
            model_counts = filtered_models.groupby('iso_alpha').size().reset_index(name='Model Count')
            fig = px.choropleth(model_counts, locations="iso_alpha", color="Model Count",
                                hover_name="iso_alpha", color_continuous_scale="Greens",
                                title="Global EV Manufacturing Hubs (Model Diversity)")
            st.plotly_chart(apply_layout(fig, height=800), width="stretch")
        else:
            st.info("No model data for origins map.")

    elif selected_map == "Market Evolution (Animated Growth)":
        if not filtered_models.empty:
            # Create cumulative counts over years for animation
            years = sorted(filtered_models['first_year'].unique())
            anim_data = []
            for year in years:
                snap = filtered_models[filtered_models['first_year'] <= year].groupby('iso_alpha').size().reset_index(name='Models')
                snap['Year'] = year
                anim_data.append(snap)
            
            full_anim_df = pd.concat(anim_data)
            fig = px.choropleth(full_anim_df, locations="iso_alpha", color="Models",
                                animation_frame="Year", range_color=[0, full_anim_df['Models'].max()],
                                color_continuous_scale="Greens", title="Global EV Market Expansion (Yearly Cumulative)")
            st.plotly_chart(apply_layout(fig, height=800), width="stretch")
        else:
            st.info("No temporal data available for animation.")

# Page Logic
def display_sdgs():
    st.title("SDGs Alignment")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SDG CARDS ROW
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background-color: #f0fdf4; padding: 2rem; border-radius: 16px; border-left: 6px solid #059669; margin-bottom: 2rem; min-height: 220px;">
                <h3 style="color: #064e3b; margin-top: 0;">Goal 7: Affordable and Clean Energy</h3>
                <p style="color: #065f46; font-size: 1.1rem; line-height: 1.6;">EV infrastructure accelerates the adoption of renewable energy by serving as flexible load and providing energy storage capabilities.</p>
                <div style="background: #ffffff; color: #059669; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; font-weight: 700;">Renewable Integration</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style="background-color: #f0f9ff; padding: 2rem; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 2rem; min-height: 220px;">
                <h3 style="color: #0c4a6e; margin-top: 0;">Goal 13: Climate Action</h3>
                <p style="color: #0c4a6e; font-size: 1.1rem; line-height: 1.6;">Every charging station deployed directly contributes to the global reduction of carbon footprints by transitioning away from internal combustion.</p>
                <div style="background: #ffffff; color: #0284c7; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; font-weight: 700;">Carbon Reduction</div>
            </div>
        """, unsafe_allow_html=True)

    # --- NEW: INTERACTIVE "WHAT-IF" SIMULATOR ---
    st.markdown("<hr style='border: 0; border-top: 2px solid #f1f5f9; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #1e293b; font-size: 1.8rem; margin-bottom: 0.5rem;'>📈 Interactive Impact Simulation</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 1.5rem;'>Simulate the environmental impact of adding more charging stations to the current network.</p>", unsafe_allow_html=True)
    
    extra_st = st.slider("Simulate Network Expansion (Additional Stations)", 0, 50000, 0, step=500, help="Visualize how expanding the infrastructure increases carbon offset.")

    # Live Calculations with Simulation
    total_st = len(filtered_stations)
    impact_st = total_st + extra_st
    
    # CO2 calculation: ~2.84 tonnes per station per year
    co2_tonnes = (impact_st * 2840) / 1000
    
    fast_st = filtered_stations[filtered_stations['power_kw'] >= 50].shape[0] if not filtered_stations.empty else 0
    # For simulation, we assume additional stations follow the same fast-charging ratio
    grid_readiness_idx = (fast_st / total_st * 100) if total_st > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    
    # LIVE IMPACT CARDS (Symmetric Sizing)
    imp1, imp2 = st.columns(2)
    
    card_style = "display: flex; flex-direction: column; justify-content: space-between; padding: 2.5rem; border-radius: 24px; color: white; min-height: 320px;"
    
    with imp1:
        st.markdown(f"""
            <div style="{card_style} background: linear-gradient(135deg, #065f46 0%, #10b981 100%); box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.3);">
                <div>
                    <div style="font-size: 0.9rem; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.05em;">Estimated Annual CO2 Saved</div>
                    <div style="font-size: 3.5rem; font-weight: 800; margin: 0.5rem 0;">{co2_tonnes:,.0f} <span style="font-size: 1.5rem; font-weight: 500;">Tonnes</span></div>
                </div>
                <p style="margin: 0; font-size: 1.1rem; line-height: 1.5; opacity: 0.9;">Equivalent to planting <b>{co2_tonnes * 45:,.0f} trees</b> per year based on {impact_st:,} total stations.</p>
            </div>
        """, unsafe_allow_html=True)

    with imp2:
        st.markdown(f"""
            <div style="{card_style} background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%); box-shadow: 0 10px 25px -5px rgba(3, 105, 161, 0.3);">
                <div>
                    <div style="font-size: 0.9rem; font-weight: 600; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.05em;">Smart Grid Readiness Index</div>
                    <div style="font-size: 3.5rem; font-weight: 800; margin: 0.5rem 0;">{grid_readiness_idx:.1f}%</div>
                    <div style="width: 100%; height: 12px; background: rgba(255,255,255,0.2); border-radius: 6px; overflow: hidden; margin: 1rem 0;">
                        <div style="width: {grid_readiness_idx}%; height: 100%; background: #6ee7b7; border-radius: 6px;"></div>
                    </div>
                </div>
                <p style="margin: 0; font-size: 1rem; opacity: 0.85;">Percentage of infrastructure supporting DC Fast Charging (>50kW) in the selected data.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- TOP COUNTRY SUFFICIENCY TRACKER ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #1e293b; font-size: 1.6rem;'>🏆 Infrastructure Sufficiency Tracker</h2>", unsafe_allow_html=True)
    
    if not filtered_stations.empty:
        country_data = filtered_stations.groupby('country_code').size().reset_index(name='Stations')
        # Target Suficiency Score: benchmarked against 1 station per 20km for Top countries
        # Simple visualization of capacity relative to the most dense region in selection
        max_stations = country_data['Stations'].max()
        top_5 = country_data.nlargest(5, 'Stations')
        
        for idx, row in top_5.iterrows():
            c_name = country_name_map.get(row['country_code'], row['country_code'])
            perc = (row['Stations'] / max_stations * 100)
            st.markdown(f"""
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-weight: 600; color: #334155;">
                        <span>{c_name}</span>
                        <span>{row['Stations']:,} Stations</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: #f1f5f9; border-radius: 4px;">
                        <div style="width: {perc}%; height: 100%; background: #10b981; border-radius: 4px;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><p style='color: #94a3b8; font-size: 0.85rem; text-align: center; font-style: italic;'>*Impact calculations based on global average benchmarks for EV infrastructure carbon displacement.*</p>", unsafe_allow_html=True)

# Page Logic Routing
if st.session_state.active_page == "📊 Dashboard Overview":
    display_dashboard()
elif st.session_state.active_page == "🧩 MultiFacet Analytics":
    display_multifacet()
elif st.session_state.active_page == "🗺️ Geospatial Intelligence":
    display_geospatial()
elif st.session_state.active_page == "🍀 SDGs Alignment":
    display_sdgs()
else:
    # This handles the 6 specific visualization pages
    display_specific_viz(st.session_state.active_page)


st.markdown("---")
st.caption("Professional EV Dashboard | Advanced Analytics Suite | Data Source: Internal CSVs")

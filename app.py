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
    initial_sidebar_state="expanded"
)

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

# Custom Styling (CSS) for extreme professionalism and readability
st.markdown("""
<style>
    /* Main Background - Soft Gradient */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #212529;
    }
    
    /* Global Text Contrast */
    h1, h2, h3, p, span, label, div {
        color: #2c3e50 !important;
    }

    /* Global Widget Fix - Selectboxes and Multi-selects everywhere */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Ensure the text inside the select input is black */
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }

    /* Multi-select Tags */
    span[data-baseweb="tag"] {
        background-color: #f1f3f5 !important;
        color: #000000 !important;
    }
    
    /* Sidebar Section - Forced White Background & Reduced Padding */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    /* Minimize Sidebar Top Padding */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 2rem !important;
        background-color: #ffffff !important;
    }
    
    /* Center Logo and remove extra gap */
    .stImage > div > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Tighten Sidebar Header Spacing */
    [data-testid="stSidebar"] h2 {
        margin-top: 0rem !important;
        margin-bottom: 0.5rem !important;
        padding-top: 0rem !important;
    }
    
    /* Change all text and icons in sidebar to black */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] svg {
        color: #000000 !important;
        fill: #000000 !important;
    }
    
    /* Global Dropdown/Popover Fix (Portaled elements) */
    div[data-baseweb="popover"], 
    div[role="listbox"], 
    ul[role="listbox"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Ensure all items in the dropdown are white with black text */
    div[role="option"], 
    li[role="option"],
    div[role="option"] *,
    li[role="option"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Hover state for dropdown items */
    div[role="option"]:hover, 
    li[role="option"]:hover {
        background-color: #f1f3f5 !important;
    }

    /* Target the 'Select all' and search box inside the popover */
    div[data-baseweb="popover"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Ensure scrollbar in dropdown is visible/styled if needed */
    div[data-baseweb="popover"] ::-webkit-scrollbar {
        width: 8px;
    }
    div[data-baseweb="popover"] ::-webkit-scrollbar-thumb {
        background: #ced4da;
        border-radius: 10px;
    }

    /* KPI Box Styling - Premium Cards */
    .kpi-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        border-radius: 12px;
        color: white;
        font-family: 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .kpi-container:hover {
        transform: translateY(-5px);
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .kpi-insight {
        font-size: 0.7rem;
        font-weight: 400;
        opacity: 0.9;
        line-height: 1.2;
    }
    
    /* Chart Container - Card Look */
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #edf2f7;
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
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR NAVIGATION & FILTERS ---
with st.sidebar:
    # Logo and Branding - Centered via CSS (above)
    st.image("logo.png", width=120)
    
    # Header after Logo
    st.header("Filters")
    
    # Country Filter
    all_countries = sorted(list(set(stations_df['country_code'].dropna().unique()) | set(models_df['origin_country'].dropna().unique())))
    selected_countries = st.multiselect(
        "Select Countries", 
        options=all_countries, 
        format_func=lambda x: country_name_map.get(x, x),
        placeholder="All Countries"
    )

    # EV Model Filter
    all_models = sorted(models_df['model'].unique())
    selected_models = st.multiselect("Select EV Models", options=all_models, placeholder="All Models")

    # Spaced Separator
    st.markdown('<hr style="margin: 20px 0 10px 0; border: none; border-top: 1px solid #f0f2f6;">', unsafe_allow_html=True)
    
    st.header("Advanced Visualizations")
    page = st.radio("Go to", ["Dashboard", "MultiFacet", "Geospatial"])

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
        font={"family": "Segoe UI, sans-serif", "size": 11, "color": "#2c3e50"},
        title_font={"size": 16, "color": "#2c3e50"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": "#2c3e50"}},
    )
    # Explicitly force axis and colorbar colors to dark
    fig.update_xaxes(
        title_font={"color": "#2c3e50"},
        tickfont={"color": "#2c3e50"},
        gridcolor="#f0f0f0",
        linecolor="#2c3e50"
    )
    fig.update_yaxes(
        title_font={"color": "#2c3e50"},
        tickfont={"color": "#2c3e50"},
        gridcolor="#f0f0f0",
        linecolor="#2c3e50"
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            tickfont=dict(color="#2c3e50"),
            title_font=dict(color="#2c3e50")
        )
    )
    return fig

# --- PAGE ROUTING ---

def display_dashboard():
    st.title("Electric Vehicle Charging Infrastructure Analytics Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)

    # KPI COLORS (Emerald/Teal Palette)
    kpi_gradients = [
        "linear-gradient(135deg, #065f46 0%, #10b981 100%)",
        "linear-gradient(135deg, #059669 0%, #34d399 100%)",
        "linear-gradient(135deg, #0d9488 0%, #2dd4bf 100%)",
        "linear-gradient(135deg, #0f766e 0%, #5eead4 100%)"
    ]

    # --- KPI CALCULATIONS ---
    # 1. Charging Demand Pressure Index (Scaled by 10,000 for visibility)
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
    avg_ev_range = 400 # Placeholder as it's not in the dataset
    range_support_index = total_stations_count / avg_ev_range
    
    # KPI ROW
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="kpi-container" style="background: {kpi_gradients[0]};"><div class="kpi-label">Charging Demand Pressure</div><div class="kpi-value">{demand_pressure:.2f}</div><div class="kpi-insight">(Tot Capacity * 10k) / Tot Power</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="kpi-container" style="background: {kpi_gradients[1]};"><div class="kpi-label">Fast Charging Availability</div><div class="kpi-value">{fast_charging_score:.1f}%</div><div class="kpi-insight">Stations > 50kW / Total Stations</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="kpi-container" style="background: {kpi_gradients[2]};"><div class="kpi-label">Charging Compatibility</div><div class="kpi-value">{compatibility_score:.2f}</div><div class="kpi-insight">Avg Capacity (kWh) / Avg Power (kW)</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="kpi-container" style="background: {kpi_gradients[3]};"><div class="kpi-label">Range Support Sufficiency</div><div class="kpi-value">{range_support_index:.3f}</div><div class="kpi-insight">Stations / Avg Range (400km)</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ROW 1
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        if not filtered_models.empty:
            trend_data = filtered_models.groupby('first_year').size().reset_index(name='count')
            fig1 = px.line(trend_data, x='first_year', y='count', title="EV Market Entrance Trend", markers=True, line_shape='spline', color_discrete_sequence=['#10b981'])
            st.plotly_chart(apply_layout(fig1), width="stretch")
    with row1_col2:
        if not filtered_stations.empty:
            top_countries = filtered_stations['country_code'].value_counts().head(10).reset_index()
            top_countries.columns = ['Country', 'Stations Count']
            fig2 = px.bar(top_countries, x='Stations Count', y='Country', orientation='h', title="Top 10 Infrastructure Leaders", color='Stations Count', color_continuous_scale='Emrld')
            st.plotly_chart(apply_layout(fig2), width="stretch")
    with row1_col3:
        if not filtered_stations.empty:
            corr = filtered_stations[['ports', 'power_kw', 'latitude', 'longitude']].corr()
            fig3 = px.imshow(corr, text_auto=".2f", title="Port vs Power Correlation", color_continuous_scale='YlGn', aspect="auto")
            st.plotly_chart(apply_layout(fig3), width="stretch")

    # ROW 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        if not filtered_stations.empty:
            scatter_data = filtered_stations[filtered_stations['power_kw'] > 0].sample(min(len(filtered_stations), 5000))
            fig4 = px.scatter(scatter_data, x='ports', y='power_kw', color='power_class', log_y=True, title="Power Output vs Port Capacity", color_discrete_sequence=['#064e3b', '#065f46', '#059669', '#34d399', '#6ee7b7', '#a7f3d0'])
            st.plotly_chart(apply_layout(fig4), width="stretch")
    with row2_col2:
        if not filtered_stations.empty:
            power_dist = filtered_stations['power_class'].value_counts().reset_index()
            power_dist.columns = ['Power Class', 'Count']
            fig5 = px.pie(power_dist, values='Count', names='Power Class', title="Charging Infrastructure Mix", hole=0.5, color_discrete_sequence=['#d1fae5', '#a7f3d0', '#6ee7b7', '#34d399', '#10b981'])
            fig5.update_traces(textinfo='none')
            st.plotly_chart(apply_layout(fig5), width="stretch")
    with row2_col3:
        if not filtered_models.empty:
            model_dist = filtered_models['origin_country'].value_counts().reset_index()
            model_dist.columns = ['Country', 'EV Models']
            fig6 = px.bar(model_dist, x='Country', y='EV Models', title="Manufacturing Hubs", color='EV Models', color_continuous_scale='Greens')
            st.plotly_chart(apply_layout(fig6), width="stretch")

def display_multifacet():
    st.title("MultiFacet Analytics")
    st.subheader("Critical Infrastructure Insights")
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
    st.title("Geospatial Intelligence")
    st.subheader("Global Distribution & Infrastructure Reach")
    
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
if page == "Dashboard":
    display_dashboard()
elif page == "MultiFacet":
    display_multifacet()
elif page == "Geospatial":
    display_geospatial()

st.markdown("---")
st.caption("Professional EV Dashboard | Advanced Analytics Suite | Data Source: Internal CSVs")

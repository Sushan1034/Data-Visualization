#  EV & Charging Infrastructure Analytics Dashboard

A professional-grade, high-performance analytics suite designed to visualize global electric vehicle (EV) trends and charging infrastructure development. Built with **Streamlit**, **Plotly**, and **Pandas**, this dashboard provides actionable insights into market growth, regional capacity, and charging compatibility.

---

##  Features

###  1. Core Analytics Dashboard
*   **Dynamic KPIs**: Real-time calculation of metrics including:
    *   **Charging Demand Pressure**: Battery capacity vs. total available power.
    *   **Fast Charging Availability**: Percentage of high-power stations (>50kW).
    *   **Charging Compatibility**: Average battery size vs. average station power.
    *   **Range Support Sufficiency**: Station density relative to average EV range.
*   **6-Chart Insight Grid**:
    *   Market Entrance Trends (Line)
    *   Infrastructure Leadership (Horizontal Bar)
    *   Port/Power Correlation (Heatmap)
    *   Power vs. Port Scatter Analysis
    *   Infrastructure Mix (Donut)
    *   Global Manufacturing Hubs (Bar)

###  2. MultiFacet Deep-Dive
*   **Infrastructure Capacity**: Comparison of port distribution across power categories.
*   **Regional Intensity**: Stacked analysis of the top 10 infrastructure-leading countries.

###  3. Geospatial Intelligence
*   **Infrastructure Density**: Interactive choropleth map showing global station counts.
*   **Manufacturing Origins**: Global mapping of EV model diversity by country.
*   **Animated Market Evolution**: Time-lapse visualization of global EV market expansion.

---

##  Tech Stack & Requirements

*   **Language**: Python 3.8+
*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
*   **Visualization**: [Plotly Express & Graph Objects](https://plotly.com/python/)

---

##  Installation & Setup

1.  **Clone the Repository** (assuming authentication is configured):
    ```bash
    git clone https://github.com/Sushan1034/Data-Visualization.git
    cd Data-Visualization/dashboard
    ```

2.  **Install Dependencies**:
    Ensure you have Python installed, then run:
    ```bash
    py -m pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    py -m streamlit run app.py
    ```

---

##  Project Structure

```text
dashboard/
├── app.py                # Main Streamlit application logic
├── charging_station.csv   # Global infrastructure dataset
├── ev_models_updated.csv  # Electric vehicle specification dataset
├── logo.png               # Sidebar branding asset
└── README.md              # Project documentation
```

---

##  Aesthetic Design
The dashboard uses a **Clean & Sustainable** theme:
*   **Color Palette**: Professional Emerald and Teal gradients.
*   **UI/UX**: Minimalist card-based layout with glassmorphism effects.
*   **Responsiveness**: Fully responsive sidebar navigation and auto-scaling visualizations.

---
*Created for the Data Visualization project suite.*

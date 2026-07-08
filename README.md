# Google Play Store Insights & Visualisation Dashboard 🛍️

A modern, interactive Streamlit web dashboard built to analyze and visualize the Google Play Store apps dataset. This project productionizes the **Google Play Store Case Study** Jupyter notebook, converting static analyses into a high-fidelity, fully interactive web application with theme-adaptive glassmorphic styles.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15+-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://datavisualization-frs4effsednb6rhs6nstzk.streamlit.app/)

**🌐 Deployed Live App:** [https://datavisualization-frs4effsednb6rhs6nstzk.streamlit.app/](https://datavisualization-frs4effsednb6rhs6nstzk.streamlit.app/)

---

## 🌟 Dashboard Features

This web app contains **6 dedicated analysis tabs** mapped to the original case study modules:

1. **📊 App Overview & KPI Dashboard**
   - High-level metric KPI cards showing Total Apps, Average Rating, Total Installs, Average Price, and Free App share ratio.
   - A search-by-name interactive data table allowing deep searches through the dataset.
2. **🧹 Interactive Data Cleaning Pipeline**
   - Step-by-step audit showing exactly how the raw data of **10,841 apps** gets converted and capped down to **8,878 clean apps**.
   - An interactive waterfall chart showing row count drops across cleaning steps.
3. **📈 Univariate Analysis**
   - Distribute and examine single attributes like Rating (histogram with adjustable bins), Reviews, Sizes, and Content Rating proportions (toggleable between pie and bar charts).
4. **🔗 Bivariate Analysis**
   - **Size vs. Rating**: Multi-dimensional scatter plot featuring marginal histograms and box plots.
   - **Price vs. Rating**: Regression analysis for Paid Apps (fitted with OLS trend lines).
   - **Spread Distribution**: Rating spread comparisons across Content Ratings and the **Top 4 Popular Genres** (Tools, Entertainment, Medical, Education).
5. **🗺️ Multivariate Heatmaps**
   - Pivot-table heatmaps representing Rating vs. Size Buckets or Review Count Buckets.
   - Live configurations to toggle the aggregation function (Median, Mean, Min, 20th percentile) and color themes.
6. **📅 Temporal & Proportional Trends**
   - Line chart monitoring Average Rating changes by release months.
   - Stacked bar charts depicting monthly installs bifurcation (toggleable between absolute counts and percentages).

---

## 🧹 The Data Cleaning Pipeline

The application implements the exact cleaning parameters from the case study:
1. **Null Values**: Rows with null `Rating` values are removed. Shifted cells (like row `10472`) are dropped.
2. **Imputation**: Missing `Android Ver` and `Current Ver` are replaced with their respective modes.
3. **Datatypes**: Cleans `Price` (strips `$`, parses floats), `Installs` (converts strings to integers), and `Reviews` (converts to `int32`).
4. **Sanity Checks**: Restricts data where `Reviews <= Installs`.
5. **Outlier Filtering**:
   - `Price` capped at **$30**
   - `Reviews` capped at **1,000,000**
   - `Installs` capped at **100,000,000**
6. **Content Rating**: Filters out rare target labels ("Adults only 18+" and "Unrated").

---

## 🎨 Theme-Adaptive Glassmorphism UI

Designed with modern styling conventions:
- **Automatic Dark/Light Mode Support**: Card containers, backgrounds, borders, and text labels adapt seamlessly to your active Streamlit theme using native CSS variables.
- **Modern Typography**: Injects Google Font `Outfit` for a premium, clean visual layout.
- **Micro-Animations**: Hover animations on visual elements and KPI cards.

---

## 🚀 Setup & Execution

### Prerequisites
Make sure you have **Python 3.9+** installed on your machine.

### Installation & Run Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mrgraciz123/Data_Visualization.git
   cd Data_Visualization
   ```

2. **Install requirements**:
   Install the required libraries listed in [requirements.txt](requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## 📁 Repository Structure

```
├── .gitignore                                      # Ignored file configurations
├── README.md                                       # Project documentation
├── requirements.txt                                # Python package list
├── app.py                                          # Main Streamlit dashboard script
├── googleplaystore_v2.csv                          # Dataset source csv
└── Data Visualisation in Python - Case Study...    # Jupyter notebook
```

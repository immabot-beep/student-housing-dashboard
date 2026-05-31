[README.md](https://github.com/user-attachments/files/28432622/README.md)
# 🏘️ Student Housing Market Research & Pricing Dashboard

An interactive Python dashboard for analysing supply-demand dynamics, affordability,
and investment attractiveness across major US student housing markets.

Built as a portfolio project to demonstrate data analysis and real estate research
skills relevant to **real estate investment and data analytics roles**.

---

## 📌 Project Background

Student housing is one of the most resilient segments of US real estate.
Enrollment-driven demand, predictable lease cycles, and proximity-to-campus
premiums make university markets attractive targets for institutional and
private investors alike.

This project simulates the kind of market research an analyst might perform
when building a target-city pipeline:

- Screen markets by supply-demand tightness
- Assess rental growth momentum
- Proxy investment attractiveness with a simple composite score
- Surface insights through an interactive dashboard

---

## 💼 Why This Is Relevant to Real Estate Investment Analysis

| Analyst Task | How This Project Covers It |
|---|---|
| Building a property/market database | `data/student_housing_market.csv` with 10 core KPIs per city |
| Supply-demand analysis | Demand-Supply Ratio calculation in `src/analysis.py` |
| Pricing & affordability research | Affordability Ratio (rent burden) metric |
| Investment screening | Composite Investment Attractiveness Score |
| Stakeholder-facing reporting | Streamlit dashboard with interactive charts |
| Python / data tools proficiency | pandas, plotly, streamlit pipeline |

---

## 📁 Project Structure

```
student_housing_dashboard/
│
├── app.py                        # Streamlit dashboard (main entry point)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── data/
│   └── student_housing_market.csv   # Sample dataset (10 US university cities)
│
└── src/
    ├── __init__.py               # Makes src a Python package
    └── analysis.py              # Data loading, cleaning & metric calculations
```

---

## 📊 Data Dictionary

| Column | Type | Description |
|---|---|---|
| `city` | string | City name |
| `state` | string | Two-letter US state code |
| `major_university` | string | Primary university driving student demand |
| `student_population` | integer | Total enrolled students |
| `estimated_student_housing_beds` | integer | Estimated off-campus rental beds available |
| `average_monthly_rent` | float | Average monthly rent for a student unit ($) |
| `occupancy_rate` | float | Market occupancy rate (0–1 decimal) |
| `annual_rent_growth` | float | Year-over-year rent growth (0–1 decimal) |
| `median_household_income` | float | Median household income in the city ($) |
| `average_property_price` | float | Average residential property price ($) |
| `distance_to_campus_miles` | float | Avg distance of rentals from main campus (miles) |

> ⚠️ Data is illustrative and for portfolio/educational purposes only.

---

## 🔢 Methodology

### 1. Demand-Supply Ratio
```
demand_supply_ratio = student_population / estimated_student_housing_beds
```
- A ratio **above 1.0** indicates more students than available beds — a supply-constrained market that favours landlords and investors.

### 2. Affordability Ratio
```
affordability_ratio = (average_monthly_rent × 12) / median_household_income
```
- Measures the share of annual income a household spends on rent.
- Higher ratios indicate less affordability for renters; used alongside occupancy to gauge demand durability.

### 3. Investment Attractiveness Score (0–100)
A composite score built from four equally weighted sub-components, each min-max normalised to a 0–1 scale:

| Sub-Score | Proxy For |
|---|---|
| Annual rent growth | Rental pricing power & market momentum |
| Occupancy rate | Vacancy risk |
| Demand-supply ratio | Supply constraint / undersupply |
| Gross yield proxy (annual rent ÷ property price) | Return on capital |

```
investment_score = mean(score_rent_growth, score_occupancy,
                        score_demand_supply, score_yield) × 100
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Step 1 — Clone or download the project
```bash
git clone https://github.com/YOUR_USERNAME/student-housing-dashboard.git
cd student-housing-dashboard
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Launch the dashboard
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

### Step 4 — Explore
- Use the **sidebar** to select a city
- Review the **KPI cards** for that market
- Explore the three **interactive charts**
- Scroll down for the **full rankings table**
- Open the **Methodology** expander for metric definitions

---

## 💡 Sample Insights

Based on the illustrative dataset:

- **Boulder, CO** ranks highly due to extremely tight supply (0.98 occupancy),
  strong rent growth (9.2%), and the highest demand-supply ratio — driven by
  University of Colorado's large enrollment relative to available beds.

- **Tempe, AZ** (Arizona State) offers the largest absolute student population
  (77,000) in the dataset, creating deep, durable rental demand even as
  absolute rents remain moderate — an attractive volume-play market.

- **Tuscaloosa, AL** scores lowest primarily because of slower rent growth
  (4.8%) and lower gross yields relative to peers, though low entry prices
  could still appeal to value-focused investors.

- Markets like **Austin, TX** and **Durham, NC** combine high rent growth with
  strong occupancy, reflecting tech-economy spillover demand layered on top
  of student housing fundamentals.

---

## 🛠️ Potential Extensions

- Pull live rental data from Zillow Research or CoStar APIs
- Add a cap rate / NOI estimator for individual properties
- Build a time-series view of rent growth trends
- Integrate census data for deeper demographic analysis
- Add a portfolio optimiser (e.g., allocate capital across top-ranked markets)

---

## 👤 Author

Built by Brian as a portfolio project for real estate investment and
data analytics 

- LinkedIn: https://www.linkedin.com/in/brianztp

---

## 📄 License

MIT License — free to use, modify, and share.

# Were the Warning Signs Visible? Evidence from Kenya's Debt Sustainability Indicators (1980–2024)

Kenya's public debt has come under increasing scrutiny following a sharp rise in debt service
costs, a depreciating shilling, and the signing of a new IMF programme in 2024. These pressures
did not emerge suddenly. They developed over years, shaped by a structural shift toward commercial
borrowing from 2014 onward, compounded by external shocks including COVID-19 and the Russia-Ukraine
war. The question this project asks is whether the data was signalling these pressures before they
became critical.

Using World Bank data from 1980 to 2024, I tracked Kenya's performance against two IMF debt
sustainability thresholds, external debt to GNI (40%) and debt service to exports (15%),
and identified when each indicator began crossing its limit. The analysis involved threshold
comparison, trend analysis, and a structured timeline of key debt events. The full pipeline
was built in Python using pandas, matplotlib,numpy, seaborn,requests and Streamlit.

The central finding is that debt service to exports crossed the 15% IMF threshold in 2018,
five years before external debt to GNI crossed its 40% limit in 2023. Between 2017 and 2019,
the debt service ratio rose by 23.8 percentage points in just two years, a deterioration that
was visible in publicly available data. This suggests that flow indicators like debt service
to exports can serve as earlier warning signals than stock indicators like total debt, with
direct implications for how debt sustainability is monitored across sub-Saharan Africa.

## Live Dashboard

[Link will be added after deployment]

## Tools

Python, pandas, matplotlib, seaborn, numpy, requests, Streamlit

## Data Source

World Bank (World Development Indicators)

## Project Structure

- data/ — raw and cleaned datasets
- notebooks/ — exploratory analysis and visualizations
- src/ — data fetching and cleaning scripts
- dashboard/ — Streamlit app

## Author

Loreen Atenge, Economics and Statistics, University of Nairobi
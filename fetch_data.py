import requests
import pandas as pd

def get_world_bank_data(indicator, country="KE", start=1980, end=2024):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start}:{end}&format=json&per_page=100"
    response = requests.get(url)
    data = response.json()
    records = []
    for entry in data[1]:
        records.append({
            "year": int(entry["date"]),
            "value": entry["value"]
        })
    df = pd.DataFrame(records)
    df = df.sort_values("year").reset_index(drop=True)
    return df

debt_gdp = get_world_bank_data("DT.DOD.DECT.GD.ZS")
debt_gdp = debt_gdp.rename(columns={"value": "debt_to_gdp"})


external_debt = get_world_bank_data("DT.DOD.DECT.GN.ZS")
external_debt = external_debt.rename(columns={"value": "external_debt_to_gni"})


debt_service_exports = get_world_bank_data("DT.TDS.DECT.EX.ZS")
debt_service_exports = debt_service_exports.rename(columns={"value": "debt_service_to_exports"})

revenue = get_world_bank_data("GC.REV.XGRT.GD.ZS")
revenue = revenue.rename(columns={"value": "revenue_to_gdp"})


gdp_growth = get_world_bank_data("NY.GDP.MKTP.KD.ZG")
gdp_growth = gdp_growth.rename(columns={"value": "gdp_growth"})


df = debt_gdp.merge(external_debt, on="year")
df = df.merge(debt_service_exports, on="year")
df = df.merge(revenue, on="year")
df = df.merge(gdp_growth, on="year")


print(df.isnull().sum())
print(df.shape)
print(df.head(10))
df.to_csv("data/cleaned/kenya_debt.csv", index=False)
print("saved")


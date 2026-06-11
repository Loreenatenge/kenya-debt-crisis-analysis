import pandas as pd

df = pd.read_csv("data/raw/wb_debt.csv", skipfooter=5, engine="python")

df = df.drop(columns=["Country Name", "Country Code", "Series Code"])


df.columns = [col.split(" ")[0] if col.startswith("19") or col.startswith("20") else col for col in df.columns]


df = df.melt(id_vars=["Series Name"], var_name="year", value_name="value")


df = df.pivot(index="year", columns="Series Name", values="value").reset_index()


df.columns.name = None


df = df.rename(columns={
    "year": "year",
    "External debt stocks (% of GNI)": "external_debt_gni",
    "Total debt service (% of exports of goods, services and primary income)": "debt_service_exports",
    "Revenue, excluding grants (% of GDP)": "revenue_gdp",
    "GDP growth (annual %)": "gdp_growth"
})


df["year"] = df["year"].astype(int)


df = df[(df["year"] >= 1980) & (df["year"] <= 2024)]


df = df.replace("..", float("nan"))


for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
                            
print(df.isnull().sum())
print(df.shape)
print(df.head(10))

df.to_csv("data/cleaned/kenya_debt.csv", index=False)
print("saved")

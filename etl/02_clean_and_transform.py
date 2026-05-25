import pandas as pd
import os
import re

RAW_PATH = "../data/raw/"
CLEAN_PATH = "../data/clean/"

os.makedirs(CLEAN_PATH, exist_ok=True)

files = {
    "companies": "companies.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "documents": "documents.xlsx"
}

def clean_numeric(val):
    if pd.isna(val):
        return None
    val = str(val).replace(",", "").replace("%", "").strip()
    try:
        return float(val)
    except:
        return None

def standardize_year(value):
    if pd.isna(value):
        return None, None, None, False
    value = str(value).strip()
    if value.upper() == "TTM":
        return "TTM", None, None, True
    match = re.match(r"([A-Za-z]{3})[-\s]?(\d{2,4})", value)
    if match:
        month = match.group(1)
        year = match.group(2)
        if len(year) == 2:
            year = "20" + year
        year = int(year)
        return f"{month} {year}", year, month, False
    return value, None, None, False

def parse_analysis(val):
    if pd.isna(val):
        return None, None
    val = str(val)
    match = re.match(r"(\d+)\s*Years?:\s*([\d\.]+)%", val)
    if match:
        return match.group(1) + "Y", float(match.group(2))
    return None, None

def clean_dataframe(df):
    df.columns = df.columns.str.strip()
    df.replace(["NULL", "Null", ""], pd.NA, inplace=True)
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()
    return df

def process_files():
    for name, file in files.items():
        path = os.path.join(RAW_PATH, file)
        df = pd.read_excel(path, header=1)
        df = clean_dataframe(df)

        for col in df.columns:
            if any(keyword in col.lower() for keyword in [
                "sales", "profit", "income", "expense", "assets",
                "liabilities", "equity", "borrowings", "cash",
                "eps", "roe", "roce", "margin"
            ]):
                df[col] = df[col].apply(clean_numeric)

        for col in df.columns:
            if "year" in col.lower() or "fy" in col.lower():
                y = df[col].apply(standardize_year)
                df["year_label"], df["fiscal_year"], df["month"], df["is_ttm"] = zip(*y)

        if name == "analysis":
            if df.shape[1] > 1:
                parsed = df.iloc[:, 1].apply(parse_analysis)
                df["period"], df["value_pct"] = zip(*parsed)

        output_path = os.path.join(CLEAN_PATH, f"{name}.csv")
        df.to_csv(output_path, index=False)

        print(f"{name} -> rows: {len(df)}")

if __name__ == "__main__":
    process_files()
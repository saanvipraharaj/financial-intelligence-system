import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = "postgresql://neondb_owner:npg_xck7OyrI8PUa@ep-weathered-feather-aoy5tmq8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DB_URL)

CLEAN_PATH = "../data/clean/"

def load_table(file_name, table_name):
    path = os.path.join(CLEAN_PATH, file_name)
    df = pd.read_csv(path)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print(f"{table_name} loaded: {len(df)} rows")

def main():
    load_table("companies.csv", "companies")
    load_table("balancesheet.csv", "balancesheet")
    load_table("profitandloss.csv", "profitandloss")
    load_table("cashflow.csv", "cashflow")
    load_table("analysis.csv", "analysis")
    load_table("prosandcons.csv", "prosandcons")
    load_table("documents.csv", "documents")

if __name__ == "__main__":
    main()
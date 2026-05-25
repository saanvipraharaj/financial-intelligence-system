import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:npg_7RDo4YgEBVpr@ep-weathered-feather-aoy5tmq8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)

df = pd.read_csv("../data/sector_mapping.csv")

df.to_sql(
    "sector_mapping",
    engine,
    if_exists="replace",
    index=False
)

print("sector mapping loaded successfully")
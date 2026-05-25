import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = 'postgresql://neondb_owner:npg_v9zepBRQlFY5@ep-weathered-feather-aoy5tmq8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(DATABASE_URL)

companies = pd.read_sql('SELECT * FROM dim_company', engine)

print('Total Companies:', len(companies))

print('Null Company IDs:', companies['company_id'].isnull().sum())

print('Duplicate Company IDs:', companies['company_id'].duplicated().sum())
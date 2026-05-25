import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler

DATABASE_URL = "postgresql://neondb_owner:npg_7RDo4YgEBVpr@ep-weathered-feather-aoy5tmq8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)

query = """
SELECT
    dc.company_id,
    dc.company_name,
    dc.sector,
    dc.roe_percentage,
    dc.roce_percentage,

    fp.sales,
    fp.net_profit,
    fp.opm_percentage,

    fb.borrowings,
    fb.equity_capital,

    fc.free_cash_flow,
    fc.cash_conversion_ratio

FROM dim_company dc

LEFT JOIN fact_profit_loss fp
    ON dc.company_id = fp.company_id

LEFT JOIN fact_balance_sheet fb
    ON dc.company_id = fb.company_id

LEFT JOIN fact_cash_flow fc
    ON dc.company_id = fc.company_id
"""

df = pd.read_sql(query, engine)

print("Data Loaded")
print(df.head())

numeric_cols = [
    'roe_percentage',
    'roce_percentage',
    'sales',
    'net_profit',
    'opm_percentage',
    'borrowings',
    'equity_capital',
    'free_cash_flow',
    'cash_conversion_ratio'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[numeric_cols] = df[numeric_cols].fillna(0)

df['debt_to_equity'] = (
    df['borrowings'] / df['equity_capital']
)

df['profit_margin'] = (
    df['net_profit'] / df['sales']
)

score_features = [
    'roe_percentage',
    'roce_percentage',
    'opm_percentage',
    'free_cash_flow',
    'cash_conversion_ratio',
    'profit_margin'
]

scaler = MinMaxScaler()

scaled_values = scaler.fit_transform(df[score_features])

scaled_df = pd.DataFrame(
    scaled_values,
    columns=score_features
)

weights = {
    'roe_percentage': 0.20,
    'roce_percentage': 0.20,
    'opm_percentage': 0.15,
    'free_cash_flow': 0.15,
    'cash_conversion_ratio': 0.15,
    'profit_margin': 0.15
}

scaled_df['health_score'] = (
    scaled_df['roe_percentage'] * weights['roe_percentage'] +
    scaled_df['roce_percentage'] * weights['roce_percentage'] +
    scaled_df['opm_percentage'] * weights['opm_percentage'] +
    scaled_df['free_cash_flow'] * weights['free_cash_flow'] +
    scaled_df['cash_conversion_ratio'] * weights['cash_conversion_ratio'] +
    scaled_df['profit_margin'] * weights['profit_margin']
)

scaled_df['health_score'] = (
    scaled_df['health_score'] * 100
).round(2)

def classify(score):
    if score >= 45:
        return 'Excellent'
    elif score >= 25:
        return 'Good'
    else:
        return 'Weak'

scaled_df['health_label'] = scaled_df['health_score'].apply(classify)

final_df = pd.DataFrame({
    'company_id': df['company_id'],
    'company_name': df['company_name'],
    'sector': df['sector'],
    'health_score': scaled_df['health_score'],
    'health_label': scaled_df['health_label']
})

final_df = final_df.drop_duplicates(
    subset=['company_id']
)

print(final_df.head())

final_df.to_sql(
    'company_health_scores',
    engine,
    if_exists='replace',
    index=False
)

print("Health score table created successfully")
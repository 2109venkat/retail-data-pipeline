import process
from sqlalchemy import create_engine


def load_data(dim_products_df, dim_customers_df, fact_product_revenue_dly_df, df_fact_revenue_dly, target_db):
    db_host, db_user, db_pass, db_name = target_db['DB_HOST'], target_db['DB_USER'], target_db['DB_PASS'], \
                                         target_db['DB_NAME']
    engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}')
    dim_products_df.to_sql('dim_products', engine, if_exists='replace',index=False)
    dim_customers_df.to_sql('dim_customers',engine,if_exists='replace',index=False)
    fact_product_revenue_dly_df.to_sql('fact_product_revenue_dly',engine,if_exists='replace',index=False)
    df_fact_revenue_dly.to_sql('fact_revenue_dly',engine,if_exists='replace',index=False)
    return
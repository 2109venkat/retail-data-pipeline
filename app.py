# Load the runtime properties

import sys
from config import DB_DETAILS
from process import process_data
from read import get_connection
from write import load_data


def main():
    env = sys.argv[1]
    db_details = DB_DETAILS[env]
    source_db = db_details['SOURCE_DB']
    target_db = db_details['TARGET_DB']
    # Read data from retail_db
    mysql_conn = get_connection(source_db)
    # Process data using pandas
    dim_products_df, dim_customers_df, fact_product_revenue_dly_df, df_fact_revenue_dly= process_data(mysql_conn)
    # Write the data to retail_dw
    load_data(dim_products_df, dim_customers_df, fact_product_revenue_dly_df, df_fact_revenue_dly, target_db)


if __name__ == '__main__':
    main()
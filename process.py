import read
import pandas as pd


def process_data(conn):
    # Dataframe for products dimensions table
    dim_products_df = pd.read_sql('SELECT p.product_id, p.product_name, \
                        p.product_price, c.category_id, c.category_name, d.department_id, \
                        d.department_name, CURDATE() as batch_date, CURRENT_TIMESTAMP as batch_id  \
                        FROM products p JOIN categories c \
                        ON p.product_category_id= c.category_id \
                        JOIN departments d \
                        ON c.category_department_id= d.department_id',conn)
    print(dim_products_df)

    # Dataframe for customers dimension table
    dim_customers_df = pd.read_sql('SELECT customer_id, customer_fname, customer_lname, customer_email, \
                                customer_password, customer_street, customer_city, customer_state, \
                                customer_zipcode, CURDATE() as batch_date, CURRENT_TIMESTAMP as batch_id FROM customers',conn)
    print(dim_customers_df)

    # Dataframe for fact_product_revenue_dly_table
    fact_product_revenue_dly_df = pd.read_sql('SELECT REGEXP_REPLACE(SUBSTRING(o.order_date,1,10),"-","")  AS date_id, \
                                         oi.order_item_product_id AS product_id, \
                                         ROUND(SUM(CASE WHEN o.order_status IN ("COMPLETE", "CLOSED") THEN oi.order_item_subtotal END),2) AS product_revenue, \
                                         ROUND(SUM(CASE WHEN o.order_status IN ("PROCESSING","PENDING","PENDING_PAYMENT") THEN oi.order_item_subtotal END),2) AS outstanding_revenue \
                                         FROM orders o JOIN order_items oi ON o.order_id=oi.order_item_order_id \
                                         GROUP BY o.order_date, oi.order_item_product_id', conn)
    print(fact_product_revenue_dly_df)

    # Dataframe for fact_revenue_dly
    fact_revenue_dly_df = pd.read_sql('SELECT REGEXP_REPLACE(SUBSTRING(o.order_date,1,10),"-","") AS date_id, \
                                 ROUND(SUM(oi.order_item_subtotal),2) AS revenue \
                                 FROM orders o JOIN order_items oi ON o.order_id=oi.order_item_order_id \
                                 WHERE o.order_status IN ("CLOSED","COMPLETE") \
                                 GROUP BY o.order_date', conn)
    print(fact_revenue_dly_df)

    # Dataframe for other columns in fact_revenue_dly
    fact_revenue_dly_df2 = pd.read_sql('SELECT REGEXP_REPLACE(SUBSTRING(order_date,1,10),"-","") AS date_id, \
                    COUNT(order_id) total_order_count, \
                    SUM(order_status IN ("CLOSED", "COMPLETE")) revenue_order_cnt, \
                    SUM(order_status= "CANCELED") canceled_order_cnt, \
                    SUM(order_status IN ("PROCESSING", "PENDING","PENDING_PAYMENT")) outstanding_order_cnt \
                    FROM orders \
                    GROUP BY order_date', conn)
    print(fact_revenue_dly_df2)

    # Dataframe for fact_revenue_dly table
    df_fact_revenue_dly = pd.merge(fact_revenue_dly_df, fact_revenue_dly_df2, on='date_id')
    print(df_fact_revenue_dly)
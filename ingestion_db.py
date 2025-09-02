from tracemalloc import start
import pandas as pd
import os
from sqlalchemy import create_engine
import time


engine = create_engine("mysql+pymysql://root:root@localhost/inventory")


import logging 
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="a"
)

def ingest_db(df,table_name,engine):
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

def load_raw_data():
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            df=pd.read_csv('data/'+file)
            logging.info(f'ingesting{file} in db')
            ingest_db(df,file[:-4],engine)
    end=time.time()
    total_time=(end-start)/60
    logging.info(f'Total time taken to ingest data: {total_time} minutes')
    return total_time
    logging.info('ingestion complete')   
    
     
if __name__ == "__main__":
    load_raw_data()
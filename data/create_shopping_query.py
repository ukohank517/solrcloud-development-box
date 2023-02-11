import pandas as pd
import urllib.parse

SPLIT_SIZE=10000
INPUT_FOLDER='esci-data/shopping_queries_dataset'

df_examples = pd.read_parquet(f'{INPUT_FOLDER}/shopping_queries_dataset_examples.parquet')
df_products = pd.read_parquet(f'{INPUT_FOLDER}/shopping_queries_dataset_products.parquet')
df_sources = pd.read_csv(f"{INPUT_FOLDER}/shopping_queries_dataset_sources.csv")

df_examples_products = pd.merge(
    df_examples,
    df_products,
    how='left',
    left_on=['product_locale','product_id'],
    right_on=['product_locale', 'product_id']
)

queries = df_examples_products[['query']].drop_duplicates().sample(10000).reset_index(drop=True)
for q in queries['query']:
    print('/select?q=text:' + urllib.parse.quote(q))
import pandas as pd
import json
import os

SPLIT_SIZE=10000
INPUT_FOLDER='esci-data/shopping_queries_dataset'
OUTPUT_FOLDER='amazonshopping'


print("reading data file ...")
df_examples = pd.read_parquet(f'{INPUT_FOLDER}/shopping_queries_dataset_examples.parquet')
df_products = pd.read_parquet(f'{INPUT_FOLDER}/shopping_queries_dataset_products.parquet')
df_sources = pd.read_csv(f"{INPUT_FOLDER}/shopping_queries_dataset_sources.csv")
print("data reading complete")

df_examples_products = pd.merge(
    df_examples,
    df_products,
    how='left',
    left_on=['product_locale','product_id'],
    right_on=['product_locale', 'product_id']
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for i in range(0, len(df_examples_products), SPLIT_SIZE):
    data_from = i
    data_to = min((i + SPLIT_SIZE), len(df_examples_products)) - 1
    with open(f"{OUTPUT_FOLDER}/shopping_products_{str(i // SPLIT_SIZE).zfill(3)}.json", "w") as outputFile:
        json.dump(json.loads(df_examples_products[data_from:data_to].to_json(orient='records')), outputFile, indent=2)
    print(f'\rcreating json file {i//SPLIT_SIZE} / {len(df_examples_products)//SPLIT_SIZE}', end='')
print(f'\nsuccessfully creating feeding json file in [{OUTPUT_FOLDER}]')
import pandas as pd

def clean_data(query):
    df = pd.read_csv(f"{query}.csv", encoding='utf-8')

    df.drop_duplicates(subset=df.columns[0])
    df.to_excel(f"{query}.xlsx", encoding='utf-8')
import korean_financial_minute_data_miner.run.first_entry

df = korean_financial_minute_data_miner.run.first_entry.get_first_entries_df(20190919, force_ingest=False)
print(df.head())
print(df.tail())

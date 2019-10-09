import run.first_entry

df = run.first_entry.get_first_entries_df(20190919, force_ingest=False)
print(df.head())
print(df.tail())

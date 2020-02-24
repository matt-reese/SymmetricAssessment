import pandas as pd

gudid_df = pd.read_csv('gudid_data.csv', low_memory=False).astype(str)
mdall_df = pd.read_csv('mdall_data.csv', low_memory=False).astype(str)
aligned_df = pd.read_csv('aligned_data.csv', low_memory=False).astype(str)

print('GUDID-only catalog count: ' + str(gudid_df.shape[0] - aligned_df.shape[0]))
print('MDALL-only catalog count: ' + str(mdall_df.shape[0] - aligned_df.shape[0]))
print('Catalogs in both datasets: ' + str(aligned_df.shape[0]))

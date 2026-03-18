import pandas as pd

use_cols = ['NPI', 'Entity Type Code', 'Provider Organization Name (Legal Business Name)',
            'Provider First Name', 'Healthcare Provider Taxonomy Group_1',
            'Healthcare Provider Taxonomy Group_2', 'Healthcare Provider Taxonomy Group_3',
            'Healthcare Provider Taxonomy Group_4', 'Healthcare Provider Taxonomy Group_5',
            'Healthcare Provider Taxonomy Group_6', 'Healthcare Provider Taxonomy Group_7',
            'Healthcare Provider Taxonomy Group_8', 'Healthcare Provider Taxonomy Group_9',
            'Healthcare Provider Taxonomy Group_10', 'Healthcare Provider Taxonomy Group_11',
            'Healthcare Provider Taxonomy Group_12', 'Healthcare Provider Taxonomy Group_13',
            'Healthcare Provider Taxonomy Group_14', 'Healthcare Provider Taxonomy Group_15',
            'Provider Business Practice Location Address Postal Code']

df = pd.read_parquet('npidata.parquet')

print(df.columns.tolist())

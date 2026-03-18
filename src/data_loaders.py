from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
import pandas as pd
import requests
#still need import .env
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")
from census import Census


def fetch_nppes() -> pd.DataFrame:
    #filtering for dental providers only using taxonomy codes, which are hierarchical and standardized across the industry.

    use_cols = ['NPI', 'Entity Type Code', 'Provider Organization Name (Legal Business Name)',
            'Provider First Name','Healthcare Provider Taxonomy Code_1',
            'Healthcare Provider Taxonomy Code_2',
            'Provider Business Practice Location Address Postal Code',
            'Provider Business Practice Location Address State Name']
    codes = [
        '1223G0001X', '1223D0001X', '1223E0200X', '1223P0221X',
        '1223P0300X', '1223P0700X', '1223S0112X', '1223X0400X',
        '122300000X', '1223D0008X', '1223X0008X'
    ]

    batch = []

    for chunk in pd.read_csv('npidata_pfile_20050523-20240523.csv', usecols=use_cols, chunksize=50000):
        mask = chunk[[c for c in chunk.columns if 'taxonomy' in c.lower()]].isin(codes).any(axis=1)
        filtered_chunk = chunk[mask]
        if len(filtered_chunk) > 0:
            batch.append(filtered_chunk)
        print(f"Processed chunk with {len(chunk)} rows, found {len(filtered_chunk)} dental providers.")
    df = pd.concat(batch, ignore_index=True)
    return df



def fetch_cbp_dental(year: int,api_key: str) -> pd.DataFrame:
    url = f"https://api.census.gov/data/{year}/cbp"
    params = {
        'get': 'ESTAB,EMP,PAYANN,NAME',
        'for': 'county:*',
        'NAICS2017': '621210',
        'key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def fetch_acs_demographics(year: int, api_key: str) -> pd.DataFrame:
    resp = requests.get("https://api.census.gov/data/2021/acs/acs5/variables.json")
    variables = resp.json()['variables']

    b27001_vars = {k: v for k, v in variables.items() if k.startswith('B27001')}

    need = []

    for code, meta in sorted(b27001_vars.items()):
        if "with" in meta['label'].lower():
            need.append(code)

    c = Census(CENSUS_API_KEY)
    variables = ['B19013_001E', 
                'B01002_001E', 
                'B27001_001E',] + need

    result = c.acs5.get(variables, {'for': 'zip code tabulation area:*'},
                        year=2021)
    df = pd.DataFrame(result)
    insurance_cols = [col for col in df.columns if col.startswith('B27001') and col != 'B27001_001E']
    df = df.replace(-666666666.0, pd.NA)
    df[insurance_cols] = df[insurance_cols].apply(pd.to_numeric, errors='coerce')
    df['insured_total'] = df[insurance_cols].sum(axis=1)
    df['pct_insured'] = df['insured_total'] / df['B27001_001E'].astype(float) * 100
        
def fetch_gcspi() -> pd.DataFrame:
     #requests pull: https://www.newyorkfed.org/medialibrary/research/interactives/GSCPI/downloads/gscpi_data.xlsx 
     #pressure index only value column, positive value indicates above average supply chain pressure
     pass

def fetch_bdi(api_key: str) -> pd.DataFrame:
    #FRED API series ID is DBDNTD for baltic dry index. full history pull so no date parameter needed
    pass


def __main__():
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    cbp_dfs = [fetch_cbp_dental(year, CENSUS_API_KEY) for year in years]
    cbp_all = pd.concat(cbp_dfs, ignore_index=True)
    cbp_all.to_csv('cbp_dental_2018_2023.csv', index=False)

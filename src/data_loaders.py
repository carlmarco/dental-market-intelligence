from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

def fetch_cpb_dental(year: int, api_key: str) -> pd.DataFrame:
    #https://api.census.gov/data/2021/cbp
    #ESTAB (number of establishments)
    #EMP employment
    #NAICS2017=621210 county level
    #2018->most recent year
   
    pass

def fetch_acs_demographics(year: int, api_key: str) -> pd.DataFrame:
    # acs5 dataset
    # at zip-code level: B19013_001E (median household income)
    #B01002_001E (median age)
    # B27001_001E (total population w/ health insurance coverage)
    pass
    
 def fetch_gcspi() -> pd.DataFrame:
     #requests pull: https://www.newyorkfed.org/medialibrary/research/interactives/GSCPI/downloads/gscpi_data.xlsx 
     #pressure index only value column, positive value indicates above average supply chain pressure
     pass

def fetch_bdi(api_key: str) -> pd.DataFrame:
    #FRED API series ID is DBDNTD for baltic dry index. full history pull so no date parameter needed.
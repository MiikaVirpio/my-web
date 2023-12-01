import os
import pandas as pd
import numpy as np
from miika.settings import BASE_DIR


def gdp_dataset():
    # Read from 5th row to skip metadata
    df = pd.read_csv(os.path.join(BASE_DIR, 'miika/static/dash_apps/bda_va_1/gdp_data_for_countries.csv'),skiprows=4)
    # Drop columns that are not needed
    df = df.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 67"])
    # Set index to country name
    df = df.set_index("Country Name")
    # Transpose to make years the index
    df = df.transpose()
    # Convert to float values
    df = df.astype(float)
    # Apply lambda function to convert values to billions
    df = df.map(lambda x: np.round(x / 1e9, 0) if pd.notnull(x) else None) # type: ignore
    return df
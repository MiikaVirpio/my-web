import os
import pandas as pd
import numpy as np
from miika.settings import BASE_DIR

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

def make_dataset():
    # Make columns more usable
    column_names = ["ID", "Date", "Month", "Year", "Segment", "Country", "Product", "Discount Band", "Units Sold", "Manufacturing Price", "Quotation Price", "Gross Sales", "Discounts Value", "Actual Sales", "Total Costs", "Profit", "Delivery Time"]
    df = pd.read_excel(os.path.join(BASE_DIR, 'miika/static/dash_apps/bda_va_2/financial_insights_assignment_2_raw.xlsx'), names=column_names)
    # Make a datetime column from string date
    df["Datetime"] = pd.to_datetime(df["Date"])
    # Make month number for monthly analysis later
    df["Month nbr"] = df["Datetime"].dt.month 
    return df

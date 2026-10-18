# -*- coding: utf-8 -*-
import os
import pandas as pd

def get_dataset_analysis_v4():
    data_path = 'data/flood_data.csv'
    if not os.path.exists(data_path):
        return None, {}
    df = pd.read_csv(data_path)
    risk_dist = df['Risk'].value_counts().to_dict()
    return df.head(10), risk_dist

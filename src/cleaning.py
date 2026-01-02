import pandas as pd
import json
from pathlib import Path

# src/cleaning.py  (append at bottom)
import streamlit as st   # add only if not already imported
@st.cache_data(show_spinner=False)
def load_data():
    return cleaning_data(fetch_raw_data())

def fetch_raw_data(url=None):
    '''
    
    That function fetch the data from internet if url id passed
    Current version of this function not use url


    '''
    print("__file__  ->", __file__)
    print("resolved  ->", Path(__file__).resolve())
    print("parent    ->", Path(__file__).resolve().parent)
    project_root = Path(__file__).resolve().parent.parent
    path = project_root / 'data' / 'raw' / 'USvideos.csv'
    data = pd.read_csv(path)
    
    return data



def cleaning_data(data, save=False):
    '''
    This function is take raw data and make flow steps:
        - drop [video_id, description, thumbnail_link, trending_date]
        - add category name to columns
        - change and reindex columns
        - change dtypes of the columns
    
    Parameters:
        - Data [data frame it must be cleaned ]
        - Save switch [option for saving cleaned data]
            - path to save ./cleaned.csv
            - default is True
    '''

    # drop columns and get category title

    columns_to_drop = ['video_id', 'description', 'thumbnail_link', 'trending_date']
    df = data.drop(columns=columns_to_drop)
    project_root = Path(__file__).resolve().parent.parent
    path = project_root / 'data' / 'raw' / 'US_category_id.json'
    with open(path) as f:
        data = json.load(f)
    category_map = {item['id']:item['snippet']['title'] for item in data['items']}
    df['Category_Title'] = df['category_id'].astype(str).map(category_map)
    df = df.drop(columns=['category_id'])
    
    # reindex and rename
    new_columns = [
    "Channel_Title", 
    "Category_Title",
    "Pub_Date",
    "Views", 
    "Likes", 
    "Dislikes", 
    "Comments", 
    "Dis_Comments", 
    "Dis_Ratings", 
    "Err_Or_Removed", 
    "Title", 
    "Tags"
]
    new_order = [
    "channel_title",
    'Category_Title',
    'publish_time',
    'views', 'likes', 'dislikes', 'comment_count',
    'comments_disabled', 'ratings_disabled',
    'video_error_or_removed',
    'title','tags'
    ]
    df = df.reindex(columns=new_order)
    df.columns = new_columns

    # change dtypes [Pub_Date]
    df['Pub_Date'] = pd.to_datetime(df['Pub_Date'])

    # reset index
    df.reset_index(drop=True,inplace=True)

    if save:
        project_root = Path(__file__).resolve().parent.parent
        path = project_root / 'data' / 'processed' / 'final.csv'
        df.to_csv(path)
    else:
        pass

    print(f'All needs satisfied successfully ...')
    return df

if __name__ == '__main__':

    cleaning_data(fetch_raw_data(),save=False)


import pandas as pd

# params = {'x':'Likes','y':'Category_Title','Top':True,'grouping':{True:'Channel_Title'}}
def prepare_to_plot_Bar_Heat(data,_type,key,grouping_switch=False,grouping_by='Category_Title',head=True):
    '''
    That function return one data frame ready t plot only have first 10 rows depend on params
    params:
        - data => data frame
        - key => the values that function will return only top 10 or lowest 10
        - grouping_switch => to make function know if you will use grouping or not
        - grouping_by => column that we will grouby by
        - head => to determine what the function will return head or tail
    '''
    valid_columns = list(data.columns)
    columns_to_keep = [
    "Channel_Title",
    "Category_Title",
    "Title",
]
    # 
    if grouping_switch:
        if grouping_by in valid_columns:
            df = data.groupby(grouping_by,as_index=False).agg({"Views":'sum',"Likes":'sum',"Dislikes":'sum',"Comments":'sum'})
        else:
            return f'Please enter valid credentials!'
    else:
        df = data
    
    # sort_values depend on the key
    if key in valid_columns:
        if grouping_switch:
            df = df[[grouping_by, key]]
        else:
            columns_to_keep.append(key) 
            df = df[columns_to_keep]
        
        df = df.sort_values(by=key,ascending=False)
    else:
        return f'Please enter valid credentials!'
    
    # choosing depend on head=True
    if _type == 'Bar':
        if head:
            df = df.head(10)
        else:
            df = df.tail(10)
    else:
        pass
    
    print(f'All need satisfied successfully')
    return df


# tokens = {'channel':'Dude Perfect', '_by':'Likes'}
def channel_analysis(data,channel,_by):
    '''
    This function return a precise dataframe ready to plot it as linear chart
    Return:
        - publish date
        - _by [views, comments, likes, dislikes]
        - channel
    '''
    valid_traces = ['Likes','Comments','Dislikes','Views']

    # filter according to channel
    df = data.loc[data['Channel_Title'] == channel , ['Channel_Title','Pub_Date',_by,'Category_Title']]
    df = df.sort_values(by='Pub_Date',ascending=True)
    print('All needs satisfied successfully ...')
    return df


if __name__ == '__main__':
    pass


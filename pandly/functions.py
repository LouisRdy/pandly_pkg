import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from datetime import datetime

def data_shape(dataframe):

    # Store values in a dictionnary
    dtypes = {
        "column": [],
        "missing_values": None,
        "dtype": []
    }

    # Retreive col names, missing values and dtypes
    for i in dataframe.columns:
        dtypes["column"].append(i) # Column names
        dtypes["missing_values"] = dataframe.isna().sum().values # Missing values
        dtypes["dtype"].append(dataframe[i].dtype) # Dtype

    # Convert dictionnary to pandas dataframe
    data = pd.DataFrame(dtypes)

    # Data shape
    print(f"Number of rows: {dataframe.shape[0]}")
    print(f"Number of columns: {dataframe.shape[1]}")

    # Display first 5 rows of dataframe
    #dataframe.head()
    data["dtype"] = data["dtype"].astype(str)
    return data


# Calculate trend rate
def trend_calculation(data, col_1, col_2, metric, round_to=1):
    data_frame = pd.DataFrame(data.groupby(col_1)[col_2].agg([metric])).reset_index().rename(columns={metric: col_2})
    
    # List of col_2 values
    count = data_frame[col_2].tolist()

    # Preparing growth rate list that has to start from 0
    trend = [0]

    # Get growth rate
    for i in range(1, len(count)):
        trend.append(round((count[i] - count[i-1]) / count[i-1] * 100, round_to))
        
    # Result
    data_frame['trend_percentage'] = trend
    
    # Text -> useful in chart
    l = data_frame["trend_percentage"].astype(str).tolist()

    text = []

    for i in l:
        if "-" not in i:
            if i != "0":
                text.append("+"+i)
            else:
                text.append(i)
        else:
            text.append(i)    
    
    data_frame['trend_percentage_text'] = text

    return data_frame


# Load to Big Query
def load_to_gbq(data, project_id, table, write_disposition, insert_sync_date=False):

    # Formatting columns
    data.columns = [i.replace(".", "_") for i in data.columns]
    
    if insert_sync_date == True:
        data["sync_date"] = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    
   # Load data to BQ
    print("Loading data....")
    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition) # Replace existing data
    job = client.load_table_from_dataframe(data, f"{project_id}.{table}", job_config=job_config)
    job.result()
    print("...Loaded!")


    
    # Function that will return percentage and count
def groupby_2(data, column_1, column_2, round_to=2):
    dff = data
    groupby = pd.DataFrame(dff.groupby([column_1, column_2]).agg({column_2 : "count"})).groupby(level=0).apply(lambda x: round(100*x/x.sum(),round_to))
    groupby = groupby.rename(columns={column_2: 'percentage'}).reset_index()
    groupby['count'] = dff.groupby([column_1, column_2])[column_2].agg(['count']).values

    return groupby



def missing_value_counts(data, round_to=3, show_plot=False, darkmode=True, height=None, width=None, horizontal=False):
    # retreive dataframe basic shape stats
    dic = {
        'missing_val_count' : data.isna().sum(), # nan count
        'missing_val_percentage' : (round(data.isna().sum()/len(data), round_to)*100), # nan percentage
    }
    
    data = pd.DataFrame(dic) \
        .reset_index(names="column") \
        .sort_values(by="missing_val_count", ascending=False) \
        .reset_index(drop=True)

    # Dark theme
    if darkmode == True:
        template = "plotly_dark"
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            #font_family="Rockwell"
        )
             
    else:
        template = "plotly"
        hoverlabel=None
        
    # Height and width    
    if height:
        while not width:
            width = height
            
    # Orientation
    if horizontal == False:
        x="column"
        y = "missing_val_count"
        xaxis_title=None
        yaxis_title="Count"
        hovermode = "x unified"
        
    else:
        data = data.sort_values(by="missing_val_count")
        y="column"
        x = "missing_val_count"
        yaxis_title=None
        xaxis_title="Count"
        hovermode = "y unified"
    
    fig = px.bar(
        data,
        x=x,
        y=y,
        text="missing_val_percentage",
        color_discrete_sequence=["#bfe3ab"],
        hover_data={
            "column": False
        }
    )
    
    fig.update_layout(
        template=template,
        title="Missing values per column",
        title_x=.5,
        height=height,
        width=width,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hovermode=hovermode,
        hoverlabel=hoverlabel
        
    )
    
    fig.update_traces(
        texttemplate = "%{text}%",
        
    )
    
    if show_plot == True:
        fig.show()
        
    return data

#######################################
#######################################

months = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
        ]

days = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]


def vcounts(data, col, metric="count", show_nans=False, horizontal=False, show_plot=False, height=None, width=None, text=None, darkmode=False):
    
    dff = data
    
    if show_nans == True:
        try:
            dff.fillna("Unknown")
        except TypeError as t:
            print(t)
            dff = dff.groupby(col)[col].agg([metric]).reset_index().sort_values(by=metric, ascending=False)
        else:
            dff = dff.fillna("Unknown")
            dff = dff.groupby(col)[col].agg([metric]).reset_index().sort_values(by=metric, ascending=False)
    else:
        dff = dff.groupby(col)[col].agg([metric]).reset_index().sort_values(by=metric, ascending=False)
    
    if metric == "count":
        dff["percentage"] = dff["count"]/len(data)
        
    display(dff)

    if horizontal == False:
        x=col
        y = metric
        hovermode = "x"
        
    else:
        y=col
        x = metric
        hovermode = "y"
        dff = dff.sort_values(by="count", ascending=True)
        
    if text == "percentage":
        texttemplate = "%{text:,.1%}"
    else:
        texttemplate=None
        
    if height:
        while not width:
            width = height
            
    if darkmode == True:
        template="plotly_dark"
    else:
        template=None
            
    hovertext = ["<b>Count</b>: " + i for i in dff["count"].astype(str)]

    fig = px.bar(
        dff,
        x=x,
        y=y,
        text=text,
        hover_name=x,
        hover_data={
            col: False,
            "count": True,
            "percentage": True
        }
    )

    fig.update_layout(
        template=template,
        title=f"{col.replace('_', ' ').capitalize()} value counts",
        title_x=.5,
        height=height,
        width=width,
        hovermode=hovermode
    )
    
    fig.update_traces(
        texttemplate=texttemplate,
        hovertemplate=hovertext
    )
    
    if show_plot == True:
        fig.show()
        
    
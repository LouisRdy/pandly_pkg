import pandas as pd
import plotly.express as px


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


    
    # Function that will return percentage and count
def groupby_2(data, column_1, column_2, round_to=2):
    dff = data
    groupby = pd.DataFrame(dff.groupby([column_1, column_2]).agg({column_2 : "count"})).groupby(level=0).apply(lambda x: round(100*x/x.sum(),round_to))
    groupby = groupby.rename(columns={column_2: 'percentage'}).reset_index()
    groupby['count'] = dff.groupby([column_1, column_2])[column_2].agg(['count']).values

    return groupby



def missing_value_counts(data, round_to=3):
    # retreive dataframe basic shape stats
    data = {
        'missing_val_count' : df.isna().sum(), # nan count
        'missing_val_percentage' : (round(df.isna().sum()/len(df), round_to)*100), # nan percentage
    }
    
    data = pd.DataFrame(data)
    
    return data



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


def vcounts(data, col, metric="count", show_nans=False, horizontal=False, show_plot=False, height=None, width=None, text=None):
    
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
        
    
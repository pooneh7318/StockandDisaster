from ast import Div
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
sectors = pd.read_csv('sectors_price_2000_2021')
sectors.rename(columns = {'mining_prc' : 'mining','manufacturing_prc' : 'manufacturing','transportation_prc' : 'transportation','wholesale_prc' : 'wholesale','retail_prc' : 'retail','insurance_prc' : 'insurance','services_prc' : 'services'}, inplace = True)

drought_1=pd.read_csv('drought1.csv')
drought_2=pd.read_csv('drought2.csv')
fire_1=pd.read_csv('fire1.csv')
fire_2=pd.read_csv('fire2.csv')
storm_1=pd.read_csv('storm1.csv')
storm_2=pd.read_csv('storm2.csv')
disaster_info = pd.read_csv('disaster_info.csv')

sectors["date"] = pd.to_datetime(sectors["date"], format="%Y-%m-%d")
data = pd.read_csv('avocado.csv')
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, -1, 2, -2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Effects of Natural Disasters on U.S. Market"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Effects of Natural Disasters on U.S. Market", className="header-title"
                ),
                html.P(
                    children="Analyze the effects of natural disasters"
                    " on different sectors of the financial markets in the U.S."
                    " between 2000 and 2021",
                    className="header-description",
                ),
                
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Disaster", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": disas, "value": disas}
                                for disas in np.array(['Storm','Wildfire','Drought'])
                            ],
                            value="Storm",
                            clearable=False,
                            
                            className="dropdown",
                        ),
                        
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Sectors", className="menu-title"),
                        
                        dcc.Dropdown(
                            id='type-filter',
                            options=[
                                {"label": region, "value": region}
                                for region in np.array(['mining','manufacturing','transportation','wholesale','retail','insurance','services'])
                            ],
                            multi=False,
                            value="mining",
                            className="dcc_control"
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
                    [
                        html.Div(
                            [
                                html.P("Disaster Type"),
                                html.H6(
                                    id="well_text",
                                    className="info_text"
                                )
                            ],
                            id="wells",
                            className="pretty_container"
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("Location"),
                                        html.H6(
                                            id="gasText",
                                            className="info_text"
                                        )
                                    ],
                                    id="gas",
                                    className="pretty_container"
                                ),
                                html.Div(
                                    [
                                        html.P("Insured Damage"),
                                        html.H6(
                                            id="oilText",
                                            className="info_text"
                                        )
                                    ],
                                    id="oil",
                                    className="pretty_container"
                                ),
                                html.Div(
                                    [
                                        html.P("Date"),
                                        html.H6(
                                            id="waterText",
                                            className="info_text"
                                        )
                                    ],
                                    id="water",
                                    className="pretty_container"
                                ),
                            ],
                            id="tripleContainer",
                        )

                    ],
                    id="infoContainer",
                    className="menu"
                ),
        
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="example-graph1",
                        config={"displayModeBar": False},
                        #figure =fig
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="example-graph2",
                        config={"displayModeBar": False},
                        #figure =fig
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        )
    ]
)


@app.callback(
    [Output("price-chart", "figure"),
     Output("example-graph1", "figure"),
     Output("example-graph2", "figure"),
     Output('well_text', 'children'),
     Output('gasText', 'children'),
     Output('oilText', 'children'),
     Output('waterText', 'children'),],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        
        (sectors.date >= start_date)
        & (sectors.date <= end_date)
    )
    filtered_data = sectors.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data[avocado_type],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Sector Price of Return Index of "+avocado_type,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    
    
    if region=="Storm":
        dframe1=storm_1
        dframe2=storm_2
        d_type = disaster_info['Disaster_Type'][2]
        location = disaster_info['location'][2]
        dmg = "$"+str(disaster_info['insured_dmg'][2])+"B"
        d_date = disaster_info['date'][2]
    elif region=="Wildfire":
        dframe1 = fire_1
        dframe2 = fire_2
        d_type = disaster_info['Disaster_Type'][1]
        location = disaster_info['location'][1]
        dmg = "$"+str(disaster_info['insured_dmg'][1])+"B"
        d_date = disaster_info['date'][1]
    else:
        dframe1 = drought_1
        dframe2 = drought_2
        d_type = disaster_info['Disaster_Type'][0]
        location = disaster_info['location'][0]
        dmg = "$"+str(disaster_info['insured_dmg'][0])+"B"
        d_date = disaster_info['date'][0]
    fig1 = px.bar(dframe1, x="sector", y="perc", barmode="group")
    fig2 = px.bar(dframe2,x="sector", y="factor", barmode="group")
    #d_type = 0
    #location = 0
    #dmg = 0
    #d_date = 0


    return price_chart_figure, fig1,fig2, d_type,location,dmg,d_date








if __name__ == "__main__":
    app.run_server(debug=True)

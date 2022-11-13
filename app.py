import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd

from itertools import islice

import yfinance as yf

from generate_group import main

import os


# Define app
# VAPOR, LUX, QUARTZ
# external_stylesheets=[dbc.themes.QUARTZ]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])
app.title = "Draft"
server = app.server
# Define callbacks

navbar = dbc.NavbarSimple(
    brand="CYBER5 PRODUCT DRAFT",
    brand_href="#",
    brand_style={"font-family": "Lato, -apple-system, sans-serif" , "font-size": "2rem", "padding": "0.1rem 0.1rem"},
    color="success",
    dark=True,
    expand = True,
    id = "navbar-example-update"
)

# description = """
# TODO: fill in description
# """

print("hi from global")



########## UTILITY FUNCTIONS ###############################
def generate_cards(groups, card_num_cols):
    
    len_groups = len(list(groups))
    
    # Use islice
    def convert(listA, len_2d):
        res = iter(listA)
        return [list(islice(res,i)) for i in len_2d]
    
    # this list helps dynamically display layout of the cards
    res = convert(list(groups), [card_num_cols]*(len_groups//card_num_cols) + [len_groups%card_num_cols])
    
    # get card body
    cards_body = []
    for r in res:
        row_list = []
        for c in list(r):
            
            card_content = [dbc.CardBody(html.H5(", ".join(list(c)), className="card-title"))]
            
            row_list.append(dbc.Col(dbc.Card(card_content, color = "success", inverse=True,), style={"display": "flex", "margin-top": "2%", "margin-bottom": "2%"}))
            
        cards_body.append(dbc.Row(row_list, className="mb-4", justify="center"))
    
    cards = html.Div(cards_body)

    return cards



#############################################################

cards = html.Div(id="cards")



# app.layout = [navbar, dbc.Container()]

def serve_layout():
    return html.Div([ dcc.Store(id="navbar-example-input", data=""), navbar, 
dcc.Graph(id = "live-update-graph", style = {"margin-left": "5%", "margin-right": "5%"}),
 dcc.Interval(
            id='interval-component',
            interval=300000, # in milliseconds # 300K ms = 5 min
            n_intervals=0
        ),
 dcc.Store(id="cards-input", data=""), dcc.Store(id="seed", data=10), dbc.Container([cards], style = {"margin-top": "5%", "margin-bottom": "5%"})])


app.layout = serve_layout

######### CALLBACK #############################
@app.callback(
    Output("cards", "children"), [Input("cards-input", "data"), Input("seed", "data")]
)
def get_data_and_cards(data_input, seed):
    print("generating groups...")
   
    
    # frozen set of frozen sets, get most recent grouping
    groups = main(seed = seed)

    # can parametrize this later if necessary
    card_num_cols = 3
    
    # generate cards
    cards = generate_cards(groups = groups, card_num_cols = card_num_cols)
    
    return cards
    
    
@app.callback([Output('live-update-graph', 'figure'),
                Output("seed", "data")],
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    price_history = yf.Ticker('DKS').history(period='1d', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='5m', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)
    fig = px.line(price_history.reset_index(), x = "Datetime", y="Open", template="plotly_white", title = "<b>DKS Stock Price</b>")
    fig.update_traces(line_color = "green", line_width = 4)

    return fig, int(round(price_history.reset_index().sort_values(by="Datetime").tail(1)[["Open"]].iloc[0,0],2)*100)



    
if __name__=='__main__':
    # app.run_server(debug=True, port=8005)
    app.run_server(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

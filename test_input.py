import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            # Want the value of this dcc.Tabs to be whatever dcc.Location.pathname is
            # dcc.Tabs(id="tabs", value="/page-1", children=[
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Page 1', value='/page-1'),
                dcc.Tab(label='Page 2', value='/page-2'),
                dcc.Tab(label='Page 3', value='/page-3'),
            ]),
        ]),
    ]),
    html.Div(id='page-content'),
])

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    #html.H1(pathname),
])

page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

# This causes a circular reference (although it does work to change tab on clicking link)

# @app.callback([dash.dependencies.Output('page-content', 'children'),
#                dash.dependencies.Output('tabs', 'value')],
#               [dash.dependencies.Input('url', 'pathname')],
#               )
# def display_page(pathname):
#     if pathname == '/page-1':
#         return page_1_layout, pathname
#     elif pathname == '/page-2':
#         return page_2_layout, pathname
#     else:
#         return html.Div([html.H1('Error 404 - Page not found')]), pathname


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')],
              )
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return html.Div([html.H1('Error 404 - Page not found')])

@app.callback(dash.dependencies.Output('url', 'pathname'),
              [dash.dependencies.Input('tabs', 'value')])
def tab_updates_url(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

################################################################################################################
# LOAD AND PROCESS DATA
df0 = pd.read_csv('./data/IHME_GBD_2017_HEALTH_SDG_1990_2030_SCALED_Y2018M11D08.CSV')
loc_meta = pd.read_csv('./data/location_metadata.csv')

# Indicator Value by country in wide format
df = df0.pivot(index='location_name', columns='indicator_short', values='scaled_value')
df = pd.merge(loc_meta, df.reset_index())
indicators = df0.indicator_short.unique().tolist()
indicator_key = df0.drop_duplicates('indicator_short').set_index('indicator_short')[
    'ihme_indicator_description'].to_dict()

################################################################################################################


top_markdown_text = '''
### Dash Tutorial - Sustainable Development Goals 
#### Zane Rankin, 2/17/2019
The [Institute for Health Metrics and Evaluation](http://www.healthdata.org/) publishes estimates for 41 health-related SDG indicators for
195 countries and territories.
I downloaded the [data](http://ghdx.healthdata.org/record/global-burden-disease-study-2017-gbd-2017-health-related-sustainable-development-goals-sdg)
for a tutorial on Medium and Github
**Indicators are scaled 0-100, with 0 being worst observed (e.g. highest mortality) and 100 being best.**
'''

app.layout = html.Div([

    # HEADER
    dcc.Markdown(children=top_markdown_text),

    # LEFT - CHOROPLETH MAP
    html.Div([
        dcc.Dropdown(
            id='x-varname',
            options=[{'label': i, 'value': i} for i in indicators],
            value='SDG Index'
        ),
        dcc.Markdown(id='x-description'),
        dcc.Graph(id='county-choropleth'),
        dcc.Markdown('*Hover over map to select country for plots*'),

    ], style={'float': 'left', 'width': '39%'}),

    # RIGHT - SCATTERPLOT
    html.Div([
        dcc.Dropdown(
            id='y-varname',
            options=[{'label': i, 'value': i} for i in indicators],
            value='Under-5 Mort'
        ),
        dcc.Markdown(id='y-description'),
        dcc.Graph(id='scatterplot'),
    ], style={'float': 'right', 'width': '59%'}),

    dcc.Input(id='intermediate-value', style={}),

    dcc.Input(id='input', style={}),


    #dcc.Input(id="input-2", type="text", value={href}),




])


@app.callback(
    Output('x-description', 'children'),
    [Input('x-varname', 'value')])
def x_description(i):
    return f'{indicator_key[i]}'


@app.callback(
    Output('y-description', 'children'),
    [Input('y-varname', 'value')])
def y_description(i):
    return f'{indicator_key[i]}'


@app.callback(
    Output('county-choropleth', 'figure'),
    [Input('x-varname', 'value')])
def update_map(x_varname):
    return dict(
        data=[dict(
            locations=df['ihme_loc_id'],
            z=df[x_varname],
            text=df['location_name'],
            autocolorscale=False,
            reversescale=True,
            type='choropleth',
        )],
        layout=dict(
            title=x_varname,
            height=400,
            margin={'l': 0, 'b': 0, 't': 40, 'r': 0},
            geo=dict(showframe=False,
                     projection={'type': 'Mercator'}))
    )


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('x-varname', 'value'),
     Input('y-varname', 'value'),
     Input('county-choropleth', 'hoverData'),])

#@app.callback(Output('children'), [Input('intermediate-value', 'href')])

#@app.callback(dash.dependencies.Output('intermediate-value', 'children')
#,
              #[dash.dependencies.Input('intermediate-value', 'url')]
#              )


#@app.callback(
    #Output('input', 'pathname'),
    #[Input('url', 'pathname')])

#[Input('url', 'pathname')],

#def display_page(pathname):
#    return html.Div([
#        html.H3('You are on page {}'.format(pathname))
#    ])

def update_graph(x_varname, y_varname, hoverData):
    if hoverData is None:  # Initialize before any hovering
        location_name = 'Nigeria'
    else:
        location_name = hoverData['points'][0]['text']

    # Make size of marker respond to map hover
    df['size'] = 12
    df.loc[df.location_name == location_name, 'size'] = 30

    return {
        'data': [
            go.Scatter(
                x=df[df['super_region_name'] == i][x_varname],
                y=df[df['super_region_name'] == i][y_varname],
                text=df[df['super_region_name'] == i]['location_name'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': df[df['super_region_name'] == i]['size'],
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.super_region_name.unique()
        ],
        'layout': go.Layout(
            height=400,
            xaxis={'title': x_varname},
            yaxis={'title': y_varname},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


    def write_to_data_uri(s):
        """
        Writes to a uri.
        Use this function to embed javascript into the dash app.
        Adapted from the suggestion by user 'mccalluc' found here:
        https://community.plot.ly/t/problem-of-linking-local-javascript-file/6955/2
        """
        uri = (
            ('data:;base64,').encode('utf8') +
            urlsafe_b64encode(s.encode('utf8'))
        ).decode("utf-8", "strict")
        return uri

    # Get parentDomain
    # Define JS func "sendMessageToParent"
    app.scripts.append_script({
        'external_url': write_to_data_uri("""
    var parentDomain = '';

    window.addEventListener('message',function(event) {
       console.log('message received from parent:  ' + event.data,event);
       parentDomain = event.data;
    },false);

    function sendMessageToParent(s) {
       console.log("Sending message to parent at ("+parentDomain+") s=" + s);
       parent.postMessage(s,parentDomain);
    }

    alert("Hi");

        """)})

    # Hidden div to store the message/string which will be sent to the parent domain
    # using 'title' to store the message/string because it is easy to get javascript
    # funciton to retrieve the value of the title
    html.Div(
        id='msg_for_parent',
        title='',
        style={'display': 'none'}
        ),

    # Button to execute javascript. Does nothing in the dash world
    html.Button(
        'Click Me',
        id='exec_js',
    ),

    # call back to update the title of the hidden div, i.e. update the message for
    # the parent domain
    # using 'url' as an input but any dash component will do.
    @app.callback(
        dash.dependencies.Output('msg_for_parent', 'title'),
        [dash.dependencies.Input('url', 'pathname')]
        )
    def update_msg_for_parent(pathname):
        msg = "hello from %s" % pathname
        return msg

    # Javascript to message the parent. Or, in more detail, to send the 'title' of
    # the div 'msg_for_parent' to the parent domain.
    #
    # setTimeout is a dirty, dirty hack. Forces the page to wait two seconds before
    # appending this script, by which time "msg_for_parent" and "exec_js" are
    # defined. Without this, there is an error to the effect of "cannot set property
    # onclick of null"
    app.scripts.append_script({
        'external_url': write_to_data_uri("""
    setTimeout(function(){
       $(document).ready(function(){
            document.getElementById("exec_js").onclick = function(){
                var msg = document.getElementById("msg_for_parent").title;
                sendMessageToParent(msg);
            };
        });
    }, 2000);
        """)})

if __name__ == '__main__':
    app.run_server(debug=True)

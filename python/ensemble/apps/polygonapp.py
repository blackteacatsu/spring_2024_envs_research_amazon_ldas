import json
import urllib.request
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import xarray as xr
import plotly.graph_objects as go


# Initialize the app
app = Dash(__name__)

#Load and read the geojson file for Italys regions. 
hydrobasins_lev05_url = "https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson"
with urllib.request.urlopen(hydrobasins_lev05_url) as url:
        jdata = json.loads(url.read().decode())

fig1 = go.Figure()
fig1.update_layout(width=1000,  height=900)
for feature in jdata['features']:
    pts = []
    if feature['geometry']['type'] == 'Polygon':
        pts.extend(feature['geometry']['coordinates'][0])    
        pts.append([None, None])#mark the end of a polygon   
        
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            pts.extend(polyg[0])
            pts.append([None, None])#end of polygon
    elif feature['geometry']['type'] == 'LineString': 
        points.extend(feature['geometry']['coordinates'])
        points.append([None, None])
    else: pass           
    #else: raise ValueError("geometry type irrelevant for map")
    x, y = zip(*pts)
    fig1.add_scatter(x=x, y=y, mode='lines', line_color='#121212', line_width=1.5, showlegend=False)


app.layout = html.Div([
    html.H1(children='Mapping - Forecast Data'),
    html.Hr(),
    #dcc.Slider(min=0, max=len(time) - 1, step=4, value=0, marks={i: format_date(time[i].values) for i in range(len(time))}, id='time_index'),
    html.H2(children='Select your variable below'),
    #dcc.RadioItems(options=list_of_variables, value='Rainf_tavg', id='var-selector'),
    html.H2(children='Depth'),
    dcc.Dropdown(id='profile-selector', className='',
        options=[{'label': '0-10cm', 'value': '0'}, {'label': '10-40cm', 'value': '1' }, 
                 {'label': '40-100cm', 'value': '2'}, {'label': '100-200cm', 'value': '3'}],
        value='0',
        #placeholder='0'
    ),
    html.Hr(),
    dcc.Graph(figure=fig1, id='graph1', clickData=None)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os
st.set_page_config(layout='wide')
st.write("""

# RAPTOR538 Web App @msuatgunerli

##### __*FiveThirtyEight's Historical RAPTOR Ratings*__
""")

dflist = [0]*4
filenames = ['historical_RAPTOR_by_player.csv','historical_RAPTOR_by_team.csv','modern_RAPTOR_by_player.csv','modern_RAPTOR_by_team.csv']
for i in range(4):
    os.chdir('./data')
    dflist[i] = pd.read_csv(filenames[i])
    os.chdir('../')

df_historical = dflist[1]
df_modern = dflist[3]

df = df_historical
df = df.sort_values(by=['season'])
df.astype({'war_total': 'float'})
df['Season'] = (df['season'] - 1).astype(str) + '-' + df['season'].astype(str)
df['Raptor WAR per48'] = 48*df['war_total'] / df['mp']
df['war_total'] = round(df['war_total'].astype('float'),2)

st.sidebar.header('User Input Features')
selection1 = st.sidebar.selectbox('Select Legend',
                                  ['team', 'Season', 'season_type'], key='<selectbox1a>')

container2 = st.sidebar.container()
all2 = st.sidebar.checkbox("Select/Deselect all", key='<checkbox3>')
if all2:
    user_season = container2.multiselect("Select Seasons:", reversed(sorted(list(set(df['Season'])))), reversed(sorted(list(set(df['Season'])))))
else:
    user_season = container2.multiselect("Select Seasons:", reversed(sorted(list(set(df['Season'])))))

if len(user_season) == 0:
    st.markdown(f'<h1 style="color:#ff5454;font-size:18px;">{"Error: Please select a season or multiple seasons."}</h1>', unsafe_allow_html=True)
elif len(user_season) > 0:
    df = df[df['Season'].isin(user_season)]

    def plot(data, x, y, year_id, name_common, mins, selection1):
        if selection1 == 'Season':
            data = data.sort_values(by=selection1)
        elif selection1 != 'Season':
            data = data.sort_values(by=selection1, ascending=False)
        min_slider = st.slider('Minutes Played', min_value=0, max_value=int(df['mp'].max    ()), value=660, key="<slider1a>")
        data = data[data['mp'] >= min_slider]
        if name_common == None:
            data = data
        else:
            data = data[data['player_name'] == name_common]
        
        if mins == None:
            data = data
        else:
            data = data[data['mp'] >= mins]

        fig = px.scatter(data, x=x, y=y,
                         color=selection1, hover_name='player_name', hover_data=['war_total', 'team', 'season_type', 'mp'],
                        labels={'war_total': 'WAR', 'team': 'Team', 'season_type': 'Season Type', 'mp': 'Minutes Played', 'raptor_offense' : 'Offensive Raptor', 'raptor_defense' : 'Defensive Raptor'}, template='plotly_dark')
        fig.update_traces(marker_size=12)
        fig.update_layout(xaxis_title="Offensive RAPTOR Rating", yaxis_title="Defensive RAPTOR Rating", font=dict(family="Courier New, monospace", size=14))

        fig.update_layout(autosize=False, width=1000, height=1000)  
        fig.update_layout(legend_traceorder="reversed")
        fig.layout.xaxis.tickformat = '.2f'
        fig.layout.yaxis.tickformat = '.2f'
        
        fig.add_trace(go.Scatter(x=[0, 0, 25, 25, 0], y=[0, 25, 25, 0, 0],
        fill='tozeroy',mode='lines',line_color= '#7f7f7f', fillcolor = 'rgba(63,193,201,0.2)', opacity = 0.1, showlegend = False))

        fig.add_trace(go.Scatter(x=[0, 0, -25, -25, 0], y=[0, -25, -25, 0, 0],
        fill='tozeroy', mode='lines', line_color='#7f7f7f', fillcolor='rgba(252,95,143,0.2)', opacity=0.1, showlegend = False))
        
        fig.update_yaxes(scaleanchor = "x",scaleratio = 1)
        fig.update_xaxes(showgrid=True, gridwidth=2, gridcolor='#7f7f7f', range = [-17.5, 17.5])
        fig.update_yaxes(showgrid=True, gridwidth=2, gridcolor='#7f7f7f', range = [-17.5, 17.5])
        
        fig.add_annotation(x=12.5,y=13,xref="x",yref="y",text="+ offense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(63,193,201,1)")
        fig.add_annotation(x=12.5,y=12,xref="x",yref="y",text="+ defense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(63,193,201,1)")

        fig.add_annotation(x=12.5,y=-12,xref="x",yref="y",text="+ offense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(63,193,201,1)")
        fig.add_annotation(x=12.5,y=-13,xref="x",yref="y",text="- defense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(252,95,143,1)")

        fig.add_annotation(x=-12.5,y=13,xref="x",yref="y",text="- offense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(252,95,143,1)")
        fig.add_annotation(x=-12.5,y=12,xref="x",yref="y",text="+ defense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(63,193,201,1)")

        fig.add_annotation(x=-12.5,y=-12,xref="x",yref="y",text="- offense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(252,95,143,1)")
        fig.add_annotation(x=-12.5,y=-13,xref="x",yref="y",text="- defense",showarrow=False,font=dict(size=14,color="black"),align="center", borderpad=1,bgcolor="rgba(252,95,143,1)")
        
        fig.update_layout(dict(updatemenus=[dict(type="buttons",direction="left",
        buttons=list([dict(args=["visible", "True"],label="Select All",method="restyle"),dict(args=["visible", 'legendonly'],label="Deselect All",method="restyle")]),
        pad={"r": 10, "t": 10},showactive=False,x=0.518,xanchor="center",y=1.06,yanchor="top"),]))
        fig.update_layout(height = 1100, width = 1100)
        st.plotly_chart(fig)

    plot(data=df[df['mp'] >= 35], x='raptor_offense', y='raptor_defense',
         year_id=None, name_common=None, mins=661, selection1 = selection1)

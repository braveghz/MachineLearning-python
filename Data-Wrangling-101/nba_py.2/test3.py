#!/usr/bin/python
# -*- coding: UTF-8 -*-

# two graphs

import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

knicks = pd.read_csv('csv/New York.csv')
#print knicks  #[77 rows x 37 columns]
spurs =  pd.read_csv('csv/San Antonio.csv')
warriors = pd.read_csv('csv/Golden State.csv')
thunder = pd.read_csv('csv/Oklahoma City.csv')
celtics =  pd.read_csv('csv/Boston.csv')



'''
trace0 = go.Box(
    y=knicks['PASS'],
    name='Knicks',
    boxmean='sd'
)
trace1 = go.Box(
    y=spurs['PASS'],
    name='Spurs',
    boxmean='sd'
)
trace2 = go.Box(
    y=warriors['PASS'],
    name='Warriors',
    boxmean='sd'
)
trace3 = go.Box(
    y=thunder['PASS'],
    name='Thunder',
    boxmean='sd'
)
trace4 = go.Box(
    y=celtics['PASS'],
    name='Celtics',
    boxmean='sd'
)

layout = go.Layout(
    title='Passing Box Plot',
)
data = [trace0, trace1, trace2, trace3, trace4]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)

'''

trace0 = go.Box(
    y=knicks.loc[knicks['WL'] == 'W']['PASS_AST'],
    name='Knicks Wins',
    boxmean='sd'
)
trace1 = go.Box(
    y=knicks.loc[knicks['WL'] == 'L']['PASS_AST'],
    name='Knicks Loss',
    boxmean='sd'
)
trace2 = go.Box(
    y=spurs.loc[spurs['WL'] == 'W']['PASS_AST'],
    name='Spurs Wins',
    boxmean='sd'
)
trace3 = go.Box(
    y=spurs.loc[spurs['WL'] == 'L']['PASS_AST'],
    name='Spurs Loss',
    boxmean='sd'

)
trace4 = go.Box(
    y=warriors.loc[warriors['WL'] == 'W']['PASS_AST'],
    name='Warriors Wins',
    boxmean='sd'
)
trace5 = go.Box(
    y=warriors.loc[warriors['WL'] == 'L']['PASS_AST'],
    name='Warriors Losses',
    boxmean='sd'
)
trace6 = go.Box(
    y=thunder.loc[thunder['WL'] == 'W']['PASS_AST'],
    name='Thunder Wins',
    boxmean='sd'
)
trace7 = go.Box(
    y=thunder.loc[thunder['WL'] == 'L']['PASS_AST'],
    name='Thunder Losses',
    boxmean='sd'
)
trace8 = go.Box(
    y=celtics.loc[celtics['WL'] == 'W']['PASS_AST'],
    name='Celtics Wins',
    boxmean='sd'
)
trace9 = go.Box(
    y=celtics.loc[celtics['WL'] == 'L']['PASS_AST'],
    name='Celtics Lossses',
    boxmean='sd'
)
layout = go.Layout(
    title='Passes per Assist in Wins vs Losses',
)
data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


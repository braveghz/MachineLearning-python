import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd


clippers  = pd.read_csv('csv/LA Clippers.csv')
clippers  = clippers.sort_values(by = 'GAME_DATE', ascending = True)
clippers_rolling = clippers[['GAME_DATE','PTS','TOV','PASS',  'OPEN_SHOTS', 'OPEN_EFG', 'AST',  'PASS_AST']].rolling(5).mean()
clippers_norm = clippers[['GAME_DATE', 'PTS','TOV','PASS',  'OPEN_SHOTS', 'OPEN_EFG', 'AST',  'PASS_AST']]
for c in clippers_norm.columns[1:]:
    clippers_rolling[c] = (clippers_rolling[c] - clippers_norm[c].mean())/clippers_norm[c].std()

print clippers_rolling.head(10)

'''
braveghz@braveghz:~/MachineLearning-python/Data-Wrangling-101/nba_py.2$ python test5.py 
     GAME_DATE       PTS       TOV      PASS  OPEN_SHOTS  OPEN_EFG       AST  \
77  2016-10-27       NaN       NaN       NaN         NaN       NaN       NaN   
76  2016-10-30       NaN       NaN       NaN         NaN       NaN       NaN   
75  2016-10-31       NaN       NaN       NaN         NaN       NaN       NaN   
74  2016-11-02       NaN       NaN       NaN         NaN       NaN       NaN   
73  2016-11-04 -0.705388  0.033424 -0.403622   -0.504550 -0.714018 -0.878286   
72  2016-11-05 -0.672092  0.088895 -0.284434   -0.504550 -0.480817 -0.376102   
71  2016-11-07 -0.239256 -0.077516  0.090155   -0.202852 -0.161093  0.084234   
70  2016-11-09 -0.322493 -0.576750  0.115695   -0.269896 -0.241857  0.209780   
69  2016-11-11  0.126991 -0.965042  0.362583    0.132369  0.037146  0.042385   
68  2016-11-12  0.459943 -0.798631  0.268936    0.065325  0.331470  0.293477   

    PASS_AST  
77       NaN  
76       NaN  
75       NaN  
74       NaN  
73  0.739290  
72  0.083865  
71 -0.178321  
70 -0.261513  
69 -0.006014  
68 -0.237828 
'''
trace = go.Scatter(
    x = clippers_rolling['GAME_DATE'],
    y = clippers_rolling['PASS'],
    name = 'Pass to Assist'
)
trace1 = go.Scatter(
    x = clippers_rolling['GAME_DATE'],
    y = clippers_rolling['PTS'],
    name = 'Points'
)
trace2 = go.Scatter(
    x = clippers_rolling['GAME_DATE'],
    y = clippers_rolling['AST'],
    name = 'Assists'
)
trace3 = go.Scatter(
    x = clippers_rolling['GAME_DATE'],
    y = clippers_rolling['PASS_AST'],
    name = 'PASSES PER ASSIST'
)
data = [trace1,trace2 ,trace3]


layout = go.Layout(
    title  = 'Clippers Offense',
    showlegend=True,
    annotations=[
        dict(
            x='2016-12-20',
            y=-1,
            xref='x',
            yref='y',
            text='Blake Griffin Injury',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-330
        ),
          dict(
            x='2017-01-19',
            y=-1,
            xref='x',
            yref='y',
            text='Chris Paul Injury',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-275
        ),
        dict(
            x='2017-01-24',
            y=-1,
            xref='x',
            yref='y',
            text='Blake Griffin Returns',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-330
        ),
         dict(
            x='2017-02-24',
            y=-1,
            xref='x',
            yref='y',
            text='Chris Paul Returns',
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-330
        )
    ]
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)
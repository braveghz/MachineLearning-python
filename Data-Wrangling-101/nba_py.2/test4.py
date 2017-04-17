import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go


clippers  = pd.read_csv('csv/LA Clippers.csv')
#clippers  = clippers.sort(['GAME_DATE'], ascending = True)
clippers  = clippers.sort_values(by = 'GAME_DATE', ascending = True)
#print clippers.head() #[5 rows x 38 columns]
'''
    Unnamed: 0     Team_ID   Game_ID   GAME_DATE      MATCHUP WL  W  L  W_PCT  \
77        53.0  1610612746  21600017  2016-10-27    LAC @ POR  W  1  0   1.00   
76        52.0  1610612746  21600035  2016-10-30  LAC vs. UTA  W  2  0   1.00   
75        51.0  1610612746  21600045  2016-10-31  LAC vs. PHX  W  3  0   1.00   
74        50.0  1610612746  21600064  2016-11-02  LAC vs. OKC  L  3  1   0.75   
73        49.0  1610612746  21600074  2016-11-04    LAC @ MEM  W  4  1   0.80   

    MIN   ...    DAYS_REST   PASS  FG2M  FG2_PCT  OPEN_SHOTS  COVERED_SHOTS  \
77  240   ...          NaN  301.0  21.0    4.047        41.0           50.0   
76  240   ...          3.0  275.0  22.0    4.757        34.0           48.0   
75  240   ...          1.0  276.0  28.0    4.795        38.0           42.0   
74  240   ...          2.0  302.0  24.0    2.893        33.0           54.0   
73  240   ...          2.0  300.0  17.0    2.681        41.0           44.0   

    OPEN_EFG  COVERED_EFG   PASS_AST  RESULT  
77  0.463415     0.440000  25.083333     1.0  
76  0.558824     0.375000  16.176471     1.0  
75  0.565789     0.511905  13.142857     1.0  
74  0.424242     0.435185  13.727273     0.0  
73  0.451220     0.397727  15.789474     1.0  
'''

clippers_rolling = clippers[['GAME_DATE','PTS','TOV','PASS',  'OPEN_SHOTS', 'OPEN_EFG', 'AST',  'PASS_AST']].rolling(5).mean()
print clippers_rolling.head(10)


'''
braveghz@braveghz:~/MachineLearning-python/Data-Wrangling-101/nba_py.2$ python test4.py 

     GAME_DATE    PTS   TOV   PASS  OPEN_SHOTS  OPEN_EFG   AST   PASS_AST
77  2016-10-27    NaN   NaN    NaN         NaN       NaN   NaN        NaN
76  2016-10-30    NaN   NaN    NaN         NaN       NaN   NaN        NaN
75  2016-10-31    NaN   NaN    NaN         NaN       NaN   NaN        NaN
74  2016-11-02    NaN   NaN    NaN         NaN       NaN   NaN        NaN
73  2016-11-04  100.0  12.8  290.8        37.4  0.492698  18.2  16.783881
72  2016-11-05  100.4  13.0  293.6        37.4  0.514649  20.6  14.392215
71  2016-11-07  105.6  12.4  302.4        39.2  0.544745  22.8  13.435492
70  2016-11-09  104.6  10.6  303.0        38.8  0.537143  23.4  13.131921
69  2016-11-11  110.0   9.2  308.8        41.2  0.563405  22.6  14.064244
68  2016-11-12  114.0   9.8  306.6        40.8  0.591110  23.8  13.218349

'''
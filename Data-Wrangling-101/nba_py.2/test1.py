#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
from nba_py import team

#print "-----------test-----------"

#-----------------
'''
knicks = team.TeamPassTracking(1610612752)
#the dataframe.head(N) command returns the first N rows of a dataframe
print knicks.passes_made().head(10)
'''

#-----------------
'''
knicks_last_game = team.TeamPassTracking(1610612752, last_n_games =  1)
print knicks_last_game.passes_made().head(10)
'''

#-----------------

knicks_id = 1610612752
knicks_shots = team.TeamShotTracking(knicks_id, last_n_games =  1)
knicks_shots.closest_defender_shooting() #最近的防守射击
#print knicks_shots.closest_defender_shooting()


#-----------------

df_grouped = knicks_shots.closest_defender_shooting()

df_grouped['OPEN'] = df_grouped['CLOSE_DEF_DIST_RANGE'].map(lambda x : True if 'Open' in x else False)
##This creates a new column  OPEN,  mapped from the 'CLOSE_DEF_DIST_RANGE' column.
df_grouped
#print df_grouped

#-----------------

total_open_shots  = df_grouped.loc[df_grouped['OPEN'] == True, 'FGA'].sum()  #fga 投射次数
print total_open_shots  #36

# We definitely have all the information we need to compute this 
# for open and covered shots:

# eFG% (Effective Field Goal Percentage)	有效的投射百分比
#Mapping the formula above into a column:
open_efg = (df_grouped.loc[df_grouped['OPEN']== True, 'FGM'].sum() + (.5 * df_grouped.loc[df_grouped['OPEN']== True, 'FG3M'].sum()))/(df_grouped.loc[df_grouped['OPEN']== True, 'FGA'].sum())
covered_efg = (df_grouped.loc[df_grouped['OPEN']== False, 'FGM'].sum() + (.5 * df_grouped.loc[df_grouped['OPEN']== False, 'FG3M'].sum()))/(df_grouped.loc[df_grouped['OPEN']== False, 'FGA'].sum())

print open_efg
print covered_efg


#----------------

#let's look at a single game the Knicks played on Sunday, January 29th:

date = '2017-01-29'
knicks_jan = team.TeamShotTracking(knicks_id, date_from = date, date_to =  date)
knicks_jan_shots =  knicks_jan.closest_defender_shooting()
# print knicks_jan_shots  #FGA == Knicks shot a total of 128


#----------------
#Hitting another endpoint
knicks_log = team.TeamGameLogs(knicks_id)

# print knicks_log.info()  #[82 rows x 27 columns]



#-----------------
df_game_log = knicks_log.info()

df_game_log['GAME_DATE']=pd.to_datetime(df_game_log['GAME_DATE'])  ##converting the columns datatype

df_game_log['DAYS_REST'] = df_game_log['GAME_DATE']- df_game_log['GAME_DATE'].shift(-1)

#print df_game_log.head() #[5 rows x 28 columns]

#print df_game_log.dtypes
#-----------------

#We have the information we need, but it's not the right data type. To switch it back:
df_game_log['DAYS_REST'] =  df_game_log['DAYS_REST'].astype('timedelta64[D]')
#print df_game_log.dtypes
#-----------------

#print df_game_log.head()

#-----------------
#Get the dates from the game logs and pass them into the other functions:

dates = df_game_log['GAME_DATE']

print len(dates) #82

#-----------------
#We have the first date, so now to get the relevant passing and shot info we need:
date = dates[2] ##picking a random date
game_info = team.TeamPassTracking(knicks_id, date_from =date, date_to = date).passes_made()
game_info['GAME_DATE'] = date
#print "game info", game_info

#-----------------
##Sum everything by GAME_DATE, similar to SQL-style aggregation/groupby:
df_sum = game_info.groupby(['GAME_DATE']).sum()
#print df_sum
#-----------------
print "############################"
df_sum.reset_index(level =  0,  inplace =  True)
#print df_sum

#-----------------

#When we merge this row back up to the bigger dataframe, we can drop the columns we don't need.
shot_info = team.TeamShotTracking(knicks_id, date_from = date, date_to = date).closest_defender_shooting()
#print shot_info

#-----------------
#From  earlier
shot_info['OPEN'] = shot_info['CLOSE_DEF_DIST_RANGE'].map(lambda  x: True if 'Open' in x else False)
df_sum['OPEN_SHOTS'] = shot_info.loc[shot_info['OPEN']== True, 'FGA'].sum()
df_sum['OPEN_EFG'] = (shot_info.loc[shot_info['OPEN']== True, 'FGM'].sum() + (.5 * shot_info.loc[shot_info['OPEN']== True, 'FG3M'].sum()))/(shot_info.loc[shot_info['OPEN']== True, 'FGA'].sum())
df_sum['COVERED_EFG']= (shot_info.loc[shot_info['OPEN']== False, 'FGM'].sum() + (.5 * shot_info.loc[shot_info['OPEN']== False, 'FG3M'].sum()))/(shot_info.loc[shot_info['OPEN']== False, 'FGA'].sum())

#print df_sum
#-----------------
#Now to append the columns we need back up. This is going to work like a SQL left-join.
df_custom_boxscore  =  pd.merge(df_game_log, df_sum[['PASS', 'FG2M', 'OPEN_SHOTS' ,'OPEN_EFG', 'COVERED_EFG']], how = 'left', left_on = df_game_log['GAME_DATE'],  right_on =  df_sum['GAME_DATE'])
#print df_custom_boxscore.head(10) #[10 rows x 33 columns]

#-----------------


df_custom_boxscore['PASS_AST'] = df_custom_boxscore['PASS'] / df_custom_boxscore['AST']

#It's easier to work with dichotomos variables as binaries instead of letters
df_custom_boxscore['RESULT'] = df_custom_boxscore['WL'].map(lambda x: 1 if 'W' in x else 0)

#print df_custom_boxscore


#-----------------

def custom_boxscore(roster_id):
    game_logs  = team.TeamGameLogs(roster_id)

    df_game_logs = game_logs.info()

    df_game_logs['GAME_DATE'] =  pd.to_datetime(df_game_logs['GAME_DATE'])
    df_game_logs['days_rest'] =  df_game_logs['GAME_DATE'] - df_game_logs['GAME_DATE'].shift(-1)
    df_game_logs['days_rest'] =  df_game_logs['days_rest'].astype('timedelta64[D]')

    ##Just like before, that should get us the gamelogs we need and the rest days column

    ##Now to loop through the list of dates for our other stats

    ##Build up a  dataframe of our custom stats and join that to the gamelogs instead of joining  each individual row

    df_all =pd.DataFrame() ##blank dataframe

    dates = df_game_logs['GAME_DATE']

    for date in dates:

        game_info = team.TeamPassTracking(roster_id,  date_from=date, date_to=date).passes_made()
        game_info['GAME_DATE'] = date ## We need to append the date to this so we can  join back

        temp_df = game_info.groupby(['GAME_DATE']).sum()
        temp_df.reset_index(level =  0,  inplace =  True)

        ##now to get the shot info. For the most part, we're just reusing code we've already written
        open_info =  team.TeamShotTracking(roster_id,date_from =date,  date_to =  date).closest_defender_shooting()
        open_info['OPEN'] = open_info['CLOSE_DEF_DIST_RANGE'].map(lambda x: True if 'Open' in x else False)

        temp_df['OPEN_SHOTS'] = open_info.loc[open_info['OPEN'] == True, 'FGA'].sum()
        temp_df['COVERED_SHOTS'] = open_info.loc[open_info['OPEN'] == False, 'FGA'].sum()

        if open_info.loc[open_info['OPEN']== True, 'FGA'].sum() > 0:
            temp_df['OPEN_EFG']= (open_info.loc[open_info['OPEN']== True, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== True, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== True, 'FGA'].sum())
        else:
             temp_df['OPEN_EFG'] = 0

        if open_info.loc[open_info['OPEN']== False, 'FGA'].sum() > 0:
             temp_df['COVER_EFG']= (open_info.loc[open_info['OPEN']== False, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== False, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== False, 'FGA'].sum())
        else:
            temp_df['COVER_EFG'] = 0
        ##append this to our bigger dataframe

        df_all = df_all.append(temp_df)

    df_boxscore =  pd.merge(df_game_logs, df_all[['PASS', 'FG2M', 'FG2_PCT', 'OPEN_SHOTS','COVERED_SHOTS', 'OPEN_EFG', 'COVER_EFG']], how = 'left', left_on = df_game_logs['GAME_DATE'], right_on = df_all['GAME_DATE'])
    df_boxscore['PASS_ASSIST'] = df_boxscore['PASS'] /  df_boxscore['AST']
    df_boxscore['RESULT'] = df_boxscore['WL'].map(lambda x: 1 if 'W' in x else 0 )

    return df_boxscore

df_knicks_box_scores = custom_boxscore(knicks_id)

#-----------------



#-----------------


#-----------------



#-----------------


#-----------------



#-----------------


#-----------------



#-----------------


#-----------------


#-----------------



#-----------------



#-----------------


#-----------------
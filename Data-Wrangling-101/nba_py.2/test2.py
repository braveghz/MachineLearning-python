#!/usr/bin/python
# -*- coding: UTF-8 -*-

import nba_py
import time
import sys
import os
import pandas as pd
from nba_py import team

teams =  nba_py.Scoreboard()
df_teams = pd.concat([teams.east_conf_standings_by_day()[['TEAM','TEAM_ID']], teams.west_conf_standings_by_day()[['TEAM','TEAM_ID']]])
#print df_teams.head()'

def make_log_folder():
    #make parent's folder
    path='csv_log/'
    if not os.path.exists(path):
        print 'Creating the csv_log folder ... Completed'
        os.mkdir(path)


# get the data for each team. 
# You might have to run the code above piece by piece, or just use the CSVs here:
def game_summary_teams(roster_ids, team_names):
    print "----------------------game_summary_teams------------------- "

    print "[i]begin print roster_ids and team_names------------------- "
    print roster_ids, team_names
    print "[i]end print roster_ids and team_names------------------- "

    for i in range (0, len(roster_ids)):
        #time.sleep(35)
        print roster_ids[i]
        print team_names[i]

        info = team.TeamGameLogs(roster_ids[i])
        df = info.info()
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
        df['DAYS_REST'] = df['GAME_DATE'] - df['GAME_DATE'].shift(-1) ##this gives us our days rest column
        df['DAYS_REST'] = df['DAYS_REST'].astype('timedelta64[D]')

        vals  = df['GAME_DATE']

        df_passes =  pd.DataFrame()
        for v in vals:
            #time.sleep(.5)
            ##these values are  being over-written each time
            print 'GAME FOR' +  team_names[i] + ' for ' + str(v)
            game_info = team.TeamPassTracking(roster_ids[i], date_from =v, date_to = v).passes_made()
            time.sleep(5)

            game_info['EVENT_DATE'] = v
            df_sum = game_info.groupby(['EVENT_DATE']).sum()
            df_sum.reset_index(level = 0, inplace =  True)

            open_info = team.TeamShotTracking(roster_ids[i], date_from =v, date_to = v).closest_defender_shooting()
            time.sleep(5)
            open_info['OPEN'] = open_info['CLOSE_DEF_DIST_RANGE'].map(lambda  x: True if 'Open' in x else False)
            df_sum['OPEN_SHOTS'] = open_info.loc[open_info['OPEN']== True, 'FGA'].sum()
            df_sum['COVERED_SHOTS'] = open_info.loc[open_info['OPEN']== False, 'FGA'].sum()

            ##gotta figure out a better divide by 0 fix.
            if (open_info.loc[open_info['OPEN']== True, 'FGA'].sum() > 0):
                df_sum['OPEN_EFG']= (open_info.loc[open_info['OPEN']== True, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== True, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== True, 'FGA'].sum())
            else:
                df_sum['OPEN_EFG'] = 0

            if (open_info.loc[open_info['OPEN']== False, 'FGA'].sum() > 0):
                df_sum['COVERED_EFG']= (open_info.loc[open_info['OPEN']== False, 'FGM'].sum() + (.5 * open_info.loc[open_info['OPEN']== False, 'FG3M'].sum()))/(open_info.loc[open_info['OPEN']== False, 'FGA'].sum())
            else:
                df_sum['COVERED_EFG']=0
            df_passes = df_passes.append(df_sum)

            info = pd.merge(df, df_passes[['PASS', 'FG2M', 'FG2_PCT','OPEN_SHOTS', 'OPEN_EFG','COVERED_SHOTS', 'COVERED_EFG']], how = 'left',left_on = df['GAME_DATE'], right_on = df_passes['EVENT_DATE'])
            info['PASS_AST'] = info['PASS']/info['AST']

            info['RESULT'] = info['WL'].map(lambda x: 1 if 'W' in x else 0 )

            print "[i]------------------info-----------------"
            #print info

            file_name = team_names[i]
            print "[i]-------------team_names", i, "-----------", team_names[i]

            print "[i]-------------file_name---------------", file_name

            '''
            write_file='csv_log/'+str(file_name)+'.csv'
            log_file = open(write_file,'w+')
            log_file.write(info)
            '''
            #info.to_csv(file_name, index =  False)  #导出到csv文件
teams = df_teams['TEAM']
roster_ids = df_teams['TEAM_ID']

def main():
    print "------------------------------main-------------------------"
    make_log_folder()
    game_summary_teams(roster_ids, teams)

if __name__ == '__main__':
    main()

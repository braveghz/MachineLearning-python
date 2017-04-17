---
title: Data Wrangling 101-Using Python to Fetch, Manipulate & Visualize NBA Data
tags:
- MachineLearning
- python
---

# Data Wrangling 101 - 使用Python来获取，操作和可视化NBA数据

[原文链接](http://blog.yhat.com/posts/visualize-nba-pipelines.html)

这是一个基本的教程，使用pandas和其他几个软件包来构建一个简单的datapipe来获取NBA数据。即使本教程是使用NBA数据完成的，你也不需要成为NBA球迷---2333。相同的概念和技术可以应用于您选择的任何项目。

在Python or R中有一些经验的初学者使用的一般教程。

### Step One: What data do we need?
任何数据项目的第一步是了解您想要的内容。我们将通过game来获得NBA数据的team level。这些team level统计数据通常存在于不同的地方，使得他们难比较。我们的目标是在team level建立box scores以简易比较。希望这将有助于了解球队在赛季中的发挥如何变化，或者使得更容易做任何其他类型的分析。

### Next step: Where is the data coming from?
stats.nba.com拥有所有的NBA数据，但困难的是找到一种快速的方式来获取和操作它需要的形式。
*分析很有趣，但它周围的一切都很难2333* 

我们要使用nba_py包 [nba_py](https://github.com/seemethere)
插一句
```py
git clone https://github.com/seemethere/nba_py.git
cd nba_py/
sudo pip install .
```
让我们来了解 what we're working with.

首先导入我们需要的软件包：

```py
import pandas as pd
from nba_py import team
```

让我们看看传递的数据是如何工作的：
```py
class nba_py.team.TeamPassTracking(
    team_id, 
    measure_type='Base',
    per_mode='PerGame', 
    plus_minus='N',
    pace_adjust='N',
    rank='N', 
    league_id='00', 
    season='2016-17', 
    season_type='Regular Season', 
    po_round='0', 
    outcome='', 
    location='', 
    month='0', 
    season_segment='', 
    date_from='', 
    date_to='', 
    opponent_team_id='0', 
    vs_conference='', 
    vs_division='', 
    game_segment='',
    period='0', 
    shot_clock_range='', 
    last_n_games='0')

passes_made() passes_recieved()

```

```py
knicks = team.TeamPassTracking(1610612752)
```
All the info is stored in the knicks object:

```py
#the dataframe.head(N) command returns the first N rows of a dataframe
knicks.passes_made().head(10)
```

TEAM_ID	 队id
TEAM_NAME 队名
PASS_TYPE  ？ made
G	Games	参与的比赛场数
PASS_FROM
PASS_TEAMMATE_PLAYER_ID	
FREQUENCY
PASS 
AST
FGM
FGA  Field Goal Attempts	投射次数
FG_PCT FG%--Field Goal Percentage	投球命中次数
FG2M
FG2A	
FG2_PCT	FG3M
FG3A	
FG3_PCT

```py
knicks_last_game = team.TeamPassTracking(1610612752, last_n_games =  1)
knicks_last_game.passes_made().head(10)
```

```py
knicks_id = 1610612752
knicks_shots = team.TeamShotTracking(knicks_id, last_n_games =  1)


knicks_shots.closest_defender_shooting()



-----
### 可视化

这些可视化将在Plotly中完成，因为我认为它是最好的vizualiation库，可以快速，轻松地制作视觉上的applea和互动图形，但是可以随意使用别的东西（尽管我不能想象你为什么会这样 ）。
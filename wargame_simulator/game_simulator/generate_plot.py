import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import pandas as pd



def generate_plot(games, username_x, username_y):
    df = pd.DataFrame.from_records(games.values())

    stats_df = df.describe().reset_index(drop = False).\
                    drop(index=0).round(2)

    number_of_games = df.shape[0]

    win_count = df.groupby('winner').count().\
                    reset_index(drop = False)['id'].to_list()
  
    # Summary Table
    fig = go.Figure(data=[
                        go.Table(
                        header = dict(values = ['Statisitics', 'Number of Rounds',
                                             'Number of War Rounds'],
                                    fill_color = 'paleturquoise',
                                    align = 'left',
                                    font_size = 20,
                                    height = 50),
                        cells = dict(values = [stats_df['index'], 
                                           stats_df.number_of_rounds,
                                           stats_df.number_of_war_rounds],
                                fill_color = 'lavender',
                                align = 'left',
                                font_size = 20,
                                height = 50)
                        )
                    ])
    stats_table = plot(fig, output_type = 'div')

    # pie chart of winner
    fig = go.Figure(data=[
                        go.Pie(labels = [username_x, username_y],
                               values = win_count)
                        ]
                    )
                            
    fig.update_traces(title_font_size = 30,
                      title_text = "Chance of Winning",
                      textfont_size = 25,
                      marker = dict(colors= ['lightgreen', 'darkorange'],
                                  line=dict(color='#000000', width=2)))
    pie_chart_wins = plot(fig, output_type = 'div')

    # histogram for number of rounds played
    fig = px.histogram(df, x = "number_of_rounds",
                       title = "Distribution of Number of Rounds",
                       labels = {'number_of_rounds':'number of rounds'}
                       )
    fig.update_layout(
                title = "Distribution of Number of Total Rounds",
                xaxis_title = "Number of Total Rounds",
                yaxis_title = "Game Count",
                font = dict(
                    family = "Courier New, monospace",
                    size = 18,
                    color = "Black"
                )
            )
    histogram_number_of_rounds = plot(fig, output_type = 'div')

    # histogram for number of ward rounds
    fig = px.histogram(df, x = "number_of_war_rounds",
                       labels = {'number_of_war_rounds':'number of war rounds'},
                       color_discrete_sequence = ['indianred'])
    fig.update_layout(
                    title = "Distribution of Number of War Rounds",
                    xaxis_title = "Number of War Rounds",
                    yaxis_title = "Game Count",
                    font = dict(
                        family = "Courier New, monospace",
                        size = 18,
                        color = "Black"
                    )
                )
    histogram_number_of_war_rounds = plot(fig, output_type = 'div')

    # scatter plot for war rounds vs total rounds
    fig = px.scatter(df, x = "number_of_rounds", 
                     y = "number_of_war_rounds", 
                     trendline = "ols",
                     trendline_color_override = 'orange'
                )
    
    fig.update_layout(
                    title = "Number of War Rounds VS Total Round",
                    xaxis_title = "Number of Total Rounds in a game",
                    yaxis_title = "Number of War Rounds",
                    legend_title = "Legend Title",
                    font = dict(
                        family = "Courier New, monospace",
                        size = 18,
                        color = "Black"
                    )
                )   
    scatter_plot_round = plot(fig, output_type = 'div')

    return number_of_games, stats_table, pie_chart_wins, histogram_number_of_rounds, \
            histogram_number_of_war_rounds, scatter_plot_round
      
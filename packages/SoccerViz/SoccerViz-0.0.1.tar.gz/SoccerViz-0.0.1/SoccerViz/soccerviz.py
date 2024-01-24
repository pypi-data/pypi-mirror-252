#import libraries
import re
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import matplotlib.patheffects as path_effects
from mplsoccer import VerticalPitch, Pitch, FontManager
from highlight_text import ax_text

#function to extract passing data
def extract_pass_data(url,HEADERS):
    response = requests.get(url)
    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
    else:
        response = requests.get(url, headers=HEADERS)
        html = BeautifulSoup(response.text, 'html.parser')

    # Define your regex pattern accurately to match the data you want
    regex_pattern = r'(?<=require\.config\.params\["args"\].=.)[\s\S]*?;'
    data_txt = re.findall(regex_pattern, str(html))[0]

    # Clean up the text if necessary
    data_txt = data_txt.replace('matchId', '"matchId"')
    data_txt = data_txt.replace('matchCentreData', '"matchCentreData"')
    data_txt = data_txt.replace('matchCentreEventTypeJson', '"matchCentreEventTypeJson"')
    data_txt = data_txt.replace('formationIdNameMappings', '"formationIdNameMappings"')
    data_txt = data_txt.replace('};', '}')
    data = data_txt
    data = json.loads(data)

    # Access the JSON data as needed
    event_types_json = data["matchCentreData"]
    formation_mappings = data["formationIdNameMappings"]
    events_dict = data["matchCentreData"]["events"]
    teams_dict = {
        data["matchCentreData"]['home']['teamId']: data["matchCentreData"]['home']['name'],
        data["matchCentreData"]['away']['teamId']: data["matchCentreData"]['away']['name']
    }
    players_dict = data["matchCentreData"]["playerIdNameDictionary"]

    # Create players DataFrame
    players_home_df = pd.DataFrame(data["matchCentreData"]['home']['players'])
    players_home_df["teamId"] = data["matchCentreData"]['home']['teamId']
    players_away_df = pd.DataFrame(data["matchCentreData"]['away']['players'])
    players_away_df["teamId"] = data["matchCentreData"]['away']['teamId']
    players_df = pd.concat([players_home_df, players_away_df])

    events = events_dict

    df = pd.DataFrame(events)

    # Create 'eventType' column based on 'type' key if available, else set it to 'Unknown'
    df['eventType'] = df.apply(lambda row: row['type']['displayName'] if 'type' in row else 'Unknown', axis=1)

    # Create 'outcomeType' column based on 'outcomeType' key if available, else set it to 'Unknown'
    df['outcomeType'] = df.apply(lambda row: row['outcomeType']['displayName'] if 'outcomeType' in row else 'Unknown',
                                 axis=1)

    # Filter only passes
    passes_ids = df.index[df['eventType'] == 'Pass']
    df_passes = df.loc[
        passes_ids, ["id", "x", "y", "endX", "endY", "teamId", "playerId", "eventType", "outcomeType", "minute"]]

    return df_passes

#function to extract players dataframe
def extract_player_data(url, HEADERS):
    response = requests.get(url)
    if response.status_code == 200:
        html = BeautifulSoup(response.text, 'html.parser')
    else:
        response = requests.get(url, headers=HEADERS)
        html = BeautifulSoup(response.text, 'html.parser')

    # Define your regex pattern accurately to match the data you want
    regex_pattern = r'(?<=require\.config\.params\["args"\].=.)[\s\S]*?;'
    data_txt = re.findall(regex_pattern, str(html))[0]

    # Clean up the text if necessary
    data_txt = data_txt.replace('matchId', '"matchId"')
    data_txt = data_txt.replace('matchCentreData', '"matchCentreData"')
    data_txt = data_txt.replace('matchCentreEventTypeJson', '"matchCentreEventTypeJson"')
    data_txt = data_txt.replace('formationIdNameMappings', '"formationIdNameMappings"')
    data_txt = data_txt.replace('};', '}')
    data = data_txt
    data = json.loads(data)

    # Access the JSON data as needed
    event_types_json = data["matchCentreData"]
    formation_mappings = data["formationIdNameMappings"]
    events_dict = data["matchCentreData"]["events"]
    teams_dict = {
        data["matchCentreData"]['home']['teamId']: data["matchCentreData"]['home']['name'],
        data["matchCentreData"]['away']['teamId']: data["matchCentreData"]['away']['name']
    }
    players_dict = data["matchCentreData"]["playerIdNameDictionary"]

    # Create players DataFrame
    players_home_df = pd.DataFrame(data["matchCentreData"]['home']['players'])
    players_home_df["teamId"] = data["matchCentreData"]['home']['teamId']
    players_away_df = pd.DataFrame(data["matchCentreData"]['away']['players'])
    players_away_df["teamId"] = data["matchCentreData"]['away']['teamId']
    players_df = pd.concat([players_home_df, players_away_df])

    events = events_dict

    df = pd.DataFrame(events)

    # Create 'eventType' column based on 'type' key if available, else set it to 'Unknown'
    df['eventType'] = df.apply(lambda row: row['type']['displayName'] if 'type' in row else 'Unknown', axis=1)

    # Create 'outcomeType' column based on 'outcomeType' key if available, else set it to 'Unknown'
    df['outcomeType'] = df.apply(lambda row: row['outcomeType']['displayName'] if 'outcomeType' in row else 'Unknown',
                                 axis=1)

    # Filter only passes
    passes_ids = df.index[df['eventType'] == 'Pass']
    df_passes = df.loc[
        passes_ids, ["id", "x", "y", "endX", "endY", "teamId", "playerId", "eventType", "outcomeType", "minute"]]

    return players_df


#function to prep and filter the data extracted
def prep_data(df, players_df, home_team_id, away_team_id):
    df = df
    df1 = df

    # differentiating data for 2 teams
    teamid = home_team_id
    df = df[df['teamId'] == teamid]
    df['passer'] = df['playerId']
    df['reciever'] = df['playerId'].shift(-1)
    passes = df[df['eventType'] == 'Pass']
    successful = df[df['outcomeType'] == 'Successful']
    teamid1 = away_team_id
    df1 = df1[df1['teamId'] == teamid1]
    df1['passer'] = df1['playerId']
    df1['reciever'] = df1['playerId'].shift(-1)
    passes1 = df1[df1['eventType'] == 'Pass']
    successful1 = df1[df1['outcomeType'] == 'Successful']

    # filtering passes to player and successful
    passes = passes.merge(players_df[["playerId", "name"]], on='playerId', how='left')
    passes1 = passes1.merge(players_df[["playerId", "name"]], on='playerId', how='left')
    successful = successful.merge(players_df[["playerId", "isFirstEleven"]], on='playerId', how='left')
    successful = successful[successful['isFirstEleven'] == True]
    successful1 = successful1.merge(players_df[["playerId", "isFirstEleven"]], on='playerId', how='left')
    successful1 = successful1[successful1['isFirstEleven'] == True]

    # avg_locations filter
    avg_loc = successful.groupby('playerId').agg({'x': ['mean'], 'y': ['mean', 'count']})
    avg_loc.columns = ['x', 'y', 'count']
    avg_loc = avg_loc.merge(players_df[['playerId', 'name', 'shirtNo', 'position']], on='playerId', how='left')
    avg_loc1 = successful1.groupby('playerId').agg({'x': ['mean'], 'y': ['mean', 'count']})
    avg_loc1.columns = ['x', 'y', 'count']
    avg_loc1 = avg_loc1.merge(players_df[['playerId', 'name', 'shirtNo', 'position']], on='playerId', how='left')

    # passes in between players filter
    pass_between = successful.groupby(['passer', 'reciever']).id.count().reset_index()
    pass_between.rename({'id': 'pass_count'}, axis='columns', inplace=True)
    pass_between = pass_between.merge(avg_loc, left_on='passer', right_on='playerId')
    pass_between = pass_between.merge(avg_loc, left_on='reciever', right_on='playerId',
                                      suffixes=['', '_end'])
    pass_between1 = successful1.groupby(['passer', 'reciever']).id.count().reset_index()
    pass_between1.rename({'id': 'pass_count'}, axis='columns', inplace=True)
    pass_between1 = pass_between1.merge(avg_loc1, left_on='passer', right_on='playerId')
    pass_between1 = pass_between1.merge(avg_loc1, left_on='reciever', right_on='playerId',
                                        suffixes=['', '_end'])
    # filtering for more than 3 passing combinations
    pass_between = pass_between[pass_between['pass_count'] > 3]
    pass_between1 = pass_between1[pass_between1['pass_count'] > 3]

    passes['beginning'] = np.sqrt(np.square(100 - passes['x']) + np.square(50 - passes['y']))
    passes['end'] = np.sqrt(np.square(100 - passes['endX']) + np.square(50 - passes['endY']))
    passes['progressive'] = [(passes['end'][x]) / (passes['beginning'][x]) < .75 for x in range(len(passes.beginning))]
    df_prg = passes[passes['progressive'] == True]
    df_comp_prg = df_prg[df_prg['outcomeType'] == 'Successful']
    df_uncomp_prg = df_prg[df_prg['outcomeType'] == 'Unsuccessful']

    passes1['beginning'] = np.sqrt(np.square(100 - passes1['x']) + np.square(50 - passes1['y']))
    passes1['end'] = np.sqrt(np.square(100 - passes1['endX']) + np.square(50 - passes1['endY']))
    passes1['progressive'] = [(passes1['end'][x]) / (passes1['beginning'][x]) < .75 for x in
                              range(len(passes1.beginning))]
    df_prg1 = passes1[passes1['progressive'] == True]
    df_comp1_prg = df_prg1[df_prg1['outcomeType'] == 'Successful']
    df_uncomp1_prg = df_prg1[df_prg1['outcomeType'] == 'Unsuccessful']

    return pass_between, pass_between1, avg_loc, avg_loc1, passes, passes1, df_prg, df_comp_prg, df_uncomp_prg, df_prg1, df_comp1_prg, df_uncomp1_prg

#function to plot the pass network plot
def pass_network_plot(pass_between, pass_between1, avg_loc, avg_loc1, team1_name, team2_name):
    # Specify the URL or local path to the Oswald font file
    oswald_font_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"

    # Create the FontManager instance
    oswald_regular = FontManager(oswald_font_url)

    TEAM1 = team1_name
    TEAM2 = team2_name

    # Define your parameters
    MAX_LINE_WIDTH = 500
    MAX_MARKER_SIZE = 1500
    MIN_TRANSPARENCY = 0.0

    # Calculate line width and marker size based on your data
    pass_between['width'] = (pass_between.pass_count / pass_between.pass_count.max() * MAX_LINE_WIDTH)
    avg_loc['marker_size'] = (avg_loc['count'] / avg_loc['count'].max() * MAX_MARKER_SIZE)

    # Calculate color and transparency
    color = np.array(to_rgba('black'))
    color = np.tile(color, (len(pass_between), 1))
    c_transparency = pass_between.pass_count / pass_between.pass_count.max()
    c_transparency = (c_transparency * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color[:, 3] = c_transparency

    # Create a VerticalPitch object
    pitch = VerticalPitch(
        pitch_type="opta",
        pitch_color="white",
        line_color="black",
        linewidth=1,
    )

    fig, axs = pitch.grid(ncols=2, title_height=0.08, endnote_space=0,
                          # Turn off the endnote/title axis. I usually do this after
                          # I am happy with the chart layout and text placement
                          axis=False,
                          title_space=0, grid_height=0.82, endnote_height=0.05)

    # Plot the pass network
    arrows = pitch.arrows(
        pass_between.x,
        pass_between.y,
        pass_between.x_end,
        pass_between.y_end,
        lw=c_transparency,
        color=color,
        zorder=2,
        ax=axs['pitch'][0],
    )
    pass_nodes = pitch.scatter(
        avg_loc.x,
        avg_loc.y,
        color="red",
        edgecolors="black",
        s=avg_loc.marker_size,
        linewidth=0.5,
        alpha=1,
        ax=axs['pitch'][0],
    )

    for index, row in avg_loc.iterrows():
        text = pitch.annotate(
            row.shirtNo,
            xy=(row.x, row.y),
            c="white",
            va="center",
            ha="center",
            size=12,
            weight="bold",
            ax=axs['pitch'][0],
            fontproperties=oswald_regular.prop,
        )
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground="yellow")])

    # 2nd Team Pass Network Plots Start

    # Define your parameters
    MAX_LINE_WIDTH = 500
    MAX_MARKER_SIZE = 1500
    MIN_TRANSPARENCY = 0.0

    # Calculate line width and marker size based on your data
    pass_between1['width'] = (pass_between1.pass_count / pass_between1.pass_count.max() * MAX_LINE_WIDTH)
    avg_loc1['marker_size'] = (avg_loc1['count'] / avg_loc1['count'].max() * MAX_MARKER_SIZE)

    # Calculate color and transparency
    color1 = np.array(to_rgba('black'))
    color1 = np.tile(color1, (len(pass_between1), 1))
    c_transparency1 = pass_between1.pass_count / pass_between1.pass_count.max()
    c_transparency1 = (c_transparency1 * (1 - MIN_TRANSPARENCY)) + MIN_TRANSPARENCY
    color1[:, 3] = c_transparency1

    # Plot the pass network
    arrows = pitch.arrows(
        pass_between1.x,
        pass_between1.y,
        pass_between1.x_end,
        pass_between1.y_end,
        lw=c_transparency1,
        color=color1,
        zorder=2,
        ax=axs['pitch'][1],
    )
    pass_nodes = pitch.scatter(
        avg_loc1.x,
        avg_loc1.y,
        color="blue",
        edgecolors="black",
        s=avg_loc1.marker_size,
        linewidth=0.5,
        alpha=1,
        ax=axs['pitch'][1],
    )

    for index, row in avg_loc1.iterrows():
        text = pitch.annotate(
            row.shirtNo,
            xy=(row.x, row.y),
            c="white",
            va="center",
            ha="center",
            size=12,
            weight="bold",
            ax=axs['pitch'][1],
            fontproperties=oswald_regular.prop,
        )
        text.set_path_effects([path_effects.withStroke(linewidth=1, foreground="black")])

    # Add labels to the pass networks
    highlight_text = [{'color': 'red', 'fontproperties': oswald_regular.prop},
                      {'color': 'blue', 'fontproperties': oswald_regular.prop}]
    ax_text(0.5, 0.7, f"<{TEAM1}> & <{TEAM2}> Pass Networks", fontsize=28, color='#000009',
            fontproperties=oswald_regular.prop, highlight_textprops=highlight_text,
            ha='center', va='center', ax=axs['title'])
    axs["endnote"].text(
        1,
        1,
        "@athalakbar13",
        color="black",
        va="center",
        ha="right",
        fontsize=20,
        fontproperties=oswald_regular.prop,
    )
    plt.show()

#function to plot the progressive passes of both the teams
def prg_passes_plot(df_comp_prg, df_uncomp_prg, df_comp1_prg, df_uncomp1_prg, team1_name, team2_name):
    # Specify the URL or local path to the Oswald font file
    oswald_font_url = "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"

    # Create the FontManager instance
    oswald_regular = FontManager(oswald_font_url)

    TEAM1 = team1_name
    TEAM2 = team2_name
    # Set up the pitch
    pitch = Pitch(pitch_type='opta', pitch_color='white', line_color='black')
    fig, axs = pitch.grid(nrows=2, ncols=2, title_height=0.08, endnote_space=0,
                          # Turn off the endnote/title axis. I usually do this after
                          # I am happy with the chart layout and text placement
                          axis=False,
                          title_space=0, grid_height=0.82
                          , endnote_height=0.05)
    fig.set_facecolor('white')

    # Plot the completed passes
    pitch.lines(df_comp_prg.x, df_comp_prg.y,
                df_comp_prg.endX, df_comp_prg.endY, comet=True, color='green', ax=axs['pitch'][0, 0],
                label='completed passes', alpha=0.35)

    pitch.scatter(df_comp_prg.endX, df_comp_prg.endY, color='green', s=100, ax=axs['pitch'][0, 0], alpha=0.5)
    pitch.lines(df_uncomp_prg.x, df_uncomp_prg.y,
                df_uncomp_prg.endX, df_uncomp_prg.endY, comet=True, color='red', ax=axs['pitch'][0, 1],
                label='unsuccessful passes', alpha=0.35)
    pitch.scatter(df_uncomp_prg.endX, df_uncomp_prg.endY, color='red', s=100, ax=axs['pitch'][0, 1], alpha=0.5)
    highlight_text = [{'color': 'green', 'fontproperties': oswald_regular.prop},
                      {'color': 'red', 'fontproperties': oswald_regular.prop}]
    ax_text(0.5, 0.7, f"{TEAM1} <Successful> Prg Passes & <Unsuccessful> Prg Passes v. {TEAM2}", fontsize=25,
            color='#000009',
            fontproperties=oswald_regular.prop, highlight_textprops=highlight_text,
            ha='center', va='center', ax=axs['title'])

    pitch.lines(df_comp1_prg.x, df_comp1_prg.y,
                df_comp1_prg.endX, df_comp1_prg.endY, comet=True, color='green', ax=axs['pitch'][1, 0],
                label='completed passes', alpha=0.35)

    pitch.scatter(df_comp1_prg.endX, df_comp1_prg.endY, color='green', s=100, ax=axs['pitch'][1, 0], alpha=0.5)
    pitch.lines(df_uncomp1_prg.x, df_uncomp1_prg.y,
                df_uncomp1_prg.endX, df_uncomp1_prg.endY, comet=True, color='red', ax=axs['pitch'][1, 1],
                label='unsuccessful passes', alpha=0.35)
    pitch.scatter(df_uncomp1_prg.endX, df_uncomp1_prg.endY, color='red', s=100, ax=axs['pitch'][1, 1], alpha=0.5)
    highlight_text = [{'color': 'green', 'fontproperties': oswald_regular.prop},
                      {'color': 'red', 'fontproperties': oswald_regular.prop}]
    ax_text(0.5, -5.25, f"{TEAM2} <Successful> Prg Passes & <Unsuccessful> Prg Passes v. {TEAM1}", fontsize=25,
            color='#000009',
            fontproperties=oswald_regular.prop, highlight_textprops=highlight_text,
            ha='center', va='center', ax=axs['title'])

    axs["endnote"].text(
        1,
        1,
        "@athalakbar13",
        color="black",
        va="center",
        ha="right",
        fontsize=20,
        fontproperties=oswald_regular.prop,
    )
    plt.show()
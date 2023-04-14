import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import urllib.request
from PIL import Image


def nation_wise_participation(fifa: pd.DataFrame):
    """
    This function returns a bar plot of the top 20 nations with the highest number of players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A bar plot of the top 20 nations with the highest number of players in the FIFA game.
    """
    nat_cnt = fifa.groupby('Nationality').apply(lambda x: x['Name'].count()).reset_index(name='Counts')
    nat_cnt.sort_values(by='Counts', ascending=False, inplace=True)
    top_20_nat_cnt = nat_cnt[:20]
    fig = px.bar(top_20_nat_cnt, x='Nationality', y='Counts', color='Counts',
                 title='Nation-wise Distribution of Players in FIFA for Top 20 Nations')
    return fig


def nation_over_performing_players(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the Nationwise Player counts and Average Potential
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the Nationwise Player counts and Average Potential
    """
    cnt_best_avg = fifa.groupby('Nationality').apply(lambda x: np.average(x['OVA'])).reset_index(name='Overall Ratings')
    cnt_best_cnt = fifa.groupby('Nationality').apply(lambda x: x['OVA'].count()).reset_index(name='Player Counts')
    snt_best_avg_cnt = pd.merge(cnt_best_avg, cnt_best_cnt, how='inner', left_on='Nationality', right_on='Nationality')
    sel_best_avg_cnt = snt_best_avg_cnt[snt_best_avg_cnt['Player Counts'] >= 200]
    sel_best_avg_cnt.sort_values(by=['Overall Ratings', 'Player Counts'], ascending=[False, False])
    fig = px.scatter(sel_best_avg_cnt, x='Overall Ratings', y='Player Counts', color='Player Counts',
                     size='Overall Ratings', hover_data=['Nationality'],
                     title='Overall Nationwise Player counts and Average Potential')
    return fig


def club_wise_player(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the Clubwise Player counts in FIFA 21
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the Clubwise Player counts in FIFA 21
    """
    clb_cnt = fifa.groupby('Club').apply(lambda x: x['Name'].count()).reset_index(name='Counts')
    clb_cnt.sort_values(by='Counts', ascending=False, inplace=True)
    top_20_clb_cnt = clb_cnt[:20]
    fig = px.bar(top_20_clb_cnt, x='Club', y='Counts', color='Counts',
                 title='Club-wise Distribution of Players in FIFA for Top 20 Clubs')
    return fig


def club_wise_over_performing_players(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the Clubwise Player counts and Average Potential
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the Clubwise Player counts and Average Potential
    """
    cnt_best_avg = fifa.groupby('Club').apply(lambda x: np.average(x['OVA'])).reset_index(name='Overall Ratings')
    cnt_best_cnt = fifa.groupby('Club').apply(lambda x: x['OVA'].count()).reset_index(name='Player Counts')
    snt_best_avg_cnt = pd.merge(cnt_best_avg, cnt_best_cnt, how='inner', left_on='Club', right_on='Club')
    sel_best_avg_cnt = snt_best_avg_cnt[snt_best_avg_cnt['Player Counts'] >= 25]
    sel_best_avg_cnt.sort_values(by=['Overall Ratings', 'Player Counts'], ascending=[False, False])
    fig = px.scatter(sel_best_avg_cnt, x='Overall Ratings', y='Player Counts', color='Player Counts',
                     size='Overall Ratings', hover_data=['Club'],
                     title='Overall Clubwise player counts and Average Potential')
    return fig


## player stats

def height_vs_weight_variation(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the Height vs Weight Variation of the players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the Height vs Weight Variation of the players in the FIFA game.
    """
    props = fifa[['Name', 'Nationality', 'Club', 'Height', 'Weight']]
    props['Ht in ft'] = pd.to_numeric(props['Height'].str[0])
    props['Ht in in'] = pd.to_numeric(props['Height'].str.split("\'").str[1].str.strip('"'))
    props['Ht in cm'] = (props['Ht in ft'] * 12 + props['Ht in in']) * 2.54
    props['Weight in lb'] = pd.to_numeric(props['Weight'].str.strip('lbs'))
    fig = px.scatter(props, x='Weight in lb', y='Ht in cm', color='Ht in cm', size='Weight in lb',
                     hover_data=['Name', 'Nationality', 'Club'],
                     title='Overall Height vs Weight Variation of the players in FIFA 21')
    return fig


def players_position(fifa: pd.DataFrame):
    """
    This function returns a bar plot of the top 20 positions with the highest number of players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A bar plot of the top 20 positions with the highest number of players in the FIFA game.
    """
    pos_cnt = fifa.groupby('BP').apply(lambda x: x['Name'].count()).reset_index(name='Counts')
    pos_cnt.sort_values(by='Counts', ascending=False, inplace=True)
    top_20_pos_cnt = pos_cnt[:20]
    fig = px.bar(top_20_pos_cnt, x='BP', y='Counts', color='Counts', title='Top 20 Position-wise Player counts in FIFA')
    return fig


def age_distribution(fifa: pd.DataFrame):
    """
    This function returns a histogram of the Age distribution of the players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A histogram of the Age distribution of the players in the FIFA game.
    """
    age_cnt = fifa.groupby('Age').apply(lambda x: x['Name'].count()).reset_index(name='Counts')
    fig = px.bar(age_cnt, x='Age', y='Counts', color='Counts', title='Agewise Player distribution in FIFA')
    return fig


def distibution_of_market_value_and_wage(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the Market Value and Wage distribution of the players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the Market Value and Wage distribution of the players in the FIFA game.
    """
    cost_prop = fifa[['Name', 'Club', 'Nationality', 'Wage', 'Value', 'BP']]
    cost_prop['MultW'] = np.where(cost_prop.Wage.str[-1] == 'K', 1000, 1)
    cost_prop['Wage'] = cost_prop.Wage.str.strip('K')
    cost_prop['Wage'] = cost_prop.Wage.str.strip('€')
    cost_prop['Wage'] = pd.to_numeric(cost_prop['Wage'])
    cost_prop['Wage in €'] = cost_prop['Wage'] * cost_prop['MultW']
    cost_prop['MultV'] = np.where(cost_prop.Value.str[-1] == 'K', 1000,
                                  np.where(cost_prop.Value.str[-1] == 'M', 1000000, 1))
    cost_prop['Value'] = cost_prop.Value.str.strip('€')
    cost_prop['Value'] = cost_prop.Value.str.strip('K')
    cost_prop['Value'] = cost_prop.Value.str.strip('M')
    cost_prop['Value'] = pd.to_numeric(cost_prop['Value'])
    cost_prop['Value in €'] = cost_prop['Value'] * cost_prop['MultV']
    fig = px.scatter(cost_prop, x='Value in €', y='Wage in €', color='Value in €', size='Wage in €',
                     hover_data=['Name', 'Club', 'Nationality', 'BP'],
                     title='Value vs Wage Presentation of all the Players')
    return fig


def best_players(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the top 100 players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the top 100 players in the FIFA game.
    """
    top_play = fifa[['Name', 'OVA', "Age", 'Club', 'BP']]
    top_play.sort_values(by='OVA', ascending=False, inplace=True)
    top_30_play = top_play[:100]
    fig = px.scatter(top_30_play, x='Age', y='OVA', color='Age', size='OVA', hover_data=['Name', 'Club', 'BP'],
                     title='Top Football Players in the FIFA 21')
    return fig


def highest_potential(fifa: pd.DataFrame):
    """
    This function returns a scatter plot of the top 50 players with the highest potential in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A scatter plot of the top 50 players with the highest potential in the FIFA game.
    """
    cond_1 = fifa['OVA'] != fifa['POT']
    cond_2 = fifa['Age'] < 25
    fifa_fil = fifa[cond_1 & cond_2]
    pot_play = fifa_fil[['Name', 'Age', 'Nationality', 'Club', 'POT', 'BP', 'OVA', 'Value', 'Release Clause']]
    pot_play.sort_values(by='POT', ascending=False, inplace=True)
    top_pot_play = pot_play[:50]
    fig = px.scatter(top_pot_play, x='Age', y='POT', size='POT', color='Age',
                     hover_data=['Name', 'Age', 'Nationality', 'BP', 'OVA', 'Value', 'Release Clause'],
                     title='Age vs Maximum Potential Distribution of the young Players')
    return fig


def overall_attributes(fifa: pd.DataFrame):
    """
    This function returns a radar plot of the overall attributes of the players in the FIFA game.
    :param fifa: The dataframe containing the FIFA game data
    :return: A radar plot of the overall attributes of the players in the FIFA game.
    """
    pos_head = fifa.groupby('BP').apply(lambda x: np.average(x['Heading Accuracy'])).reset_index(
        name='Heading Accuracy')
    pos_sp = fifa.groupby('BP').apply(lambda x: np.average(x['Short Passing'])).reset_index(name='Short Passing')
    pos_d = fifa.groupby('BP').apply(lambda x: np.average(x['Dribbling'])).reset_index(name='Dribbling')
    pos_c = fifa.groupby('BP').apply(lambda x: np.average(x['Curve'])).reset_index(name='Curve')
    pos_fk = fifa.groupby('BP').apply(lambda x: np.average(x['FK Accuracy'])).reset_index(name='FK Accuracy')
    pos_lp = fifa.groupby('BP').apply(lambda x: np.average(x['Long Passing'])).reset_index(name='Long Passing')
    pos_bc = fifa.groupby('BP').apply(lambda x: np.average(x['Ball Control'])).reset_index(name='Ball Control')
    pos_ss = fifa.groupby('BP').apply(lambda x: np.average(x['Sprint Speed'])).reset_index(name='Sprint Speed')
    pos_spo = fifa.groupby('BP').apply(lambda x: np.average(x['Shot Power'])).reset_index(name='Shot Power')
    pos_jm = fifa.groupby('BP').apply(lambda x: np.average(x['Jumping'])).reset_index(name='Jumping')

    pos_overall1 = pd.merge(pos_head, pos_sp, how='inner', left_on='BP', right_on='BP')
    pos_overall2 = pd.merge(pos_d, pos_c, how='inner', left_on='BP', right_on='BP')
    pos_overall3 = pd.merge(pos_fk, pos_lp, how='inner', left_on='BP', right_on='BP')
    pos_overall4 = pd.merge(pos_bc, pos_ss, how='inner', left_on='BP', right_on='BP')
    pos_overall5 = pd.merge(pos_spo, pos_jm, how='inner', left_on='BP', right_on='BP')
    pos_overall11 = pd.merge(pos_overall1, pos_overall2, how='inner', left_on='BP', right_on='BP')
    pos_overall22 = pd.merge(pos_overall3, pos_overall4, how='inner', left_on='BP', right_on='BP')
    pos_overall12 = pd.merge(pos_overall11, pos_overall22, how='inner', left_on='BP', right_on='BP')
    pos_overall = pd.merge(pos_overall12, pos_overall5, how='inner', left_on='BP', right_on='BP')

    pos_overall_long = pos_overall.melt(id_vars=['BP'], var_name='Attribute', value_name='Value')

    fig = px.line_polar(
        pos_overall_long,
        r='Value',
        theta='Attribute',

        animation_frame='BP',
        line_close=True,
    )
    fig.update_traces(fill='toself')
    fig.update_layout(
        width=600,
        height=600,

        title="Overall Attributes of the Players in FIFA 21",
        title_x=0.5,
        title_y=0.97,
        title_xanchor='center',
        title_yanchor='top',

        polar=dict(radialaxis=dict(range=[13, 80])))
    return fig


def get_similar_players(fifa: pd.DataFrame, player_name: str):
    normalized_data = fifa
    normalized_data = normalized_data.drop(columns=['Age', 'Nationality', 'Club', 'Value',
            'Wage', 'Joined','Release Clause','Height', 'Weight', 'Name','Goalkeeping', 'GK Diving', 'GK Handling',
            'GK Kicking', 'GK Positioning', 'GK Reflexes','Player Photo','Club Logo','Flag Photo','ID', 'OVA', 'BOV',
            'BP', 'Position','POT', 'Team & Contract', 'foot', 'Growth', 'Loan Date End', 'Contract','W/F', 'SM', 'A/W',
            'D/W', 'IR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Hits', 'LS','ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
            'LAM', 'CAM', 'RAM', 'LM','LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM', 'CDM', 'RDM', 'RWB', 'LB',
            'LCB', 'CB', 'RCB', 'RB', 'GK', 'Gender','Total Stats', 'Base Stats','Vision'
            ],axis=1)
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(normalized_data)
    normalized_data.loc[:,:] = scaled_values
    normalized_data['Name'] = fifa['Name']
    col_name = "Name"
    first_col = normalized_data.pop(col_name)
    normalized_data.insert(0, col_name, first_col)
    player_index = [list(normalized_data['Name']).index(x) for x in list(normalized_data['Name']) if player_name in x]
    player_index = int(player_index[0])
    df = normalized_data.iloc[:,1:]
    cos = cosine_similarity(df, df)
    player_cos = sorted(list(cos[player_index]))[-4:-1]
    indexes = [list(cos[player_index]).index(x) for x in player_cos]
    indexes.append(player_index)
    nor_data= normalized_data.iloc[indexes].melt(id_vars=['Name'], var_name='Attribute', value_name='Value')
    images = []
    for img in fifa.iloc[indexes]['Player Photo'].values:
        img = img.split('/')
        img[2] = 'cdn.sofifa.net'
        images.append('/'.join(img))
    fig = px.line_polar(
            nor_data,
            color='Name',
            r='Value',
            theta='Attribute',


            line_close=True,
        )
    x_intercept = [0.1,0.1,0.9,0.9]
    y_intercept = [0.0,0.8,0.0,0.8]
    for i in range(4):
        url = images[i]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        with open('1.png', 'wb') as f:
            f.write(response.read())

        pic = Image.open("1.png")
        fig.add_layout_image(
            dict(
                source=pic,
                x=x_intercept[i],
                y=y_intercept[i],
            ))
    fig.update_layout_images(dict(
        xref="paper",
        yref="paper",
        sizex=0.3,
        sizey=0.3,
        xanchor="right",
        yanchor="bottom"
    ))
    return fig

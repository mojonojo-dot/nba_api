from wrapper_functions.helper_functions.get_team_info import get_team_info
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.library.parameters import SeasonTypePlayoffs
from nba_api.stats.library.parameters import SeasonID
import pandas as pd

game_id_dict = {}

def get_game_ids(team_id=None, season=None, season_type=None):
        # Define teams
        if team_id is None:
            team_info = get_team_info()
            team_ids = team_info['id']
        else:
            team_ids = team_id

        # Define season
        if season is None:
            season_code = Season.default
        else:
            season_code  = '{}-{}'.format(season, str(season + 1)[2:])

        # Define Season Type
        if season_type is None:
            season_seg = SeasonType.regular
        elif season_type == 'Pre-Season':
            season_seg = SeasonType.preseason
        elif season_type == 'Regular':
            season_seg = SeasonType.regular
        elif season_type == 'Playoffs':
            season_seg = SeasonTypePlayoffs.playoffs
            

        for team in team_ids:
            gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team,
                                                        season_nullable=season_code,
                                                        season_type_nullable=season_seg)
            game_info_dict0 = gamefinder.get_normalized_dict()
            game_info_dict1 = game_info_dict0['LeagueGameFinderResults']
            game_info_df = pd.DataFrame(game_info_dict1)
            game_id_list = list(game_info_df['GAME_ID'])
            game_id_dict[team] = game_id_list
            
        # extract unique dictionary values
        ll = list(game_id_dict.values())
        l = [item for sublist in ll for item in sublist]
        return(list(set(l)))
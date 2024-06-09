import pandas as pd

def get_last_matches(team: str, home: bool, matches: pd.DataFrame, date: pd.Timestamp, amount: int) -> pd.DataFrame:
    if home:
        return matches[(matches['HomeTeam'] == team) & (matches['Date'] < date)].tail(amount)
    else:
        return matches[(matches['AwayTeam'] == team) & (matches['Date'] < date)].tail(amount)
    
def get_last_matches_stats(last_matches: pd.DataFrame, home: bool) -> pd.Series:
    if home:
        label = 'H'
        goals = 'FTHG'
        halftime_goals = 'HTHG'
        shots = 'HS'
        shots_on_target = 'HST'
    else:
        label = 'A'
        goals = 'FTAG'
        halftime_goals = 'HTAG'
        shots = 'AS'
        shots_on_target = 'AST'

    stats = {
        'Wins': (last_matches['FTR'] == label).sum(),
        'Draws': (last_matches['FTR'] == 'D').sum(),
        'HalfTimeWins': (last_matches['HTR'] == label).sum(),
        'HalfTimeDraws': (last_matches['HTR'] == 'D').sum(),
        'AvgGoals': last_matches[goals].mean() if not last_matches.empty else 0,
        'AvgHalfTimeGoals': last_matches[halftime_goals].mean() if not last_matches.empty else 0,
        'AvgShots': last_matches[shots].mean() if not last_matches.empty else 0,
        'AvgShotsOnTarget': last_matches[shots_on_target].mean() if not last_matches.empty else 0
    }
    
    return pd.Series(stats)

def get_last_season_standing(team: str, standings: pd.DataFrame, season: int) -> int:
    last_season = season - 1
    standing = standings[(standings['Team'] == team) & (standings['Season_End_Year'] == last_season)]
    return standing['Rk'].iloc[0] if not standing.empty else 18

def get_season(date: pd.Timestamp) -> int:
    return date.year if date.month < 7 else date.year + 1

def get_match_stats(row: pd.Series, matches: pd.DataFrame, standings: pd.DataFrame, amount: int) -> dict:
    date = row['Date']
    season = get_season(date)
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    
    home_matches = get_last_matches(home_team, True, matches, date, amount)
    away_matches = get_last_matches(away_team, False, matches, date, amount)
    
    home_matches_stats = get_last_matches_stats(home_matches, True)
    away_matches_stats = get_last_matches_stats(away_matches, False)
    
    home_standing = get_last_season_standing(home_team, standings, season)
    away_standing = get_last_season_standing(away_team, standings, season)
    standing_diff = home_standing - away_standing
    
    match_stats = {
        'Season': season,
        'Date': date,
        'HomeTeam': home_team,
        'AwayTeam': away_team,
        'FTR': row['FTR'],
        'HomeGoals': row['FTHG'],
        'AwayGoals': row['FTAG'],
        'HTR': row['HTR'],
        'HalfTimeHomeGoals': row['HTHG'],
        'HalfTimeAwayGoals': row['HTAG'],
        'StandingDiff': standing_diff
    }
    
    for key in home_matches_stats.index:
        match_stats[f'Home{key}'] = home_matches_stats[key]
        match_stats[f'Away{key}'] = away_matches_stats[key]
    
    return match_stats


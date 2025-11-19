# =============================================================================
# DOMAIN
# Functions to create and access player data
# =============================================================================

def create_player(name, nationality, points, tournaments):  
    return {
        'name': name,
        'nationality': nationality,
        'points': points,
        'tournaments': tournaments
    }

def get_name(player):
    return player['name']

def get_nationality(player):
    return player['nationality']

def get_points(player):
    return player['points']

def get_tournaments(player):
    return player['tournaments']

def set_points(player, new_points):
    player['points'] = new_points

def set_tournaments(player, new_tournaments):
    player['tournaments'] = new_tournaments

def to_str(player):
    return (f"{get_name(player)}, {get_nationality(player)}, "
            f"{get_points(player)} points, {get_tournaments(player)} tournaments")

import json
from pong.server.match import PongMatch
from pong.socket_utils import sendall_json
from pong.settings import RequestCodes as r_code

request_funcs = {}


def request(code):
    def wrapper(func):
        request_funcs[code] = func
        def wrapper1(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper1

    return wrapper
 
def handle_request(server, conn, addr, body):
    request = {
        "server": server,
        "conn": conn,
        "addr": addr,
        "body": body,
    }
    
    request_handler = request_funcs[body["code"]]
    response = request_handler(request, **body["params"])

    sendall_json(conn, response)

@request(code=r_code.CREATE_MATCH)
def create_match(request):
    """ 
    Create a match in server.

    request body: {}
    response body:
        match_id: str,
        player_id: str
        is_host: bool
    """
    matchs = request["server"].matchs
    match = matchs.create_custom_match()
    player = match.add_player(1000, 10)

    return {
        "match_id": match.match_id,
        "player_id": player.id, 
        "is_host": player.is_host
    }

@request(code=r_code.CONNECT_MATCH)
def connect_match(request, match_id):
    """
    Connect to a match in server

    request body: 
        match_id: str

    response body: 
        match_id: str
        player_id: str
        is_host: bool
    """
    matchs = request["server"].matchs

    if match_id == None:
        match = matchs.get_random_match()
    else:
        match = matchs.get_match_by_id(match_id)

    player = match.add_player(100, 10)

    return {
        "match_id": match.match_id,
        "player_id": player.id,
        "is_host": player.is_host
    }


@request(code=r_code.DISCONNECT_GAME)
def disconnect_game(request, player_id, match_id):
    pass

@request(code=r_code.IS_PLAYABLE)
def is_playable(request, match_id):
    """
    Return if an match is playable

    request body: 
        match_id: str

    response body:
        is_playable: bool
    """
    matchs = request["server"].matchs
    match = matchs.get_match_by_id(match_id)
    return {"is_playable" : match.is_playable}

@request(code=r_code.UPDATE_GAME)
def update_game(request, match_id, player_id, 
                player_pos, ball_pos, score):
    """ 
    Update game in server

    request body:
        match_id: str
        player_id: str
        player_pos: (int, int)
        ball_pos: (int, int)
        score: (int, int)

    response body:
        
    """
    matchs = request["server"].matchs
    match = matchs.get_match_by_id(match_id)
    match.update_player(player_id, player_pos)
    if player_id == match.player1.id:
        match.update_ball(*ball_pos)
        match.update_score(*score)

    return match.get_response(player_id)

@request(code=r_code.MATCH_LIST)
def get_match_list(request):
    """ 
    Return an list of server matchs

    request body:
    
    response body:
        matchs: list
            id: str
            name: str
    
    """
    match_list = []
    matchs = request["server"].matchs
    for i, match in enumerate(matchs.custom_matchs):
        if not match.is_playable:
            match_list.append({
                "match_id": match.match_id,
                "match_name": f"partida {i}"
            })

    return {"match_list": match_list}
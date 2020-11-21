import uuid 

class PongPlayer():
    def __init__(self, host, port, posx, posy, is_host):
        self.host = host
        self.port = port 
        self.id = str(uuid.uuid1())
        self.posx = posx
        self.posy = posy
        self.is_host = is_host

    @property
    def pos(self):
        return (self.posx, self.posy)

    def update_position(self, posx, posy):
        self.posx = posx
        self.posy = posy

class PongMatch():
    matchs = {}

    def __init__(self):
        self.match_id = str(uuid.uuid1())
        self.ball_pos = (0.5, 0.5)
        self.player1 = None
        self.player2 = None
        self.score = (0, 0)
        self.dx = 5
        self.dy = 5
        self.is_playable = False
        self.matchs[self.match_id] = self
        self.is_closed = False

    def get_response(self, player_id):
        player2 = self.player2
        if player_id != self.player1.id:
            player2 = self.player1

        return {
            "ball_pos": self.ball_pos,
            "other_player_pos": player2.pos,
            "score": self.score
        }

    def add_player(self, player_host, player_port):
        if self.player1 is None:
            self.player1 = PongPlayer(player_host, player_port, posx=0, posy=0.5, is_host=True)
            return self.player1
        elif self.player2 is None:
            self.player2 = PongPlayer(player_host, player_host, posx=1, posy=0.5, is_host=False)
            self.is_playable = True
            return self.player2
        else:
            raise Exception("game can't have more than 2 players")
    
    def update_ball(self, posx, posy):
        self.ball_pos = (posx, posy)

    def update_score(self, player_1_score, player_2_score):
        self.score = (player_1_score, player_2_score)

    def update_player(self, player_id, player_pos):
        if player_id == self.player1.id:
            self.player1.update_position(*player_pos)
        elif player_id == self.player2.id:
            self.player2.update_position(*player_pos)
        else:
            raise Exception(f"player with id {player_id} doen't exist in match {self.match_id}")

    def close(self):
        self.is_closed = True

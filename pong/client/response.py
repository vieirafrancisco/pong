import json
from dataclasses import dataclass

@dataclass
class Response():
    other_player_pos: tuple
    ball_pos: tuple
    score: tuple

    def encode(self):
        return b'{"other_player_pos": (%d, %d), \
                 "ball_pos": (%d, %d)}' % \
                  (self.other_player_pos[0], self.other_player_pos[1],
                   self.ball_pos[0], self.ball_pos[1])


    def decode(self, string):
        resp = json.dumps(string)
        return Response(**resp)
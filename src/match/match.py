from match.judge import judge
from events import Event
class Match:
    def __init__(self,game_id,map_id,player_ids):
        self.players=player_ids
        self.game_id=game_id
        self.map_id=map_id

    def hold(self, first_team_name: str, second_team_name: str)->[Event]:
        return judge(players=self.players,map_id=self.map_id,game_id=self.game_id, first_team_name, second_team_name)
        
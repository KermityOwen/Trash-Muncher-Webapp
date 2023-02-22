from trashusers.models import Player, GameKeeper, User

def get_player_team(user):
    '''
    Assume is isPlayer permission has been run prior to this.
    Simply returns the team the palyer belongs to
    '''
    player = Player.objects.get(user=user)
    return player.team
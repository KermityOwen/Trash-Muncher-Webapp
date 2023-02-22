from trashusers.models import Player, GameKeeper, User

def get_player_team(user):
    '''
    Assume is isPlayer permission has been run prior to this.
    Simply returns the team the player belongs to.
    Returns None if the player cant be found, should only happen if the isPlayer permission wasn't checked
    '''
    player = Player.objects.get(user=user)
    if player is None:
        return None
    return player.team
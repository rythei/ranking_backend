from peer_rank import *
import trueskill

def updateRatings(teams, skill, subskill, ranking):
    #teams is a list ['team1', 'team2', 'team3']
    #skill is the MAJOR skill we want to rate the players on: i.e. programming
    #subskill is the MINOR skill we want to rate the players on: i.e. Python
    #ranking is the ranking returned from the getRanking function in peer_rank.py
    # load players from the database

    #example of loading players
    p1 = load_player_from_database('team1',skill)
    p2 = load_player_from_database('team2',skill)
    p3 = load_player_from_database('team3',skill)
    p4 = load_player_from_database('team4',skill)
    # calculate new ratings
    rating_groups = [{p1: p1.rating, p2: p2.rating}, {p3: p3.rating}]
    rated_rating_groups = env.rate(rating_groups, ranks=[0, 1]) #impletements trueskill update
    # save new ratings
    for player in [p1, p2, p3]:
        player.rating = rated_rating_groups[player.team][player]

def load_player_from_database(player,skill):
    #this function needs to pull users from the database
    allObs = PlayerSkills.objects.filter(user = player)

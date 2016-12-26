import numpy as np
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import select2.fields
import select2.models
import pickle
from phonenumber_field.modelfields import PhoneNumberField

def getUsersToRank(currentTeam, currentComp):
    #this is an example function of pulling 3 users at random, where user isn't current user (for user to rank)
    availUsers = Team.objects.filter(competition = currentComp)
    availUsers = availUsers.exclude(name = currentTeam) #is "name" the username of the members of the team? or is it a team name?
    availUsers = availUsers.users
    index = np.random.choice(len(availUsers.username), 3, replace = False)
    returnUsers = [availUsers[index[0]],availUsers[index[1]],availUsers[index[2]]]
    return returnUsers

def getProbMatrix(currentComp): #generates a probability matrix for rankings
    #i.e. matrix[i][j] = Prob(i beats j) -- we say i beats j if Prob(i beats j) > .5
    #allObs = PeerRanks.objects.filter(competition = currentComp)
    #allRanks = allObs.peer_ranks #this should be a list of lists with ranked results - i.e. [team1, team3, team2]

    #this is an example of ranks that I'm using for testing, these would actually come from the database in practice (see above code)
    allRanks = [[1,3,2],[1,2,4],[1,3,4],[3,2,4],[2,3,4]]
    teamDict = {0: "team1", 1: "team2", 2: "team3", 3: "team4"}
    allTeams = []
    for i in range(len(allRanks)):
        allTeams = allTeams + allRanks[i]

    uTeams = list(set(allTeams)) #unique team submissions
    denMatrix = [[0 for i in range(len(uTeams))] for j in range(len(uTeams))]
    numMatrix = [[0 for i in range(len(uTeams))] for j in range(len(uTeams))]

    for i in range(len(allRanks)):
        for j in range(len(uTeams)):
            for k in range(len(uTeams)):
                if(uTeams[j] in allRanks[i] and uTeams[k] in allRanks[i]):
                    denMatrix[j][k] = denMatrix[j][k] + 1
                    if(allRanks[i].index(uTeams[j])< allRanks[i].index(uTeams[k])):
                        numMatrix[j][k] = numMatrix[j][k] + 1

    probMatrix = [[0 for i in range(len(uTeams))] for j in range(len(uTeams))]
    for i in range(len(uTeams)):
        for j in range(len(uTeams)):
            probMatrix[i][j] = float(numMatrix[i][j])/denMatrix[i][j]

    return probMatrix, teamDict

def getRanking(currentComp):
    #implements topolical sorting to get aggregate ranking from the probability matrix
    mat = getProbMatrix(currentComp)
    probMatrix = mat[0]
    teamDict = mat[1]
    graph = []
    for i in range(len(probMatrix)):
        curr = (i,)
        temp = []
        for j in range(len(probMatrix)):
            if(probMatrix[i][j] < .5 and not (i == j)):
                temp.append(j)
        graph.append(curr + (temp,))

    result = topolgical_sort(graph)
    ranking = []
    for i in range(len(result)):
        ranking.append(teamDict[result[i][0]])

    return(ranking)

def topolgical_sort(graph_unsorted):
    #implements topological sort

    graph_sorted = []
    graph_unsorted = dict(graph_unsorted)

    while graph_unsorted:
        acyclic = False
        for node, edges in graph_unsorted.items():
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))

        if not acyclic:
            raise RuntimeError("A cyclic dependency occurred")

    return graph_sorted

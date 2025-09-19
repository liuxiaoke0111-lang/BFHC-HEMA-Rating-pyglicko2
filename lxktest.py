import json
import glicko2

class PlayerData:
    name = "",
    rating = 1500,
    rd = 350,
    games = []

    def __init__(self, name, rating, rd):
        self.name = name
        self.rating = rating
        self.rd = rd

    def getRating(self):
        return self.rating

    def getRd(self):
        return self.rd

    def getName(self):
        return self.name

    def setGames(self, games):
        self.games = games

    def getGames(self):
        return self.games

    def toString(self):
        return "Name: %s\tRating: %i\tRD: %i" % (self.name, self.rating, self.rd)

class Game:
    player1 = ""
    player2 = ""
    score1 = 0
    score2 = 0
    result = 0

    def getPlayer1(self):
        return self.player1
    
    def getPlayer2(self):
        return self.player2
    
    def getResult(self):
        if self.result == 1:
            return 1
        elif self.result == 0:
            return 0.5
        else :
            return 0
    
    def __init__(self, player1, player2, score1, score2, result):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
        self.result = result

    def toString(self):
        resultStr = ""
        if self.result == 1:
            resultStr = self.player1 + " " + "Win" + " " + self.player2 + " " + "Loss"
        elif self.result == 0:
            resultStr = self.player1 + " " + "And" + " " + self.player2 + " " + "Draw"
        else :
            resultStr = self.player2 + " " + "Win" + " " + self.player1 + " " + "Loss"
        return "%s vs %s\t%i-%i\tResult: %s" % (self.player1, self.player2, self.score1, self.score2, resultStr)

def runRating():
    # get players from json
    playerDatas = []
    with open('players.json') as f:
        playersJson = json.load(f)
        players = playersJson['players']
        for player in players:
            name = player['name']
            rating = player['rating']
            rd = player['rd']
            p = PlayerData(name, rating, rd)
            playerDatas.append(p)
    
    print("before rating")
    for player in playerDatas:
        print(player.toString())

    allGames = []
    allGamesData = []
    with open('testdata.json') as f:
        data = json.load(f)
        allGames = data['games']
        for game in allGames:
            allGamesData.append(Game(game['player1'], game['player2'], game['score1'], game['score2'], game['result']))
        for player in playerDatas:
            games = []
            for game in allGames:
                if game['player1'] == player.name or game['player2'] == player.name:
                    g = Game(game['player1'], game['player2'], game['score1'], game['score2'], game['result'])
                    games.append(g)
            player.setGames(games)

    # dictionary
    d = {}

    for player in playerDatas:
        p = glicko2.Player()
        p.rating = player.rating
        p.rd = player.rd
        d[player.getName()] = p
        # print(player.name)
        # for game in player.games:
        #     print(game.toString())

    print("----------------------")

    for gameData in allGamesData:
        if d.has_key(gameData.getPlayer1()) and d.has_key(gameData.getPlayer2()):
            print("match " + gameData.getPlayer1() + " " + gameData.getPlayer2())
            p1Result = gameData.getResult()
            d[gameData.getPlayer1()].update_player([d[gameData.getPlayer2()].getRating()], [d[gameData.getPlayer2()].getRd()], [p1Result])
            p2Result = 0
            if p1Result == 1:
                p2Result = 0
            elif p1Result == 0:
                p2Result = 1
            else:
                p2Result = 0.5
            d[gameData.getPlayer2()].update_player([d[gameData.getPlayer1()].getRating()], [d[gameData.getPlayer1()].getRd()], [p2Result])
            print("update_player " + gameData.getPlayer1() + " " + str(d[gameData.getPlayer1()].getRating()) + " " + str(d[gameData.getPlayer1()].getRd()) + " " + str(gameData.getResult()))
            print("update_player " + gameData.getPlayer2() + " " + str(d[gameData.getPlayer2()].getRating()) + " " + str(d[gameData.getPlayer2()].getRd()) + " " + str(gameData.getResult()))

    print("----------------------")
    print("after rating")
    for playerName in d.keys():
        print(playerName)
        print("rating: " + str(d[playerName].getRating()))
        print("rd: " + str(d[playerName].getRd()))

       

if __name__ == "__main__":
    runRating()
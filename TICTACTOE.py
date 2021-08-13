from flask import Flask, jsonify

from flask_ngrok import run_with_ngrok


class tictactoe:


    def __init__(self, player,opponent):
        self.player = player
        self.opponent = opponent


    def __isMovementleft( self, board ):

        for i in range(3):
            for j in range(3):
                if board[i][j]=="-":
                    return True
        return False

    def __evaluate(self, b):

        for row in range(b)):
            if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
                if (b[row][0] == self.player):
                    return 10
                elif (b[row][0] == self.opponent):
                    return -10




        for column in range(len(b)+2):
            if (b[0][column] == b[1][column] and b[1][column] == b[2][column]):
                if (b[0][column] == self.player):
                    return 10
                elif (b[0][column] == self.opponent):
                    return -10


        if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):
            if b[0][0] == self.player:
                return 10
            elif b[0][0] == self.opponent:
                return -10

        if (b[0][2] == b[1][0] and b[1][1] == b[2][0]):

            if b[0][2] == self.player:
                return 10
            elif b[0][2] == self.opponent:
                return -10
        return 0
    def __minmax(self, board, depth, isMax):

        score = self.__evaluate(board)

        if score == 10:
            return score

        if score == -10:
            return score

        if (self.__isMovementleft(board)) == False:
            return 0

        if(isMax):

            best = -1000
            for i in range(3):
                for j in range(3):

                    if board[i][j] == "-":
                        board[i][j] = self.player

                        best = max(best, self.__minmax(board, depth+1, not isMax))

                        board[i][j] = "-"
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "-":
                        board[i][j] = self.opponent
                        best = min(best, self.__minmax(board, depth+1, not isMax))
                        board[i][j] = "-"
            return best


    def findBestMove(self, board):
        bestval=-1000
        bestMove=(-1,-1)

        for i in range(3):
            for j in range(3):

                if board[i][j]=="-":

                    board[i][j]=self.player

                    moveval= self.__minmax(board, 0, False)

                    board[i][j]="-"

                    if( moveval > bestval ):
                        bestMove = (i, j)
                        bestval = moveval
        print("the value of best move ", bestval)
        print()
        return bestMove , bestval


game=tictactoe("x","o")

board=[["o","x","x"],
       ["o","x","x"],
       ["x","-","-"]]
bestmove , bestval=game.findBestMove(board)
print(bestmove,"  ",bestval)




app=Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def hellow_world():

    return "Hello"

@app.route("/tictactoe.api.hg/<string:s>")
def findmove(s):

    if (len(s)<9 or len(s)>9):
        if len(s)<9:
            return "less number of move"
        else:
            return "large number of move"
    else:
        a1,a2,a3,b1,b2,b3,c1,c2,c3=s
        bo=[[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]]
        bestmove, bestval=game.findBestMove(bo)

        result={
            "move(row,column)":bestmove,
            "bestMoveVal":bestval,
            "Developer":"Hritik"
        }

        return jsonify(result)






if __name__ == "__main__":
    app.run()

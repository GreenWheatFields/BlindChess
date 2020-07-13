from flask import Flask
import chess
import random
import uuid


def testing():
    board = chess.Board()
    board.turn = chess.BLACK
    move = chess.Move.from_uci("g1f4")
    board.push(move)
    print(board.turn)
    for i in board.generate_legal_moves():
        print(i)


def play():
    gameId = uuid.uuid4()
    print(gameId)
    playBoard = chess.Board()
    while not playBoard.is_game_over():
        p = [i for i in playBoard.generate_legal_moves()]
        index = random.randrange(len(p)) - 1
        move = chess.Move.from_uci(str(p[index]))
        playBoard.push(move)
        print(playBoard)
    print(playBoard.result())


if __name__ == '__main__':
    play()

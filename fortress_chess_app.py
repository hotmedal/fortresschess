from flask import Flask, render_template, request, redirect, url_for
import chess
import chess.svg
import os

app = Flask(__name__)
board = chess.Board()
fortress_declared = False
fortress_agreed = False
result = None

@app.route('/')
def index():
    global board, fortress_declared, fortress_agreed, result
    svg_board = chess.svg.board(board, size=400)
    return render_template('index.html', board_svg=svg_board, result=result,
                           fortress_declared=fortress_declared, fortress_agreed=fortress_agreed)

@app.route('/move', methods=['POST'])
def move():
    global board, result
    move_san = request.form.get('move')
    
    if result is not None:
        return redirect(url_for('index'))
    
    try:
        move = board.parse_san(move_san)
        if move in board.legal_moves:
            board.push(move)

            if board.is_checkmate():
                result = "0-1" if board.turn else "1-0"
            elif board.is_stalemate() or board.is_insufficient_material():
                result = "0.5-0.5"
        else:
            return redirect(url_for('index', error="Illegal move."))
    except ValueError:
        return redirect(url_for('index', error="Invalid move format."))
    
    return redirect(url_for('index'))

@app.route('/declare_fortress')
def declare_fortress():
    global fortress_declared
    if not fortress_declared and not board.is_game_over():
        fortress_declared = True
    return redirect(url_for('index'))

@app.route('/agree_fortress')
def agree_fortress():
    global fortress_declared, fortress_agreed, result
    if fortress_declared and not fortress_agreed:
        fortress_agreed = True
        result = "1.5-0"
    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    global board, fortress_declared, fortress_agreed, result
    board.reset()
    fortress_declared = False
    fortress_agreed = False
    result = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

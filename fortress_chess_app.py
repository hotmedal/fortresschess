import streamlit as st
import chess
import chess.svg
from streamlit_drag_and_drop import drag_and_drop

# Initialize board and game state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'fortress_declared' not in st.session_state:
    st.session_state.fortress_declared = False
if 'fortress_agreed' not in st.session_state:
    st.session_state.fortress_agreed = False
if 'result' not in st.session_state:
    st.session_state.result = None

def display_board():
    """Display the chess board as SVG."""
    svg_board = chess.svg.board(st.session_state.board, size=400)
    st.write(svg_board, unsafe_allow_html=True)

def handle_move(source, target):
    """Handle chess moves from drag-and-drop."""
    try:
        move = chess.Move.from_uci(f"{source}{target}")
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)

            # Check for game-ending conditions
            if st.session_state.board.is_checkmate():
                st.session_state.result = "0-1" if st.session_state.board.turn else "1-0"
            elif st.session_state.board.is_stalemate() or st.session_state.board.is_insufficient_material():
                st.session_state.result = "0.5-0.5"
        else:
            st.error("Illegal move.")
    except ValueError:
        st.error("Invalid move format.")

def declare_fortress():
    """Declare the fortress."""
    if not st.session_state.fortress_declared and not st.session_state.board.is_game_over():
        st.session_state.fortress_declared = True

def agree_fortress():
    """Agree to the fortress."""
    if st.session_state.fortress_declared and not st.session_state.fortress_agreed:
        st.session_state.fortress_agreed = True
        st.session_state.result = "1.5-0"

def restart_game():
    """Restart the game."""
    st.session_state.board.reset()
    st.session_state.fortress_declared = False
    st.session_state.fortress_agreed = False
    st.session_state.result = None

# Streamlit UI
st.title("Fortress Chess Game")

# Display the board
display_board()

# Drag-and-drop interface
if 'drag_source' not in st.session_state:
    st.session_state.drag_source = None

# Piece movement
for i in range(8):
    for j in range(8):
        square = chess.square(i, j)
        piece = st.session_state.board.piece_at(square)

        if piece:
            piece_str = piece.symbol() + str(square)
            target_square = f"{chess.square_name(square)}"

            # Drag and Drop functionality
            if st.button(f"Drop {piece_str} on {target_square}", key=target_square):
                if st.session_state.drag_source:
                    handle_move(st.session_state.drag_source, target_square)
                    st.session_state.drag_source = None
                else:
                    st.session_state.drag_source = target_square

# Input for move
move_input = st.text_input("Enter your move (e.g., e4, Nf3):")
if st.button("Make Move"):
    if move_input:
        handle_move(move_input)

# Buttons for fortress actions
if st.button("Declare Fortress"):
    declare_fortress()
st.write(f"Fortress Declared: {st.session_state.fortress_declared}")

if st.button("Agree to Fortress"):
    agree_fortress()
st.write(f"Fortress Agreed: {st.session_state.fortress_agreed}")

# Show result if the game is over
if st.session_state.result is not None:
    st.write(f"Result: {st.session_state.result}")

# Restart button
if st.button("Restart Game"):
    restart_game()
import streamlit as st
import chess
import chess.svg

# Initialize board and game state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'fortress_declared' not in st.session_state:
    st.session_state.fortress_declared = False
if 'fortress_agreed' not in st.session_state:
    st.session_state.fortress_agreed = False
if 'result' not in st.session_state:
    st.session_state.result = None

def display_board():
    """Display the chess board as SVG."""
    svg_board = chess.svg.board(st.session_state.board, size=400)
    st.write(svg_board, unsafe_allow_html=True)

def handle_move(move_san):
    """Handle chess moves."""
    try:
        move = st.session_state.board.parse_san(move_san)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)

            # Check for game-ending conditions
            if st.session_state.board.is_checkmate():
                st.session_state.result = "0-1" if st.session_state.board.turn else "1-0"
            elif st.session_state.board.is_stalemate() or st.session_state.board.is_insufficient_material():
                st.session_state.result = "0.5-0.5"
        else:
            st.error("Illegal move.")
    except ValueError:
        st.error("Invalid move format.")

def declare_fortress():
    """Declare the fortress."""
    if not st.session_state.fortress_declared and not st.session_state.board.is_game_over():
        st.session_state.fortress_declared = True

def agree_fortress():
    """Agree to the fortress."""
    if st.session_state.fortress_declared and not st.session_state.fortress_agreed:
        st.session_state.fortress_agreed = True
        st.session_state.result = "1.5-0"

def restart_game():
    """Restart the game."""
    st.session_state.board.reset()
    st.session_state.fortress_declared = False
    st.session_state.fortress_agreed = False
    st.session_state.result = None

# Streamlit UI
st.title("Fortress Chess Game")

# Display the board
display_board()

# Input for move
move_input = st.text_input("Enter your move (e.g., e4, Nf3):")
if st.button("Make Move"):
    if move_input:
        handle_move(move_input)

# Buttons for fortress actions
if st.button("Declare Fortress"):
    declare_fortress()
st.write(f"Fortress Declared: {st.session_state.fortress_declared}")

if st.button("Agree to Fortress"):
    agree_fortress()
st.write(f"Fortress Agreed: {st.session_state.fortress_agreed}")

# Show result if the game is over
if st.session_state.result is not None:
    st.write(f"Result: {st.session_state.result}")

# Restart button
if st.button("Restart Game"):
    restart_game()


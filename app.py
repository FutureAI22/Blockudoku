import streamlit as st
import random

# Constants
CELL_SIZE = 50
BOARD_SIZE = 9
BLOCK_COLORS = ["lightblue", "lightgreen", "lightcoral", "lightyellow", "lightcyan", "lightsalmon", "plum", "palegreen", "powderblue"]

def create_blockudoku_board():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def generate_blocks():
    blocks = []
    block_shapes = [
        [[1, 1, 1, 1]],
        [[1, 1, 1], [1]],
        [[1, 1, 1], [0, 0, 1]],
        [[1, 1, 1], [0, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 1]],
        [[1], [1], [1]]
    ]
    for _ in range(3):
        blocks.append(random.choice(block_shapes))
    return blocks

def draw_board(board):
    board_html = "<div style='display: grid; grid-template-columns: repeat(9, 50px); border: 2px solid black;'>"
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                board_html += f"<div style='width: 50px; height: 50px; background-color: gray; border: 1px solid black;'></div>"
            else:
                board_html += f"<div style='width: 50px; height: 50px; background-color: white; border: 1px solid black;'></div>"
    board_html += "</div>"
    return board_html

def draw_blocks(blocks):
    blocks_html = "<div style='display: flex;'>"
    for i, block in enumerate(blocks):
        blocks_html += "<div style='margin-right: 20px;'>"
        for r, block_row in enumerate(block):
            block_row_html = "<div style='display: flex;'>"
            for c, cell in enumerate(block_row):
                if cell == 1:
                    block_row_html += f"<div style='width: 50px; height: 50px; background-color: {BLOCK_COLORS[i % len(BLOCK_COLORS)]}; border: 1px solid black;'></div>"
                else:
                    block_row_html += f"<div style='width: 50px; height: 50px;'></div>"
            blocks_html += block_row_html + "</div>"
        blocks_html += "</div>"
    blocks_html += "</div>"
    return blocks_html

def can_place_block(board, block, row, col):
    for r, block_row in enumerate(block):
        for c, cell in enumerate(block_row):
            if cell == 1:
                if row + r >= BOARD_SIZE or col + c >= BOARD_SIZE or board[row + r][col + c] != 0:
                    return False
    return True

def place_block(board, block, row, col):
    for r, block_row in enumerate(block):
        for c, cell in enumerate(block_row):
            if cell == 1:
                board[row + r][col + c] = 1

def clear_lines(board):
    cleared_rows = []
    cleared_cols = []
    for r in range(BOARD_SIZE):
        if all(board[r][c] == 1 for c in range(BOARD_SIZE)):
            cleared_rows.append(r)
    for c in range(BOARD_SIZE):
        if all(board[r][c] == 1 for r in range(BOARD_SIZE)):
            cleared_cols.append(c)
    for r in cleared_rows:
        for c in range(BOARD_SIZE):
            board[r][c] = 0
    for c in cleared_cols:
        for r in range(BOARD_SIZE):
            board[r][c] = 0
    return len(cleared_rows) + len(cleared_cols)

def check_game_over(board, blocks):
    for block in blocks:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if can_place_block(board, block, row, col):
                    return False
    return True

def main():
    st.title("Blockudoku")

    if "board" not in st.session_state:
        st.session_state.board = create_blockudoku_board()
        st.session_state.blocks = generate_blocks()
        st.session_state.score = 0
        st.session_state.selected_block = None

    st.write(draw_board(st.session_state.board), unsafe_allow_html=True)
    st.write(draw_blocks(st.session_state.blocks), unsafe_allow_html=True)
    st.write(f"Score: {st.session_state.score}")

    col1, col2 = st.columns(2)

    with col1:
        row = st.number_input("Row (1-9)", min_value=1, max_value=9, step=1) - 1
    with col2:
        col = st.number_input("Column (1-9)", min_value=1, max_value=9, step=1) - 1

    block_num = st.radio("Select Block", options=range(1, len(st.session_state.blocks) + 1)) - 1

    if st.button("Place Block"):
        if can_place_block(st.session_state.board, st.session_state.blocks[block_num], row, col):
            place_block(st.session_state.board, st.session_state.blocks[block_num], row, col)
            cleared = clear_lines(st.session_state.board)
            st.session_state.score += cleared * 10
            st.session_state.blocks.pop(block_num)
            if check_game_over(st.session_state.board, st.session_state.blocks):
                st.write("Game Over!")
                st.session_state.board = create_blockudoku_board()
                st.session_state.blocks = generate_blocks()
                st.session_state.score = 0
            else:
                st.experimental_rerun()
        else:
            st.error("Cannot place block here")

if __name__ == "__main__":
    main()

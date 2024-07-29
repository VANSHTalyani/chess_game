#!/usr/bin/env python3

import sys
from typing import List, Optional, Tuple, Dict


class ChessBoard:
    def __init__(self, fen: Optional[str] = None):
        self.board = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
                      'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
                      '.', '.', '.', '.', '.', '.', '.', '.',
                      '.', '.', '.', '.', '.', '.', '.', '.',
                      '.', '.', '.', '.', '.', '.', '.', '.',
                      '.', '.', '.', '.', '.', '.', '.', '.',
                      'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
                      'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.turn = 'w'
        self.castling_rights = {'w': {'K': True, 'Q': True}, 'b': {'K': True, 'Q': True}}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        if fen:
            self.load_fen(fen)
        self.history = []

    def print_board(self):
        for i in range(0, 64, 8):
            print(' '.join(self.board[i:i + 8]))
        print()

    def apply_move(self, move: str):
        src_idx = self.move_to_index(move[:2])
        tgt_idx = self.move_to_index(move[2:])
        if src_idx is None or tgt_idx is None:
            return

        self.history.append(
            (self.board[:], self.turn, self.castling_rights.copy(), self.en_passant_target, self.halfmove_clock))

        piece = self.board[src_idx].lower()
        target_piece = self.board[tgt_idx]

        # Handle pawn promotion
        if piece == 'p' and (tgt_idx < 8 or tgt_idx >= 56):
            promotion_piece = 'Q' if self.turn == 'w' else 'q'
            self.board[tgt_idx] = promotion_piece
        else:
            self.board[tgt_idx] = self.board[src_idx]

        self.board[src_idx] = '.'

        # Handle en passant
        if piece == 'p' and tgt_idx == self.en_passant_target:
            if self.turn == 'w':
                self.board[tgt_idx + 8] = '.'
            else:
                self.board[tgt_idx - 8] = '.'

        # Update en passant target
        if piece == 'p' and abs(src_idx - tgt_idx) == 16:
            self.en_passant_target = src_idx + (tgt_idx - src_idx) // 2
        else:
            self.en_passant_target = None

        # Handle castling
        if piece == 'k' and abs(src_idx - tgt_idx) == 2:
            if tgt_idx > src_idx:  # King-side castling
                self.board[tgt_idx - 1] = self.board[tgt_idx + 1]
                self.board[tgt_idx + 1] = '.'
            else:  # Queen-side castling
                self.board[tgt_idx + 1] = self.board[tgt_idx - 2]
                self.board[tgt_idx - 2] = '.'

        # Update castling rights
        if piece == 'k':
            self.castling_rights[self.turn]['K'] = False
            self.castling_rights[self.turn]['Q'] = False
        elif piece == 'r':
            if src_idx == 0 or tgt_idx == 0:
                self.castling_rights['b']['Q'] = False
            elif src_idx == 7 or tgt_idx == 7:
                self.castling_rights['b']['K'] = False
            elif src_idx == 56 or tgt_idx == 56:
                self.castling_rights['w']['Q'] = False
            elif src_idx == 63 or tgt_idx == 63:
                self.castling_rights['w']['K'] = False

        self.turn = 'b' if self.turn == 'w' else 'w'
        self.halfmove_clock = 0 if piece == 'p' or target_piece != '.' else self.halfmove_clock + 1
        self.fullmove_number += 1 if self.turn == 'w' else 0

    def undo_move(self):
        if self.history:
            self.board, self.turn, self.castling_rights, self.en_passant_target, self.halfmove_clock = self.history.pop()

    def is_move_valid(self, move: str) -> bool:
        src_idx = self.move_to_index(move[:2])
        tgt_idx = self.move_to_index(move[2:])
        if src_idx is None or tgt_idx is None:
            return False
        piece = self.board[src_idx]
        if piece == '.':
            return False
        if piece.isupper() != (self.turn == 'w'):
            return False
        if not self.is_legal_move(src_idx, tgt_idx):
            return False
        return True

    def is_legal_move(self, src_idx: int, tgt_idx: int) -> bool:
        piece = self.board[src_idx]
        if piece.lower() == 'p':
            return self.is_legal_pawn_move(src_idx, tgt_idx)
        elif piece.lower() == 'r':
            return self.is_legal_rook_move(src_idx, tgt_idx)
        elif piece.lower() == 'n':
            return self.is_legal_knight_move(src_idx, tgt_idx)
        elif piece.lower() == 'b':
            return self.is_legal_bishop_move(src_idx, tgt_idx)
        elif piece.lower() == 'q':
            return self.is_legal_queen_move(src_idx, tgt_idx)
        elif piece.lower() == 'k':
            return self.is_legal_king_move(src_idx, tgt_idx)
        return False

    def is_legal_pawn_move(self, src_idx: int, tgt_idx: int) -> bool:
        direction = 1 if self.board[src_idx] == 'P' else -1
        src_row, src_col = divmod(src_idx, 8)
        tgt_row, tgt_col = divmod(tgt_idx, 8)

        if src_col == tgt_col:
            if tgt_row - src_row == direction and self.board[tgt_idx] == '.':
                return True
            if tgt_row - src_row == 2 * direction and self.board[tgt_idx] == '.' and \
               self.board[src_idx + direction * 8] == '.' and \
               ((src_row == 1 and self.board[src_idx] == 'P') or (src_row == 6 and self.board[src_idx] == 'p')):
                return True
        elif abs(tgt_col - src_col) == 1 and tgt_row - src_row == direction:
            if self.board[tgt_idx] != '.' and self.board[tgt_idx].isupper() != self.board[src_idx].isupper():
                return True
            if tgt_idx == self.en_passant_target:
                return True

        return False

    def is_legal_rook_move(self, src_idx: int, tgt_idx: int) -> bool:
        src_row, src_col = divmod(src_idx, 8)
        tgt_row, tgt_col = divmod(tgt_idx, 8)

        if src_row != tgt_row and src_col != tgt_col:
            return False

        if src_row == tgt_row:
            step = 1 if src_col < tgt_col else -1
            for col in range(src_col + step, tgt_col, step):
                if self.board[src_row * 8 + col] != '.':
                    return False
        else:
            step = 1 if src_row < tgt_row else -1
            for row in range(src_row + step, tgt_row, step):
                if self.board[row * 8 + src_col] != '.':
                    return False

        return self.board[tgt_idx] == '.' or self.board[tgt_idx].isupper() != self.board[src_idx].isupper()

    def is_legal_knight_move(self, src_idx: int, tgt_idx: int) -> bool:
        src_row, src_col = divmod(src_idx, 8)
        tgt_row, tgt_col = divmod(tgt_idx, 8)

        if (abs(src_row - tgt_row), abs(src_col - tgt_col)) in [(1, 2), (2, 1)]:
            return self.board[tgt_idx] == '.' or self.board[tgt_idx].isupper() != self.board[src_idx].isupper()
        return False

    def is_legal_bishop_move(self, src_idx: int, tgt_idx: int) -> bool:
        src_row, src_col = divmod(src_idx, 8)
        tgt_row, tgt_col = divmod(tgt_idx, 8)

        if abs(src_row - tgt_row) != abs(src_col - tgt_col):
            return False

        row_step = 1 if src_row < tgt_row else -1
        col_step = 1 if src_col < tgt_col else -1
        for step in range(1, abs(src_row - tgt_row)):
            if self.board[(src_row + step * row_step) * 8 + src_col + step * col_step] != '.':
                return False

        return self.board[tgt_idx] == '.' or self.board[tgt_idx].isupper() != self.board[src_idx].isupper()

    def is_legal_queen_move(self, src_idx: int, tgt_idx: int) -> bool:
        return self.is_legal_rook_move(src_idx, tgt_idx) or self.is_legal_bishop_move(src_idx, tgt_idx)

    def is_legal_king_move(self, src_idx: int, tgt_idx: int) -> bool:
        src_row, src_col = divmod(src_idx, 8)
        tgt_row, tgt_col = divmod(tgt_idx, 8)

        if max(abs(src_row - tgt_row), abs(src_col - tgt_col)) == 1:
            return self.board[tgt_idx] == '.' or self.board[tgt_idx].isupper() != self.board[src_idx].isupper()

        return False

    def load_fen(self, fen: str):
        parts = fen.split()
        position, turn, castling, en_passant, halfmove, fullmove = parts[:6]

        rows = position.split('/')
        self.board = []
        for row in rows:
            for char in row:
                if char.isdigit():
                    self.board.extend(['.'] * int(char))
                else:
                    self.board.append(char)

        self.turn = turn
        self.castling_rights = {'w': {'K': 'K' in castling, 'Q': 'Q' in castling},
                                'b': {'K': 'k' in castling, 'Q': 'q' in castling}}
        self.en_passant_target = self.move_to_index(en_passant) if en_passant != '-' else None
        self.halfmove_clock = int(halfmove)
        self.fullmove_number = int(fullmove)

    def move_to_index(self, move: str) -> Optional[int]:
        if len(move) != 2:
            return None
        file = move[0].lower()
        rank = move[1]
        if file < 'a' or file > 'h' or rank < '1' or rank > '8':
            return None
        return (8 - int(rank)) * 8 + (ord(file) - ord('a'))

    def index_to_move(self, index: int) -> str:
        row, col = divmod(index, 8)
        return chr(col + ord('a')) + str(8 - row)


class UCI:
    def __init__(self):
        self.board = ChessBoard()

    def uci(self):
        print("id name AdvancedChessEngine")
        print("id author YourName")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        self.board = ChessBoard()

    def position(self, command: str):
        parts = command.split()
        if len(parts) < 2:
            print("Invalid position command")
            return

        if parts[1] == 'startpos':
            self.board = ChessBoard()
            moves = parts[2:]
        elif parts[1] == 'fen':
            fen = ' '.join(parts[2:8])
            self.board = ChessBoard(fen)
            moves = parts[9:]

        for move in moves:
            if self.board.is_move_valid(move):
                self.board.apply_move(move)

        # Print the board to verify
        self.board.print_board()

    def go(self):
        # Implement a simple move selection mechanism
        best_move = self.find_best_move()
        print(f"bestmove {best_move}")

    def find_best_move(self) -> str:
        # For now, return a simple default move
        # You can implement Minimax or other algorithms here
        valid_moves = self.generate_valid_moves()
        if valid_moves:
            return valid_moves[0]
        return "0000"  # Indicate no valid move

    def generate_valid_moves(self) -> List[str]:
        # Generate all valid moves for the current board state
        moves = []
        for i, piece in enumerate(self.board.board):
            if piece == '.' or (piece.isupper() != (self.board.turn == 'w')):
                continue
            for j in range(64):
                move = self.board.index_to_move(i) + self.board.index_to_move(j)
                if self.board.is_move_valid(move):
                    moves.append(move)
        return moves

    def loop(self):
        input_stream = sys.stdin
        while True:
            try:
                command = input_stream.readline().strip()
                if command == "uci":
                    self.uci()
                elif command == "isready":
                    self.isready()
                elif command == "ucinewgame":
                    self.ucinewgame()
                elif command.startswith("position"):
                    self.position(command)
                elif command == "go":
                    self.go()
                elif command == "quit":
                    break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
def main():
    UCI().loop()

if __name__ == "__main__":
    UCI().loop()

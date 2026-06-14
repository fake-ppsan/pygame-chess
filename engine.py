white_king_moved = False
black_king_moved = False

white_left_rook_moved = False
white_right_rook_moved = False

black_left_rook_moved = False
black_right_rook_moved = False

en_passant_target = None

white_king_pos = (7,4)
black_king_pos = (0,4)

checked_square = None

game_over = False
winner = None



def create_starting_board():

    board = []

    for i in range(8):
        board.append([None] * 8)

    for col in range(8):
        board[1][col] = "bp"
        board[6][col] = "wp"


    board[0][0] = board[0][7] = "br"
    board[0][1] = board[0][6] = "bn"
    board[0][2] = board[0][5] = "bb"
    board[0][3] = "bq"
    board[0][4] = "bk"
    board[7][0] = board[7][7] = "wr"
    board[7][1] = board[7][6] = "wn"
    board[7][2] = board[7][5] = "wb"
    board[7][3] = "wq"
    board[7][4] = "wk"

    return board

def switch_turn(turn):

    if turn == "w":
        return "b"
    else:
        return "w"
    

def square_name(rank, file):

    chess_file = chr(ord("a") + file)
    chess_rank = str(8 - rank)

    return chess_file + chess_rank


def is_square_attacked(board,
                       rank, file,
                       opp_color,):

    for r in range(8):
        for f in range(8):

            if board[r][f] is not None:
                if board[r][f][0] == opp_color:
                                        
                    if board[r][f][1] == "p":
                        
                        if opp_color == "w":
                            direction = -1

                        else:
                            direction = 1

                        
                        if rank == r + direction and abs(file - f) == 1:
                            return True

                    if board[r][f][1] == "r" or board[r][f][1] == "q":
                        if r == rank or f == file:
                            blocked = False

                            if r == rank:
                                if file > f:
                                    step = 1
                                else:
                                    step = -1

                                for i in range(f + step, file, step):
                                    if board[r][i] is not None:
                                        blocked = True
                                        break
                                    
                            elif f == file:
                                if rank > r:
                                    step = 1
                                else:
                                    step = -1
    
                                for i in range(r + step, rank, step):
                                    if board[i][f] is not None:
                                        blocked = True
                                        break

                            if not blocked:
                                return True

                    if board[r][f][1] == "b" or board[r][f][1] == "q":
                        if abs(rank - r) == abs(file - f):
                            blocked = False

                            if rank > r:
                                row_step = 1
                            else:
                                row_step = -1
                                                        
                            if file > f:
                                file_step = 1
                            else:
                                file_step = -1

                            current_r = r + row_step
                            current_f = f + file_step

                            while (current_r, current_f) != (rank, file):
                                if board[current_r][current_f] is not None:
                                    blocked = True
                                    break

                                current_r += row_step
                                current_f += file_step

                            if not blocked:
                                return True
                            
                    
                    if board[r][f][1] == "n":
                        if (abs(rank - r), abs(file - f)) in [(2,1), (1,2)]:
                            return True

                    if board[r][f][1] == "k":
                        if max(abs(rank - r), abs(file - f)) == 1:
                            return True

    return False


def is_king_attacked(board,
                     color,
                     capture_moves=None):

    if color == "w":
        
        king_rank, king_file = white_king_pos
        return is_square_attacked(
            board,
            king_rank,
            king_file,
            "b"
            )

    else:
        
        king_rank, king_file = black_king_pos
        return is_square_attacked(
            board,
            king_rank,
            king_file,
            "w"
            )

    



def make_move(board,
              old_rank, old_file,
              new_rank, new_file,
              promotion = False,
              castling = False,
              en_passant = False):

    moved_piece = board[old_rank][old_file]
    captured_piece = board[new_rank][new_file]
    global white_king_pos, \
    black_king_pos, \
    en_passant_target, \
    white_king_moved, \
    black_king_moved, \
    white_left_rook_moved, \
    white_right_rook_moved, \
    black_left_rook_moved, \
    black_right_rook_moved
    
    en_passant_target = None

    if moved_piece == "wk":
        white_king_pos = (new_rank, new_file)
        white_king_moved = True
        
    elif moved_piece == "bk":
        black_king_pos = (new_rank, new_file)
        black_king_moved = True

    elif en_passant and moved_piece[0] == "w":
        captured_piece = board[new_rank + 1][new_file]
        board[new_rank + 1][new_file] = None

    elif en_passant and moved_piece[0] == "b":
        captured_piece = board[new_rank - 1][new_file]
        board[new_rank - 1][new_file] = None

    if castling:

        if new_file > old_file:

            board[new_rank][5] = board[new_rank][7]
            board[new_rank][7] = None

        else:

            board[new_rank][3] = board[new_rank][0]
            board[new_rank][0] = None

    if promotion and moved_piece[0] == "w":
        moved_piece = "wq"

    elif promotion and moved_piece[0] == "b":
        moved_piece = "bq"

    if moved_piece == "wr":

        if old_rank == 7 and old_file == 0:
            white_left_rook_moved = True

        elif old_rank == 7 and old_file == 7:
            white_right_rook_moved = True
    
    if moved_piece == "br":

        if old_rank == 0 and old_file == 0:
            black_left_rook_moved = True

        elif old_rank == 0 and old_file == 7:
            black_right_rook_moved = True

    if moved_piece == "wp" and old_rank == 6 and new_rank == 4:
        en_passant_target = (5, new_file)

    elif moved_piece == "bp" and old_rank == 1 and new_rank == 3:
        en_passant_target = (2, new_file)

    board[new_rank][new_file] = moved_piece
    board[old_rank][old_file] = None


    if captured_piece == "wr":

        if new_rank == 7 and new_file == 0:
            white_left_rook_moved = True

        elif new_rank == 7 and new_file == 7:
            white_right_rook_moved = True

    elif captured_piece == "br":

        if new_rank == 0 and new_file == 0:
            black_left_rook_moved = True

        elif new_rank == 0 and new_file == 7:
            black_right_rook_moved = True
    

    return captured_piece

def undo_move(board,
              old_rank, old_file,
              new_rank, new_file,
              captured_piece,
              promotion = False,
              castling = False,
              en_passant = False):

    moved_piece = board[new_rank][new_file]
    global white_king_pos, black_king_pos

    if moved_piece == "wk":
        white_king_pos = (old_rank, old_file)
        
    elif moved_piece == "bk":
        black_king_pos = (old_rank, old_file)      

    elif en_passant:
        board[new_rank][new_file] = None
        board[old_rank][old_file] = moved_piece
        board[old_rank][new_file] = captured_piece
        return

    elif promotion:

        if moved_piece[0] == "w":
            board[old_rank][old_file] = "wp"

        else:
            board[old_rank][old_file] = "bp"

        board[new_rank][new_file] = captured_piece

        return

    if castling:

        if new_file > old_file:

            board[new_rank][7] = board[new_rank][5]
            board[new_rank][5] = None

        else:

            board[new_rank][0] = board[new_rank][3]
            board[new_rank][3] = None

    
        

    board[old_rank][old_file] = moved_piece    
    board[new_rank][new_file] = captured_piece

                                           
                
def try_move(board,
             old_rank, old_file,
             new_rank, new_file,
             promotion=False,
             castling=False,
             en_passant=False):

    global en_passant_target, \
    white_king_moved, \
    black_king_moved, \
    white_left_rook_moved, \
    white_right_rook_moved, \
    black_left_rook_moved, \
    black_right_rook_moved

    old_en_passant_target = en_passant_target
    old_white_king_moved = white_king_moved
    old_black_king_moved = black_king_moved
    old_white_left_rook_moved = white_left_rook_moved
    old_white_right_rook_moved = white_right_rook_moved
    old_black_left_rook_moved = black_left_rook_moved
    old_black_right_rook_moved = black_right_rook_moved

    moved_piece = board[old_rank][old_file]
    color = moved_piece[0]

    captured_piece = make_move(
        board,
        old_rank, old_file,
        new_rank, new_file,
        promotion,
        castling,
        en_passant
    )

    illegal = is_king_attacked(board, color)

    undo_move(
        board,
        old_rank, old_file,
        new_rank, new_file,
        captured_piece,
        promotion,
        castling,
        en_passant
    )

    en_passant_target = old_en_passant_target
    white_king_moved = old_white_king_moved
    black_king_moved = old_black_king_moved
    white_left_rook_moved = old_white_left_rook_moved
    white_right_rook_moved = old_white_right_rook_moved
    black_left_rook_moved = old_black_left_rook_moved
    black_right_rook_moved = old_black_right_rook_moved
    

    return not illegal


def get_legal_moves(board,
                    rank, file,
                    capture_moves):

    piece = board[rank][file]

    color = piece[0]

    legal_moves = []

    # generate pseudo moves

    if piece[1] == "r" or piece[1] == "q":

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
            ]

        for dr, df in directions:

            r = rank + dr
            f = file + df

            while 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is None:

                    if try_move(board, rank, file, r, f):
                        legal_moves.append((r, f))

                else:

                    if board[r][f][0] != color:

                        if try_move(board, rank, file, r, f):
                            legal_moves.append((r, f))
                            capture_moves.append((r,f))

                    break

                r += dr
                f += df
            
           
    if piece[1] == "b" or piece[1] == "q":

        directions = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
            ]

        for dr, df in directions:

            r = rank + dr
            f = file + df

            while 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is None:

                    if try_move(board, rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(board, rank, file, r, f):
                            legal_moves.append((r,f))
                            capture_moves.append((r,f))

                    break

                r += dr
                f += df

    if piece[1] == "n":

        moves = [
            (-2, -1),
            (-2, 1),
            (2, -1),
            (2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2)
            ]

        for dr, df in moves:

            r = rank + dr
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is None:

                    if try_move(board, rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(board, rank, file, r, f):
                            legal_moves.append((r,f))
                            capture_moves.append((r,f))

    if piece[1] == "k":

        moves = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
            ]

        for dr, df in moves:

            r = rank + dr
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is None:

                    if try_move(board, rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(board, rank, file, r, f):
                            legal_moves.append((r,f))
                            capture_moves.append((r,f))

        #castle

        if color == "w":

            if not white_king_moved \
               and not white_right_rook_moved:

                if board[7][5] is None \
                   and board[7][6] is None \
                   and board[7][7] == "wr":

                    if not is_square_attacked(board, 7, 4, "b") \
                       and not is_square_attacked(board, 7, 5, "b") \
                       and not is_square_attacked(board, 7, 6, "b"):

                        if try_move(board, rank, file,
                                    7, 6,
                                    castling = True
                                    ):

                            legal_moves.append((7,6))

            if not white_king_moved \
               and not white_left_rook_moved:

                if board[7][3] is None \
                   and board[7][2] is None \
                   and board[7][0] == "wr":

                    if not is_square_attacked(board, 7, 4, "b") \
                       and not is_square_attacked(board, 7, 3, "b") \
                       and not is_square_attacked(board, 7, 2, "b"):

                        if try_move(board, rank, file,
                                    7, 2,
                                    castling = True
                                    ):

                            legal_moves.append((7,2))

        if color == "b":

            if not black_king_moved \
               and not black_right_rook_moved:

                if board[0][5] is None \
                   and board[0][6] is None \
                   and board[0][7] == "br":

                    if not is_square_attacked(board, 0, 4, "w") \
                       and not is_square_attacked(board, 0, 5, "w") \
                       and not is_square_attacked(board, 0, 6, "w"):

                        if try_move(board, rank, file,
                                    0, 6,
                                    castling = True
                                    ):

                            legal_moves.append((0,6))

            if not black_king_moved \
               and not black_left_rook_moved:

                if board[0][3] is None \
                   and board[0][2] is None \
                   and board[0][0] == "br":

                    if not is_square_attacked(board, 0, 4, "w") \
                       and not is_square_attacked(board, 0, 3, "w") \
                       and not is_square_attacked(board, 0, 2, "w"):

                        if try_move(board, rank, file,
                                    0, 2,
                                    castling = True
                                    ):

                            legal_moves.append((0,2))
                            
                            

    if piece[1] == "p":
        if color == "w":

            direction = -1
            start = 6
            promotion_rank = 0

        else:

            direction = 1
            start = 1
            promotion_rank = 7

        r = rank + direction

        if 0 <= r < 8:

            if board[r][file] is None:

                if r == promotion_rank:

                    if try_move(board, rank, file, r, file, promotion = True):
                        legal_moves.append((r, file))

                else:

                    if try_move(board, rank, file, r, file):
                        legal_moves.append((r, file))

        if rank == start:

            r2 = rank + 2 * direction

            if 0 <= r2 < 8:

                if board[r][file] is None and board[r2][file] is None:

                    if try_move(board, rank, file, r2, file):
                        legal_moves.append((r2, file))

        for df in [-1, 1]:

            r = rank + direction
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is not None:

                    if board[r][f][0] != color:

                        if r == promotion_rank:

                            if try_move(board, rank, file, r, f, promotion = True):
                                legal_moves.append((r, f))
                                capture_moves.append((r,f))

                        else:

                            if try_move(board, rank, file, r, f):
                                legal_moves.append((r,f))
                                capture_moves.append((r,f))

        for df in [-1, 1]:

            r = rank + direction
            f = file + df

            if 0<= r < 8 and 0 <= f < 8:

                if (r, f) == en_passant_target:

                    if try_move(board, rank, file, r, f, en_passant=True):

                        legal_moves.append((r, f))
                        capture_moves.append((r,f))

    return legal_moves


def player_has_moves(board,
                     color,
                     capture_moves):

    for rank in range(8):
        for file in range(8):

            if board[rank][file] is not None:

                if board[rank][file][0] == color:

                    if get_legal_moves(board, rank, file, capture_moves):

                        return True

    return False



def check_game_state(board,
                     color,
                     capture_moves):
    
    global game_over, winner, checked_square

    checked_square = None

    if is_king_attacked(board,
                        color,
                        capture_moves):
        
        if color == "w":
            checked_square = white_king_pos
        else:
            checked_square = black_king_pos
        print(f"Checked Square engine: {checked_square}")

        if player_has_moves(board,
                            color,
                            capture_moves):
            print("Check!")
            
        else:
            print("Checkmate!")
            game_over = True
            winner = switch_turn(color)

    elif not player_has_moves(board,
                              color,
                              capture_moves):
        print("Stalemate!")
        game_over = True


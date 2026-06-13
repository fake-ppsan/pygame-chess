# PYGAME-CHESS
# VERSION 1.0




import pygame
from constants import *
from renderer import *


#---------------IMPORTANT DATA-------------------
runTime=True
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 24)

piece_images = {}
captured_piece_images = {}

piece_names = [
    "wp","wn","wb","wr","wq","wk",
    "bp","bn","bb","br","bq","bk"
    ]

for piece in piece_names:

    image = pygame.image.load(
        f"pieces/{piece}.png"
        )

    piece_images[piece] = pygame.transform.smoothscale(
        image,
        (SQUARE_SIZE, SQUARE_SIZE)
        )

    captured_piece_images[piece] = pygame.transform.smoothscale(
        image,
        (40, 40)
        )

#-----------------Board variables---------------


selected_square = None
clicked_square = None
checked_square = None

current_turn = "w"

white_king_moved = False
black_king_moved = False

white_left_rook_moved = False
white_right_rook_moved = False

black_left_rook_moved = False
black_right_rook_moved = False

en_passant_target = None

white_king_pos = (7,4)
black_king_pos = (0,4)

legal_moves = []
capture_moves = []
move_history = []
capture_by_white = []
capture_by_black = []

white_score = 0
black_score = 0

game_over = False
winner = None


#--------------Board Creation-------------
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

#--------------FUNCTIONS------------------------

def is_square_attacked(rank, file, opp_color):

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


def is_king_attacked(color):

    if color == "w":
        
        king_rank, king_file = white_king_pos
        return is_square_attacked(
            king_rank,
            king_file,
            "b"
            )

    else:
        
        king_rank, king_file = black_king_pos
        return is_square_attacked(
            king_rank,
            king_file,
            "w"
            )

    



def make_move(old_rank, old_file,
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

def undo_move(old_rank, old_file,
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


def switch_turn(turn):

    if turn == "w":
        return "b"
    else:
        return "w"                                               
                
def try_move(old_rank, old_file,
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
        old_rank, old_file,
        new_rank, new_file,
        promotion,
        castling,
        en_passant
    )

    illegal = is_king_attacked(color)

    undo_move(
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


def get_legal_moves(rank, file):

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

                    if try_move(rank, file, r, f):
                        legal_moves.append((r, f))

                else:

                    if board[r][f][0] != color:

                        if try_move(rank, file, r, f):
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

                    if try_move(rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(rank, file, r, f):
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

                    if try_move(rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(rank, file, r, f):
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

                    if try_move(rank, file, r, f):
                        legal_moves.append((r,f))

                else:

                    if board[r][f][0] != color:

                        if try_move(rank, file, r, f):
                            legal_moves.append((r,f))
                            capture_moves.append((r,f))

        #castle

        if color == "w":

            if not white_king_moved \
               and not white_right_rook_moved:

                if board[7][5] is None \
                   and board[7][6] is None \
                   and board[7][7] == "wr":

                    if not is_square_attacked(7, 4, "b") \
                       and not is_square_attacked(7, 5, "b") \
                       and not is_square_attacked(7, 6, "b"):

                        if try_move(rank, file,
                                    7, 6,
                                    castling = True
                                    ):

                            legal_moves.append((7,6))

            if not white_king_moved \
               and not white_left_rook_moved:

                if board[7][3] is None \
                   and board[7][2] is None \
                   and board[7][0] == "wr":

                    if not is_square_attacked(7, 4, "b") \
                       and not is_square_attacked(7, 3, "b") \
                       and not is_square_attacked(7, 2, "b"):

                        if try_move(rank, file,
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

                    if not is_square_attacked(0, 4, "w") \
                       and not is_square_attacked(0, 5, "w") \
                       and not is_square_attacked(0, 6, "w"):

                        if try_move(rank, file,
                                    0, 6,
                                    castling = True
                                    ):

                            legal_moves.append((0,6))

            if not black_king_moved \
               and not black_left_rook_moved:

                if board[0][3] is None \
                   and board[0][2] is None \
                   and board[0][0] == "br":

                    if not is_square_attacked(0, 4, "w") \
                       and not is_square_attacked(0, 3, "w") \
                       and not is_square_attacked(0, 2, "w"):

                        if try_move(rank, file,
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

                    if try_move(rank, file, r, file, promotion = True):
                        legal_moves.append((r, file))

                else:

                    if try_move(rank, file, r, file):
                        legal_moves.append((r, file))

        if rank == start:

            r2 = rank + 2 * direction

            if 0 <= r2 < 8:

                if board[r][file] is None and board[r2][file] is None:

                    if try_move(rank, file, r2, file):
                        legal_moves.append((r2, file))

        for df in [-1, 1]:

            r = rank + direction
            f = file + df

            if 0 <= r < 8 and 0 <= f < 8:

                if board[r][f] is not None:

                    if board[r][f][0] != color:

                        if r == promotion_rank:

                            if try_move(rank, file, r, f, promotion = True):
                                legal_moves.append((r, f))
                                capture_moves.append((r,f))

                        else:

                            if try_move(rank, file, r, f):
                                legal_moves.append((r,f))
                                capture_moves.append((r,f))

        for df in [-1, 1]:

            r = rank + direction
            f = file + df

            if 0<= r < 8 and 0 <= f < 8:

                if (r, f) == en_passant_target:

                    if try_move(rank, file, r, f, en_passant=True):

                        legal_moves.append((r, f))
                        capture_moves.append((r,f))

    return legal_moves



def square_name(rank, file):

    chess_file = chr(ord("a") + file)
    chess_rank = str(8 - rank)

    return chess_file + chess_rank






def player_has_moves(color):

    for rank in range(8):
        for file in range(8):

            if board[rank][file] is not None:

                if board[rank][file][0] == color:

                    if get_legal_moves(rank, file):

                        return True

    return False

def check_game_state(color):

    global game_over, winner, checked_square

    checked_square = None

    if is_king_attacked(color):
        
        if color == "w":
            checked_square = white_king_pos
        else:
            checked_square = black_king_pos

        if player_has_moves(color):
            print("Check!")
            
        else:
            print("Checkmate!")
            game_over = True
            winner = switch_turn(color)

    elif not player_has_moves(color):
        print("Stalemate!")
        game_over = True

def move_to_notation(
    moved_piece,
    start_square,
    end_square,
    captured_piece = None,
    castling = False,
    promotion = False):

    color = switch_turn(moved_piece[0])
    promotion_piece = "Q"

    piece_letter = {
        "p": "",
        "n": "N",
        "b": "B",
        "r": "R",
        "q": "Q",
        "k": "K"
        }

    if castling:

        if end_square[0] == "g":
            notation = "O-O"

        else:
            notation = "O-O-O"

    

    else:
        notation = piece_letter[moved_piece[1]]

        if captured_piece is not None:

            if moved_piece[1] == "p":

                notation += start_square[0]

            notation += "x"

        notation += end_square

        if promotion:

            notation += f"={promotion_piece}"

    if is_king_attacked(color):

        if player_has_moves(color):

            notation += "+"

        else:

            notation += "#"

    return notation


def add_capture(captured_piece, color):

    global capture_by_white, capture_by_black, \
           white_score, black_score

    if captured_piece is None:
        return

    if color == "w":

        capture_by_white.append(captured_piece)
        capture_by_white.sort(
            key = lambda piece: CAPTURE_SORT_ORDER[piece[1]]
            )

        white_score = sum(PIECE_VALUE[p[1]]
                          for p in capture_by_white)

    else:
        capture_by_black.append(captured_piece)
        capture_by_black.sort(
            key = lambda piece: CAPTURE_SORT_ORDER[piece[1]]
            )

        black_score = sum(PIECE_VALUE[p[1]]
                          for p in capture_by_black)    
def render():

    draw_board(screen,
               selected_square,
               checked_square)
    draw_legal_moves(screen,
                     legal_moves,
                     capture_moves)
    draw_pieces(screen, board,
                piece_images)
    draw_move_history(screen,
                      move_history, font)
    draw_captured_piece(screen,
                        capture_by_white,
                        capture_by_black,
                        white_score,
                        black_score, font,
                        captured_piece_images)

    if game_over:
        draw_game_over(screen,
                       font,
                       winner)

                

#--------------MAIN GAME LOOP-------------------
while runTime:
    
    clock.tick(60) #framrate

    screen.fill((230,230,230)) #bg color

    render()

    pygame.display.flip()

    
    #---------------Square detection logic---------------------
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_X, mouse_Y = pygame.mouse.get_pos()
                file = (mouse_X - OFFSET_X) // SQUARE_SIZE
                rank = (mouse_Y - OFFSET_Y) // SQUARE_SIZE

                if file < 0 or file > 7 or rank < 0 or rank > 7:
                    continue

                rank_letter = chr(ord("a") + file)
                file_number = 8 - rank

                square_id = rank_letter + str(file_number)

                
    #---------------MOVE LOGIC-----------------

                if selected_square is None:

                    capture_moves = []

                    
                    if board[rank][file] is not None and board[rank][file][0] == current_turn:

                        
                        selected_square = (rank, file)

                        legal_moves = get_legal_moves(rank, file)
                        

                elif selected_square == (rank, file):

                    selected_square = None
                    legal_moves = []
                    capture_moves = []
                        
                    
                else:

                    old_rank, old_file = selected_square
                    piece = board[old_rank][old_file]


                    if board[rank][file] is not None and board[rank][file][0] == current_turn:

                        selected_square = (rank, file)
                        legal_moves = get_legal_moves(rank, file)
                        continue

                    legal_moves = get_legal_moves(old_rank, old_file)

                    if (rank, file) in legal_moves:

                        promotion = False
                        castling = False
                        en_passant = False

                        if piece[1] == "p":

                            if (piece[0] == "w" and rank == 0) or \
                               (piece[0] == "b" and rank == 7):

                                promotion = True

                            if (rank, file) == en_passant_target and abs(file - old_file) == 1:

                                en_passant = True

                        if piece[1] == "k" and abs(file - old_file) == 2:

                            castling = True

                        captured_piece = make_move(
                            old_rank,
                            old_file,
                            rank,
                            file,
                            promotion=promotion,
                            castling=castling,
                            en_passant=en_passant
                        )

                        notation = move_to_notation(
                            piece,
                            square_name(old_rank, old_file),
                            square_name(rank, file),
                            captured_piece,
                            castling,
                            promotion
                            )

                        move_history.append(notation)

                        add_capture(captured_piece, current_turn)

                        current_turn = switch_turn(current_turn)
                        selected_square = None

                        check_game_state(current_turn)

                        legal_moves = []
                        capture_moves = []

                        continue

                    #illegal square
                    selected_square = None
                    legal_moves = []
                    capture_moves = []


                        
       #--------------------DEBUGGING AND HANDLING OUTSIDE BOARD CLICKS---------------------------
            
                
                print(move_history)
                print(f"Rank: {rank}, File: {file}, Square Name: {square_id}, Piece: {board[rank][file]}, En Passant Target: {en_passant_target}, King positions: {white_king_pos, black_king_pos}, white_king_moved: {white_king_moved}")
            if event.type == pygame.QUIT:
                runTime = False

    
    

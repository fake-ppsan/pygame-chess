# PYGAME-CHESS
# VERSION 1.5




import pygame
from constants import *
import engine
from renderer import *


#---------------IMPORTANT DATA-------------------
runTime=True
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
font = pygame.font.SysFont(None, 24)

#-----------------Board variables---------------


selected_square = None
clicked_square = None

current_turn = "w"

legal_moves = []
capture_moves = []
move_history = []
capture_by_white = []
capture_by_black = []

white_score = 0
black_score = 0

board = engine.create_starting_board()

#--------------FUNCTIONS------------------------



def move_to_notation(
    moved_piece,
    start_square,
    end_square,
    captured_piece = None,
    castling = False,
    promotion = False):

    color = engine.switch_turn(moved_piece[0])
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

    if engine.is_king_attacked(board, color):

        if engine.player_has_moves(board,
                                    color,
                                    capture_moves):

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
               engine.checked_square)
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

    if engine.game_over:
        draw_game_over(screen,
                       font,
                       engine.winner)

                

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

                        legal_moves = engine.get_legal_moves(board,
                                                      rank, file,
                                                      capture_moves)
                        

                elif selected_square == (rank, file):

                    selected_square = None
                    legal_moves = []
                    capture_moves = []
                        
                    
                else:

                    old_rank, old_file = selected_square
                    piece = board[old_rank][old_file]


                    if board[rank][file] is not None and board[rank][file][0] == current_turn:

                        selected_square = (rank, file)
                        legal_moves = engine.get_legal_moves(board, rank, file, capture_moves)
                        continue

                    legal_moves = engine.get_legal_moves(board, old_rank, old_file, capture_moves)

                    if (rank, file) in legal_moves:

                        promotion = False
                        castling = False
                        en_passant = False

                        if piece[1] == "p":

                            if (piece[0] == "w" and rank == 0) or \
                               (piece[0] == "b" and rank == 7):

                                promotion = True

                            if (rank, file) == engine.en_passant_target and abs(file - old_file) == 1:

                                en_passant = True

                        if piece[1] == "k" and abs(file - old_file) == 2:

                            castling = True

                        captured_piece = engine.make_move(
                            board,
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
                            engine.square_name(old_rank, old_file),
                            engine.square_name(rank, file),
                            captured_piece,
                            castling,
                            promotion
                            )

                        move_history.append(notation)

                        add_capture(captured_piece, current_turn)

                        current_turn = engine.switch_turn(current_turn)
                        selected_square = None

                        engine.check_game_state(board,
                                         current_turn,
                                         capture_moves)

                        legal_moves = []
                        capture_moves = []

                        continue

                    #illegal square
                    selected_square = None
                    legal_moves = []
                    capture_moves = []


                        
       #--------------------DEBUGGING---------------------------

                debug = False

                if debug:
                    print(move_history)
                    print(f"Rank: {rank}, File: {file}, Square Name: {square_id}, Piece: {board[rank][file]}, En Passant Target: {engine.en_passant_target}, King positions: {engine.white_king_pos, engine.black_king_pos}, white_king_moved: {engine.white_king_moved}")

            if event.type == pygame.QUIT:
                runTime = False

    
    

from constants import *
import pygame


def draw_board(screen,
               selected_square,
               checked_square):
    
    for rank in range(8):
        for file in range(8):
            posX = file * SQUARE_SIZE + OFFSET_X
            posY = rank * SQUARE_SIZE + OFFSET_Y

            
            if (rank+file)%2 == 0:
                color = (255, 255, 255)
            else:
                color = (50, 255, 50)

            if (rank, file) == selected_square:
                color = (255, 255, 0)

            elif (rank, file) == checked_square:
                color = (255, 0, 0)
                
            pygame.draw.rect(screen, color, (posX, posY, SQUARE_SIZE, SQUARE_SIZE))
    

def draw_legal_moves(screen, legal_moves, capture_moves):

    for rank, file in legal_moves:

        posX = file * SQUARE_SIZE + OFFSET_X
        posY = rank * SQUARE_SIZE + OFFSET_Y

        center_x = posX + SQUARE_SIZE // 2
        center_y = posY + SQUARE_SIZE // 2

        pygame.draw.circle(
            screen,
            (100,100,100),
            (center_x, center_y),
            SQUARE_SIZE // 8
        )

    for rank, file in capture_moves:

        posX = file * SQUARE_SIZE + OFFSET_X
        posY = rank * SQUARE_SIZE + OFFSET_Y

        center_x = posX + SQUARE_SIZE // 2
        center_y = posY + SQUARE_SIZE // 2

        pygame.draw.circle(
            screen,
            (100,100,100),
            (center_x, center_y),
            SQUARE_SIZE // 2 - 2,
            4
        )
        
        


def draw_pieces(screen, board,
                piece_images):

    for rank in range(8):
        for file in range(8):

            if board[rank][file] is None:
                continue

            piece = board[rank][file]

            posX = file * SQUARE_SIZE + OFFSET_X
            posY = rank * SQUARE_SIZE + OFFSET_Y


            screen.blit(
                piece_images[piece],
                (posX - 1, posY - 2)
                )


def draw_game_over(screen, font, winner):
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            ((SCREEN_WIDTH - 500) // 2, (SCREEN_HEIGHT - 150) // 2, 500, 150)
            )

        if winner == "w":

            text = font.render(
            "WHITE WON BY CHECKMATE",
            True,
            (255,255,255)
            )

            screen.blit(text, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2))

        elif winner == "b":

            text = font.render(
            "BLACK WON BY CHECKMATE",
            True,
            (255,255,255)
            )

            screen.blit(text, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2))

        elif winner == None:

            text = font.render(
            "DRAW BY STALEMATE",
            True,
            (255,255,255)
            )        
        

            screen.blit(text, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2))

def draw_move_history(screen, move_history, font):

    x = 150
    y = 50

    move_number = 1

    for i in range(0, len(move_history), 2):

        white_move = move_history[i]

        if i + 1 < len(move_history):
            black_move = move_history[i + 1]

        else:
            black_move = ""

        text = (
            f"{move_number}."
            f"{white_move} "
            f"{black_move}"
            )
            

        text_surface = font.render(
            text,
            True,
            (0, 0, 0)
            )

        screen.blit(text_surface, (x, y))

        y += 25
        move_number += 1



def draw_captured_piece(screen,
                        capture_by_white,
                        capture_by_black,
                        white_score,
                        black_score, font,
                        captured_piece_images):

    x = 900

    for piece in capture_by_white:
        

        screen.blit(captured_piece_images[piece], (x, 560))

        x += 25

    if white_score - black_score > 0:

        text_surface = font.render(
            f"+{white_score - black_score}",
            True,
            (0, 0, 0)
            )

        screen.blit(text_surface, (x + 30, 560))

    x = 900

    for piece in capture_by_black:

        screen.blit(captured_piece_images[piece], (x, 120))

        x += 25

    if white_score - black_score < 0:

        text_surface = font.render(
            f"+{black_score - white_score}",
            True,
            (0, 0, 0)
            )

        screen.blit(text_surface, (x + 30, 120))

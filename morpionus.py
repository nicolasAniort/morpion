import pygame
import sys

confirm = 0

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)

# Paramètres de la fenêtre
fenêtre_largeur, fenêtre_hauteur = 300, 300
screen = pygame.display.set_mode((fenêtre_largeur, fenêtre_hauteur))
pygame.display.set_caption("Jeu de Morpion")

# Grille
cell_size = fenêtre_largeur // 3

class Morpion:
       
    def __init__(self):
        
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        pygame.font.init()  # Initialisation de la police de caractères
        self.font = pygame.font.Font("./font/Montserrat-Bold.ttf", 36)
        self.current_player = 'X'
        self.game_over = False
        
    def draw_grid(self):
        for row in range(1, 3):
            pygame.draw.line(screen, BLACK, (0, row * cell_size), (fenêtre_largeur, row * cell_size), 2)
            pygame.draw.line(screen, BLACK, (row * cell_size, 0), (row * cell_size, fenêtre_hauteur), 2)

    def draw_board(self):
        for row in range(3):
            for col in range(3):
                text = self.font.render(self.board[row][col], True, PINK)
                text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                screen.blit(text, text_rect)

    def check_win(self, player):
        for row in range(3):
            if all(self.board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player or self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        #traitement par ligne
        for row in range(3):
            if all(self.board[row][col] == 'X' for col in range(3)):
                return True
        #traitement par colonne    
        for col in range(3):
            if all(self.board[row][col] == 'X' for row in range(3)):
                return True
        #traitement par diagonale    
        if all(self.board[i][i] == 'X' for i in range(3)) or all(self.board[i][2 - i] == 'X' for i in range(3)):
            return True
        
        return False

    def handle_click(self, pos):
        row, col = pos[1] // cell_size, pos[0] // cell_size
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_win(self.current_player):
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'


# Paramètres du bouton recommencer
button_width, button_height = 120, 40
button_rect = pygame.Rect((fenêtre_largeur - button_width) // 2, fenêtre_hauteur - button_height - 10, button_width, button_height)

def main():
    global morpion

    pygame.init()  # Initialisation de Pygame

    # Paramètres de la fenêtre
    fenêtre_largeur, fenêtre_hauteur = 300, 300
    screen = pygame.display.set_mode((fenêtre_largeur, fenêtre_hauteur))
    pygame.display.set_caption("Jeu de Morpion")

    # Paramètres du bouton recommencer
    button_width, button_height = 120, 40
    button_rect = pygame.Rect((fenêtre_largeur - button_width) // 2, fenêtre_hauteur - button_height - 10, button_width, button_height)

    morpion = Morpion()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                morpion.handle_click(event.pos)

                if morpion.check_win(morpion.current_player):
                    morpion.game_over = True
                    if morpion.current_player == 'X':
                        confirm = 1
                        print(confirm)
                    else:
                        confirm = 2

                if morpion.game_over and button_rect.collidepoint(event.pos):
                    morpion.__init__()  # Réinitialisation du jeu en créant une nouvelle instance de Morpion

                if morpion.check_draw():
                    morpion.game_over = True
                    confirm = 0

        screen.fill('#FFFFFF') # Remplir la surface de la fenêtre avec la couleur blanche
        morpion.draw_grid()
        morpion.draw_board()

        if morpion.game_over:
            
            result_text = []
            
            if morpion.check_win(morpion.current_player) :
                winner_message = f"Le Joueur\n {morpion.current_player}\n a gagné !"
                result_text = winner_message
            elif morpion.check_draw()==True:
                result_text = "Match nul !"
            else:    
                result_text = "OUPS!!!"
            
            
            lines = result_text.split("\n")
            total_text_height = len(lines) * morpion.font.get_height()
            
            for i, line in enumerate(lines):
                text = morpion.font.render(line, True, '#424142')
                text_rect = text.get_rect(center=(fenêtre_largeur // 2, fenêtre_hauteur // 2 + (i - len(lines) // 2) * morpion.font.get_height()))
                screen.blit(text, text_rect)
            
            pygame.draw.rect(screen, PINK, button_rect)
            button_font = pygame.font.Font(None, 20)
            button_text = button_font.render("Recommencer", True, WHITE)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)
        else:
            morpion.draw_grid()
            morpion.draw_board()
        
        pygame.display.update()  # Rafraîchir l'affichage

if __name__ == "__main__":
    main()  # Appeler la fonction main pour exécuter le jeu
    pygame.quit()  # Quitter pygame à la fin
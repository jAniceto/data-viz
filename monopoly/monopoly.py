import random
import csv

# Game settings
GAMES = 10000
DIE_ROLLS_PER_GAME = 30
PLAYERS = 4

class Board:
    """Class representing the Monopoly game board"""
    SPACES = [
        {"name": "Partida", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Campo Grande (Lisboa)", "color": "#934824", "value": 60, "rent": 2},
        {"name": "Caixa da Comunidade 1", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Rua Faria Guimarães (Porto)", "color": "#934824", "value": 60, "rent": 4},
        {"name": "Imposto sobre Capitais", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Estação do Rossio (Lisboa)", "color": "#C2C7CA", "value": 200, "rent": 25},
        {"name": "Alameda das Linhas de Torres (Lisboa)", "color": "#BCE4F9", "value": 100, "rent": 6},
        {"name": "Sorte 1", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida das Nações Unidas (Lisboa)", "color": "#BCE4F9", "value": 100, "rent": 6},
        {"name": "Avenida 24 de Julho (Lisboa)", "color": "#BCE4F9", "value": 120, "rent": 8},
        {"name": "Cadeia", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida Central (Braga)", "color": "#D73189", "value": 140, "rent": 10},
        {"name": "Companhia de Electricidade", "color": "#68625E", "value": 150, "rent": 24},
        {"name": "Rua Ferreira Borges (Coimbra)", "color": "#D73189", "value": 140, "rent": 10},
        {"name": "Avenida de Roma (Lisboa)", "color": "#D73189", "value": 160, "rent": 12},
        {"name": "Gare do Oriente (Lisboa)", "color": "#C2C7CA", "value": 200, "rent": 25},
        {"name": "Avenida da Boavista (Porto)", "color": "#F39000", "value": 180, "rent": 14},
        {"name": "Caixa da Comunidade 2", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida da República (Lisboa)", "color": "#F39000", "value": 180, "rent": 14},
        {"name": "Rua Mouzinho da Silveira (Porto)", "color": "#F39000", "value": 200, "rent": 16},
        {"name": "Estacionamento Livre", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Rua de Santa Catarina (Porto)", "color": "#E2000D", "value": 220, "rent": 18},
        {"name": "Sorte 2", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida Infante Santo (Lisboa)", "color": "#E2000D", "value": 220, "rent": 18},
        {"name": "Rua Júlio Diniz (Porto)", "color": "#E2000D", "value": 240, "rent": 20},
        {"name": "Estação de S. Bento (Porto)", "color": "#C2C7CA", "value": 200, "rent": 25},
        {"name": "Praça da República (Porto)", "color": "#FFED00", "value": 260, "rent": 22},
        {"name": "Avenida Fontes Pereira de Melo (Lisboa)", "color": "#FFED00", "value": 260, "rent": 22},
        {"name": "Companhia das Águas", "color": "#68625E", "value": 150, "rent": 24},
        {"name": "Rotunda da Boavista (Porto)", "color": "#FFED00", "value": 280, "rent": 24},
        {"name": "Vá para a cadeia", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida da Liberdade (Lisboa)", "color": "#01B259", "value": 300, "rent": 26},
        {"name": "Rua dos Clérigos (Porto)", "color": "#01B259", "value": 300, "rent": 26},
        {"name": "Caixa da Comunidade 3", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Avenida do Parque das Nações (Lisboa)", "color": "#01B259", "value": 320, "rent": 28},
        {"name": "Estação de Sta Apolónia (Lisboa)", "color": "#C2C7CA", "value": 200, "rent": 25},
        {"name": "Sorte 3", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Rua das Amoreiras (Lisboa)", "color": "#0068B3", "value": 350, "rent": 35},
        {"name": "Imposto de Luxo", "color": "#CCE5D2", "value": None, "rent": None},
        {"name": "Rossio (Lisboa)", "color": "#0068B3", "value": 400, "rent": 50},
    ]

    def __init__(self):
        """Set up chand and community card piles (shuffle them)"""
        self.chance_chest = ["No movement"]*6 + ["Next station"]*2 + [24, 11, 5, 0, 39, 30, "Back 3 spaces", "Next company"]
        self.community_chest = ["No movement"]*14 + [30, 0]
        random.shuffle(self.chance_chest)
        random.shuffle(self.community_chest)

    def draw_chance(self, position):
        """Handle drawing of a chance card"""
        chance = self.chance_chest.pop(0)  # get first card (top of the pile)
        self.chance_chest.append(chance)  # place card at the end (bottom of the pile)
        if chance == "No movement":
            return position
        elif chance == "Next station":
            if position >= 35:
                return 5
            elif position >= 25:
                return 35
            elif position >= 15:
                return 25
            elif position >= 5:
                return 15
            return 5
        elif chance == "Back 3 spaces":
            if position < 3:
                return 37 + position
            else:
                return position - 3
        elif chance == "Next company":
            if position >= 12 and position < 28:
                return 28
            else:
                return 12
        else:
            return chance

    def draw_community(self, position):
        """Handle drawing of a community card"""
        community = self.community_chest.pop(0)  # get first card (top of the pile)
        self.community_chest.append(community)  # place card at the end (bottom of the pile)
        if community == "No movement":
            return position
        else:
            return community


class Player:
    def __init__(self, board):
        """Set starting game info"""
        self.position = 0  # starting position
        self.visits = []  # save spaces
        self.board = board  # initialize board
        self.doubles = 0  # doubles rolled in a row
        self.jail = False  # whether or not in jail
        self.jail_exit_attempts = 0  # number of attempts to exit jail

    def play(self):
        """Play the game"""
        # Check if player stays in jail
        if self.jail_exit_attempts == 3:
            self.jail = False

        # Roll dice
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        if die1 == die2:
            self.jail = False
            self.doubles += 1
        else:
            self.doubles = 0
        
        if self.doubles == 3:
            self.position = 10  # Go to jail
            self.jail = True
            self.doubles = 0
        elif self.jail:
            self.jail_exit_attempts += 1
        else:
            self.position = (self.position + die1 + die2) % 40
            if self.position in [7, 22, 36]:
                self.position = self.board.draw_chance(self.position)
            if self.position in [2, 17, 33]:
                self.position = self.board.draw_community(self.position)
            if self.position == 30:
                self.position = 10
                self.jail = True
        self.visits.append(self.board.SPACES[self.position]["name"])


def run(save=False):
    # Games
    visits = []
    for i in range(GAMES):
        board = Board()
        player = Player(board)
        # Die rolls in each game
        for j in range(DIE_ROLLS_PER_GAME * PLAYERS):
            player.play()
            visits += player.visits

    if save:
        with open('visits.csv', 'w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(visits)

    return visits


if __name__ == "__main__":
    run()

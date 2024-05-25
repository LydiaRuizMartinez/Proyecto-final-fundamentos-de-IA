"""
agente_bayesiano.py

Fundamentos de Inteligencia Artificial - IMAT
ICAI, Universidad Pontificia Comillas

Proyecto realizado por Lydia Ruiz Martínez

Descripción:
Definición de las clases usadas en el agente lógico bayesiano.
"""

# Import necessary modules

import random
from colorama import Fore


class Room:
    """
    Class that represents a room in the game
    """

    def __init__(self, element, color, position):
        # Constructor for Room class
        self.element = element
        self.color = color
        self.position = position

    def __str__(self):
        # String representation of a room, combining color and element
        return f"{self.color}{self.element}{Fore.RESET}"


class Palace:
    """
    Class that represents the game map (palace)
    """

    def __init__(self, dimension):
        # Constructor for Palace class
        self.dimension = dimension

        # Define different types of rooms with specific elements and colors
        self.base_cell = Room("|::::|", "", (0, 0))
        self.entry_cell = Room("|::::|", Fore.YELLOW, (0, 0))
        self.exit_cell = Room("|:S::|", Fore.GREEN, (0, 0))
        self.CW_cell = Room("|:CW:|", Fore.RED, (0, 0))
        self.D_cell = Room("|:D::|", Fore.MAGENTA, (0, 0))
        self.F_cell = Room("|:F::|", Fore.MAGENTA, (0, 0))
        self.P_cell = Room("|:P::|", Fore.MAGENTA, (0, 0))
        self.monster_cell = Room("|:M::|", Fore.LIGHTCYAN_EX, (0, 0))
        self.CK_cell = Room("|:CK:|", Fore.BLUE, (0, 0))

        self.exit_monster_cell = Room("|:SM:|", Fore.LIGHTCYAN_EX, (0, 0))
        self.exit_ck_cell = Room("|SCK:|", Fore.BLUE, (0, 0))
        self.monster_ck_cell = Room("|MCK:|", Fore.BLUE, (0, 0))
        self.exit_monster_ck_cell = Room("|SCKM|", Fore.BLUE, (0, 0))

        self.F_D_cell = Room("|:FD:|", Fore.MAGENTA, (0, 0))
        self.F_P_cell = Room("|:FP:|", Fore.MAGENTA, (0, 0))
        self.D_P_cell = Room("|:DP:|", Fore.MAGENTA, (0, 0))
        self.F_D_P_cell = Room("|FDP:|", Fore.MAGENTA, (0, 0))

        # Initialize the game board with the base cell and generate the map
        self.board = [[self.base_cell] * self.dimension for _ in range(self.dimension)]

        # Generate the map with entry, exit, and special elements
        self.generate_map()

    def generate_map(self):
        # Method to generate the game map by placing elements on the board
        entry_x, entry_y = 0, 0
        self.board[entry_x][entry_y] = self.entry_cell

        self.board[0][0] = self.CW_cell

        f_x, f_y = self.get_random_position()
        self.board[f_x][f_y] = self.F_cell

        d_x, d_y = self.get_random_position()
        self.board[d_x][d_y] = self.D_cell

        p_x, p_y = self.get_random_position()
        self.board[p_x][p_y] = self.P_cell

        if (f_x, f_y) == (d_x, d_y) and (f_x, f_y) == (p_x, p_y):
            self.board[f_x][f_y] = self.F_D_P_cell

        elif (f_x, f_y) == (d_x, d_y):
            self.board[f_x][f_y] = self.F_D_cell

        elif (f_x, f_y) == (p_x, p_y):
            self.board[f_x][f_y] = self.F_P_cell

        elif (d_x, d_y) == (p_x, p_y):
            self.board[d_x][d_y] = self.D_P_cell

        exit_x, exit_y = self.get_second_random_position()
        self.board[exit_x][exit_y] = self.exit_cell

        monster_x, monster_y = self.get_second_random_position()
        self.board[monster_x][monster_y] = self.monster_cell

        ck_x, ck_y = self.get_second_random_position()
        self.board[ck_x][ck_y] = self.CK_cell

        if (exit_x, exit_y) == (monster_x, monster_y) and (exit_x, exit_y) == (
            ck_x,
            ck_y,
        ):
            self.board[monster_x][monster_y] = self.exit_monster_ck_cell

        elif (exit_x, exit_y) == (monster_x, monster_y):
            self.board[monster_x][monster_y] = self.exit_monster_cell

        elif (exit_x, exit_y) == (ck_x, ck_y):
            self.board[exit_x][exit_y] = self.exit_ck_cell

        elif (monster_x, monster_y) == (ck_x, ck_y):
            self.board[monster_x][monster_y] = self.monster_ck_cell

    def get_random_position(self):
        # Helper method to get a random position on the board
        while True:
            x, y = random.randint(0, self.dimension - 1), random.randint(
                0, self.dimension - 1
            )
            if (x, y) != (0, 0) and (x, y) != (1, 0) and (x, y) != (0, 1):
                return x, y

    def get_second_random_position(self):
        # Helper method to get a second random position on the board
        while True:
            x, y = random.randint(0, self.dimension - 1), random.randint(
                0, self.dimension - 1
            )
            if (x, y) != (0, 0) and (
                self.board[x][y] != self.F_D_cell
                and self.board[x][y] != self.F_P_cell
                and self.board[x][y] != self.D_P_cell
                and self.board[x][y] != self.F_D_P_cell
                and self.board[x][y] != self.F_cell
                and self.board[x][y] != self.P_cell
                and self.board[x][y] != self.D_cell
            ):
                return x, y

    def display_palace(self):
        # Print the current state of the palace board
        for row in self.board:
            print("".join(str(room) for room in row))

    def find_element_position(self, element):
        # Method to find the position of a specific element on the board
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.board[x][y].element == element:
                    return x, y
        return None

    # Various methods to check the type of a room at a given position
    def is_precipice(self, position):
        x, y = position
        return (
            self.board[x][y].element == "|:F::|"
            or self.board[x][y].element == "|:FD:|"
            or self.board[x][y].element == "|:DP:|"
            or self.board[x][y].element == "|FDP:|"
            or self.board[x][y].element == "|:FP:|"
            or self.board[x][y].element == "|:P::|"
            and self.board[x][y].element == "|:D::|"
        )

    def is_monster(self, position):
        x, y = position
        return (
            self.board[x][y].element == "|:M::|"
            or self.board[x][y].element == "|:SM:|"
            or self.board[x][y].element == "|MCK:|"
            or self.board[x][y].element == "|SCKM|"
        )

    def is_coronel(self, position):
        x, y = position
        return (
            self.board[x][y].element == "|:CK:|"
            or self.board[x][y].element == "|SCK:|"
            or self.board[x][y].element == "|MCK:|"
            or self.board[x][y].element == "|SCKM|"
        )

    def is_exit(self, position):
        x, y = position
        return (
            self.board[x][y].element == "|:S::|"
            or self.board[x][y].element == "|:SM:|"
            or self.board[x][y].element == "|SCK:|"
            or self.board[x][y].element == "|SCKM|"
        )

    def is_secure(self, position):
        x, y = position
        return not (self.palace.is_monster() or self.palace.is_precipice())


class CaptainWillard:
    """
    Class that represents Captain Willard
    """

    def __init__(self, palace):
        self.position = (0, 0)
        self.palace = palace
        self.alive = True
        self.monster_defeated = False
        self.kurtz_found = False
        self.explored_cells = []

    # Captain Willard's actions: move, detonate, exit

    def move(self, direction):
        # Move Captain Willard in a given direction
        new_position = self.calculate_new_position(direction)

        if self.is_valid_move(new_position):
            # Update explored cells and handle specific cases (precipice, monster, Kurtz)
            self.explored_cells.append(self.position)
            x, y = self.position

            if (
                self.palace.board[new_position[0]][new_position[1]]
                == self.palace.base_cell
            ):
                (
                    self.palace.board[x][y],
                    self.palace.board[new_position[0]][new_position[1]],
                ) = (self.palace.base_cell, self.palace.board[x][y])

            else:
                if self.palace.is_precipice(new_position):
                    self.alive = False
                    print(
                        "¡Ahhh! Capitán Willard ha caído en un precipicio. Ha muerto."
                    )

                elif self.palace.is_monster(new_position):
                    self.alive = False
                    print(
                        "¡Ahhh! Capitán Willard ha sido devorado por el monstruo. Ha muerto."
                    )

                else:
                    if self.palace.is_coronel(new_position):
                        self.kurtz_found = True
                        (
                            self.palace.board[x][y],
                            self.palace.board[new_position[0]][new_position[1]],
                        ) = self.palace.base_cell, Room(
                            "|CWCK|", Fore.LIGHTYELLOW_EX, (0, 0)
                        )
                        print(
                            "Está en la misma celda que en Coronel Kurtz, ahora viaja junto a él."
                        )
                        

            self.position = new_position

        else:
            print("Movimiento no válido. ¡No puedes atravesar las paredes!")

    def calculate_new_position(self, direction):

        x, y = self.position

        if direction == "arriba":
            return x - 1, y
        elif direction == "abajo":
            return x + 1, y
        elif direction == "izquierda":
            return x, y - 1
        elif direction == "derecha":
            return x, y + 1

    def is_valid_move(self, position):
        x, y = position
        return 0 <= x < self.palace.dimension and 0 <= y < self.palace.dimension

    def detonate(self):

        dart = 1
        adjacent_cells = self.get_adjacent_cells()
        monster_position = self.palace.find_element_position("|:M::|")

        if monster_position in adjacent_cells and dart > 0:
            print("¡Boom! El dardo ha tenido efecto y has derrotado al monstruo.")
            self.defeat_monster(monster_position)
            self.monster_defeated = True
            dart -= 1
            self.get_perception()[7] == True

        elif monster_position not in adjacent_cells:
            print(
                "No hay monstruo cerca. El dardo no ha tenido efecto. Ya no dispone de más recursos."
            )
            dart -= 1

        else:
            print("No tiene más dardos disponibles.")

    def defeat_monster(self, monster_position):
        x, y = monster_position
        if self.palace.board == "|:M::|":
            self.palace.board[x][y] = self.palace.base_cell
        elif [x][y].element == "|:SM:|":
            self.palace.board[x][y] = self.palace.exit_cell
        elif self.board[x][y].element == "|MCK:|":
            self.palace.board[x][y] = self.palace.CK_cell
        elif self.board[x][y].element == "|SCKM|":
            self.palace.board[x][y] = self.palace.exit_ck_cell

    def get_adjacent_cells(self):
        x, y = self.position
        adjacent_cells = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [cell for cell in adjacent_cells if self.is_valid_move(cell)]

    def exit_palace(self):
        # Attempt to exit the palace
        if self.palace.is_exit(self.position):
            if self.kurtz_found:
                print(
                    "¡Felicidades! Has completado tu misión y has encontrado a Kurtz. Has ganado."
                )
                self.alive = False
            else:
                print("Te has rendido.")
                self.alive = False
        else:
            print("Solo puedes realizar esta acción si estás en la celda de salida.")

    # Captain Willard's perceptions

    def get_perception(self):
        adjacent_cells = self.get_adjacent_cells()

        fire_positions = [
            self.palace.find_element_position("|:F::|"),
            self.palace.find_element_position("|:FD:|"),
            self.palace.find_element_position("|:FP:|"),
            self.palace.find_element_position("|FDP:|"),
        ]
        spikes_positions = [
            self.palace.find_element_position("|:P::|"),
            self.palace.find_element_position("|:FP:|"),
            self.palace.find_element_position("|:DP:|"),
            self.palace.find_element_position("|FDP:|"),
        ]
        darts_positions = [
            self.palace.find_element_position("|:D::|"),
            self.palace.find_element_position("|:FD:|"),
            self.palace.find_element_position("|:DP:|"),
            self.palace.find_element_position("|FDP:|"),
        ]

        monster_positions = [
            self.palace.find_element_position("|:M::|"),
            self.palace.find_element_position("|:SM:|"),
            self.palace.find_element_position("|MCK:|"),
            self.palace.find_element_position("|SCKM|"),
        ]

        exit_positions = [
            self.palace.find_element_position("|:S::|"),
            self.palace.find_element_position("|:SM:|"),
            self.palace.find_element_position("|SCK:|"),
            self.palace.find_element_position("|SCKM|"),
        ]

        fire = any(position in adjacent_cells for position in fire_positions)
        spikes = any(position in adjacent_cells for position in spikes_positions)
        darts = any(position in adjacent_cells for position in darts_positions)
        smelly = any(position in adjacent_cells for position in monster_positions)
        glowing = (
            any(position in adjacent_cells for position in exit_positions)
            or self.position in exit_positions
        )
        wall_up = self.position[0] == 0
        wall_down = self.position[0] == self.palace.dimension - 1
        wall_left = self.position[1] == 0
        wall_right = self.position[1] == self.palace.dimension - 1
        shout = False
        found_kurtz = self.kurtz_found

        return [
            fire,
            spikes,
            darts,
            smelly,
            glowing,
            wall_up,
            wall_down,
            wall_left,
            wall_right,
            shout,
            found_kurtz,
        ]


class BayesianLogicAgent:
    """
    Class that represents a bayesian knowledge-based agent
    """

    def __init__(self, palace, capitan):
        self.palace = palace
        self.capitan = capitan
        self.F_matrix = [
            [None] * self.palace.dimension for _ in range(self.palace.dimension)
        ]
        self.P_matrix = [
            [None] * self.palace.dimension for _ in range(self.palace.dimension)
        ]
        self.D_matrix = [
            [None] * self.palace.dimension for _ in range(self.palace.dimension)
        ]
        self.M_matrix = [
            [None] * self.palace.dimension for _ in range(self.palace.dimension)
        ]
        self.S_matrix = [
            [None] * self.palace.dimension for _ in range(self.palace.dimension)
        ]

        self.F_visited_cells = set()
        self.P_visited_cells = set()
        self.D_visited_cells = set()
        self.M_visited_cells = set()
        self.S_visited_cells = set()

    def posterior_F(self):
        # Method to calculate the posterior distribution for the fire trap
        percepts = self.capitan.get_perception()
        adjacent_cells = self.capitan.get_adjacent_cells()
        self.F_visited_cells.update(adjacent_cells)

        if percepts[0]:
            percept = True
            adjacent_null_cells = []
            adjacent_non_null_cells = []
            for cell in adjacent_cells:
                x, y = cell[0], cell[1]
                if self.F_matrix[x][y] == 0.00:
                    adjacent_null_cells.append(cell)
                else:
                    adjacent_non_null_cells.append(cell)
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    self.F_matrix[x][y] = 0.00
            for cell in adjacent_non_null_cells:
                x, y = cell[0], cell[1]
                self.F_matrix[x][y] = 1 / len(adjacent_non_null_cells)

        else:
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    if (x, y) in self.F_visited_cells:
                        self.F_matrix[x][y] = 0.0
                    else:
                        self.F_matrix[x][y] = 1 / (
                            (self.palace.dimension) ** 2 - len(self.F_visited_cells)
                        )

        return self.F_matrix

    # Methods for calculating posterior distributions for other traps and entities
    def posterior_P(self):
        percepts = self.capitan.get_perception()
        adjacent_cells = self.capitan.get_adjacent_cells()
        self.P_visited_cells.update(adjacent_cells)

        if percepts[1]:
            adjacent_null_cells = []
            adjacent_non_null_cells = []
            for cell in adjacent_cells:
                x, y = cell[0], cell[1]
                if self.P_matrix[x][y] == 0.00:
                    adjacent_null_cells.append(cell)
                else:
                    adjacent_non_null_cells.append(cell)
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    self.P_matrix[x][y] = 0.00
            for cell in adjacent_non_null_cells:
                x, y = cell[0], cell[1]
                self.P_matrix[x][y] = 1 / len(adjacent_non_null_cells)
        else:
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    if (x, y) in self.F_visited_cells:
                        self.P_matrix[x][y] = 0.0
                    else:
                        self.P_matrix[x][y] = 1 / (
                            (self.palace.dimension) ** 2 - len(self.P_visited_cells)
                        )

        return self.P_matrix

    def posterior_D(self):
        percepts = self.capitan.get_perception()
        adjacent_cells = self.capitan.get_adjacent_cells()
        self.D_visited_cells.update(adjacent_cells)

        if percepts[2]:
            adjacent_null_cells = []
            adjacent_non_null_cells = []
            for cell in adjacent_cells:
                x, y = cell[0], cell[1]
                if self.D_matrix[x][y] == 0.00:
                    adjacent_null_cells.append(cell)
                else:
                    adjacent_non_null_cells.append(cell)
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    self.D_matrix[x][y] = 0.00
            for cell in adjacent_non_null_cells:
                x, y = cell[0], cell[1]
                self.D_matrix[x][y] = 1 / len(adjacent_non_null_cells)
        else:
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    if (x, y) in self.F_visited_cells:
                        self.D_matrix[x][y] = 0.0
                    else:
                        self.D_matrix[x][y] = 1 / (
                            (self.palace.dimension) ** 2 - len(self.D_visited_cells)
                        )

        return self.D_matrix

    def posterior_M(self):
        percepts = self.capitan.get_perception()
        adjacent_cells = self.capitan.get_adjacent_cells()
        self.M_visited_cells.update(adjacent_cells)

        if percepts[3]:
            adjacent_null_cells = []
            adjacent_non_null_cells = []
            for cell in adjacent_cells:
                x, y = cell[0], cell[1]
                if self.M_matrix[x][y] == 0.00:
                    adjacent_null_cells.append(cell)
                else:
                    adjacent_non_null_cells.append(cell)
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    self.M_matrix[x][y] = 0.00
            for cell in adjacent_non_null_cells:
                x, y = cell[0], cell[1]
                self.M_matrix[x][y] = 1 / len(adjacent_non_null_cells)
        else:
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    if (x, y) in self.F_visited_cells:
                        self.M_matrix[x][y] = 0.0
                    else:
                        self.M_matrix[x][y] = 1 / (
                            (self.palace.dimension) ** 2 - len(self.M_visited_cells)
                        )

        return self.M_matrix

    def posterior_S(self):
        percepts = self.capitan.get_perception()
        adjacent_cells = self.capitan.get_adjacent_cells()
        self.S_visited_cells.update(adjacent_cells)

        if percepts[4]:
            adjacent_null_cells = []
            adjacent_non_null_cells = []
            for cell in adjacent_cells:
                x, y = cell[0], cell[1]
                if self.S_matrix[x][y] == 0.00:
                    adjacent_null_cells.append(cell)
                else:
                    adjacent_non_null_cells.append(cell)
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    self.S_matrix[x][y] = 0.00
            for cell in adjacent_non_null_cells:
                x, y = cell[0], cell[1]
                self.S_matrix[x][y] = 1 / len(adjacent_non_null_cells)
        else:
            for x, row in enumerate(self.palace.board):
                for y, room in enumerate(row):
                    if (x, y) in self.F_visited_cells:
                        self.S_matrix[x][y] = 0.0
                    else:
                        self.S_matrix[x][y] = 1 / (
                            (self.palace.dimension) ** 2 - len(self.S_visited_cells)
                        )

        return self.S_matrix

    # Method to display the posterior distributions for different elements
    def display_palace_prob(self, element, position, perception, captain_position):
        posterior_distribution_F = self.posterior_F()
        print("Posterior para la trampa de fuego:")
        for i, row in enumerate(self.palace.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end=" ")
                else:
                    print(f"{posterior_distribution_F[i][j]:.2f}", end=" ")
            print()

        posterior_distribution_P = self.posterior_P()
        print("Posterior para la trampa de pinchos:")
        for i, row in enumerate(self.palace.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end=" ")
                else:
                    print(f"{posterior_distribution_P[i][j]:.2f}", end=" ")
            print()

        posterior_distribution_D = self.posterior_D()
        print("Posterior para la trampa de dardos:")
        for i, row in enumerate(self.palace.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end=" ")
                else:
                    print(f"{posterior_distribution_D[i][j]:.2f}", end=" ")
            print()

        posterior_distribution_M = self.posterior_M()
        print("Posterior para el monstruo:")
        for i, row in enumerate(self.palace.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end=" ")
                else:
                    print(f"{posterior_distribution_M[i][j]:.2f}", end=" ")
            print()

        posterior_distribution_S = self.posterior_S()
        print("Posterior para la salida:")
        for i, row in enumerate(self.palace.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end=" ")
                else:
                    print(f"{posterior_distribution_S[i][j]:.2f}", end=" ")
            print()

"""
agente_logico.py

Fundamentos de Inteligencia Artificial - IMAT
ICAI, Universidad Pontificia Comillas

Proyecto realizado por Lydia Ruiz Martínez

Descripción:
Definición de las clases usadas en el agente lógico.
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

    # Define special elements with their colors and quantities
    elements = [
        (Room("|:P::|", Fore.MAGENTA, (0, 0)), 3),
        (Room("|:M::|", Fore.LIGHTCYAN_EX, (0, 0)), 1),
        (Room("|:CW:|", Fore.RED, (0, 0)), 1),
        (Room("|:CK:|", Fore.BLUE, (0, 0)), 1),
    ]

    def __init__(self, dimension):
        # Initialize the palace with a given dimension
        self.dimension = dimension

        # Define base, entry, and exit cells
        self.base_cell = Room("|::::|", "", (0, 0))
        self.entry_cell = Room("|::::|", Fore.YELLOW, (0, 0))
        self.exit_cell = Room("|:S::|", Fore.GREEN, (0, 0))

        # Create a 2D board filled with base cells
        self.board = [[self.base_cell] * self.dimension for _ in range(self.dimension)]

        # Generate the map with entry, exit, and special elements
        self.generate_map()

    def generate_map(self):
        # Set the entry cell at position (0, 0)
        entry_x, entry_y = 0, 0
        self.board[entry_x][entry_y] = self.entry_cell

        # Set the exit cell at a random position
        exit_x, exit_y = self.get_random_position()
        self.board[exit_x][exit_y] = self.exit_cell

        # Place special elements on the map
        for room, count in self.elements:
            if room.element == "|:CW:|":
                self.board[0][0] = room
            elif room.element == "|:CK:|":
                self.place_element(room, count)
            else:
                self.place_other_element(room, count)

    def get_random_position(self):
        # Get a random position on the map that is not occupied
        while True:
            x, y = random.randint(0, self.dimension - 1), random.randint(
                0, self.dimension - 1
            )
            if self.board[x][y] == self.base_cell:
                return x, y

    def place_element(self, room, count):
        # Place a specific element on the map in random positions
        for _ in range(count):
            x, y = self.get_random_position()
            self.board[x][y] = room

    def place_other_element(self, room, count):
        # Place elements (excluding specific positions) on the map in random positions
        for _ in range(count):
            while True:
                x, y = self.get_random_position()
                if (x, y) != (1, 0) and (x, y) != (0, 1):
                    break
            self.board[x][y] = room

    def display_palace(self):
        # Print the current state of the palace board
        for row in self.board:
            print("".join(str(room) for room in row))

    def display_palace_player(self, captain_position):
        # Print the current state of the palace board with Captain Willard's position
        for i, row in enumerate(self.board):
            for j, room in enumerate(row):
                if (i, j) == captain_position:
                    print(str(room), end="")
                else:
                    print("|::::|", end="")
            print()

    def find_element_position(self, element):
        # Find the position of a specific element on the map
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.board[x][y].element == element:
                    return x, y
        return None

    def is_precipice(self, position):
        # Check if a specific position contains a precipice
        x, y = position
        return self.board[x][y].element == "|:P::|"

    def is_monster(self, position):
        # Check if a specific position contains a monster
        x, y = position
        return self.board[x][y].element == "|:M::|"

    def is_coronel(self, position):
        # Check if a specific position contains Colonel Kurtz
        x, y = position
        return self.board[x][y].element == "|:CK:|"

    def is_exit(self, position):
        # Check if a specific position contains the exit
        x, y = position
        return self.board[x][y].element == "|:S::|"

    def is_secure(self, position):
        # Check if a specific position is not dangerous (not a precipice or monster)
        x, y = position
        return (
            self.palace.board[x][y].element != "|:P::|"
            and self.palace.board[x][y].element != "|:M::|"
        )


class CaptainWillard:
    """
    Class that represents Captain Willard
    """

    def __init__(self, palace):
        # Initialize Captain Willard with starting attributes
        self.position = (0, 0)
        self.palace = palace
        self.alive = True
        self.monster_defeated = False
        self.kurtz_found = False
        self.explored_cells = []

    # Captain Willard's actions: MOVE, DETONATE, EXIT

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
        # Calculate the new position based on the given direction
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
        # Check if a given position is within the palace boundaries
        x, y = position
        return 0 <= x < self.palace.dimension and 0 <= y < self.palace.dimension

    def detonate(self):
        # Detonate a grenade to defeat the monster if it's adjacent

        adjacent_cells = self.get_adjacent_cells()
        monster_position = self.palace.find_element_position("|:M::|")

        if monster_position in adjacent_cells:
            print("¡Boom! La granada haexplotado y has derrotado al monstruo.")
            self.defeat_monster(monster_position)
            self.monster_defeated = True
            self.get_perception()[7] == True

        else:
            print("No hay monstruo cerca. La granada no ha tenido efecto. ")

    def defeat_monster(self, monster_position):
        # Remove the defeated monster from the board
        x, y = monster_position
        self.palace.board[x][y] = self.palace.base_cell

    def get_adjacent_cells(self):
        # Get the positions of cells adjacent to Captain Willard's current position
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
        # Get perceptions based on Captain Willard's current state
        adjacent_cells = self.get_adjacent_cells()
        monster_position = self.palace.find_element_position("|:M::|")
        exit_position = self.palace.find_element_position("|:S::|")

        breezy = any(self.palace.is_precipice(cell) for cell in adjacent_cells)
        smelly = monster_position in adjacent_cells
        glowing = self.position == exit_position or exit_position in adjacent_cells
        wall_up = self.position[0] == 0
        wall_down = self.position[0] == self.palace.dimension - 1
        wall_left = self.position[1] == 0
        wall_right = self.position[1] == self.palace.dimension - 1
        shout = False
        found_kurtz = self.kurtz_found

        return [
            breezy,
            smelly,
            glowing,
            wall_up,
            wall_down,
            wall_left,
            wall_right,
            shout,
            found_kurtz,
        ]


class LogicAgent:
    """
    Class that represents a logical agent
    """

    def __init__(self, capitan):
        # Initialize the logical agent with secure cells and a knowledge base
        self.secure_cells = {(0, 0)}
        self.knowledge_base = {
            "Precipicios": set(),
            "Monstruo": set(),
            "Coronel": set(),
        }
        self.capitan = capitan

    def update_kb(self, cell, perception):
        # Update the knowledge base based on perceptions
        if perception[0]:
            possible_prec = self.capitan.get_adjacent_cells()
            for precipice_cell in possible_prec:
                if (
                    precipice_cell not in self.secure_cells
                    and precipice_cell != self.capitan.position
                ):
                    self.knowledge_base["Precipicios"].add(precipice_cell)
        elif perception[1]:
            possible_monster = self.capitan.get_adjacent_cells()
            for monster_cell in possible_monster:
                if (
                    monster_cell not in self.secure_cells
                    and monster_cell != self.capitan.position
                ):
                    self.knowledge_base["Monstruo"].add(monster_cell)
        elif not (perception[0] or perception[1]):
            if cell not in self.secure_cells:
                self.secure_cells.add(cell)
                adjacent_secure_cells = self.capitan.get_adjacent_cells()
                self.secure_cells.update(adjacent_secure_cells)
        elif perception[8]:
            self.knowledge_base["Coronel"].add(cell)

    def is_safe_cell(self, cell):
        # Check if a cell is safe (not dangerous)
        return cell in self.secure_cells

    def most_probable_precipice_location(self):
        # Get the most probable locations of precipices
        return self.knowledge_base["Precipicios"]

    def most_probable_monster_location(self):
        # Get the most probable locations of the monster
        return self.knowledge_base["Monstruo"]

    def definitely_dangerous_cells(self):
        # Get cells that are definitely dangerous (precipice or monster)
        all_dangerous_cells = self.knowledge_base["Precipicios"].union(
            self.knowledge_base["Monstruo"]
        )
        return all_dangerous_cells - self.secure_cells

    def logic_agent(self):
        # Provide logical recommendations based on perceptions and knowledge base
        perceptions = self.capitan.get_perception()
        current_cell = self.capitan.position

        self.update_kb(current_cell, perceptions)

        print(f"Celdas seguras: {self.secure_cells}")
        if self.knowledge_base["Coronel"]:
            print(
                f"Se ha inferido que el coronel está en: {self.knowledge_base['Coronel']}"
            )

        if not (perceptions[0] or perceptions[1]):
            print(
                "Puedes desplazarte a donde quieras, todas las celdas adyacentes a la actual son seguras."
            )

        if perceptions[0]:
            print(f"Cuidado, en una celda adyacente hay un precipicio.")
            print(
                f"Inferencia: El precipicio probablemente está en la celda {self.most_probable_precipice_location()}."
            )

        if perceptions[1]:
            print(
                f"Cuidado, en una celda adyacente está el monstruo. ¡Aprovecha y explota la granada!"
            )
            print(
                f"Inferencia: El monstruo probablemente está en la celda {self.most_probable_monster_location()}."
            )

        print(f"Celdas definitivamente peligrosas: {self.definitely_dangerous_cells()}")

        if self.capitan.position not in self.secure_cells:
            print("Es necesario moverse a una celda segura.")
        else:
            adjacent_cells = self.capitan.get_adjacent_cells()
            safe_adjacent_cells = [
                cell for cell in adjacent_cells if self.is_safe_cell(cell)
            ]
            print(f"Celdas adyacentes seguras: {safe_adjacent_cells}")

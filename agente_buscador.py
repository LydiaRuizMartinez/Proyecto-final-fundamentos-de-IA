"""
agente_buscador.py

Fundamentos de Inteligencia Artificial - IMAT
ICAI, Universidad Pontificia Comillas

Proyecto realizado por Lydia Ruiz Martínez

Descripción:
Definición de las clases usadas en el agente buscador.
"""

# Import necessary modules

import random

class Node:
    """
    Class that represents a state in the search space
    """
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __str__(self):
        return f"Estado: {self.state} Acción: {self.action}\n"


class Environment:
    """
    Class that represents the 2D grid where the agent moves
    """
    def __init__(self, dimension=6):
        # Initialize the environment with a given dimension
        self.dimension = dimension
        self.tablero = [[" "] * dimension for _ in range(dimension)]
        self.start = (0, 0)
        self.goal = (0, 0)
        self.cw = None
        self.colocar_elementos()

    def colocar_elementos(self):
        # Place the goal and agent (CW) in random positions on the grid
        self.goal = self.generar_posicion_aleatoria()
        self.start = (0, 0)
        while self.start == self.goal:
            self.goal = self.generar_posicion_aleatoria()
        self.cw = self.start
        self.tablero[self.start[0]][self.start[1]] = "CW"
        self.tablero[self.goal[0]][self.goal[1]] = "CK"

    def generar_posicion_aleatoria(self):
        # Generate a random position within the grid
        return random.randint(0, self.dimension - 1), random.randint(
            0, self.dimension - 1
        )

    def imprimir(self, solution=None, frontier=None, explored=None):
        # Print the current state of the environment
        print("Situación del palacio:")
        for i, row in enumerate(self.tablero):
            for j, col in enumerate(row):
                if col == "CK":
                    print("|:CK:|", end="")
                elif col == "CW":
                    print("|:CW:|", end="")
                else:
                    print("|::::|", end="")
            print()
        print()

    def actualizar_posicion_cw(self, nueva_posicion):
        # Update the position of the agent in the environment
        old_pos = self.cw
        self.tablero[old_pos[0]][old_pos[1]] = " "
        self.cw = nueva_posicion
        self.tablero[nueva_posicion[0]][nueva_posicion[1]] = "CW"


class AgentBFS:
    """
    Class that represents an agent using Breadth-First Search
    """
    def __init__(self, environment):
        # Initialize the agent with the starting node in the frontier
        self.frontier = [Node(state=environment.start)]
        self.explored = set()
        self.goal_state = environment.goal
        self.environment = environment

    def actions(self, node):
        # Define possible actions (movements) for the agent
        row, col = node.state
        possible_actions = [
            ("arriba", (row - 1, col)),
            ("abajo", (row + 1, col)),
            ("izquierda", (row, col - 1)),
            ("derecha", (row, col + 1)),
        ]
        return possible_actions

    def result(self, node):
        # Generate child nodes based on the agent's actions
        children = []
        height = len(self.environment.tablero)
        width = len(self.environment.tablero[0])

        for action, (r, c) in self.actions(node):
            if 0 <= r < height and 0 <= c < width:
                children.append(Node(state=(r, c), parent=node, action=action))

        return children

    def is_goal(self, node):
        # Check if the agent has reached the goal state
        return node.state == self.goal_state
    
    def print_solution(self, goal_node):
        # Print the solution path from the start to the goal state
        solution_path = self.extract_solution_path(goal_node)
        print("Ruta hacia Coronel Kurtz:")
        for node in solution_path:
            print(node)
        print()

    def extract_solution_path(self, goal_node):
        # Extract the solution path by traversing back through parent nodes
        path = []
        current_node = goal_node
        while current_node:
            path.insert(0, current_node)
            current_node = current_node.parent
        return path

    def solve(self):
        # Perform Breadth-First Search to find the goal state
        while self.frontier:
            current_node = self.frontier.pop(0)
            self.explored.add(current_node.state)

            if self.is_goal(current_node):
                print("¡Coronel Kurtz encontrado!")
                self.environment.actualizar_posicion_cw(current_node.state)
                self.environment.imprimir()

                self.print_solution(current_node)
                return

            for child in self.result(current_node):
                if child.state not in self.explored and child not in self.frontier:
                    self.frontier.append(child)

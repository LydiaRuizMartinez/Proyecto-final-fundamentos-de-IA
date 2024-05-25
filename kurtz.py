"""
kurtz.py

Fundamentos de Inteligencia Artificial - IMAT
ICAI, Universidad Pontificia Comillas

Proyecto realizado por Lydia Ruiz Martínez

Descripción:
Código principal del proyecto invocable con el comando "python kurtz.py".
"""

# Importing three different modules for logical agent, bayesian agent, and search agent

import agente_logico as log
import agente_bayesiano as bay
import agente_buscador as bus

# Checking if the script is being run as the main module

if __name__ == "__main__":

    valid_action = False
    
    while not valid_action:
        # Asking the user for the type of gameplay: logical agent, bayesian agent, or search agent
        action = input(
            "Ingresa la forma de jugar: agente lógico, agente bayesiano o agente de búsqueda:"
        )
        

        # Code for the logical agent gameplay
        if action == "agente lógico":
            valid_action = True
            # Creating instances of the logical agent classes and setting up the game environment
            palace = log.Palace(dimension=6)
            willard = log.CaptainWillard(palace)
            logic_agent = log.LogicAgent(willard)

            # Displaying the initial state of the game palace
            palace.display_palace()
            print(" ")
            palace.display_palace_player(willard.position)

            # Main game loop for logical agent gameplay
            while willard.alive:
                percept = willard.get_perception()
                print("Percepciones:", percept)

                # Asking the user for their action: move, detonate, or exit
                action = input("Ingresa tu acción (mover, detonar, salir): ").lower()

                # Handling different actions
                if action == "mover":
                    direction = input(
                        "Ingresa la dirección (arriba, abajo, izquierda, derecha): "
                    ).lower()
                    if direction in ["arriba", "abajo", "izquierda", "derecha"]:
                        willard.move(direction)
                        if willard.alive:
                            logic_agent.logic_agent()
                        palace.display_palace()
                        palace.display_palace_player(willard.position)
                    else:
                        print(
                            "Dirección no válida. Por favor, ingresa una dirección válida."
                        )
                elif action == "detonar":
                    willard.detonate()
                    logic_agent.logic_agent()
                    palace.display_palace()
                    palace.display_palace_player(willard.position)
                elif action == "salir":
                    willard.exit_palace()
                    logic_agent.logic_agent()
                    palace.display_palace()
                    palace.display_palace_player(willard.position)
                else:
                    print("Acción no válida. Las opciones son: mover, detonar, salir.")

            print("Juego terminado. Gracias por jugar.")

        # Code for Bayesian agent gameplay
        elif action == "agente bayesiano":
            valid_action = True
            # Creating instances of the Bayesian agent classes and setting up the game environment
            palace = bay.Palace(dimension=6)
            willard = bay.CaptainWillard(palace)
            bayesian_agent = bay.BayesianLogicAgent(palace, willard)

            # Displaying the initial state of the game palace
            palace.display_palace()

            # Main game loop for Bayesian agent gameplay
            while willard.alive:
                percept = willard.get_perception()
                print("Percepciones:", percept)

                element = "CK"
                position = (0, 0)

                # Updating Bayesian probabilities and displaying the palace with probabilities
                bayesian_agent.display_palace_prob(
                    element, position, percept, willard.position
                )

                # Asking the user for their action: move, detonate, or exit
                action = input("Ingresa tu acción (mover, detonar, salir): ").lower()

                # Handling different actions
                if action == "mover":
                    direction = input(
                        "Ingresa la dirección (arriba, abajo, izquierda, derecha): "
                    ).lower()
                    if direction in ["arriba", "abajo", "izquierda", "derecha"]:
                        willard.move(direction)
                        if willard.alive:
                            palace.display_palace()
                    else:
                        print(
                            "Dirección no válida. Por favor, ingresa una dirección válida."
                        )
                elif action == "detonar":
                    willard.detonate()
                    palace.display_palace()
                elif action == "salir":
                    willard.exit_palace()
                else:
                    print("Acción no válida. Las opciones son: mover, detonar, salir.")

            print("Juego terminado. Gracias por jugar.")

        # Code for search agent gameplay
        elif action == "agente de búsqueda":
            valid_action = True
            # Creating instances of the search agent classes and setting up the game environment
            environment = bus.Environment(dimension=6)
            environment.imprimir()
            agent = bus.AgentBFS(environment)
            agent.solve()

        # Handling the case when an invalid gameplay mode is entered
        else:
            print( 
                "Forma de jugar no válida. Las opciones son: agente lógico, agente bayesiano o agente de búsqueda"
            )

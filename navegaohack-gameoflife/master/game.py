import pygame
import numpy as np
import time

pygame.init()

width, height = 600, 600

screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1, Muertas = 0
gameState = np.zeros((nxC,nyC))

#control de la ejecución
pauseExect = False
#finalización del programa
Run = True

#creando autómata palo
gameState[10, 10] = 1
gameState[11, 10] = 1
gameState[12, 10] = 1

#creando autómata planeador
gameState[2, 2] = 1
gameState[3, 3] = 1
gameState[4, 3] = 1
gameState[3, 4] = 1
gameState[4, 2] = 1



while Run:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    
    # velocidad en segundos, a menos segundos, más rápido el juego
    time.sleep(0.1)

    # Registrando eventos de teclado y ratón
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            Run = not Run
        else:
            if event.type == pygame.KEYDOWN:
                pauseExect = not pauseExect
            
            mouseClick = pygame.mouse.get_pressed()

            if sum(mouseClick) > 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                newGameState[celX, celY] = not mouseClick[2]

    if pauseExect:
        coloring = (220, 24, 64)
    else:
        coloring = (128, 128, 128)
    
    for y in range(0, nxC):
        for x in range(0, nyC):

            #controlando la actualización de estados
            if not pauseExect:

                # Calculando el número de vecinos cercanos
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x)     % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y)     % nyC] + \
                          gameState[(x + 1) % nxC, (y)     % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x)     % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule  1: Una célula muerta con exactamente 3 vecinas vivas "revive"                    
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule 2: Una célula viva con menos de 2 o más de 3 vecinas vivas "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [( x      * dimCW,  y      * dimCH),
                    ((x + 1) * dimCW,  y      * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ( x      * dimCW, (y + 1) * dimCH)]

            # Dibujando la celda para cada par de x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, coloring, poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
            
    gameState = np.copy(newGameState)

    pygame.display.flip()

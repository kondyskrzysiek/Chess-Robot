# import bibliotek
import pygame
from pygame.locals import *

# definiuje wymiary i parametry okna
windowSurface = pygame.display.set_mode((420, 100), 1, 32)
pygame.display.set_caption('Chess Visual Interpretation - Loading API')

import sys
import math
import os
import DobotDllType as dType

api = dType.load()

dobotSelect = ["COM5", "COM9"]

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

# definiuje wymiary i parametry okna
windowSurface = pygame.display.set_mode((450, 100), 1, 32)
pygame.display.set_caption('Chess Visual Interpretation - Connecting To Dobot')

#Connect Dobot

def sync(state):
    if (state == dType.DobotConnect.DobotConnect_NoError):
        # Clean Command Queued
        dType.SetQueuedCmdClear(api)

        # Async Motion Params Setting
        dType.SetHOMEParams(api, 150, 0, 0, 0, isQueued=1)
        dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)
        dType.SetPTPCommonParams(api, 100, 100, isQueued=1)

        # Async Home:
        dType.SetHOMECmd(api, temp=0, isQueued=1)

        # Start to Execute Command Queued
        dType.SetQueuedCmdStartExec(api)
        dType.SetQueuedCmdStopExec(api)
        dType.DisconnectDobot(api)


sync(dType.ConnectDobot(api, "COM5", 115200)[0])
sync(dType.ConnectDobot(api, "COM9", 115200)[0])

# funkcja pomagajaca w implementacji obrazkow
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

# definicja wielkosci pola
xSize = 80
ySize = xSize

# initializacja pygame'a
pygame.init()

# zmienne od roszady
blackKingMoved = 0
whiteKingMoved = 0
leftBlackRook = 0
rightBlackRook = 0
leftWhiteRook = 0
rightWhiteRook = 0

# definicja kolorow i zminnych odpowiedizalnych za select
SELECTED_WHITE = (246, 246, 130)
SELECTED_GREEN = (186, 202, 68)
SELECTED_X = 0
SELECTED_Y = 0
isSelected = 0

# tablica ktora przechowuje wartosc o tym czy jakis pionek dotarl na skraj mapy
isChange = [0,0]

def dobotMove(x, y, z, r):
    dType.SetQueuedCmdStartExec(api)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued=1)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdStartExec(api)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued=1)
    dType.SetQueuedCmdStartExec(api)
    

# funkcja move odpowiedzialna za poruszanie figur
def move(startX, startY, endX, endY):
    global isChange
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

# przenosi figure jesli takowa istnieje
    if board[startY][startX] != 0:
        if startY >= 4 and endY >= 4:
            buffer = board[startY][startX]
            board[startY][startX] = 0
            board[endY][endX] = buffer
            dType.ConnectDobot(api, dobotSelect[0], 115200)
            dobotMove(150 + (7-startY) * 40, 200 - endX * 40, 0, 0)
            dobotMove(150 + (7-endY) * 40, 200 - endX * 40, 0, 0)
            dobotMove(150, 0, 0, 0)
            dType.DisconnectDobot(api)
        elif startY < 4 and endY < 4:
            buffer = board[startY][startX]
            board[startY][startX] = 0
            board[endY][endX] = buffer
            dType.ConnectDobot(api, dobotSelect[1], 115200)
            dobotMove(150 + startY * 40, -200 + startX * 40, 0, 0)
            dobotMove(150 + endY * 40, -200 + endX * 40, 0, 0)
            dobotMove(150, 0, 0, 0)
            dType.DisconnectDobot(api)
        else:
            if startY >= 4:
                buffer = board[startY][startX]
                board[startY][startX] = 0
                board[endY][endX] = buffer
                dType.ConnectDobot(api, dobotSelect[0], 115200)
                dobotMove(150 + (7-startY) * 40, 200 - startX * 40, 0, 0)
                dobotMove(200, -200, 0, 0)
                dobotMove(150, 0, 0, 0)
                dType.DisconnectDobot(api)
                dType.ConnectDobot(api, dobotSelect[1], 115200)
                dType.dSleep(3000)
                dobotMove(200, 200, 0, 0)
                dobotMove(150 + endY * 40, -200 + endX * 40, 0, 0)
                dobotMove(150, 0, 0, 0)
                dType.DisconnectDobot(api)
            elif startY < 4:
                buffer = board[startY][startX]
                board[startY][startX] = 0
                board[endY][endX] = buffer
                dType.ConnectDobot(api, dobotSelect[1], 115200)
                dobotMove(150 + startY * 40, -200 + startX * 40, 0, 0)
                dobotMove(200, 200, 0, 0)
                dobotMove(150, 0, 0, 0)
                dType.DisconnectDobot(api)
                dType.ConnectDobot(api, dobotSelect[0], 115200)
                dType.dSleep(3000)
                dobotMove(200, -200, 0, 0)
                dobotMove(150 + (7-endY) * 40, 200 - endX * 40, 0, 0)
                dobotMove(150, 0, 0, 0)
                dType.DisconnectDobot(api)

# sprawdza czy figura dotarla do kranca mapy
    if endY == 0 and board[endY][endX] == 11:
        isChange[0] = 2
        isChange[1] = endX
    if endY == 7 and board[endY][endX] == 1:
        isChange[0] = 1
        isChange[1] = endX

    print(f'Moved ({startX}, {startY}) to ({endX}, {endY}), white king is: {whiteKingMoved}, black: {blackKingMoved}')
    print(f'Left Black Rook: {leftBlackRook}, Right Black Rook: {rightBlackRook}')
    print(f'Left White Rook: {leftWhiteRook}, Right White Rook: {rightWhiteRook}')

    updateScreen()

# odswieza ekran
def updateScreen():
    ITERATION = 0

# przechodzi przez kazde pole
    while ITERATION < 64:
        spawnY = ITERATION / 8
        spawnY = math.floor(spawnY)
        spawnX = ITERATION - spawnY * 8

# sprawdza czy jest selected i spawnuje pole
        if isSelected == 1 and spawnX == SELECTED_X and spawnY == SELECTED_Y:
            COLOR = SELECTED_GREEN

            if spawnY % 2 == 0 and spawnX % 2 == 0:
                COLOR = SELECTED_WHITE
            if spawnY % 2 != 0 and spawnX % 2 != 0:
                COLOR = SELECTED_WHITE
        else:
            COLOR = (118, 150, 86)

            if spawnY % 2 == 0 and spawnX % 2 == 0:
                COLOR = (238, 238, 210)
            if spawnY % 2 != 0 and spawnX % 2 != 0:
                COLOR = (238, 238, 210)

        pygame.draw.rect(windowSurface,
                         COLOR, ((spawnX * xSize), (spawnY * ySize), xSize, ySize))

# spawnuje  czarne figury na planszy
        if board[spawnY][spawnX] != 0:
            if board[spawnY][spawnX] == 14:
                image = get_image('GFX\BlackRook.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 12:
                image = get_image('GFX\BlackHorse.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 13:
                image = get_image('GFX\BlackBishop.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 11:
                image = get_image('GFX\BlackPawn.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 15:
                image = get_image('GFX\BlackQueen.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 16:
                image = get_image('GFX\BlackKing.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
# spawnuje biale figury na planszy
            elif board[spawnY][spawnX] == 4:
                image = get_image('GFX\WhiteRook.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 2:
                image = get_image('GFX\WhiteHorse.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 3:
                image = get_image('GFX\WhiteBishop.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 1:
                image = get_image('GFX\WhitePawn.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 5:
                image = get_image('GFX\WhiteQueen.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)
            elif board[spawnY][spawnX] == 6:
                image = get_image('GFX\WhiteKing.png')

                imageRect = image.get_rect()
                imageRect.centerx = math.floor(spawnX * xSize + xSize / 2)
                imageRect.centery = math.floor(spawnY * ySize + ySize / 2 + 4)

                windowSurface.blit(image, imageRect)

# spawnuje pole do wyboru zamiany pionka
        if isChange[0] != 0:
            pygame.draw.rect(windowSurface,
                             (0, 0, 0), ((math.floor(xSize * 2 - 12.5), math.floor(xSize * 3.5 - 10)), (345, 90)))
            pygame.draw.rect(windowSurface,
                             (255, 255, 255),
                             ((math.floor(xSize * 2 - 11.5), math.floor(xSize * 3.5 - 9)), (343, 88)))
            if isChange[0] == 1:
                i = 0

                while i < 4:
                    pygame.draw.rect(windowSurface,
                                     (0, 0, 0), (
                                         (math.floor(xSize * 2 - 8.5 + i * (5 + xSize)),
                                          math.floor(xSize * 3.5 - 6)), (xSize + 2, ySize + 2)))
                    pygame.draw.rect(windowSurface,
                                     (255, 255, 255), (
                                         (math.floor(xSize * 2 - 7.5 + i * (5 + xSize)),
                                          math.floor(xSize * 3.5 - 5)), (xSize, ySize)))
# spawnuje biale piony zamiany
                    if i + 2 == 4:
                        image = get_image('GFX\WhiteRook.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 2 == 5:
                        image = get_image('GFX\WhiteQueen.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 2 == 3:
                        image = get_image('GFX\WhiteBishop.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 2 == 2:
                        image = get_image('GFX\WhiteHorse.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)

                    i += 1

            elif isChange[0] == 2:
                i = 0

                while i < 4:
                    pygame.draw.rect(windowSurface,
                                     (0, 0, 0), (
                                         (math.floor(xSize * 2 - 8.5 + i * (5 + xSize)),
                                          math.floor(xSize * 3.5 - 6)), (xSize + 2, ySize + 2)))
                    pygame.draw.rect(windowSurface,
                                     (255, 255, 255), (
                                         (math.floor(xSize * 2 - 7.5 + i * (5 + xSize)),
                                          math.floor(xSize * 3.5 - 5)), (xSize, ySize)))

#zamienia numery na obrazki podczas zamiany piona w figure
                    if i + 12 == 14:
                        image = get_image('GFX\BlackRook.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 12 == 15:
                        image = get_image('GFX\BlackQueen.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 12 == 13:
                        image = get_image('GFX\BlackBishop.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    elif i + 12 == 12:
                        image = get_image('GFX\BlackHorse.png')

                        imageRect = image.get_rect()
                        imageRect.centerx = math.floor(xSize * 2.5 - 7.5 + i * (5 + xSize))
                        imageRect.centery = math.floor(xSize * 4 - 5)

                        windowSurface.blit(image, imageRect)
                    i += 1

        ITERATION += 1
        pygame.display.update()

# ustawienie czcionki
basicFont = pygame.font.SysFont(None, 48)

# definicja glownej tablicy
board = [[4, 2, 3, 6, 5, 3, 2, 4],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [11, 11, 11, 11, 11, 11, 11, 11],
         [14, 12, 13, 16, 15, 13, 12, 14]]

# definiuje wymiary i parametry okna
windowSurface = pygame.display.set_mode((xSize * 8, ySize * 8), 1, 32)
pygame.display.set_caption('Chess Visual Interpretation - Dobot')
updateScreen()

# definicja zmiennych eventu klikniecia
clickOrder = 1
clickStartX = 0
clickStartY = 0
clickEndX = 0
clickEndY = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            # Disconnect Dobot
            dType.DisconnectDobot(api)
            pygame.quit()
            sys.exit()
# event klikniecia ktory odpowiada za cale sterowanie
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isChange[0] == 0:
                # jesli zaden z pionkow  nie jest przy granicy to ma dwa state'y
                # w pierszym pobiera skad sie ruszyc
                # w drugim pobiera gdzie masz sie ruszyc
                if clickOrder == 1:
                    clickStartX, clickStartY = event.pos
                    isSelected = 1
                    SELECTED_X = math.floor(clickStartX / xSize)
                    SELECTED_Y = math.floor(clickStartY / xSize)
                    updateScreen()
                    if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] != 0:
                        clickOrder = 2
                elif clickOrder == 2:
                    clickEndX, clickEndY = event.pos
                    clickOrder = 1
                    isSelected = 0

                    intXstart = math.floor(clickStartX / xSize)
                    intYstart = math.floor(clickStartY / xSize)
                    intXend = math.floor(clickEndX / xSize)
                    intYend = math.floor(clickEndY / xSize)

                    # sprawdza czy czarny moze bic swoich
                    if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] > 10:
                        if board[math.floor(clickEndY / xSize)][math.floor(clickEndX / xSize)] < 10:

                            # wykrywa ruch czarnej lewej wiezy
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 14 and \
                                        math.floor(clickStartX / xSize) == 0:
                                leftBlackRook = 1

                            # wykrywa ruch czarnej prawej wiezy
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 14 and \
                                        math.floor(clickStartX / xSize) == 7:
                                rightBlackRook = 1

                            #CORE KING MOVEMENT
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 16:
                                print(f'{intYend - intYstart} on Y and {intXend-intXstart} on X')
                                #roszada
                                if intYend - intYstart == 0 and intXend-intXstart == -2 and \
                                        leftBlackRook == 0 and blackKingMoved == 0:
                                    move(intXstart, intYstart, intXend, intYend)
                                    move(0, 7, 2, 7)
                                    blackKingMoved = 1
                                    break
                                elif intYend - intYstart == 0 and intXend-intXstart == 2 and \
                                        rightBlackRook == 0 and blackKingMoved == 0:
                                    move(intXstart, intYstart, intXend, intYend)
                                    move(7, 7, 4, 7)
                                    blackKingMoved = 1
                                    break
                                    # movement
                                if math.fabs(intYend - intYstart) <= 1 and math.fabs(intXend-intXstart) <= 1:
                                    move(intXstart, intYstart, intXend, intYend)
                                    blackKingMoved = 1
                                    break
                            else:
                                move(intXstart, intYstart, intXend, intYend)
                                break

                    # sprawdza czy bialy moze bic swoich
                    if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] < 10:
                        if board[math.floor(clickEndY / xSize)][math.floor(clickEndX / xSize)] > 10 or \
                                board[math.floor(clickEndY / xSize)][math.floor(clickEndX / xSize)] == 0:

                            # wykrywa czy ruszyla sie lewa biala wieza
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 4 and \
                                    math.floor(clickStartX / xSize) == 0:
                                leftWhiteRook = 1

                            # wykrywa czy ruszyla sie prawa biala wieza
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 4 and \
                                        math.floor(clickStartX / xSize) == 7:
                                rightWhiteRook = 1

                            # CORE KING MOVEMENT
                            if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] == 6:
                                print(f'{intYend - intYstart} on Y and {intXend - intXstart} on X')
                                # roszada
                                if intYend - intYstart == 0 and intXend - intXstart == -2 and \
                                        leftWhiteRook == 0 and whiteKingMoved == 0:
                                    move(intXstart, intYstart, intXend, intYend)
                                    move(0, 0, 2, 0)
                                    whiteKingMoved = 1
                                    break
                                elif intYend - intYstart == 0 and intXend - intXstart == 2 and \
                                        rightWhiteRook == 0 and whiteKingMoved == 0:
                                    move(intXstart, intYstart, intXend, intYend)
                                    move(7, 0, 4, 0)
                                    whiteKingMoved = 1
                                    break
                                    # movement
                                if math.fabs(intYend - intYstart) <= 1 and math.fabs(intXend - intXstart) <= 1:
                                    move(intXstart, intYstart, intXend, intYend)
                                    whiteKingMoved = 1
                                    break
                            else:
                                move(intXstart, intYstart, intXend, intYend)
                                break

                    clickStartX, clickStartY = event.pos
                    isSelected = 1
                    SELECTED_X = math.floor(clickStartX / xSize)
                    SELECTED_Y = math.floor(clickStartY / xSize)
                    updateScreen()
                    if board[math.floor(clickStartY / xSize)][math.floor(clickStartX / xSize)] != 0:
                        clickOrder = 2
            # jesli pionek jest przy granicy zmusza do wybrania jakiejs opcji
            elif isChange[0] == 1:
                clickStartX, clickStartY = event.pos
                if 3.5 * xSize < clickStartY < 4.5 * xSize:
                    i = 0
                    while i < 4:
                        if xSize * 2 - 7.5 + i * (5 + xSize) < clickStartX < xSize * 3 - 7.5 + i * (5 + xSize):
                            board[7][isChange[1]] = i + 2
                            isChange[0] = 0
                            updateScreen()
                        i += 1
            elif isChange[0] == 2:
                clickStartX, clickStartY = event.pos
                if 3.5 * xSize < clickStartY < 4.5 * xSize:
                    i = 0
                    while i < 4:
                        if xSize * 2 - 7.5 + i * (5 + xSize) < clickStartX < xSize * 3 - 7.5 + i * (5 + xSize):
                            board[0][isChange[1]] = i + 12
                            isChange[0] = 0
                            isChange[0] = 0
                            updateScreen()
                        i += 1

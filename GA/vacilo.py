import random
import pygame
import math

pygame.init()
tela = pygame.display.set_mode((600, 600))

t = 30      #tamanho da celula
grid = []
visitados = []
stack = []
col = []
familia = []

def construir_grid(x, y,):
    for i in range(0, 5):
        y = y + 30
        x = 30
        for j in range(0, 5):
            pygame.draw.line(tela, (0, 0, 0), [x, y], [x + t, y])           # top of cell
            pygame.draw.line(tela, (0, 0, 0), [x + t, y], [x + t, y + t])   # right of cell
            pygame.draw.line(tela, (0, 0, 0), [x + t, y + t], [x, y + t])   # bottom of cell
            pygame.draw.line(tela, (0, 0, 0), [x, y + t], [x, y])           # left of cell
            paredes = [1, 1, 1, 1]
            f = [0]
            col.append((x, y, paredes, f))
            grid.append((x, y))
            x = x + 30

def vai_cima(x, y):
    pygame.draw.rect(tela, (255, 0, 255), (x + 1, y - t + 1, 29, 59), 0)         # draw a rectangle twice the width of the cell
    index = grid.index((x, y))
    col[index][2][0] = 0
    pygame.display.update()


def vai_baixo(x, y):
    pygame.draw.rect(tela, (255, 0, 255), (x +  1, y + 1, 29, 59), 0)
    index = grid.index((x, y))
    col[index][2][1] = 0
    pygame.display.update()


def vai_esquerda(x, y):
    pygame.draw.rect(tela, (255, 0, 255), (x - t +1, y +1, 59, 29), 0)
    index = grid.index((x, y))
    col[index][2][2] = 0
    pygame.display.update()


def vai_direita(x, y):
    pygame.draw.rect(tela, (255, 0, 255), (x +1, y +1, 59, 29), 0)
    index = grid.index((x, y))
    col[index][2][3] = 0
    pygame.display.update()


def gerar_lab(x, y):
    stack.append((x,y))                                            # place starting cell into stack
    visitados.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        cell = []                                                  # define cell list
        if (x + t, y) not in visitados and (x + t, y) in grid:       # right cell available?
            cell.append("direita")                                   # if yes add to cell list

        if (x - t, y) not in visitados and (x - t, y) in grid:       # left cell available?
            cell.append("esquerda")

        if (x , y + t) not in visitados and (x , y + t) in grid:     # down cell available?
            cell.append("baixo")

        if (x, y - t) not in visitados and (x , y - t) in grid:      # up cell available?
            cell.append("cima")

        if len(cell) > 0:                                          # check to see if cell list is empty
            direcao_escolhida = (random.choice(cell))                    # select one of the cell randomly

            if direcao_escolhida  == "direita":                             # if this cell has been chosen
                vai_direita(x, y)                                   # call push_right function
                x = x + t                                          # make this cell the current cell
                index = grid.index((x, y))
                col[index][2][2] = 0
                visitados.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif direcao_escolhida  == "esquerda":
                vai_esquerda(x, y)
                x = x - t
                index = grid.index((x, y))
                col[index][2][3] = 0
                visitados.append((x, y))
                stack.append((x, y))

            elif direcao_escolhida  == "baixo":
                vai_baixo(x, y)
                y = y + t
                index = grid.index((x, y))
                col[index][2][0] = 0
                visitados.append((x, y))
                stack.append((x, y))

            elif direcao_escolhida  == "cima":
                vai_cima(x, y)
                y = y - t
                index = grid.index((x, y))
                col[index][2][1] = 0
                visitados.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack

def calcula_f(x, y, ix, iy, fx, fy):
    ponto_ix = ix
    ponto_iy = iy
    ponto_fx = fx
    ponto_fy = fy


    g = (math.fabs((ponto_ix - x)/30) + math.fabs((ponto_iy - y)/30)) * 10
    h = (math.fabs((ponto_fx - x)/30) + math.fabs((ponto_fy - y)/30)) * 10
    f = int(g + h)
    return f


def a_star(x, y, x2, y2):
    lista_a = []
    lista_f = []
    pai = []
    ponto_fx, ponto_fy = x2, y2
    ponto_ix, ponto_iy = x, y
    menor = 0
    cheguei = True

    while cheguei:
        index = grid.index((x, y))
        lista_f.append((x, y))
        if (x + t, y) in grid and col[index][2][3] == 0 and (x + t, y) not in lista_f: #direita
            if(x + t, y) not in lista_a:
                lista_a.append(grid.index((x + t, y)))
            pai = [(x, y), (x + t, y)]
            familia.append(pai)
            pai = []
            col[grid.index((x + t, y))][3][0] = calcula_f(x + t, y, ponto_ix, ponto_iy, ponto_fx, ponto_fy)
            pygame.draw.rect(tela, (255, 0, 0), (x + t + 1, y + 1, 29, 29), 0)
            pygame.display.update()
        if (x - t, y) in grid and col[index][2][2] == 0 and (x - t, y) not in lista_f: #esquerda
            if(x - t, y) not in lista_a:
                lista_a.append(grid.index((x - t, y)))
            pai = [(x, y), (x - t, y)]
            familia.append(pai)
            pai = []
            col[grid.index((x - t, y))][3][0] = calcula_f(x - t, y, ponto_ix, ponto_iy, ponto_fx, ponto_fy)
            pygame.draw.rect(tela, (255, 0, 0), (x - t + 1, y + 1, 29, 29), 0)
            pygame.display.update()
        if (x, y - t) in grid and col[index][2][0] == 0 and (x, y - t) not in lista_f: #cima
            if(x, y - t) not in lista_a:
                lista_a.append(grid.index((x, y - t)))
            pai = [(x, y), (x, y - t)]
            familia.append(pai)
            pai = []
            col[grid.index((x, y - t))][3][0] = calcula_f(x, y - t, ponto_ix, ponto_iy, ponto_fx, ponto_fy)
            pygame.draw.rect(tela, (255, 0, 0), (x + 1, y - t + 1, 29, 29), 0)
            pygame.display.update()
        if (x, y + t) in grid and col[index][2][1] == 0 and (x, y + t) not in lista_f: #baixo
            if(x, y + t) not in lista_a:
                lista_a.append(grid.index((x, y + t)))
            pai = [(x, y), (x, y + t)]
            familia.append(pai)
            pai = []
            col[grid.index((x, y + t))][3][0] = calcula_f(x, y + t, ponto_ix, ponto_iy, ponto_fx, ponto_fy)
            pygame.draw.rect(tela, (255, 0, 0), (x + 1, y + t + 1, 29, 29), 0)
            pygame.display.update()

        for i in range(len(lista_a)):
            if i+1 <= len(lista_a)-1:
                if col[lista_a[i]][3][0] <= col[lista_a[i+1]][3][0]:
                    menor = lista_a[i]
            elif menor == 0:
                menor = lista_a[i]

        x = col[menor][0]
        y = col[menor][1]
        lista_a.remove(menor)
        menor = 0
        pintados = []
        if ponto_fx == x and ponto_fy == y:
            pintarX = ponto_fx
            pintarY = ponto_fy

            while pintarX != ponto_ix or pintarY != ponto_iy:
                for itemLista in familia:
                    if(itemLista[1][0] == pintarX and itemLista[1][1] == pintarY):
                        pygame.draw.rect(tela, (0, 255, 255), (pintarX + 8, pintarY + 8, 10, 10), 0)  # used to show the solution
                        pygame.display.update()
                        pintados.append((itemLista))
                        pintarX = itemLista[0][0]
                        pintarY = itemLista[0][1]
            pygame.draw.rect(tela, (0, 255, 255), (pintarX + 8, pintarY + 8, 10, 10), 0)
            cheguei = False





x, y = 30, 30
#i2 = int(input('Digite o numero de linhas: '))
#j2 = int(input('Digite o numero de colunas: '))

construir_grid(0, 0)
gerar_lab(x, y)
a_star(30, 30, 90, 90)
pygame.display.update()

# ##### pygame loop #######
aberto = True
while aberto:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            aberto = False
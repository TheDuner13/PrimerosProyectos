import pygame as pg
import random
pg.init()

class Juego:

    def __init__(self,tamano,dificultad,cell_size):
        self.tamano = tamano
        self.dificultad = dificultad
        self.pantalla = pg.display.set_mode((tamano,tamano))
        self.comida = Comida([0,0])
        self.posicion_snake = [0,0]

        self.tamano = [0,0]
        self.cell_size = cell_size
        self.filas = self.tamano[0] // self.cell_size
        self.columnas = self.tamano[1] // self.cell_size
        self.snake = Snake([[10,9,"down"]],"down")
        self.clock = pg.time.Clock()
    
    def jugar(self):
        self.comida.aparecer(self.pantalla,self.cell_size)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP and self.snake.direccion != "down":
                        print("up")
                        self.snake.direccion = "up"
                    elif event.key == pg.K_DOWN and self.snake.direccion != "up":
                        print("down")
                        self.snake.direccion = "down"
                    elif event.key == pg.K_LEFT and self.snake.direccion != "right":
                        print("left")
                        self.snake.direccion = "left"
                    elif event.key == pg.K_RIGHT and self.snake.direccion != "left":
                        self.snake.direccion = "right"
                        print("right")

            self.pintar()
            self.posicion_snake = self.snake.mover()
            print(self.posicion_snake)
            print(self.comida.posicion)
            if self.posicion_snake[0] == self.comida.posicion[0] and self.posicion_snake[1] == self.comida.posicion[1]:
                self.comida.desaparecer()
                self.comida.aparecer(self.pantalla,self.cell_size)
                self.snake.crecer()
            if self.posicion_snake[0] < 0 or self.posicion_snake[0] > 19 or self.posicion_snake[1] < 0 or self.posicion_snake[1] > 19:
                self.snake.perder()
            for segmento in self.snake.segmentos[1:]:
                if self.snake.segmentos[0][0] == segmento[0] and self.snake.segmentos[0][1] == segmento[1]:
                    self.snake.chocar(segmento)
            pg.display.flip()  # Actualiza la pantalla completa
            self.clock.tick(5)

    def pintar(self):
        self.pantalla.fill((0,0,0))
        for segmento in self.snake.segmentos:
            x = segmento[0] * self.cell_size
            y = segmento[1] * self.cell_size
            pg.draw.rect(self.pantalla,(0,200,0),(x,y,self.cell_size,self.cell_size))
        z = self.comida.posicion[0]
        w = self.comida.posicion[1]

        pg.draw.rect(self.pantalla,(200,0,0),(z*self.cell_size,w*self.cell_size,self.cell_size,self.cell_size))


class Snake:

    def __init__(self,segmentos, direccion):
        self.segmentos = segmentos
        self.direccion = direccion
        segmentos = [[10,9,"down"]]

    def mover(self):
        for i in range(len(self.segmentos)-1,0,-1):
                if self.segmentos[i-1][2] == "up":
                    self.segmentos[i][1] -= 1
                elif self.segmentos[i-1][2] == "down":
                    self.segmentos[i][1] += 1
                elif self.segmentos[i-1][2] == "left":
                    self.segmentos[i][0] -= 1
                elif self.segmentos[i-1][2] == "right":
                    self.segmentos[i][0] += 1
        for i in range(len(self.segmentos)-1,0,-1):
            self.segmentos[i][2] = self.segmentos[i-1][2]

        if self.direccion == "up":
            self.segmentos[0][1] -= 1
            self.segmentos[0][2] = "up"

        elif self.direccion == "down":
            self.segmentos[0][1] += 1
            self.segmentos[0][2] = "down"

        elif self.direccion == "left":
            self.segmentos[0][0] -= 1
            self.segmentos[0][2] = "left"

        elif self.direccion == "right":
            self.segmentos[0][0] += 1
            self.segmentos[0][2] = "right"

        return self.segmentos[0]
                

    def crecer(self):
        if self.segmentos[-1][2] == "up":
            self.segmentos.append([self.segmentos[-1][0],self.segmentos[-1][1]+1,"up"])
        elif self.segmentos[-1][2] == "down":
            self.segmentos.append([self.segmentos[-1][0],self.segmentos[-1][1]-1,"down"])
        elif self.segmentos[-1][2] == "left":
            self.segmentos.append([self.segmentos[-1][0]+1,self.segmentos[-1][1],"left"])
        elif self.segmentos[-1][2] == "right":
            self.segmentos.append([self.segmentos[-1][0]-1,self.segmentos[-1][1],"right"])

    def chocar(self,segmento):
        print("chocó alv")
        indice = self.segmentos.index(segmento)
        self.segmentos = self.segmentos[:indice]
    
    def perder(self):
        print("perdiste")
        self.segmentos = [[10,9,"down"]]
                

class Comida:

    def __init__(self,posicion):
        self.posicion = posicion

    def aparecer(self,pantalla,cell_size):
            z = random.randint(1,19) * cell_size
            w = random.randint(1,19) * cell_size
            self.posicion = [z//20,w//20]
            pg.draw.rect(pantalla,(200,0,0),(z,w,cell_size,cell_size))
            pg.display.flip()

    def desaparecer(self):
            self.posicion = None


if __name__ == "__main__":
    juego = Juego(400,1,20)
    juego.jugar()
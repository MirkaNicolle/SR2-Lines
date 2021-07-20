#Codigo ayuda: https://github.com/churly92/Engine3D/blob/main/gl.py
#Repositorio perteneciente a Prof. Carlos Alonso

#Mirka Monzon 18139
#SR2: Lines

import struct 

#Definicion
def char(c):
    return struct.pack('=c' , c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

#Clase
class Render(object):
    #Inicializacion de software render 
    def __init__(self):
        self.framebuffer = []
    
    def glinit(self, widht, height, r, g, b):
        self.glCreateWindow(widht, height)
        self.glClearColor(r, g, b)
        self.glClear()
    
    def clear(self, r, g, b):
        self.framebuffer =[
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

#Funciones de render 
    #Inicializacion de framebuffer
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    #Creacion de espacio para dibujar
    def glViewport(self, x, y, width, height):
        self.viewportWidth = width
        self.viewportHeight = height
        self.xViewport = x
        self.yViewport = y

    #Mapa de bits de un solo color 
    def glClear(self):
        self.clear()

    #Cambio de color de glClear
    def glClearColor(self, r, g, b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.clear(r, g, b)

    #Cambio de color de punto en pantalla
    def glVertex(self, x, y):
        vx = round((x+1)*(self.viewportWidth/2)+self.xViewport)
        vy = round((y+1)*(self.viewportHeight/2)+self.yViewport)
        self.point(vx, vy)

    #Cambio de color con el que funciona glVertex
    def glColor(self, r, g, b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        return color(r, g, b)

    #Funcion para escribir el archivo .BMP
    def glFinish(self, filename):
        f = open(filename, 'bw')

        #Header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()

    #Da el color al punto en pantalla 
    def point(self, x, y):
        self.framebuffer[x][y] = self.glColor(1,1,0)

    def glCordX(self, x):
    	return round((x+1)*(self.viewportWidth/2)+self.xViewport)

    def glCordY(self, y):
    	return round((y+1)*(self.viewportHeight/2)+self.yViewport)

    def glpointi(self, x, y):
    	X = self.glCordX(x)
    	Y = self.glCordY(y)
    	self.point(X, Y)

    #Funcion para linea 
    def glLine(self, x0, y0, x1, y1):
        x0 = self.glCordX(x0)
        y0 = self.glCordY(y0)
        x1 = self.glCordX(x1)
        y1 = self.glCordY(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0 
        threshold =  dx
        y = y0
        inc = 1 if y1 > y0 else -1

        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += 2 * dy
            if offset >= threshold:
                y += inc
                threshold += 2 * dx

r = Render()
r.glCreateWindow(500, 500)
r.glClearColor(0.21, 0.2035, 0.11)
r.glViewport(10, 00, 100, 100)
r.glColor(1, 1, 0)
r.glpointi(-0.5, 1)
r.glColor(0.9,0,0)

#triangulo
r.glLine(-1,-1,0,1)
r.glLine(0, 1, 1, -1)
r.glLine(1, -1, -1, -1)

r.glFinish('out.bmp')
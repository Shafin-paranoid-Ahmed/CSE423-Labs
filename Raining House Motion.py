from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

W_Width, W_Height = 1080, 720

day_t = 1
day_flag = True

x_offset = 0
y_offset = 40

raindrop = []



def specialKeyListener(key, x, y):
    global day_t, day_flag, x_offset, y_offset, df 

    if day_t >= 1:
        day_t = 1
        day_flag = False
    if day_t <= 0:
        day_t = 0
        day_flag = True

    if key==GLUT_KEY_UP:
        if day_flag == False:
            day_t -= 0.075
        else:
            day_t += 0.075

    if key==GLUT_KEY_DOWN:
        if day_flag == False:
            day_t += 0.075
        else:
            day_t -= 0.075

    if key == GLUT_KEY_RIGHT:
        if x_offset < 30:
            x_offset += 5
    elif key == GLUT_KEY_LEFT:
        if x_offset > -30:
            x_offset -= 5
                
    glutPostRedisplay()


def drawRain():
    global x_offset, y_offset, raindrop
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0, 0, 255/255)
    for i in range(600):
        x, y = (random.randint(-1080,1080), random.randint(-720,720))
        raindrop.append((x,y))
        glVertex2f(x, y)
        glVertex2f(x + x_offset, y + y_offset)
    glEnd()

def rainDown():
    global raindrop
    for i in range(600):
        x,y = raindrop[i]
        if y <-W_Height:
            x, y = (random.randint(-W_Width//2, W_Width//2), random.randint(-W_Height, W_Height-y_offset))
    
    glutPostRedisplay()

def drawScene():
    global day_t

    #Background
    glBegin(GL_QUADS)
    glColor3f(day_t, day_t, day_t)
    glVertex2f(-W_Width, -W_Height)
    glVertex2f(-W_Width, W_Height)
    glVertex2f(W_Width, W_Height)
    glVertex2f(W_Width,-W_Height)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(128/255, 90/255, 0)
    glVertex2f(-W_Width//2, -W_Height)
    glVertex2f(-W_Width//2, 150)
    glVertex2f(W_Width//2, 150)
    glVertex2f(W_Width//2,-W_Height)
    glEnd()


    #Trees
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    x = -W_Width
    while x < W_Width:
        glColor3f(0, 1, 0)
        glVertex2f(x, 0)
        glColor3f(0,0,0)
        glVertex2f(x+(54//2),80)
        glColor3f(0, 1, 0)
        glVertex2f(x+54,0)
        x += 54
    glEnd()

    #House

    #white body
    glBegin(GL_QUADS)
    glColor3f(1,1,1)
    glVertex2f(-200, -250)
    glVertex2f(-200, 80)
    glVertex2f(200, 80)
    glVertex2f(200, -250)
    glEnd()

    # violet top head
    glBegin(GL_TRIANGLES)
    glColor3f(80/255,0,1)
    glVertex2f(-250, 80)
    glVertex2f(0, 350)
    glVertex2f(250, 80)
    glEnd()


    #door
    glBegin(GL_QUADS)
    glColor3f(0,0,1)
    glVertex2f(-50, -250)
    glVertex2f(-50, -20)
    glVertex2f(50, -20)
    glVertex2f(50, -250)    
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0,0,0)
    glVertex2f(20, -135)
    glVertex2f(20, -125)
    glVertex2f(40, -125)
    glVertex2f(40, -135)    
    glEnd()


    #windows
    glBegin(GL_QUADS)
    glColor3f(0,0,1)
    glVertex2f(-140, -135)
    glVertex2f(-140, -20)
    glVertex2f(-70, -20)
    glVertex2f(-70, -135)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0,0,1)
    glVertex2f(140, -135)
    glVertex2f(140, -20)
    glVertex2f(70, -20)
    glVertex2f(70, -135)
    glEnd()

    #window grill
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    
    glVertex2f(-105,-20)
    glVertex2f(-105,-135)
    
    glVertex2f(-70, -77.5)
    glVertex2f(-140, -77.5)

    glVertex2f(105,-20)
    glVertex2f(105,-135)

    glVertex2f(70, -77.5)
    glVertex2f(140, -77.5)


    glEnd()





def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,422,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    drawScene()
    drawRain()
    glutSwapBuffers()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)



glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

Window = glutCreateWindow(b"Rain Down On Me")
init()
glutDisplayFunc(display)
glutIdleFunc(rainDown)
glutSpecialFunc(specialKeyListener)

glutMainLoop()
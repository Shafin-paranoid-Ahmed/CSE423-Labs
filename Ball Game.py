# Task 2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random


width, height = 1600, 900
ballsList = []
size = 15
speed = 0.075
pauseFlag = False
blinkFlag = False
visibile = True



class Balls:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        self.color = (random.randint(1,255)/255, random.randint(1,255)/255, random.randint(1,255)/255)



def drawScene():
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0, 0, 1)
    glVertex2f(-800, -450)
    glVertex2f(800, -450)
    glVertex2f(800, -450)
    glVertex2f(800, 450)
    glVertex2f(800, 450)
    glVertex2f(-800, 450)
    glVertex2f(-800, 450)
    glVertex2f(-800, -450)
    glEnd()

def drawBall(ball):
    global visibile, size
    if visibile == True:
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor3f(ball.color[0],ball.color[1],ball.color[2])
        glVertex2d(ball.x, ball.y)
        glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    drawScene()

    for i in ballsList:
        drawBall(i)

    glutSwapBuffers()


def convert_coordinate(x, y):
    global width, height
    a = x - (width // 2)
    b = (height // 2) - y 
    return a, b

def moveBall(ball):
    if pauseFlag == False:
        ball.x += ball.movement[0] * speed
        ball.y += ball.movement[1] * speed
            
        if abs(ball.x) + (size // 2) >= (800):
            ball.movement = (-ball.movement[0], ball.movement[1])
        if abs(ball.y) + (size // 2) >= (450):
            ball.movement = (ball.movement[0], -ball.movement[1])

def animate():
    global ballsList
    for i in ballsList:
        moveBall(i)
    glutPostRedisplay()


def blinking():
    global blinkFlag, visibile
    if blinkFlag == True:
        visibile = not visibile
    glutTimerFunc(1000, lambda _:blinking(), 0)
    glutPostRedisplay()



def mouse_listener(button, state, x, y):
    global ballsList, blinkFlag, pauseFlag

    if button == GLUT_RIGHT_BUTTON:
        if  state == GLUT_DOWN:
            if pauseFlag == False:
                x, y = convert_coordinate(x, y)
                print(x, y)
                new_ball = Balls(x, y)
                ballsList.append(new_ball)
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if pauseFlag == False:
            blinkFlag = not blinkFlag
            if blinkFlag == True:
                blinking()

    glutPostRedisplay()



def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-800, 800, -450, 450, 0, 1)


def keyboard_listener(key, x, y):
    global size, pauseFlag, blinkFlag, visibile
    if key == b' ':
        pauseFlag = not pauseFlag
        if pauseFlag == True:
            blinkFlag = False
            visibile = True
            print("Paused")
        else:
            print("Resumed")
    glutPostRedisplay()

def special_keyboard_listener(key,x,y):
    global speed, pauseFlag

    if key == GLUT_KEY_UP:
        if pauseFlag == False:
            speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        if pauseFlag == False:
            speed /= 1.5



glutInit()
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Ball Game")

init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_keyboard_listener)
glutMouseFunc(mouse_listener)
glutMainLoop()
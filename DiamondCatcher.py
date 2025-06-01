from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

#MPL
def get_zone(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx >= 0 and dy < 0: return 7
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx >= 0 and dy < 0: return 6
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5

def convert_to_zone0(x, y, zone):
    if zone == 0: 
        return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return y, -x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0: 
        return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return -y, x
    elif zone == 3: 
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return y, -x
    elif zone == 7: 
        return x, -y

def draw_point(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def draw_line(x1, y1, x2, y2):
    zone = get_zone(x1, y1, x2, y2)
    x1_z, y1_z = convert_to_zone0(x1, y1, zone)
    x2_z, y2_z = convert_to_zone0(x2, y2, zone)
    dx = x2_z - x1_z
    dy = y2_z - y1_z
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    x, y = x1_z, y1_z

    while x <= x2_z:
        rx, ry = convert_from_zone0(x, y, zone)
        draw_point(rx, ry)
        if d > 0:
            y += 1
            d += incNE
        else:
            d += incE
        x += 1





W_Width, W_Height = 720, 960
button_size = 25
score = 0
diamond = {'x': 100, 'y': 400, 'size': 10, 'color': (1, 1, 0)}
catcher = {'x': 270, 'y': 25, 'width': 140, 'height': 20}


button = {
    "reset": {"x": 25, "y": W_Height-25-button_size, "color":(0.0, 0.5, 0.5), "size" : button_size},
    "pause": {"x": W_Width//2-button_size//2, "y": W_Height-25-button_size ,"color":(1.0, 0.75, 0.5), "size" : button_size},
    "play": {"x": W_Width//2-button_size//2, "y": W_Height-25-button_size, "color":(1.0, 0.75, 0.5), "size" : button_size},
    "cross": {"x": W_Width-button_size-20,"y": W_Height-25-button_size , "color":(1.0, 0.0, 0.0), "size" : button_size}
}
 



fall_speed = 8
is_paused = False
game_over = False


def get_diamond_colors():
    r,g,b = random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)
    return r,g,b

def draw_text(x, y, text):
    glRasterPos2i(x, y)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

def draw_diamond():
    global diamond
    s1 = diamond['size']
    s = s1*2
    x, y = diamond['x'], diamond['y']
    r, g, b = diamond['color']
    glColor3f(r, g, b)
    draw_line(x, y + s, x + s1, y)
    draw_line(x + s1, y, x, y - s)
    draw_line(x, y - s, x - s1, y)
    draw_line(x - s1, y, x, y + s)

def draw_catcher():
    global catcher
    x, y = catcher['x'], catcher['y']
    w, h = catcher['width'], catcher['height']
    w1 = w-30
    x1 = x + w
    x2 = x + (w-w1)//2
    x3 = x2 + w1
    y1 = y - h

    glColor3f(1, 1, 1) if not game_over else glColor3f(1, 0, 0)
    draw_line(x, y, x1, y)
    draw_line(x1, y, x3, y1)
    draw_line(x3, y1, x2, y1)
    draw_line(x2, y1, x, y)

def draw_buttons(shape):
    global button
    x = button[shape]["x"]
    y = button[shape]["y"]
    size = button[shape]["size"]
    r, g, b = button[shape]['color']
    if shape == 'reset':
        glColor3f(r, g, b)
        draw_line(x, y + size//2, x + size, y + size//2)
        draw_line(x, y + size//2, x + size//2, y)
        draw_line(x, y + size//2, x + size//2, y + size)
    elif shape == "play":
        glColor3f(r, g, b)
        draw_line(x, y, x, y + size)
        draw_line(x, y + size, x + size, y+size//2)
        draw_line(x+size, y+size//2, x, y)
    elif shape == "pause":
        glColor3f(r, g, b)
        draw_line(x, y, x, y + size)
        draw_line(x + size//2, y, x + size//2, y + size)
    elif shape == "cross":
        glColor3f(r, g, b)
        draw_line(x, y, x + size, y + size)
        draw_line(x + size, y, x, y + size)

    


def update(value):
    global game_over, score, fall_speed, is_paused
    if not game_over and not is_paused:
        diamond['y'] -= fall_speed
        if (catcher['x'] < diamond['x'] < catcher['x'] + catcher['width'] and
            catcher['y'] < diamond['y'] < catcher['y'] + catcher['height']):
            score += 1
            fall_speed += 0.6
            print(f"Score: {score}")
            reset_diamond()

        elif diamond['y'] < 0:
            game_over = True
            print(f"Game Over\nFinal Score: {score}")

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)


def toggle_pause():
        global is_paused, score
        is_paused = not is_paused
        print("\nGame", "paused." if is_paused else "resumed.")
        print(f"Score: {score}")

def quit_game():
    global score
    print(f"\nGoodbye!\nFinal Score: {score}")
    glutLeaveMainLoop()


def restart_game():
    global is_paused, score, game_over, fall_speed
    score = 0
    fall_speed = 5
    game_over = False
    reset_diamond()
    print("\nStarting Over!")
    print(f"Score: {score}")


def reset_diamond():
    global W_Height, W_Width, button_size
    diamond["x"] = random.randint(button_size, W_Width - button_size)
    diamond["y"] = W_Height - 100
    diamond["color"] = get_diamond_colors()

    




def special_keys(key, x, y):
    if not game_over:
        if key == GLUT_KEY_LEFT:
            catcher['x'] = max(0, catcher['x'] - 12)
        elif key == GLUT_KEY_RIGHT:
            catcher['x'] = min(W_Width - catcher['width'], catcher['x'] + 12)


def keyboard(key, x, y):
    if key == b'\x1b':
        quit_game()
    elif key == b" ":
        toggle_pause()
    elif key == b"r":
        restart_game()



def mouseInput(mouseButton, state, x, y):	
    global button, button_size
    if state != GLUT_DOWN:
        return
    y = W_Height - y
    print(x, y)
    for name, btn in button.items():
        if btn['x'] <= x <= btn['x'] + btn['size'] and btn['y'] <= y <= btn['y'] + btn['size']:
            if name == 'reset':
                restart_game()
            elif name == 'pause':
                toggle_pause()
            elif name == 'play':
                pass
            elif name == 'cross':
                quit_game()


def display():
    global button
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_diamond()
    draw_catcher()
    glColor3f(1,1,1)
    draw_text(25, W_Height-75, f"Score: {score}")
    for i in button:
        if is_paused == True  and i == "pause":
            continue
        elif is_paused == False and i == "play":
            continue
        draw_buttons(i)
    glColor3f(1,1,1)

    if game_over:
        draw_text(W_Width // 2 - 60, W_Height // 2, "GAME OVER")

    glFlush()

def init():
    glClearColor(0, 0, 0, 1)
    gluOrtho2D(0, W_Width, 0, W_Height)



glutInit(sys.argv)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamond!")
init()
reset_diamond()
glutDisplayFunc(display)

glutTimerFunc(30, update, 0)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseInput)
glutMainLoop()

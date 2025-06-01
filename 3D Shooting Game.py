from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random


### look for bugs
## when kill enemy, enemy movespeed faster by 0.01


# Game state variables
x = 0
y = 500
z = -650
camera_pos = [x, y, z]
pl_rotation = 0
fovY = 120
GRID_LENGTH = 800
cam_mode = 0
position = [0, 20, 0]
WALL_HEIGHT = 200
lives = 5
score = 0
missed_bullets = 0
enemies = []
BULLET_SPEED = 15
MAX_BULLET_DISTANCE = 1500
bullets = []
vcam = [0,0,0,
        0,0,0,
        0,0,0]
death_position = []


game_over = False
fixed_cam = False
cheat_mode = False
auto_fire = False
auto_rotate = False
cheat_rotation = 0

ENEMY_HEAD_SIZE = 25
ENEMY_BODY_SIZE = 50





class Bullet:
    def __init__(self, position, direction, is_cheat=False, target=None):
        self.x, self.y, self.z = position
        self.dx = math.sin(math.radians(direction)) * BULLET_SPEED
        self.dz = math.cos(math.radians(direction)) * BULLET_SPEED
        self.distance_traveled = 0
        self.is_cheat = is_cheat
        self.target = target  # Store target enemy reference

    def update(self):
        if self.is_cheat and self.target and self.target.active:
            # Calculate new direction towards current enemy position
            dx = self.target.x - self.x
            dz = self.target.z - self.z
            distance = math.sqrt(dx**2 + dz**2)
            if distance > 0:
                self.dx = (dx/distance) * BULLET_SPEED
                self.dz = (dz/distance) * BULLET_SPEED

        self.x += self.dx
        self.z += self.dz
        self.distance_traveled += BULLET_SPEED


class Enemy:
    def __init__(self):
        # Add this new property
        self.targeted = False
        self.size = ENEMY_BODY_SIZE
        self.x = random.randint(-GRID_LENGTH, GRID_LENGTH)
        self.z = random.randint(-GRID_LENGTH, GRID_LENGTH)
        self.speed = 0.1
        self.active = True
        self.isfive = False
        self.scale = 1.0
        self.scale_dir = 0.1
        self.moving = True


    def update(self, player_pos):
        if not self.active: 
            return
        if not self.moving:
            return
        # Move towards player
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx**2 + dz**2)
        
        if distance > 0:
            self.x += (dx/distance) * self.speed
            self.z += (dz/distance) * self.speed


## DRAWINGS


def draw_player():
    global position, pl_rotation
    if game_over:
        # Draw dead player lying on grid
        glPushMatrix()
        glTranslatef(position[0], 45, position[2])  # Adjusted Y-position to stay above grid
        glRotatef(90, 1, 0, 0)  # Face-down rotation
        glColor3f(85/255, 107/255, 47/255)  # Player color
        glScalef(40, 5, 90)  # Flattened cuboid dimensions
        glutSolidCube(1)
        glPopMatrix()

    # Regular alive player drawing
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glRotatef(pl_rotation, 0, 1, 0)  # Player rotation

    # Main body (green cuboid)
    glPushMatrix()
    glColor3f(85/255, 107/255, 47/255)
    glTranslatef(0, 60, 0)  
    glScalef(40, 90, 40)
    glutSolidCube(1)
    glPopMatrix()

    # Head (black sphere)
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 100, 0)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

    # Arms
    glPushMatrix()
    glColor3f(255/255, 224/255, 189/255)
    # Right arm
    glPushMatrix()
    glTranslatef(25, 70, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    # Left arm
    glPushMatrix()
    glTranslatef(-25, 70, 0)
    glRotatef(90, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
    glPopMatrix()
    glPopMatrix()

    # Legs
    glColor3f(0/255.0, 0/255.0, 255/255.0)
    # Right leg
    glPushMatrix()
    glTranslatef(10, 20, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 60, 20, 20)
    glPopMatrix()
    # Left leg
    glPushMatrix()
    glTranslatef(-10, 20, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 6, 60, 20, 20)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.8)
    glTranslatef(0, 70, 0)
    glutSolidCone(25, 120, 20, 20)
    glPopMatrix()

    glPopMatrix()


def player_dead():
    global position, pl_rotation, game_over
    if game_over:
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        glRotatef(90, 1, 0, 0)
        glRotatef(-pl_rotation, 0, 0, 1)  # Player rotation

        # Main body (green cuboid)
        glPushMatrix()
        glColor3f(85/255, 107/255, 47/255)
        glTranslatef(0, 60, 0)  
        glScalef(40, 90, 40)
        glutSolidCube(1)
        glPopMatrix()

        # Head (black sphere)
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, 100, 0)
        glutSolidSphere(20, 20, 20)
        glPopMatrix()

        # Arms (original implementation)
        glPushMatrix()
        glColor3f(255/255, 224/255, 189/255)
        # Right arm
        glPushMatrix()
        glTranslatef(25, 70, 0)
        glRotatef(90, 0, 0, 1)
        gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
        glPopMatrix()
        # Left arm
        glPushMatrix()
        glTranslatef(-25, 70, 0)
        glRotatef(90, 0, 0, 1)
        gluCylinder(gluNewQuadric(), 10, 10, 50, 20, 20)
        glPopMatrix()
        glPopMatrix()

        # Legs (original implementation)
        glColor3f(0/255.0, 0/255.0, 255/255.0)
        # Right leg
        glPushMatrix()
        glTranslatef(10, 20, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 6, 60, 20, 20)
        glPopMatrix()
        # Left leg
        glPushMatrix()
        glTranslatef(-10, 20, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 10, 6, 60, 20, 20)
        glPopMatrix()

        # Cone-shaped gun (fixed rotation)
        glPushMatrix()
        glColor3f(0.4, 0.4, 0.4)
        glTranslatef(0, 70, 0)  # Position at center of the body
        glRotatef(0, 0, 1, 0)  # Point forward with player
        glutSolidCone(25, 120, 20, 20)  # Base radius, height
        glPopMatrix()

        glPopMatrix()


def draw_bullets():
    glColor3f(1.0, 0.0, 0.0)  # yellow bullets
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet.x, bullet.y, bullet.z)
        glutSolidCube(10)
        glPopMatrix()


def draw_enemies():
    # Red enemies
    for enemy in enemies:
        if not enemy.active: 
            continue

        enemy.scale += enemy.scale_dir * 0.05
        if enemy.scale > 1.2 or enemy.scale < 0.5:
            enemy.scale_dir *= -1


        glPushMatrix()
        glTranslatef(enemy.x, 40, enemy.z)
        
        # Body
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        glScalef(1, enemy.scale, 1)
        glutSolidSphere(enemy.size, 25, 20)
        glPopMatrix()

        # Head
        glColor3f(0.0, 0.0, 0.0)  # Black head
        glTranslatef(0, (enemy.size * enemy.scale + ENEMY_HEAD_SIZE) - 30, 0)
        glScalef(1, enemy.scale, 1)
        glutSolidSphere(ENEMY_HEAD_SIZE, 10, 20)

        glPopMatrix()


def draw_grid():
    global WALL_HEIGHT
    # Draw dynamic grid floor
    cell_size = 50
    for p in range(-GRID_LENGTH, GRID_LENGTH, cell_size):
        for r in range(-GRID_LENGTH, GRID_LENGTH, cell_size):
            if (p // cell_size + r // cell_size) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)
            
            glBegin(GL_QUADS)
            glVertex3f(p, 0, r)
            glVertex3f(p + cell_size, 0, r)
            glVertex3f(p + cell_size, 0, r + cell_size)
            glVertex3f(p, 0, r + cell_size)
            glEnd()

    # Draw boundary walls
    
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()

    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, GRID_LENGTH)
    glEnd()

    glColor3f(0, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glVertex3f(-GRID_LENGTH, WALL_HEIGHT, -GRID_LENGTH)
    glEnd()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)





## LOGIC


def enemycount():
    if len(enemies) < 5:
        for _ in range(5-len(enemies)):
            enemies.append(Enemy())


def check_collisions():
    global bullets, score, lives, missed_bullets
    # Bullet-enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies:
            if not enemy.active: continue
            distance = math.sqrt(
                (bullet.x - enemy.x)**2 +
                (bullet.z - enemy.z)**2
            )
            if distance < enemy.size:
                enemy.active = False
                bullets.remove(bullet)
                score += 1
                respawn_enemy(enemy)
                break

    # Enemy-player collisions
    if not cheat_mode:
        for enemy in enemies:
            if not enemy.active: continue
            distance = math.sqrt(
                (position[0] - enemy.x)**2 +
                (position[2] - enemy.z)**2
            )
            if distance < enemy.size + 40:
                lives -= 1
                print(f"Remaining Player life: {lives}")
                enemy.active = False
                respawn_enemy(enemy)


def respawn_enemy(enemy):
    
    enemy.x = random.randint(-GRID_LENGTH+50, GRID_LENGTH-50)
    if enemy.x == position[0]:
        while enemy.x != position[0]:
            enemy.x = random.randint(-GRID_LENGTH+50, GRID_LENGTH-50)
    
    enemy.z = random.randint(-GRID_LENGTH+50, GRID_LENGTH-50)
    if enemy.z == position[0]:
        while enemy.z != position[0]:
            enemy.z = random.randint(-GRID_LENGTH+50, GRID_LENGTH-50)


    enemy.active = True
    enemy.targeted = False


def gameover():
    global game_over, lives, missed_bullets, enemies
    draw_text(1200, 1200, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
    enemies = []
    player_dead()


def quit_game():
    glutLeaveMainLoop()


def cheat():
    global bullets,pl_rotation

    pl_rotation += 8

    if cheat_mode and auto_fire:
        # Find first active untargeted enemy
        target_enemy = None
        for enemy in enemies:
            if enemy.active and not enemy.targeted:
                target_enemy = enemy
                break
        
        if target_enemy:
            # Calculate initial direction
            dx = target_enemy.x - position[0]
            dz = target_enemy.z - position[2]
            target_angle = math.degrees(math.atan2(dx, dz))
            
            # Create tracking bullet
            start_x = position[0] + math.sin(math.radians(target_angle)) * 50
            start_z = position[2] + math.cos(math.radians(target_angle)) * 50
            bullets.append(Bullet(
                (start_x, position[1] + 70, start_z),
                target_angle,
                is_cheat=True,
                target=target_enemy
            ))
            target_enemy.targeted = True



def update_game_state():
    global bullets, missed_bullets, cheat_rotation, pl_rotation, cheat_mode
    missed = 0
    if not game_over:
        # Update bullets
        bullets = [b for b in bullets if b.distance_traveled < MAX_BULLET_DISTANCE]
        if not cheat_mode:
            missed += len([b for b in bullets if 
                abs(b.x) >= GRID_LENGTH or 
                abs(b.z) >= GRID_LENGTH])
        
        
        missed_bullets += missed
        
        if missed > 0:
            print(f"Bullet Missed: {missed_bullets}")
        

        bullets = [b for b in bullets if 
            abs(b.x) < GRID_LENGTH and 
            abs(b.z) < GRID_LENGTH]
    
        # Update enemies
        for enemy in enemies:
            enemy.update(position)





## INPUT & OUTPUT


def mouseListener(button, state, x, y):
    global bullets, cam_mode
    if not game_over:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            start_x = position[0] + math.sin(math.radians(pl_rotation)) * 50
            start_z = position[2] + math.cos(math.radians(pl_rotation)) * 50
            bullets.append(Bullet((start_x, position[1] + 70, start_z), pl_rotation))
            print("Bullet Fired!")
    
    
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            if cam_mode == 0:
                cam_mode = 1
            else:
                cam_mode = 0



def keyboardListener(key, x, y):
    global position, pl_rotation, cheat_mode, auto_fire, auto_rotate, fixed_cam, game_over, missed_bullets, lives
    
    
    move_speed = 50
    rotate_speed = 5

    if not game_over:
        if key == b'w':
            if (-GRID_LENGTH + 20 <= position[0] + move_speed * math.sin(math.radians(pl_rotation)) <= GRID_LENGTH - 20 and
                    -GRID_LENGTH + 20 <= position[2] + move_speed * math.cos(math.radians(pl_rotation)) <= GRID_LENGTH - 20):
                position[0] += move_speed * math.sin(math.radians(pl_rotation))
                position[2] += move_speed * math.cos(math.radians(pl_rotation))
        elif key == b's':
            if (-GRID_LENGTH + 20 <= position[0] - move_speed * math.sin(math.radians(pl_rotation)) <= GRID_LENGTH -20 and 
                -GRID_LENGTH + 20 <= position[2] - move_speed * math.cos(math.radians(pl_rotation)) <= GRID_LENGTH -20):
                position[0] -= move_speed * math.sin(math.radians(pl_rotation))
                position[2] -= move_speed * math.cos(math.radians(pl_rotation))
        elif key == b'a':
            pl_rotation += rotate_speed
        elif key == b'd':
            pl_rotation -= rotate_speed
        elif key == b'c':  
            cheat_mode = not cheat_mode
            auto_rotate = cheat_mode
            auto_fire = cheat_mode
            fixed_cam = False

        elif key == b'v' and cheat_mode and cam_mode == 1: 
            fixed_cam = not fixed_cam

    if key == b'r':
        position = [0, 20, 0]
        pl_rotation = 0
        missed_bullets = 0
        lives = 5
        game_over = False
        cheat_mode = False

    if key == b'\x1b':
        quit_game()


def specialKeyListener(key, x, y):
    global camera_pos
    cam_speed = 5
    x, y, z = camera_pos
    
    if key == GLUT_KEY_UP:
        y += cam_speed
        
    elif key == GLUT_KEY_DOWN:
        y -= cam_speed
    elif key == GLUT_KEY_LEFT:
        if fixed_cam:
            vcam[3] -= cam_speed
        else: 
            x -= cam_speed
    elif key == GLUT_KEY_RIGHT:
        if fixed_cam:
            vcam[5] -= cam_speed
        else:
            x += cam_speed
    
    camera_pos = [x, y, z]



## CAMERA, IDLE, SCREEN


def setupCamera():
    global camera_pos, cam_mode, position, pl_rotation, vcam
    x,y,z = camera_pos
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.5, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if cam_mode == 0:
        nx = z * math.sin(math.radians(x))
        ny = y
        nz = z * math.cos(math.radians(x))
        gluLookAt(nx, ny, nz, 0, 0, 0, 0, 1, 0)
    else:
        if not fixed_cam:
            eye_height = 150 
            look_distance = 150
            center_x = position[0] + math.sin(math.radians(pl_rotation)) * look_distance
            center_z = position[2] + math.cos(math.radians(pl_rotation)) * look_distance
            
            vcam = [position[0], position[1] + eye_height, position[2],
                    center_x, position[1] + eye_height, center_z,
                    0, 1, 0]
            
            gluLookAt(
                position[0], position[1] + eye_height, position[2],  # Eye position
                center_x, position[1] + eye_height, center_z,        # Center point
                0, 1, 0)
        else:
            a,b,c,d,e,f,g,h,i = vcam
            gluLookAt(a,b,c,d,e,f,g,h,i)


def idle():
    global cheat_mode, game_over
    if cheat_mode and not game_over:
        cheat()

    for bullet in bullets:
        bullet.update()
    glutPostRedisplay()


def showScreen():
    global game_over, cam_mode, score, missed_bullets, lives

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()

    

    draw_grid()
    update_game_state()

    # Draw game elements
    if lives <= 0 or missed_bullets >= 10:
        game_over = True
        cam_mode = 0
        gameover()
        draw_text(10, 770, f"GAME OVER! You're score is {score}")
        draw_text(10, 740, "Press 'R' to RESTART the game")
    
    else:
        draw_player()
        draw_bullets()
        draw_enemies()
        check_collisions()
        enemycount()
        draw_text(10, 770, f"Player Life Remaining: {lives}")
        draw_text(10, 740, f"Score: {score}")
        draw_text(10, 710, f"Missed: {missed_bullets}/10")


    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Shooting Game")
    glEnable(GL_DEPTH_TEST)
    print(f"Remaining Player Life: {lives}")
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glutMainLoop()


if __name__ == "__main__":
    main()
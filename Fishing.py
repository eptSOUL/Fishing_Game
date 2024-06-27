import pygame
import sys
from PIL import Image, ImageFilter
import keyboard
import random
import time

'''-----------------------------------Variables-----------------------------------'''
pygame.init()

display_width = 700
display_height = 900

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Fishing")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

click = pygame.mixer.Sound('sounds/click.mp3')
loss_sound = pygame.mixer.Sound('sounds/loss.mp3')
hit_sound = pygame.mixer.Sound('sounds/hit.mp3')
background = pygame.image.load('img_background/background.jpg') # menu_background
background2 = pygame.image.load('img_background/background1.jpg') # game_background
background3 = pygame.image.load('img_background/info.jpg') #info_background

#-------------------------------------- Things in game
fish1 = pygame.image.load('img_fish_trash/fish1.png')
fish2 = pygame.image.load('img_fish_trash/fish2.png')
fish3 = pygame.image.load('img_fish_trash/fish3.png')
fish4 = pygame.image.load('img_fish_trash/fish4.png')
fish5 = pygame.image.load('img_fish_trash/fish5.png')
star = pygame.image.load('img_background/star.png')
garbage1 = pygame.image.load('img_fish_trash/boots.png')
garbage2 = pygame.image.load('img_fish_trash/socks.png')
garbage3 = pygame.image.load('img_fish_trash/bottle.png')

fishhook = pygame.image.load('img_background/fishhook_act.png')
fishhook_rope = pygame.image.load('img_background/fishhook_rope.png')
rock = pygame.image.load('img_fish_trash/rock.png')
health_img = pygame.image.load('img_background/heart.png')
health_img = pygame.transform.scale(health_img,(50,70))
#-------------------------------------- Things in game

garbage_img = [garbage1, garbage2, garbage3]
garbage_options = [78, 84, 70, 104, 94, 92]
fish_img = [fish1, fish2, fish3, fish4, fish5]
fish_options = [93, 76, 100, 70, 123, 99, 117, 90, 109, 70]
star_img = [star]
star_options = [93, 76]


clock = pygame.time.Clock()
INVULN_TIME = 0.3

fishhook_width_rp = 62
fishhook_height_rp = 986
fishhook_x_rp = 300
fishhook_y_rp = -800
fishhook_width = 61
fishhook_height = 129
fishhook_x = 350
fishhook_y = 450

'''-----------------------------------Variables-----------------------------------'''

def print_text1(size):
    return pygame.font.Font('font/font.ttf', size)   

class Button():
    def __init__(self, image, pos, text1, font, color1, color2):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color1, self.color2 = color1, color2
        self.text1 = text1
        self.text = self.font.render(self.text1, True, self.color1)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def updt(self, display):
        if self.image is not None:
            display.blit(self.image, self.rect)
        display.blit(self.text, self.text_rect)
    def control(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text1, True, self.color2)
        else:
            self.text = self.font.render(self.text1, True, self.color1)

class Garbage():
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False
    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))
        
class Fish():
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False
    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

class Star():
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False
    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

def game():
    global score, health
    invulnerable_Mode=False
    invulnerable_Start_Time = 0
    health = 3
    score = 0
    garbage_arr = []
    create_garbage_arr(garbage_arr)
    fish_arr = []
    create_fish_arr(fish_arr)
    star_arr = []
    create_star_arr(star_arr)
    while True:        
        display.blit(background2, (0, 0))
        draw_fishhook()
        
        draw_array_g(garbage_arr)
        
        draw_array_f(fish_arr)

        draw_array_s(star_arr)
       
        points = str(score)
        
        esc_text1 = print_text1(20).render('ESC - PAUSE', True, (255,255,255))
        score_text1 = print_text1(20).render('SCORE: ' + points, True, (255,255,255))
        esc_rect = esc_text1.get_rect(center=(100,100))
        score_rect = score_text1.get_rect(center=(600,45)) 
        display.blit(esc_text1, esc_rect)
        display.blit(score_text1, score_rect)
        pos = pygame.mouse.get_pos()
        pause_text1 = print_text1(50).render('ESC - PAUSE', True, (255,255,255))
        
        pause_rect = pause_text1.get_rect(center=(20,40))
        health_mode()
        if invulnerable_Mode and time.time()-invulnerable_Start_Time>INVULN_TIME:
            invulnerable_Mode=False
        
        if check_collision(garbage_arr) and not invulnerable_Mode:
            health -= 1
            check_health()
            invulnerable_Mode=True
            invulnerable_Start_Time=time.time()
        if check_collision_fish(fish_arr) and not invulnerable_Mode:
            score+=1
            invulnerable_Mode=True
            invulnerable_Start_Time=time.time()
        if check_collision_star(star_arr) and not invulnerable_Mode:
            score*=2
            invulnerable_Mode=True
            invulnerable_Start_Time=time.time()
            
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keyboard.is_pressed("esc"):
            pygame.mixer.Sound.play(click)
            pause()

        elif health == 0:
            game_over()
        
        pygame.display.update()
        clock.tick(80)

def create_garbage_arr(array):
    choice = random.randrange(0, 3)
    y=random.randint(200, 750)
    choice_img = random.randrange(0, 3)
    img = garbage_img[choice_img]
    width = garbage_options[choice*2]
    height = garbage_options[choice*2+1]
    array.append(Garbage(display_width + 900, y, width, height, img, random.randrange(1, 4)))

    y=random.randint(200, 750)
    choice = random.randrange(0, 3)
    choice_img = random.randrange(0, 3)
    img = garbage_img[choice_img]
    width = garbage_options[choice*2]
    height = garbage_options[choice*2+1]
    array.append(Garbage(display_width + 1400, y, width, height, img, random.randrange(1, 4)))

    y=random.randint(200, 750)
    choice = random.randrange(0, 3)
    choice_img = random.randrange(0, 3)
    img = garbage_img[choice_img]
    width = garbage_options[choice*2]
    height = garbage_options[choice*2+1]
    array.append(Garbage(display_width + 2000, y, width, height, img, random.randrange(1, 4)))


def create_fish_arr(array):
    y=random.randint(200, 750)
    choice = random.randrange(0, 5)
    choice_img = random.randrange(0, 5)
    img = fish_img[choice_img]
    width = fish_options[choice*2]
    height = fish_options[choice*2+1]
    array.append(Fish(display_width + 900, y, width, height, img, random.randrange(1, 4)))
    

    y=random.randint(200, 750)
    choice = random.randrange(0, 5)
    choice_img = random.randrange(0, 5)
    img = fish_img[choice_img]
    width = fish_options[choice*2]
    height = fish_options[choice*2+1]
    array.append(Fish(display_width + 1400, y, width, height, img, random.randrange(1, 4)))

    y=random.randint(200, 750)
    choice = random.randrange(0, 5)
    choice_img = random.randrange(0, 5)
    img = fish_img[choice_img]
    width = fish_options[choice*2]
    height = fish_options[choice*2+1]
    array.append(Fish(display_width + 2000, y, width, height, img, random.randrange(1, 4)))

def create_star_arr(array):
    y = random.randint(200, 750)
    img = star_img[0]
    width = star_options[0]
    height = star_options[1]
    array.append(Star(display_width + 20000, y, width, height, img, 10))

def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum<900:
            radius += 900
    else:
        radius = 900
    choice = random.randrange(800, 2000)
    if choice == 900:
        radius += random.randrange(900, 2000)
    else:
        radius += random.randrange(900, 1000)

    return radius

def draw_array_g(array):
    for garbage in array:
        check = garbage.move()
        if not check:
            radius = find_radius(array)
            choice = random.randrange(0, 3)
            img = garbage_img[choice]
            width = garbage_options[choice*2]
            height = random.randrange(300, 800)
            garbage.return_self(radius, height, width, img)
            
def draw_array_f(array):
    for fish in array:
        check = fish.move()
        if not check:
            radius = find_radius(array)
            choice = random.randrange(0, 5)
            img = fish_img[choice]
            width = fish_options[choice*2]
            height = random.randrange(300, 800)
            fish.return_self(radius, height, width, img)

def draw_array_s(array):
    for star in array:
        check = star.move()
        if not check:
            radius = 20000
            img = star_img[0]
            width = star_options[0]
            height = random.randrange(300, 800)
            star.return_self(radius, height, width, img)

def draw_fishhook():
    global fishhook_x, fishhook_y, fishhook_y_rp, fishhook_x_rp
    display.blit(fishhook_rope, (fishhook_x_rp, fishhook_y_rp))
    display.blit(fishhook, (fishhook_x, fishhook_y))
    if pygame.mouse.get_pressed()[0]:
        fishhook_x =  pygame.mouse.get_pos()[0] - 30
        fishhook_y = pygame.mouse.get_pos()[1] - 120

        fishhook_x_rp =  pygame.mouse.get_pos()[0] - 32
        fishhook_y_rp = pygame.mouse.get_pos()[1] - 965


def info_mode():
    while True:
        display.blit(background3,(0,0))
        pos = pygame.mouse.get_pos()
        info_text1 = print_text1(30).render('GAME DESCRIPTION', True, (255,255,255))
        info_rect = info_text1.get_rect(center=(350,50))
        display.blit(info_text1, info_rect)
        infop_text1 = print_text1(20).render('__________________________________________________________________', True, (255,255,255))
        infop_rect = info_text1.get_rect(center=(100,100))
        display.blit(infop_text1, infop_rect)
        info1_text1 = print_text1(20).render('THE GOAL OF THE GAME IS TO CATCH FISH WHILE NOT ', True, (255,255,255))
        info1_rect = info_text1.get_rect(center=(180,200))
        display.blit(info1_text1, info1_rect)
        info2_text1 = print_text1(20).render('TOUCH THE DEBRIS IN THE WATER, OTHERWISE YOUR LIVES', True, (255,255,255))
        info2_rect = info_text1.get_rect(center=(180,250))
        display.blit(info2_text1, info2_rect)
        info3_text1 = print_text1(20).render('DECREASE AND THEN THE GAME MAY END ALTOGETHER.', True, (255,255,255))
        info3_rect = info_text1.get_rect(center=(180,300))
        display.blit(info3_text1, info3_rect)
        info7_text1 = print_text1(20).render('BE ATTENTIVE! STAR MULTIPLES SCORE X2.', True, (255,255,255))
        info7_rect = info_text1.get_rect(center=(180,350))
        display.blit(info7_text1, info7_rect)
        info4_text1 = print_text1(20).render('DURING THE GAME, YOU CAN PRESS THE "ESC" BUTTON,', True, (255,255,255))
        info4_rect = info_text1.get_rect(center=(180,400))
        display.blit(info4_text1, info4_rect)
        info5_text1 = print_text1(20).render('WHICH IN THE EVENT THE GAME GOES INTO PAUSE', True, (255,255,255))
        info5_rect = info_text1.get_rect(center=(180,450))
        display.blit(info5_text1, info5_rect)
        info6_text1 = print_text1(20).render('AND DURING THE PAUSE BECOMES OUT OF THE GAME', True, (255,255,255))
        info6_rect = info_text1.get_rect(center=(180,500))
        display.blit(info6_text1, info6_rect)
        info8_text1 = print_text1(20).render('ALSO EXIT BY PRESSING THE" Q " BUTTON.', True, (255,255,255))
        info8_rect = info_text1.get_rect(center=(180,550))
        display.blit(info8_text1, info8_rect)
        back = Button(image=pygame.image.load('img_background/button.png'), pos=(343,670),text1='BACK', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
        
        for button in [back]:
            button.color(pos)
            button.updt(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.control(pos):
                    pygame.mixer.Sound.play(click)
                    menu()
        pygame.display.update()        
def menu():
    while True:
        display.blit(background, (0, 0))
        pos = pygame.mouse.get_pos()
        menu_text1 = print_text1(50).render('WELCOME TO FISHING', True, (0,0,110))
        menu_rect = menu_text1.get_rect(center=(350,170))   
        display.blit(menu_text1, menu_rect)
        play = Button(image=pygame.image.load('img_background/button.png'), pos=(350,380),text1='START', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
        info = Button(image=pygame.image.load('img_background/button.png'), pos=(350,540),text1='INFO', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
        quit = Button(image=pygame.image.load('img_background/button.png'), pos=(350,700),text1='QUIT', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
          
        for button in [play,info,quit]:
            button.color(pos)
            button.updt(display)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.control(pos):
                    pygame.mixer.Sound.play(click)
                    game()
                if info.control(pos):
                    pygame.mixer.Sound.play(click)
                    info_mode()
                if quit.control(pos):
                    pygame.mixer.Sound.play(click)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_over():
    screensaver()
    pause_back = pygame.image.load('img_pause/paused.jpg')
    display.blit(pause_back, (0, 0))
    while True:
        display.blit(pause_back, (0, 0))
        pos = pygame.mouse.get_pos()
        over_text1 = print_text1(50).render('GAME OVER', True, (255,255,255))
        over_rect = over_text1.get_rect(center=(350,220))   
        display.blit(over_text1, over_rect)

        try_again = Button(image=pygame.image.load('img_background/button.png'), pos=(350,380),text1='TRY AGAIN', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
        quit_menu = Button(image=pygame.image.load('img_background/button.png'), pos=(350,540),text1='MENU', font=print_text1(60), color1=(0, 0, 180), color2=(255, 255, 255))
        
        for button in [try_again,quit_menu]:
            button.color(pos)
            button.updt(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again.control(pos):
                    pygame.mixer.Sound.play(click)
                    game()
                if quit_menu.control(pos):
                    pygame.mixer.Sound.play(click)
                    menu()
        pygame.display.update()  

def health_mode():
    global health
    show = 0
    x = 20
    while show != health:
        display.blit(health_img,(x,5))
        x += 50
        show += 1

def check_health():
    global health
    if health == 0:
        pygame.mixer.Sound.play(loss_sound)
        game_over()
    else:
        return True
        pygame.mixer.Sound.play(hit_sound)

def check_collision(barriers):
    global fishhook_y, fishhook_x, fishhook_height, fishhook_width
    for barrier in barriers:
        if barrier.y <= fishhook_y+fishhook_height <= barrier.y+barrier.height:
            if barrier.x<=fishhook_x<=barrier.x+barrier.width:
                radius = find_radius(barriers)
                choice = random.randrange(0, 3)
                img = garbage_img[choice]
                width = garbage_options[choice*2]
                height = random.randrange(200, 750)
                barrier.return_self(radius, height, width, img)
                return True

            
    return False

def check_collision_fish(barriers):
    global fishhook_y, fishhook_x, fishhook_height, fishhook_width
    for barrier in barriers:
        if barrier.y <= fishhook_y + fishhook_height <= barrier.y + barrier.height:
            if barrier.x <= fishhook_x <= barrier.x + barrier.width:
                radius = find_radius(barriers)
                choice = random.randrange(0, 5)
                img = fish_img[choice]
                width = fish_options[choice*2]
                height = random.randrange(200, 750)
                barrier.return_self(radius, height, width, img)
                return True

            
    return False

def check_collision_star(barriers):
    global fishhook_y, fishhook_x, fishhook_height, fishhook_width
    for barrier in barriers:
        if barrier.y <= fishhook_y + fishhook_height <= barrier.y + barrier.height:
            if barrier.x <= fishhook_x <= barrier.x + barrier.width:
                radius = 20000
                img = star_img[0]
                width = star_options[0]
                height = random.randrange(200, 750)
                barrier.return_self(radius, height, width, img)
                return True

            
    return False

def screensaver():
    rect = pygame.Rect(0, 0, 700, 900)
    sub = display.subsurface(rect)
    pygame.image.save(sub, "img_pause/screenshot.jpg")
    
    im = Image.open('img_pause/screenshot.jpg')
    blur_image = im.filter(ImageFilter.GaussianBlur(radius=7))
    blur_image.save('img_pause/blured_bg.png')
    im = Image.open('img_pause/blured_bg.png')
    im.save("img_pause/paused.jpg")
def pause():
    screensaver()
    pause_back = pygame.image.load('img_pause/paused.jpg')
    display.blit(pause_back, (0, 0))
    
    paused = True
    while paused:
        paused_text1 = print_text1(50).render('PAUSED', True, (255,255,255))
        paused_rect = paused_text1.get_rect(center=(350,220))   
        display.blit(paused_text1, paused_rect)
        resume_text1 = print_text1(40).render('PRESS ENTER TO RESUME', True, (255,255,255))
        resume_rect = resume_text1.get_rect(center=(350,430))   
        display.blit(resume_text1, resume_rect)
        quit_text1 = print_text1(40).render('PRESS Q TO QUIT', True, (255,255,255))
        quit_rect = quit_text1.get_rect(center=(350,540)) 
        display.blit(quit_text1, quit_rect)
        

        if keyboard.is_pressed("enter"):
            pygame.mixer.Sound.play(click)
            paused = False
        if keyboard.is_pressed("q"):
            pygame.mixer.Sound.play(click)
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        
menu()
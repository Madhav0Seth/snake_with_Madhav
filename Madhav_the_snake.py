import pygame 
import random
import os

pygame.init()
pygame.mixer.init()

#defining font
font = pygame.font.SysFont(None,50)

#defining colours
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
blue=(0,0,255)
yellow=(240,150,150)
darkgreen=(20,100,10)
lightpurple=(180,180,225)
grey=(200,200,200)

screen_height=600
screen_width=800

#creating the base/window
window=pygame.display.set_mode((screen_width,screen_height))

#background image
start=pygame.image.load("start.jpg")
start=pygame.transform.scale(start,(screen_width,screen_height)).convert_alpha()
pink=pygame.image.load("pink.jpg")
pink=pygame.transform.scale(pink,(screen_width,screen_height)).convert_alpha()
black_header=pygame.image.load("black_header.jpg")
black_header=pygame.transform.scale(black_header,(screen_width,100)).convert_alpha()
red_pause=pygame.image.load("red_pause.jpg")
red_pause=pygame.transform.scale(red_pause,(screen_width,screen_height)).convert_alpha()
red_over=pygame.image.load("red_over.jpg")
red_over=pygame.transform.scale(red_over,(screen_width,screen_height)).convert_alpha()

#title of my game
pygame.display.set_caption("MADHAV THE SNAKE")

#defining plotting tail function
def  plot_snake(window,color,snake_list,size_x):
    for x,y in snake_list:
        pygame.draw.rect(window,color,[x,y,size_x,size_x])

#displaying the score
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x,y])

#creating Our clock
clock=pygame.time.Clock()

#creating welcome screen
def welcome():
    exit=False
    while exit==False:
        window.fill(black)
        window.blit(start,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

def gameloop():
    #game variables
    snake_x=50
    snake_y=150
    size_x=20

    exit=False
    pause=False
    over=False
    fps=60
    velocity_initial=7
    velocity_x=0
    velocity_y=0
    score=0

    #creating incrementing tail
    snake_list=[]
    snake_length=1
    #creating food for snake
    food_x=random.randint(200,700)
    food_y=random.randint(200,400)
    #cheching if highscore.txt exists
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w")as f:
            f.write("0")
    #opening highscore file
    with open("highscore.txt","r") as f:
        highscore=f.read()

    #creating the game loop
    while exit==False:
        #gameover logic
        if over==True:
            with open("highscore.txt","w")as p:
                p.write(str(highscore))
            window.fill(grey)
            window.blit(red_over,(0,0))
            text_screen(str(score),red,140,31)
            text_screen(str(highscore),red,180,75)
            for event in pygame.event.get():

                #for exiting the game by corner button
                if event.type==pygame.QUIT:
                    exit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
                        
        else:
            #defining the controls    
            for event in pygame.event.get():

                #for exiting the game by corner button
                if event.type==pygame.QUIT:
                    exit=True
                #defining controls and movent due to them
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=velocity_initial
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-velocity_initial
                        velocity_y=0
                    if event.key==pygame.K_UP:
                        velocity_y=-velocity_initial
                        velocity_x=0
                    if event.key==pygame.K_DOWN:
                        velocity_y=velocity_initial
                        velocity_x=0
                    if event.key==pygame.K_ESCAPE:
                        if pause==True:
                            pygame.mixer.music.load("pause.mp3")
                            pygame.mixer.music.play()
                            pause=False
                        elif pause==False:
                            pygame.mixer.music.load("pause.mp3")
                            pygame.mixer.music.play()
                            pause=True 

            if pause==False:
                #creating comeback of snake           
                if snake_x>screen_width:
                    snake_x=0
                if snake_y>screen_height:
                    snake_y=100  
                if snake_x<0:
                    snake_x=screen_width
                if snake_y<100:
                    snake_y=screen_height 

                    
                #eating the food
                if abs(snake_x-food_x)<20 and abs(snake_y-food_y)<20:
                    pygame.mixer.music.load("eat.mp3")
                    pygame.mixer.music.play()
                    score=score+10
                    food_x=random.randint(150,750)
                    food_y=random.randint(150,450)
                    snake_length+=5
                    if score>int(highscore):
                        highscore=score    
                    
                #moving our snake            
                snake_x=snake_x+velocity_x
                snake_y=snake_y+velocity_y

                #colouring the window
                window.fill(yellow)
                window.blit(pink,(0,100))
                window.blit(black_header,(0,0))
            
                #tail concept
                head=[]
                head.append (snake_x)
                head.append(snake_y)
                snake_list.append(head)
                plot_snake(window,darkgreen,snake_list,size_x)

                if len(snake_list)>snake_length:
                    del snake_list[0]

                #collision logic(puch katne se game over)
                if head in snake_list[:-1]:
                    over=True
                    pygame.mixer.music.load("pew.mp3")
                    pygame.mixer.music.play()    

                #drawing our food 
                pygame.draw.rect(window,red,[food_x,food_y,20,20])
                #displaying the scores
                text_screen(str(score),lightpurple,130,23)
                text_screen(str(highscore),lightpurple,165,60)

            elif pause==True:
                window.fill(lightpurple) 
                window.blit(red_pause,(0,0))  
                text_screen(str(score),red,140,25)   
                text_screen(str(highscore),red,180,67)   
        pygame.display.update()
        #defining our fps
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()    
gameloop()    
# Keeping a high score list in Pygame

import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

GRAY = (127,127,127)
BLACK = (0,0,0)

HIGH_SCORE_CAPACITY = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("High Scores")

class Label(pygame.sprite.Sprite):
    def __init__(self, msg, center, fontFile, textSize, textColor):
        pygame.sprite.Sprite.__init__(self)
        self.font     = pygame.font.Font(fontFile, textSize)
        self.text     = msg
        self.centerx   = center[0]
        self.centery   = center[1]
        self.txtColor = textColor

    def update(self):
        self.image       = self.font.render(self.text, 1, self.txtColor)
        self.rect        = self.image.get_rect()  # get a new rect after any text change
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


def game(): 
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GRAY)

    screen.blit(background, (0,0))

    score = 0

    title = Label(f"{score}",(screen.get_width()//2, 150), None, 200, BLACK)
    title2 = Label(f"Click to increase score",(screen.get_width()//2, 250), None, 100, BLACK)
    title3 = Label("Click 'X' in the top right to see the high score list",(screen.get_width()//2, 450), None, 50, BLACK)
    labelGroup = pygame.sprite.Group(title, title2, title3)
    
    running = True
    clock = pygame.time.Clock()
    
    while(running):
        
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                score += 10
                background.fill(GRAY)
                title.text = f"{score}"

        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(background)

        pygame.display.flip()

    return score


def read_and_write_toHighScoreFile(scoreFromGame):
    try:
        create = open("scoreList.txt", "x")
        create.close()
        print("Creating file scoreList.txt")
    except FileExistsError:
        print("File exists, moving on...")
    ########################################################################################################################################################
    #
    #
    #   1. THIS FUNCTION READS A TEXT FILE CALLED "scoreList.txt" IT THEN PLACES THE LINES IT READS INTO A PYTHON LIST AND CLOSES THE FILE
    #       IT THEN CHANGES THE DATA TYPE OF ALL ITEMS IN THE LIST TO BE INTEGERS AND NOT STRINGS
    #    
    #   2. if the file is empty, it appends the score that was received from "scoreFromGame" onto the "scores" list
    #
    #   3. Otherwise, it checks to see if the score that was given is less than the lowest recorded score...
    #   if this is true, it checks if the score capacity is reached, 5, and if it is, exit the loop and it does not update any new scores
    #   otherwise if the score capacity is not reached, it places that lowest score at the end of the list
    #
    #
    #   4. Else if the new score is greater than any old score, that score is replaced with the new one and the "new score" is replaced
    #       with the old one. As the loop runs again, it will swap out the scores and the lowest score will be lost.
    # 
    #   5. After the first for loop, another for loop is ran in order to prevent appending the same score twice.
    #  
    #   6. Opens the same file for writing, in a for loop, writes each item in the "scores" list to the .txt file
    #       with a "\n" newline character at the end of it and finally, closes the file.
    #  
    #   7. Lastly, this function returns two things, the "scores" list and a string value stating whether or not 
    #       the added score is a new score or if the score is a duplicate.
    #
    #
    ########################################################################################################################################################

    newOrOld = "old" # boolean for number 7
    found = False
    ############################################## 1.
    scores = []

    toRead = open("scoreList.txt","r")
    scores = toRead.readlines()
    toRead.close()
    if(len(scores) != 0):
        for i in range(len(scores)):
            scores[i] = int(scores[i])
    ############################################## 1.

    ############################################## 2.
    newScore = scoreFromGame
    print(f"Before: {scores}")
    if(len(scores) == 0):
        scores.append(newScore)
        newOrOld = "new"
    ############################################## 2.

    ############################################## 3.
    else:
        for i in range(len(scores)):
            if(newScore <= scores[-1]):
                if(len(scores) == HIGH_SCORE_CAPACITY):
                    break
                else:
                    scores.append(newScore)
                    newOrOld = "new"
                    break
    ############################################## 3.

    ############################################## 4.
            elif(newScore > scores[i]):
                temp = scores[i]
                scores[i] = newScore
                newScore = temp
                newOrOld = "new"
    ############################################## 4.

    ############################################## 5.
        for i in range(len(scores)):
            if(newScore == scores[i]):
                found = True

        if(found != True):
            if(len(scores) != HIGH_SCORE_CAPACITY):
                scores.append(newScore)
    ############################################## 5.

    ############################################## 6.
    print(f"After: {scores}")
    toWrite = open("scoreList.txt","w")
    for i in scores:
        toWrite.write(str(f"{i}\n"))
    toWrite.close()
    ############################################## 6.

    ############################################## 7.
    return scores, newOrOld
    ############################################## 7.
    

def highScore(highScores):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GRAY)

    screen.blit(background, (0,0))
    print(highScores[1])

    title = Label("High Scores",(screen.get_width()//2, 100), None, 175, BLACK)

    if(highScores[1] == "new"):
        title.text = "New High Score!"
        title.font = pygame.font.Font(None, 125)
    else:
        title.text = "High Scores"

    scores = highScores[0]
    scoreLabels = []

    down = 0
    order = 1

    for i in range(len(scores)):
        scoreLabel = Label(f"{order}.  {scores[i]}",(screen.get_width()//2 - 60, 200 + down), None, 100, BLACK)
        scoreLabels.append(scoreLabel)
        down = down + 75
        order = order + 1

    labelGroup = pygame.sprite.Group(scoreLabels, title)
    
    running = True
    clock = pygame.time.Clock()
    
    while(running):
        
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(background)

        pygame.display.flip()


def playAgain(): 
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(GRAY)

    screen.blit(background, (0,0))

    title = Label(f"Play Again? (y/n)",(screen.get_width()//2, 150), None, 100, BLACK)
    labelGroup = pygame.sprite.Group(title)
    
    running = True
    again = False
    clock = pygame.time.Clock()
    
    while(running):
        
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    running = False
                    again = True
                elif event.key == pygame.K_n:
                    running = False
                    again = False

        labelGroup.clear(screen, background)
        labelGroup.update()
        labelGroup.draw(background)

        pygame.display.flip()

    return again


def main():
    replay = True
    while replay:
        newScore = game()
        scores = read_and_write_toHighScoreFile(newScore)
        highScore(scores)
        replay = playAgain()

main()
pygame.quit()
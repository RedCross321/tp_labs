import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((900, 900))
screen.fill([192,192,192])


class Dots:
    def __init__(self):
        self.masB = []
        self.masR = []
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
    def create(self):         
        for i in range(1,7):
                for j in range(1, 6):
                    if(i == 6 or i == 1):
                        self.masB.append([j, i, 0, 0, 0, 0, 1])
                    else:
                        self.masB.append([j, i, 0, 0, 0, 0, 0])
                    pygame.draw.circle(screen, self.blue, (j * 150, i * 150 - 75), 25, 0)
        pygame.draw.rect(screen, self.blue, (150, 150 - 87, 600, 26))
        pygame.draw.rect(screen, self.blue, (150, 900 - 87, 600, 26))
        for i in range(1,6):
                for j in range(1, 7):
                    self.masR.append([j, i, 0])
                    pygame.draw.circle(screen, self.red, (j *150 - 75, i * 150), 25, 0)
        pygame.draw.rect(screen, self.red, (75 - 13, 150 - 12, 26, 600))
        pygame.draw.rect(screen, self.red, (825 - 13, 150 - 12, 26, 600))

# pygame.draw.rect(screen, self.red, (75 - 12, 150 - 12, 750, 26)) 
class Bridge:
    def __init__(self):  
        pass
    def build_G(self, ind, color):
        print(ind)
        if ind[0][6] == 1 and ind[2][6] == 1:
            print("Пошел нахуй")
            pygame.quit()
            sys.exit()
        elif ind[2][1] == ind[0][1]:
            if ind[2][0] - ind[0][0] == 1:
                pygame.draw.rect(screen, color, (ind[0][0] * 150, ind[2][1] * 150 - 87, 150, 26))
                start.masB[ind[1]][2] = 1
                start.masB[ind[3]][6] = 2
            elif ind[0][0] - ind[2][0] == 1:
                pygame.draw.rect(screen, color, (ind[2][0] * 150, ind[0][1] * 150 - 87, 150, 26))
                start.masB[ind[1]][3] = 1
                start.masB[ind[3]][6] = 2
        elif ind[2][0] == ind[0][0]:
            if ind[2][1] - ind[0][1] == 1:
                pygame.draw.rect(screen, color, (ind[0][0] * 150 - 12, ind[2][1] * 150 - 225, 26, 150))
                start.masB[ind[1]][4] = 1
                start.masB[ind[3]][6] = 2
            elif ind[0][1] - ind[2][1] == 1:
                pygame.draw.rect(screen, color, (ind[2][0] * 150 - 12, ind[0][1] * 150 - 225, 26, 150))
                start.masB[ind[1]][5] = 1
                start.masB[ind[3]][6] = 2
        # if ind[0][6] == 2 and ind[2][6] == 1:
        #     print("Пошел нахуй")
        # for j in range(0, 5):
        #     play.check_win(j) == 1


class Move:
    def __init__(self):
        self.ind = 0
        self.buffer = []
    def search(self):
        self.ind =  0
        for i in range(1,7):
            for j in range(1, 6):
                if j * 150 - 25 <= event.pos[0] <= j * 150 + 25 and i * 150 - 100 <= event.pos[1] <= i * 150 - 50:
                    self.buffer.append(start.masB[self.ind])
                    self.buffer.append(self.ind)    
                self.ind +=1
        if len(self.buffer) == 4:
            b.build_G(self.buffer, (0, 0, 255))
            self.buffer = []
    # def check_win(self, ind):
    #     if(start.masB[ind][6] == 0):
    #         if(start.masB[ind][2] == 1):
    #             self.check_win(ind+1)
    #         elif(start.masB[ind][3] == 1):
    #             self.check_win(ind-1)
    #         elif(start.masB[ind][4] == 1):
    #             self.check_win(ind+5)
    #         elif(start.masB[ind][5] == 1):
    #             self.check_win(ind-5)
    #     if(start.masB[ind][6] == 1):
    #         print("Пошел нахуй")
    
b = Bridge()
start = Dots()
play = Move()
start.create()


# print(play.masR)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play.search()
    pygame.display.flip()
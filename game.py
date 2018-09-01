import pygame
import os
import random
pygame.init()

pygame.key.set_repeat()
screenWidth = 1000
screenHeight = 1000
tileWidth = 40
tileHeight = 40
win = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("First Game")


class Player(pygame.sprite.Sprite):
    playerWidth = 40
    playerHeight = 40
    img = pygame.image.load(os.path.relpath("Plane1.png"))
    startPosX = (screenWidth * 0.5) - (tileWidth * 0.5)
    startPosY = screenHeight - tileHeight
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(self.startPosX, self.startPosY, self.playerWidth, self.playerHeight)
        self.speed = 3

    def draw(self):
        #print("Drawing Player at " + str(self.x) + ", " + str(self.y))
        #pygame.draw.rect(win, (255,0,0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        win.blit(self.img, (self.rect.x, self.rect.y))

    def moveLeft(self):
        if (self.rect.x - self.speed) >= 0:
            self.rect.x -= self.speed
        
    def moveRight(self):
        if (self.rect.x + self.speed) <= (screenWidth - self.playerWidth):
            self.rect.x += self.speed
        
    def moveForward(self):
        if self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed
        
    def moveBack(self):
        if (self.rect.y + self.speed) <= (screenHeight - self.playerHeight):
            self.rect.y += self.speed



class TerrainTile(pygame.sprite.Sprite):

    def __init__(self, x, y, color, width, isLand):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, width)
        self.color = color
        self.width = width
        self.isLand = isLand

    def draw(self):
        pygame.draw.rect(win, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.width))

    def setY(self, y):
        self.rect.y = y

    def getY(self):
        return self.rect.y




class TerrainManager:
    tileMatrix = []
    scrollSpeed = 1
    terrainTileWidth = screenWidth // tileWidth

    def __init__(self):
        for i in range(0,self.terrainTileWidth + 1):
            self.tileMatrix.append([])
            
        self.generateIntialTerrain()

    def generateIntialTerrain(self):
        x = 0
        y = screenHeight - tileHeight
        row = 0

        for i in range(self.terrainTileWidth**2 + self.terrainTileWidth):
            if x < (3 * tileWidth) or x > (screenWidth - (4 * tileWidth)):
                self.tileMatrix[row].append(TerrainTile(x, y, (0,random.randint(200,255),0), tileWidth, True))
            else:
                self.tileMatrix[row].append(TerrainTile(x, y, (0,0,random.randint(200,255)), tileWidth, False))

            
            x += tileWidth
            if x == screenWidth:
                row += 1
                x = 0
                y -= tileHeight

    def draw(self):
        for i in range(0,len(self.tileMatrix)):
            for j in range(0,len(self.tileMatrix[i])):
                self.tileMatrix[i][j].draw()


    def scroll(self):
        for i in range(0,len(self.tileMatrix)):
            for j in range(0,len(self.tileMatrix[i])):
                self.tileMatrix[i][j].setY(self.tileMatrix[i][j].getY() + self.scrollSpeed)


        if self.tileMatrix[0][0].getY() == screenHeight:
            self.tileMatrix.pop(0)

        if self.tileMatrix[0][0].getY() == (screenHeight - tileHeight):
            self.generateRow()
            

    def generateRow(self):
        tempList = []
        
        for i in range(0, screenWidth // tileWidth):
            if random.randint(1,100) < 98:
                tempList.append(TerrainTile(i*tileWidth, -tileHeight, (0,0,200), tileWidth, False))
            else:
                tempList.append(TerrainTile(i*tileWidth, -tileHeight, (0,200,0), tileWidth, True))
            
        self.tileMatrix.append(tempList)


    #puts all tile in the terrain matrix into a list
    def getTileList(self):
        tempList = []
        for i in range(0,len(self.tileMatrix)):
            for j in range(0,len(self.tileMatrix[i])):
                tempList.append(self.tileMatrix[i][j])

        return tempList

    def checkForLandCollisions(self, player):
        tileList = self.getTileList()
        collisionDetected = False
        for tile in tileList:
            if tile.isLand and tile.rect.colliderect(player.rect):
                collisionDetected = True
                tile.color = (255, 0 , 0)
                break
            
        return collisionDetected

        
            
            

#for debugging
def DrawGrid():
    x = 0
    y = 0
    evenRow = True
    for i in range((screenWidth // tileWidth) * (screenHeight // tileHeight)):
        
        if evenRow:
            if (i % 2) == 0: #if i is even - print a red square
                pygame.draw.rect(win, (0,0,0), (x,y,tileWidth,tileHeight))
            else:
                pygame.draw.rect(win, (0,0,255), (x,y,tileWidth,tileHeight))
                
        x += tileWidth
        if x == screenWidth:
            x = 0
            y += tileHeight


#for testing
def DrawSimpleTerrain():
    x = 0
    y = 0

    for i in range((screenWidth // tileWidth) * (screenHeight // tileHeight)):

        if x < (3 * tileWidth) or x > (screenWidth - (4 * tileWidth)): 
            pygame.draw.rect(win, (0,random.randint(200,255),0), (x,y,tileWidth,tileHeight))
        else:
            pygame.draw.rect(win, (0,0,random.randint(200,255)), (x,y,tileWidth,tileHeight))
                
        x += tileWidth
        if x == screenWidth:
            x = 0
            y += tileHeight
    


def DrawScreen():
    win.fill((0,0,0))
    terrain.draw()
    player.draw()
    pygame.display.update()




######################
######################
## MAIN GAME LOOP
#player = Player((screenWidth * 0.5) - (tileWidth * 0.5) , screenHeight - tileHeight)
player = Player()
terrain = TerrainManager()
player.draw()
collisionCount = 0
run = True
while run:
    ##pygame.time.delay(1) #delays the game loop

    #listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.moveLeft()
    if keys[pygame.K_RIGHT]:
        player.moveRight()
    if keys[pygame.K_UP]:
        player.moveForward()
    if keys[pygame.K_DOWN]:
        player.moveBack()


    terrain.scroll()
    if terrain.checkForLandCollisions(player):
        collisionCount += 1
        print("Collision Detected " + str(collisionCount))

    DrawScreen()


pygame.quit()

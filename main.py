from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
import kivy.metrics, random

bgWidth = kivy.metrics.dp(768)
bgHeight = kivy.metrics.dp(256)
waterRef = 1
terrainSize = kivy.metrics.dp(64)
bigCloudWidth = kivy.metrics.dp(448)
bigCloudHeight = kivy.metrics.dp(101)
bigCloudX = bigCloudWidth/2
bigCloud2X = -bigCloudWidth/2
smallCloudWidth = kivy.metrics.dp(148)
smallCloudHeight = kivy.metrics.dp(48)
smallCloudX = kivy.metrics.dp(250)
smallCloud2X = kivy.metrics.dp(10)
smallCloud3X = kivy.metrics.dp(360)
treeIndex = 1
treeWidth = kivy.metrics.dp(102)
treeHeight = kivy.metrics.dp(106)
decorationSize = kivy.metrics.dp(64)
bigPlatWidth = kivy.metrics.dp(222)
bigPlatHeight = kivy.metrics.dp(76)
platformX = terrainSize
platformY = terrainSize*2.2
platformYList = []
platform = False
platformXRandom = [random.randint(int(terrainSize-bigPlatWidth/2.6), int(terrainSize+bigPlatWidth/2.3)), random.randint(int(terrainSize-bigPlatWidth/2.6), int(terrainSize+bigPlatWidth/2.3)), random.randint(int(terrainSize-bigPlatWidth/2.6), int(terrainSize+bigPlatWidth/2.3)), terrainSize]

playerWidth = kivy.metrics.dp(128)
playerHeight = kivy.metrics.dp(80)
playerX = (Window.width/2)-(playerHeight/1.2)
groundY = (terrainSize/3.8)+playerHeight/1.7
playerY = groundY
playerRun = 1
moveRight = True
playerSpeed = kivy.metrics.mm(1.1)
jump = 0
jumpMax = kivy.metrics.mm(3.2) #kivy.metrics.cm(0.32) #kivy.metrics.dp(12)
jumpDecay = kivy.metrics.cm(0.015) #kivy.metrics.mm(0.16) #kivy.metrics.dp(0.6)
jumped = False
jumpIndex = 1
wall = False

class CaptainNosyGame(Widget):
    def update(self, dt):
        global playerX, playerY, playerRun, waterRef, bigCloudX, bigCloud2X, moveRight, jump, jumped, jumpIndex, treeIndex, groundY, platform, wall, smallCloudX, smallCloud2X, smallCloud3X, platformY, platformXRandom, platformX
        self.canvas.clear()

        # Background
        with self.canvas:
            self.sky = Rectangle(pos=(Window.width-bgWidth, Window.height-bgHeight*1.6), size=(bgWidth, bgHeight*2), source="Sprites/Background/Sky.png")
            self.water = Rectangle(pos=(Window.width-bgWidth, 0), size=(bgWidth, bgHeight), source="Sprites/Background/Water.png")
            self.bg = Rectangle(pos=(Window.width-bgWidth, Window.height/2.15-bgHeight), size=(bgWidth, bgHeight), source="Sprites/Background/BG.png")
            self.bg.texture.mag_filter = 'nearest'
            self.waterRef = Rectangle(pos=(Window.width-(kivy.metrics.dp(340)*1.02), Window.height/1.8-bgHeight*1.04), size=(kivy.metrics.dp(340), kivy.metrics.dp(20)), source="Sprites/Background/WaterRef"+str(int(waterRef))+".png")
            self.waterRef.texture.mag_filter = 'nearest'
            self.bigCloud = Rectangle(pos=(bigCloudX, terrainSize*2.68), size=(bigCloudWidth, bigCloudHeight), source="Sprites/Background/BigClouds.png")
            self.bigCloud.texture.mag_filter = 'nearest'
            self.bigCloud2 = Rectangle(pos=(bigCloud2X, terrainSize*2.68), size=(bigCloudWidth, bigCloudHeight), source="Sprites/Background/BigClouds.png")
            self.bigCloud2.texture.mag_filter = 'nearest'

            self.smallCloud = Rectangle(pos=(smallCloudX, terrainSize*5.5), size=(smallCloudWidth, smallCloudHeight), source="Sprites/Background/SmallCloud1.png")
            self.smallCloud.texture.mag_filter = 'nearest'
            self.smallCloud2 = Rectangle(pos=(smallCloud2X, terrainSize*7.5), size=(kivy.metrics.dp(199.5), kivy.metrics.dp(52.5)), source="Sprites/Background/SmallCloud2.png")
            self.smallCloud2.texture.mag_filter = 'nearest'
            self.smallCloud3 = Rectangle(pos=(smallCloud3X, terrainSize*9.5), size=(kivy.metrics.dp(140), kivy.metrics.dp(39)), source="Sprites/Background/SmallCloud3.png")
            self.smallCloud3.texture.mag_filter = 'nearest'

            treeIndex += 1/10
            if (treeIndex > 4):
                treeIndex = 1
            self.bgTree = Rectangle(pos=(terrainSize/4, terrainSize*3), size=(treeWidth, treeHeight), source="Sprites/Background/BackPalmTreeLeft"+str(int(treeIndex))+".png")
            self.bgTree.texture.mag_filter = 'nearest'
            self.bgTree2 = Rectangle(pos=(terrainSize*3.5, terrainSize*1.25), size=(terrainSize*2, terrainSize*2), source="Sprites/Background/BackPalmTreeRegular"+str(int(treeIndex))+".png")
            self.bgTree2.texture.mag_filter = 'nearest'

            self.barrel = Rectangle(pos=(terrainSize/4, terrainSize*1.25), size=(decorationSize, decorationSize), source="Sprites/Background/01.png")
            self.barrel.texture.mag_filter = 'nearest'
            self.bottle = Rectangle(pos=(terrainSize/1.3, terrainSize*1.25), size=(decorationSize, decorationSize), source="Sprites/Background/03.png")
            self.bottle.texture.mag_filter = 'nearest'
            self.bottle2 = Rectangle(pos=(terrainSize*1.1, terrainSize*1.25), size=(decorationSize, decorationSize), source="Sprites/Background/06.png")
            self.bottle2.texture.mag_filter = 'nearest'
            self.barrel2 = Rectangle(pos=(terrainSize*4.5, terrainSize*1.25), size=(decorationSize, decorationSize), source="Sprites/Background/02.png")
            self.barrel2.texture.mag_filter = 'nearest'

            self.platform = Rectangle(pos=(platformXRandom[3], terrainSize*2.2), size=(bigPlatWidth, bigPlatHeight), source="Sprites/Platforms/Platform1.png")
            self.platform.texture.mag_filter = 'nearest'
            platformYList.append(terrainSize*2.2)
            for i in range(3):
                self.platform = Rectangle(pos=(platformXRandom[i], terrainSize*(4.16+(i*1.95))), size=(bigPlatWidth, bigPlatHeight), source="Sprites/Platforms/Platform1.png")
                self.platform.texture.mag_filter = 'nearest'
                platformYList.append(terrainSize*(4.16+(i*1.95)))
            self.platform = Rectangle(pos=(platformXRandom[3], terrainSize*10), size=(bigPlatWidth, bigPlatHeight), source="Sprites/Platforms/Platform1.png")
            self.platform.texture.mag_filter = 'nearest'
            platformYList.append(terrainSize*10)
            
            for i in range(12):
                self.rock = Rectangle(pos=(-terrainSize/1.5, (terrainSize*i)+kivy.metrics.sp(17)), size=(terrainSize, terrainSize), source="Sprites/Terrain/terrain7.png")
                self.rock.texture.mag_filter = 'nearest'
            for i in range(12):
                self.rock2 = Rectangle(pos=(Window.width-terrainSize/3.2, (terrainSize*i)+kivy.metrics.sp(17)), size=(terrainSize, terrainSize), source="Sprites/Terrain/terrain5.png")
                self.rock2.texture.mag_filter = 'nearest'
            self.dirt = Rectangle(pos=(0, 0), size=(terrainSize*6, terrainSize), source="Sprites/Terrain/terrain6.png")
            for i in range(6):
                self.grass = Rectangle(pos=(terrainSize*i, terrainSize/3.8), size=(terrainSize, terrainSize), source="Sprites/Terrain/terrain3.png")
                self.grass.texture.mag_filter = 'nearest'

        if (waterRef > 4):
            waterRef = 1
        else:
            waterRef += 1/10

        bigCloudX -= kivy.metrics.dp(0.5)
        bigCloud2X -= kivy.metrics.dp(0.5)
        smallCloudX -= kivy.metrics.dp(0.35)
        smallCloud2X -= kivy.metrics.dp(0.35)
        smallCloud3X -= kivy.metrics.dp(0.35)

        if (bigCloudX < kivy.metrics.dp(-500)):
            bigCloudX = bigCloudWidth/1.15
        if (bigCloud2X < kivy.metrics.dp(-500)):
            bigCloud2X = bigCloudWidth/1.15
        if (smallCloudX < kivy.metrics.dp(-130)):
            smallCloudX = kivy.metrics.dp(360)
        if (smallCloud2X < kivy.metrics.dp(-199)):
            smallCloud2X = kivy.metrics.dp(360)
        if (smallCloud3X < kivy.metrics.dp(-140)):
            smallCloud3X = kivy.metrics.dp(360)

        # Player
        if (moveRight and not jumped):
            with self.canvas:
                self.player = Rectangle(pos=(playerX, playerY), size=(playerWidth, playerHeight), source="Sprites/Captain/Run"+str(int(playerRun))+".png")
                self.player.texture.mag_filter = 'nearest'
            playerRun += kivy.metrics.dp(1/8)
            if (playerRun > 6):
                playerRun = 1
        elif (not jumped):
            with self.canvas:
                self.player = Rectangle(pos=(playerX, playerY), size=(playerWidth, playerHeight), source="Sprites/Captain/RunLeft"+str(int(playerRun))+".png")
                self.player.texture.mag_filter = 'nearest'
            playerRun += kivy.metrics.dp(1/8)
            if (playerRun > 6):
                playerRun = 1
        elif (moveRight):
            with self.canvas:
                self.player = Rectangle(pos=(playerX, playerY), size=(playerWidth, playerHeight), source="Sprites/Captain/Jump"+str(int(jumpIndex))+".png")
                self.player.texture.mag_filter = 'nearest'
            if (jump > 0):
                jumpIndex = 1
            else:
                jumpIndex = 2
        else:
            with self.canvas:
                self.player = Rectangle(pos=(playerX, playerY), size=(playerWidth, playerHeight), source="Sprites/Captain/JumpLeft"+str(int(jumpIndex))+".png")
                self.player.texture.mag_filter = 'nearest'
            if (jump > 0):
                jumpIndex = 1
            else:
                jumpIndex = 2
        
        if (jumped):
            playerY += jump
            jump -= jumpDecay
            if (playerY < groundY):
                platform = False
                jumped = False
                jump = 0
                jumpIndex = 1
                playerY = groundY
        
        for i in platformYList:
            if (i - playerY < kivy.metrics.dp(1)):
                platformY = i
                if (platformYList.index(i) == 4):
                    platformX = platformXRandom[3]
                elif (platformYList.index(i) == 3):
                    platformX = platformXRandom[3]
                elif (platformYList.index(i) == 0):
                    platformX = platformXRandom[0]
                elif (platformYList.index(i) == 6):
                    platformX = platformXRandom[1]
                elif (platformYList.index(i) == 2):
                    platformX = platformXRandom[2]
        
        if (playerY >= platformY+playerHeight/3.2 and playerX > platformX-playerWidth/2.6 and playerX < platformX+bigPlatWidth/1.6):
            groundY = platformY+playerHeight/3
            platform = True
        else:
            if (platform):
                jumped = True
            groundY = (terrainSize/3.8)+playerHeight/1.7
        
        if (moveRight):
            if (playerX < (Window.width-terrainSize/3.2)-playerWidth/1.65):
                playerX += playerSpeed
            else:
                if (playerY == groundY):
                    moveRight = not moveRight
                    wall = False
                else:
                    wall = True
        else:
            if (playerX > (-terrainSize/1.5)+playerWidth/10):
                playerX -= playerSpeed
            else:
                if (playerY == groundY):
                    moveRight = not moveRight
                    wall = False
                else:
                    wall = True

        self.player.pos = (playerX, playerY)

        # Pop Array Elements
        for i in platformYList:
            platformYList.remove(i)
    
    def on_touch_down(self, touch):
        global jump, jumped, moveRight, wall
        if (jump == 0):
            jumped = True
            jump = jumpMax
        elif (wall):
            moveRight = not moveRight
            jumped = True
            jump = jumpMax
            wall = False

class CaptainNosyApp(App):
    def build(self):
        game = CaptainNosyGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

CaptainNosyApp().run()
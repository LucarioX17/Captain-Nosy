from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
import kivy.metrics

bgWidth = kivy.metrics.sp(768)
bgHeight = kivy.metrics.sp(256)
waterRef = 1
terrainSize = kivy.metrics.sp(64)
bigCloudWidth = kivy.metrics.sp(448)
bigCloudHeight = kivy.metrics.sp(101)
bigCloudX = bigCloudWidth/2
bigCloud2X = -bigCloudWidth/2

playerWidth = kivy.metrics.sp(128)
playerHeight = kivy.metrics.sp(80)
playerX = (Window.width/2)-(playerHeight/1.2)
playerY = Window.height/10
playerIdle = 1

class CaptainNosyGame(Widget):
    def update(self, dt):
        global playerX, playerY, playerIdle, waterRef, bigCloudX, bigCloud2X
        self.canvas.clear()

        # Background
        with self.canvas:
            self.sky = Rectangle(pos=(Window.width-bgWidth, Window.height-bgHeight*1.4), size=(bgWidth, bgHeight*1.6), source="Sprites/Background/Sky.png")
            self.water = Rectangle(pos=(Window.width-bgWidth, 0), size=(bgWidth, bgHeight), source="Sprites/Background/Water.png")
            self.bg = Rectangle(pos=(Window.width-bgWidth, Window.height/2.15-bgHeight), size=(bgWidth, bgHeight), source="Sprites/Background/BG.png")
            self.bg.texture.mag_filter = 'nearest'
            self.waterRef = Rectangle(pos=(Window.width-(kivy.metrics.sp(340)*1.02), Window.height/1.8-bgHeight), size=(kivy.metrics.sp(340), kivy.metrics.sp(20)), source="Sprites/Background/WaterRef"+str(int(waterRef))+".png")
            self.waterRef.texture.mag_filter = 'nearest'
            self.bigCloud = Rectangle(pos=(bigCloudX, bigCloudHeight*1.25), size=(bigCloudWidth, bigCloudHeight), source="Sprites/Background/BigClouds.png")
            self.bigCloud2 = Rectangle(pos=(bigCloud2X, bigCloudHeight*1.25), size=(bigCloudWidth, bigCloudHeight), source="Sprites/Background/BigClouds.png")
            
            for i in range(10):
                self.rock = Rectangle(pos=(-terrainSize/1.5, (terrainSize*i)+kivy.metrics.sp(17)), size=(terrainSize, terrainSize), source="Sprites/Terrain/terrain7.png")
                self.rock.texture.mag_filter = 'nearest'
            for i in range(10):
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

        bigCloudX -= 0.5
        bigCloud2X -= 0.5

        if (bigCloudX < kivy.metrics.sp(-500)):
            bigCloudX = bigCloudWidth/1.15
        if (bigCloud2X < kivy.metrics.sp(-500)):
            bigCloud2X = bigCloudWidth/1.15

        # Player
        if (playerIdle > 0):
            with self.canvas:
                self.player = Rectangle(pos=(playerX, playerY), size=(playerWidth, playerHeight), source="Sprites/Captain/Idle"+str(int(playerIdle))+".png")
                self.player.texture.mag_filter = 'nearest'
            playerIdle += 1/10
            if (playerIdle > 5):
                playerIdle = 1

class CaptainNosyApp(App):
    def build(self):
        game = CaptainNosyGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    CaptainNosyApp().run()
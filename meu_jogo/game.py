#biibliotecas necessárias para rodar o programa
import pgzrun
from pgzero.actor import Actor
from pgzero import music
from pgzero.keyboard import keys
import random
from pygame.rect import Rect

#botões/imagens/objetos principais do jogo e suas coordenadas
startButton = Actor("start_button", (400, 300))
musicButton = Actor("music_button", (400, 400))
exitButton = Actor("exit_button", (400, 500))
explosionButton = Actor("explosion_button", (320,400))
jumpButton = Actor("jump_button", (480,400))
blocks = [Actor("barrel", (50,400)), Actor("block", (200, 400)), Actor("box", (300, 400)), Actor("spring", (400,400))]
blocksSpeend = 1

#estados do jogo
gameStart = False
gameOver = False

musicPlaying = True
musicJump = True
musicExplosion = True

#classe do herói
class Hero:
    def __init__(self, heroLifePoint):
        #imagens do heroi
        self.spritesHero = {
            "idle": ["hero_idle1", "hero_idle2", "hero_idle3", "hero_idle4"],
            "walk": ["hero_run1", "hero_run2", "hero_run3", "hero_run4"],
            "jump": ["hero_jump1", "hero_jump2", "hero_jump3"]
        }

        self.heroIndex = 0
        #a imagem começa quando ele está parado (idle)
        self.heroState = "idle"
        self.actorHero = Actor(self.spritesHero[self.heroState][self.heroIndex], (300, 400))
        self.heroSpeed = 3
        self.heroSpeedY = 0
        self.heroGround = True  
        self.heroLifePoint = heroLifePoint

    #função para desenhar a barra de vida do herói
    def drawLifeBar(self):
        barWidth = 200  
        barHeigth = 22  
        healthPorcentage = self.heroLifePoint / 100
        currentWidth = int(barWidth * healthPorcentage)  

        screen.draw.rect(Rect((20, 20), (barWidth, barHeigth)), "red")

        screen.draw.filled_rect(Rect((20, 20), (currentWidth, barHeigth)), "green")

    #função para movimentação do herói
    def updateHero(self):
        global musicJump

        if keyboard.left:
            self.actorHero.x -= self.heroSpeed
            self.heroState = "walk"
        elif keyboard.right:
            self.actorHero.x +=self.heroSpeed
            self.heroState = "walk"
        else:
            self.heroState = "idle"

        #condição para o pulo
        if keyboard.up and self.heroGround:  
            self.heroSpeedY = -13
            self.heroState = "jump"
            self.heroGround = False  
            if musicJump:
                sounds.jump.play()

        #gravidade o eixo y
        self.heroSpeedY += 0.4  
        self.actorHero.y += self.heroSpeedY  

        #limite para o herói cair no chão
        if self.actorHero.y >= 400:
            self.actorHero.y = 400  
            self.heroGround = True  
            self.heroSpeedY = 0  

        #animação do herói
        self.heroIndex = (self.heroIndex + 1) % len(self.spritesHero[self.heroState])
        self.actorHero.image = self.spritesHero[self.heroState][self.heroIndex]
    
    def draw(self):
        self.actorHero.draw() 
        self.drawLifeBar()

#classe dos inimigos
class Enemy:
    def __init__(self, x, y):
        #imagens do inimigo
        self.enemySprites = {
            "walk": ["enemy_walk1", "enemy_walk2", "enemy_walk3", "enemy_walk4"],
            "attack": ["enemy_attack1", "enemy_attack2", "enemy_attack3"]
        }

        self.indexEnemies = 0
        #inicia no "walk"
        self.statesEnemies = "walk"
        self.actorEnemies = Actor(self.enemySprites[self.statesEnemies][self.indexEnemies], (x,y))
        self.speedEnemies = 1

    def updateEnemies(self):
        self.actorEnemies.x += self.speedEnemies

        if self.actorEnemies.x > 800:
            self.actorEnemies.x = random.randint(-100,-50)  
        
        self.indexEnemies = (self.indexEnemies + 1) % len(self.enemySprites[self.statesEnemies])
        self.actorEnemies.image = self.enemySprites[self.statesEnemies][self.indexEnemies]
    
    def draw(self):
        self.actorEnemies.draw()

hero = Hero(heroLifePoint = 100)
enemies = [Enemy(random.randint(0,100), 400) for _ in range(3)]

#funçao para verificar colisão
def collision(hero, enemy):
    return hero.colliderect(enemy)

#função para movimentação dos blocos
def updateBlocks():
    global blocksSpeend

    for block in blocks:
        block.x += blocksSpeend
        if block.x > 750 or block.x < 50:
            blocksSpeend *= -1

#funçaõ para a lógica do jogo e pontuação
def update():
    global gameOver, gameStar, musicExplosion

    if gameStart and not gameOver:
        hero.updateHero()
        for enemy in enemies:
            enemy.updateEnemies()
            if collision(hero.actorHero, enemy.actorEnemies):
                hero.heroLifePoint -= 1
                if musicExplosion:
                    sounds.explosion.play()
                if hero.heroLifePoint <= 0:
                    gameOver = True

        updateBlocks()

#função para desenhar na tela
def draw():
    screen.clear()

    if not gameStart:
        screen.blit("background_image.png", (0, 0))  
        screen.draw.text("Menu do Jogo", center=(400, 100), fontsize=60, color="white")
        startButton.draw()
        musicButton.draw()
        exitButton.draw()
        jumpButton.draw()
        explosionButton.draw()

    elif gameOver: 
        screen.draw.text("GAME OVER!", center=(400, 300), fontsize=80, color="red")
    
    else:
        screen.blit("background_image.png", (0, 0))  
        for block in blocks:
            block.draw()

        hero.draw()
        for enemy in enemies:
            enemy.draw()

#função para cliques de mouse nos botões
def on_mouse_down(pos):
    global gameStart, musicPlaying, gameOver, hero, musicJump, musicExplosion

    if startButton.collidepoint(pos):
        gameStart = True
        gameOver = False
    if musicButton.collidepoint(pos):
        if musicPlaying:
            music.stop() 
            musicPlaying = False
        else:
            try:
                music.play("background_music.mp3") 
                musicPlaying = True  
            except Exception as e:
                print('Erro ao tentar tocar a música: ', e)

    if jumpButton.collidepoint(pos):
       musicJump = not musicJump
    if explosionButton.collidepoint(pos):
        musicExplosion = not musicExplosion

    if exitButton.collidepoint(pos):
        print("Saindo do jogo...")
        exit()
    
if musicPlaying:
    try:
        music.play("background_music.mp3")
    except Exception as e:
        print('Erro ao tocar música', e)

pgzrun.go()
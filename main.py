import pygame


#  Game Classes
class PlayerPaddle:
    def __init__(self, player):
        self.player = player
        self.color = WHITE if self.player == 1 else RED
        self.width = 10
        self.height = 150
        self.posX = 50 if self.player == 1 else SCREENWIDTH - 50 - self.width
        self.posY = SCREENHEIGHT // 2 - (self.height // 2)
        self.imageRect = pygame.rect.Rect(self.posX, self.posY, self.width, self.height)
        self.velY = 0
        self.score = 0


    def move(self):
        """Moving the paddle up and down the screen"""
        self.imageRect[1] = self.posY + self.velY


    def direction(self, action):
        """increasing or decreasing the Y position of the player paddle"""
        if action == 'UP' and self.imageRect[1] > 0:
            self.velY += -5
        elif action == 'DOWN' and self.imageRect[1] + self.height <= SCREENHEIGHT:
            self.velY += 5


    def draw(self, window):
        """Draw the oplayer paddle to the screen"""
        pygame.draw.rect(window, self.color, self.imageRect)
        self.move()


class Ball:
    def __init__(self):
        self.posX = 65
        self.posY = SCREENHEIGHT//2 - 15
        self.ballRect = pygame.rect.Rect(self.posX, self.posY, 30, 30)
        self.directionX = 5
        self.directionY = 0


    def move(self):
        """Moving the ball around the game screen"""
        if self.ballRect.midtop[1] <= 0 or self.ballRect.midbottom[1] >= SCREENHEIGHT:
            self.directionY = self.directionY * -1

        if self.posX < SCREENWIDTH//2:
            self.ballRect[0] += self.directionX

        self.ballRect[1] += self.directionY

        if self.ballRect[0] + 30 <= 0:
            updatePlayerScore(player2)
        elif self.ballRect[0] >= SCREENWIDTH:
            updatePlayerScore(player1)


    def paddleAngle(self, player):
        """Checking the ball collision with the paddle, and setting angles once off the paddle"""
        if self.ballRect.bottom >= player.imageRect.top and self.ballRect.bottom <= player.imageRect.top + 10:
            self.directionY = -5
        if self.ballRect.bottom >= player.imageRect.top + 10 and self.ballRect.bottom <= player.imageRect.top + 20:
            self.directionY = -4
        if self.ballRect.bottom >= player.imageRect.top + 20 and self.ballRect.bottom <= player.imageRect.top + 30:
            self.directionY = -3
        if self.ballRect.bottom >= player.imageRect.top + 30 and self.ballRect.bottom <= player.imageRect.top + 40:
            self.directionY = -2
        if self.ballRect.bottom >= player.imageRect.top + 40 and self.ballRect.bottom <= player.imageRect.top + 50:
            self.directionY = -1

        if self.ballRect.top <= player.imageRect.bottom and self.ballRect.bottom >= player.imageRect.bottom - 10:
            self.directionY = 5
        if self.ballRect.top <= player.imageRect.bottom - 10 and self.ballRect.bottom >= player.imageRect.bottom - 20:
            self.directionY = 4
        if self.ballRect.top <= player.imageRect.bottom - 20 and self.ballRect.bottom >= player.imageRect.bottom - 30:
            self.directionY = 3
        if self.ballRect.top <= player.imageRect.bottom - 30 and self.ballRect.bottom >= player.imageRect.bottom - 40:
            self.directionY = 2
        if self.ballRect.top <= player.imageRect.bottom -40 and self.ballRect.bottom >= player.imageRect.bottom - 50:
            self.directionY = 1

        if self.ballRect.center[1] >= player.imageRect.center[1] - 10 and self.ballRect.center[1] <= player.imageRect.center[1] + 10:
            self.directionY = 0


    def draw(self, window):
        """Draws the ball to the screen, then calls the ball move method"""
        pygame.draw.circle(window, (0, 0, 255), (self.ballRect[0] + 15, self.ballRect[1] + 15), 20)
        pygame.draw.rect(window, WHITE, self.ballRect, 1)
        self.move()



#  Utility game functions
def drawGameNet(window):
    """Draw the net for the pong Board"""
    pygame.draw.line(window, WHITE, (SCREENWIDTH//2, 0), (SCREENWIDTH//2, SCREENHEIGHT))


def updatePlayerScore(player):
    """Increases the player score and resets the game for a new round"""
    player.score += 1
    resetRound(player)


def textToScreen(msg):
    """Utility function to draw the tesxt to the screen"""
    font = pygame.font.SysFont('Comic sans', 22)
    message = font.render(msg, 1, WHITE)
    return message


def resetRound(player):
    """Resets the paddles and the ball and start the game anew"""
    player1.velY = 0
    player2.velY = 0
    ball.ballRect[0] = 65 if player.player == 1 else SCREENWIDTH -50 -player.width - 40
    ball.ballRect[1] = SCREENHEIGHT//2 - 15
    ball.directionY = 0
    ball.directionX = 5 if player.player == 1 else - 5
    pygame.time.wait(3000)


def updateGameScreen(window):
    """Updates the game display screen"""
    window.fill((0, 0, 0))

    drawGameNet(window)
    player1.draw(window)
    player2.draw(window)
    ball.draw(window)

    player1Score = textToScreen(f'Player 1 Score: {player1.score}')
    window.blit(player1Score, (20, 30))
    player2Score = textToScreen(f'Player 2 Score: {player2.score}')
    window.blit(player2Score, (SCREENWIDTH - 20 - player2Score.get_width(), 30))

    pygame.display.update()


#  initialise pygame module
pygame.init()

#  Game variables and settings
SCREENWIDTH = 1080
SCREENHEIGHT = 720
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CLOCK = pygame.time.Clock()


#  initialise the pygame window
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('PONG')

#  initialise our game classes
player1 = PlayerPaddle(1)
player2 = PlayerPaddle(2)
ball = Ball()


#  Running the main game loop
RUN = True
while RUN:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    keyPresses = pygame.key.get_pressed()
    if keyPresses[pygame.K_w]:
        player1.direction('UP')
    if keyPresses[pygame.K_s]:
        player1.direction('DOWN')
    if keyPresses[pygame.K_UP]:
        player2.direction('UP')
    if keyPresses[pygame.K_DOWN]:
        player2.direction('DOWN')

    if ball.ballRect.left == player1.imageRect.right and ball.ballRect.bottom >= player1.imageRect.top \
            and ball.ballRect.top <= player1.imageRect.bottom:
        ball.paddleAngle(player1)
        ball.directionX = ball.directionX * -1


    if ball.ballRect.right == player2.imageRect.left and ball.ballRect.bottom >= player2.imageRect.top \
            and ball.ballRect.top <= player2.imageRect.bottom:
        ball.paddleAngle(player2)
        ball.directionX = ball.directionX * -1


    updateGameScreen(GAMESCREEN)
    CLOCK.tick(60)



pygame.quit()
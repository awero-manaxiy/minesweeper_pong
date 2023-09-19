import pygame
import random
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Cobol', 30)
witdh, height = 500, 500


class Platform:

    def __init__(self, surface, coordinates=(10, 10), velocity=2,
                 inputs=(pygame.K_UP, pygame.K_DOWN)):
        self.surface = surface
        self.x, self.y = coordinates
        self.vel = velocity
        self.r = None
        self.inputs = inputs


class PlayerPlatform(Platform):

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[self.inputs[0]] and self.y > 0:
            self.y -= self.vel
        if keys[self.inputs[1]] and self.y < height - 100:
            self.y += self.vel

        self.r = pygame.draw.rect(self.surface, (255, 255, 255), (self.x, self.y, 10, 100))


class EnemyPlatform(Platform):

    def __init__(self, surface, coordinates=(10, 10), velocity=2,
                 inputs=(pygame.K_UP, pygame.K_DOWN)):
        super().__init__(surface, coordinates, velocity, inputs)
        self.desired_pos = random.randint(0, witdh)

    def move(self):

        if self.desired_pos < self.y and self.y > 0:
            self.y -= self.vel
        if self.desired_pos > self.y and self.y < height - 100:
            self.y += self.vel

        self.r = pygame.draw.rect(self.surface, (255, 255, 255), (self.x, self.y, 10, 100))

    def predict_pos(self, y, x_inc, y_inc):
        tg = x_inc/y_inc
        if tg <= 0:
            if y * abs(tg) > witdh:
                self.desired_pos = y - witdh / abs(tg) - 50
            else:
                self.desired_pos = witdh / abs(tg) - y - 50
        else:
            if y * abs(tg) > witdh:
                self.desired_pos = witdh - ((witdh - y) - witdh / abs(tg)) - 50
            else:
                self.desired_pos = witdh - (witdh / abs(tg) - (witdh - y)) - 50


class Ball:

    def __init__(self, surface, speed=1):
        self.surface = surface
        self.x, self.y = witdh/2, height/2
        self.vel = speed
        self.x_inc = speed
        self.y_inc = 0
        self.r = None

    def move(self):

        self.x += self.x_inc

        if self.y <= 0 or self.y >= height:
            self.y_inc = -self.y_inc
        self.y += self.y_inc

        self.r = pygame.draw.circle(self.surface, (255, 255, 255), (self.x, self.y),  5)

    def update_vec(self, vec):
        self.y_inc = vec * self.x_inc
        self.x_inc = -1.1 * self.x_inc

    def return_to_center(self):
        self.x, self.y = witdh / 2, height / 2
        self.y_inc = 0
        self.x_inc = - self.vel


win = pygame.display.set_mode((witdh, height))
pygame.display.set_caption("Pong")
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)


def menu():

    text = my_font.render('PLAY', True, color)
    u_text = my_font.render('PING PONG', True, color)

    while True:

        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if witdh / 2 - 70 <= mouse[0] <= witdh / 2 + 70 and height / 2 - 20 <= mouse[1] <= height / 2 + 20:
                    run_game()

        win.fill((0, 0, 0))

        if witdh / 2 - 70 <= mouse[0] <= witdh / 2 + 70 and height / 2 - 20 <= mouse[1] <= height / 2 + 20:
            pygame.draw.rect(win, color_light, [witdh / 2 - 70, height / 2 - 20, 140, 40])

        else:
            pygame.draw.rect(win, color_dark, [witdh / 2 - 70, height / 2 - 20, 140, 40])

        win.blit(text, (witdh / 2 - 25, height / 2 - 7))
        win.blit(u_text, (witdh / 2 - 50, height / 2 - 100))

        pygame.display.update()


def run_game():
    points = [0, 0]
    left_points = my_font.render(str(points[0]), False, (255, 255, 255))
    right_points = my_font.render(str(points[1]), False, (255, 255, 255))

    ball = Ball(win)
    left_platform = PlayerPlatform(win, (10, 10))
    right_platform = EnemyPlatform(win, (witdh - 20, 10), 2, inputs=(pygame.K_RIGHT, pygame.K_LEFT))
    run = True

    while run:

        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((0, 0, 0))
        win.blit(left_points, (witdh/2 - 30, 10))
        win.blit(right_points, (witdh/2 + 15, 10))
        pygame.draw.line(win, (255, 255, 255), (witdh/2, 0), (witdh/2, height))
        left_platform.move()
        right_platform.move()
        ball.move()

        if pygame.Rect.colliderect(left_platform.r, ball.r) and ball.x >= 10:
            ball.update_vec(((left_platform.y + 50) - ball.y) / 50)
            right_platform.predict_pos(ball.y, ball.x_inc, ball.y_inc)

        if pygame.Rect.colliderect(right_platform.r, ball.r) and ball.x <= witdh - 10:
            ball.update_vec((ball.y - (right_platform.y + 50)) / 50)

        if ball.x <= 0:
            ball.return_to_center()
            points[1] = points[1] + 1
            if points[1] > 5:
                win_state(points)
            right_points = my_font.render(str(points[1]), False, (255, 255, 255))
            pygame.time.delay(100)

        if ball.x >= witdh:
            ball.return_to_center()
            points[0] = points[0] + 1
            if points[0] > 5:
                win_state(points)
            left_points = my_font.render(str(points[0]), False, (255, 255, 255))
            pygame.time.delay(100)

        pygame.display.update()

    pygame.quit()


def win_state(score):

    if score[0] > score[1]:
        w_text = my_font.render('ТЫ ВЫИГРАЛ!!!', True, color)
    else:
        w_text = my_font.render('Ты проиграл(((', True, color)
    replay_text = my_font.render('PLAY', True, color)
    while True:

        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if witdh / 2 - 70 <= mouse[0] <= witdh / 2 + 70 and height / 2 - 20 <= mouse[1] <= height / 2 + 20:
                    run_game()

        win.fill((0, 0, 0))

        if witdh / 2 - 70 <= mouse[0] <= witdh / 2 + 70 and height / 2 - 20 <= mouse[1] <= height / 2 + 20:
            pygame.draw.rect(win, color_light, [witdh / 2 - 70, height / 2 - 20, 140, 40])

        else:
            pygame.draw.rect(win, color_dark, [witdh / 2 - 70, height / 2 - 20, 140, 40])
        win.blit(w_text, (witdh / 2 - 100, height / 2 - 100))
        win.blit(replay_text, (witdh / 2 - 25, height / 2 - 7))

        pygame.display.update()


if __name__ == '__main__':
    menu()

import pygame
import neat
import os

from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

WIN_HEIGHT = 800
WIN_WIDTH = 500
DRAW_LINES = True
GEN = 0

pygame.display.set_caption("Flappy Bird")

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load('imgs\\bird1.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird2.png')),
             pygame.transform.scale2x(pygame.image.load('imgs\\bird3.png'))]
BASE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\base.png'))
BG_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\bg1.png'))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs\\pipe.png'))

STAT_FONT = pygame.font.SysFont('comicsans', 50)


def draw_window(win, birds, pipes, base, score, GEN, pipe_ind):
    global DRAW_LINES
    win.blit(BG_IMG, (0, 0))  # drawing the background
    for pipe in pipes:  # drawing the pipe or pipes as there can be more than one pipes also in one window
        pipe.draw(win)
    base.draw(win)  # drawing the base

    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255, 0, 0),
                                 (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                 (pipes[pipe_ind].x + pipes[pipe_ind].TOP_PIPE.get_width() / 2, pipes[pipe_ind].height),
                                 5)
                pygame.draw.line(win, (255, 0, 0),
                                 (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                     pipes[pipe_ind].x + pipes[pipe_ind].BOTTOM_PIPE.get_width() / 2,
                                     pipes[pipe_ind].bottom), 5)
            except:
                pass

        bird.draw(win)

    text = STAT_FONT.render('Score : ' + str(score), True, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render('Gen : ' + str(GEN), True, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render('Alive : ' + str(len(birds)), True, (255, 255, 255))
    win.blit(text, (10, 50))

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    birds = []
    ge = []
    neural_networks = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        neural_networks.append(net)
        birds.append(Bird(230, 350, BIRD_IMGS))
        g.fitness = 0
        ge.append(g)

    pipes = [Pipe(500, PIPE_IMG)]
    base_object = Base(630, BASE_IMG)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].TOP_PIPE.get_width():
                pipe_ind = 1
        else:
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = neural_networks[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird) or (bird.y + bird.img.get_height() >= 630 or bird.y < 0):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    ge.pop(x)
                    neural_networks.pop(x)

                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    for g in ge:
                        g.fitness += 5
                    score += 1
                    pipes.append(Pipe(500, PIPE_IMG))

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                pipes.remove(pipe)

            pipe.move()

        base_object.move()
        draw_window(win, birds, pipes, base_object, score, GEN, pipe_ind)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    best = population.run(main, 50)

    print('\nBest genome:\n{!s}'.format(best))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

import random
import pygame


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x, pipe_img: pygame.Surface):
        self.x = x
        self.height = 0  # for random purpose
        self.top = 0  # y coordinates of top pipe
        self.bottom = 0  # y coordinates of bottom pipe
        self.TOP_PIPE = pygame.transform.flip(pipe_img, False, True)
        self.BOTTOM_PIPE = pipe_img
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.bottom = self.height + self.GAP
        self.top = self.height - self.TOP_PIPE.get_height()

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.TOP_PIPE, (self.x, self.top))
        win.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.TOP_PIPE)
        bottom_pipe_mask = pygame.mask.from_surface(self.BOTTOM_PIPE)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_overlap = bird_mask.overlap(top_pipe_mask, top_offset)
        bottom_overlap = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

        if top_overlap or bottom_overlap:
            return True
        return False
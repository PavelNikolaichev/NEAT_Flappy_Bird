import pygame


class Base:
    VEL = 5

    def __init__(self, y, bg_image: pygame.Surface):  # base will be shown moving by taking two images of the same base and putting it one after other
        self.IMG = bg_image
        self.WIDTH = bg_image.get_width()

        self.y = y
        self.x1 = 0  # here x1 and x2 are the 2 images where x1 comes first and then x2
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 < -self.WIDTH:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 < -self.WIDTH:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
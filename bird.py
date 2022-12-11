import pygame


class Bird:
    ROTATION_VEL = 20
    MAX_ROTATION = 25
    ANIMATION_TIME = 5

    def __init__(self, x, y, bird_images: list[pygame.Surface]):
        self.x = x
        self.y = y
        self.height = self.y
        self.frame_count = 0
        self.tilt = 0
        self.vel = 0
        self.img_number = 0  # image in which the bird's wings are upwards
        self.IMGS = bird_images
        self.img = self.IMGS[0]  # image in which the bird's wings are upwards

    def jump(self):
        self.vel = -10.5  # negative velocity refers to jump upwards
        self.frame_count = 0  # reset the frames
        self.height = self.y  # reset the height

    def move(self):
        self.frame_count += 1  # update the frames when the bird moves
        # d > 0 means downwards and d<0 means upwards and same for velocity also
        # and also bird is just moving in y direction and not in x direction
        d = self.vel * self.frame_count + 1.5 * self.frame_count ** 2  # frame count also works as time
        if d >= 16: # if the bird is falling and it falls more than 16 pixels then stop falling and face straight moving
            d = 16
        # if d < 0:   # just for tuning so that upward movement is seen clear
        #     d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:  # (d<0) this is the case when when bird is going upward
            if self.tilt < self.MAX_ROTATION:  # so making a tilt angle of max rotation
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90:  # if the tilt is greater than -90 then keep on reducing it till it reaches -90 to show
                self.tilt -= self.ROTATION_VEL  # the arc like falling

    def draw(self, win):
        self.img_number += 1

        # below work is done to show the flapping of the bird
        # animation time is that for how much time bird should be in one image state
        if self.img_number < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_number < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_number < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_number < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_number < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_number = 0

        if self.tilt < -80:  # when the bird is nose diving it should not flap its wings
            self.img = self.IMGS[1]
            self.img_number = self.ANIMATION_TIME * 2  # reset the image number so that next image should be IMG[2]

        rotated_image = pygame.transform.rotate(self.img, self.tilt)  # just rotating the image around its center
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect)

    def get_mask(self):  # getting the mask of the bird means the contour of bird to check its collision with any pipe
        return pygame.mask.from_surface(self.img)
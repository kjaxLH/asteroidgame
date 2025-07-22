import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.veloc = 0
        self.rotation_veloc = 0
        self.timer = 0
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        if self.rotation_veloc > MAX_ROTATION_VELOC or self.rotation_veloc < -MAX_ROTATION_VELOC:
            if self.rotation_veloc > 0:
                self.rotation_veloc = MAX_ROTATION_VELOC
            if self.rotation_veloc < 0:
                self.rotation_veloc = -MAX_ROTATION_VELOC
            
        self.rotation += PLAYER_TURN_SPEED * dt * self.rotation_veloc

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.veloc > MAX_VELOC or self.veloc < -MAX_VELOC:
            if self.veloc > 0:
                self.veloc = MAX_VELOC
            if self.veloc < 0:
                self.veloc = -MAX_VELOC

        self.position += forward * PLAYER_SPEED * dt * self.veloc

    def shoot(self):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = shot.velocity.rotate(self.rotation)
        shot.velocity = shot.velocity * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotation_veloc -= PLAYER_ROTATION_ACCELERATION

        if keys[pygame.K_d]:
            self.rotation_veloc += PLAYER_ROTATION_ACCELERATION

        if keys[pygame.K_w]:
            self.veloc += PLAYER_ACCELERATION

        if keys[pygame.K_s]:
            self.veloc -= PLAYER_ACCELERATION

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            if self.veloc > 0:
                self.veloc -= DECEL_SPEED
            elif self.veloc < 0:
                self.veloc += DECEL_SPEED
            if self.veloc <= DECEL_SPEED and self.veloc >= -DECEL_SPEED:
                self.veloc = 0

        if self.veloc > ZERO or self.veloc < -ZERO:
            self.move(dt)

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.rotation_veloc > 0:
                self.rotation_veloc -= ROTATION_DECEL_SPEED
            elif self.rotation_veloc < 0:
                self.rotation_veloc += ROTATION_DECEL_SPEED
            if self.rotation_veloc <= ROTATION_DECEL_SPEED and self.rotation_veloc >= -ROTATION_DECEL_SPEED:
                self.rotation_veloc = 0

        if self.rotation_veloc > ZERO or self.rotation_veloc < -ZERO:
            self.rotate(dt)
        
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.timer -= dt
import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Animation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.speed = random.uniform(0.2, 2.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.life = random.randint(50, 200)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        # Apply a slight gravity effect
        self.vy += 0.03
        
        # Add some randomness to movement
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        
        # Slow down particles
        self.vx *= 0.99
        self.vy *= 0.99
        
        # Decrease life
        self.life -= 1
        
        # Bounce off edges
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -0.8
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -0.8
            if self.y > HEIGHT:
                self.y = HEIGHT
                if random.random() > 0.5:
                    self.vy -= random.uniform(1, 3)

    def draw(self):
        # Fade out based on remaining life
        alpha = int(255 * (self.life / self.max_life))
        current_color = (self.color[0], self.color[1], self.color[2])
        
        # Draw the particle
        pygame.draw.circle(screen, current_color, (int(self.x), int(self.y)), self.size)
        
        # Optional glow effect (simple version)
        if self.size > 2:
            glow_size = self.size * 2
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (current_color[0], current_color[1], current_color[2], alpha // 3), 
                              (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)), special_flags=pygame.BLEND_RGB_ADD)

# Main function
def main():
    clock = pygame.time.Clock()
    particles = []
    mouse_pressed = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Add particles when mouse is pressed
        if mouse_pressed:
            for _ in range(5):
                particles.append(Particle(mouse_x + random.uniform(-10, 10), 
                                        mouse_y + random.uniform(-10, 10)))
        
        # Add some random particles occasionally
        if random.random() < 0.1:
            particles.append(Particle(random.randint(0, WIDTH), 
                                    random.randint(0, HEIGHT)))
        
        # Update and draw particles
        screen.fill(BLACK)
        
        # Remove dead particles and update/draw living ones
        particles = [p for p in particles if p.life > 0]
        
        for particle in particles:
            particle.update()
            particle.draw()
        
        # Connect nearby particles with lines
        for i, p1 in enumerate(particles):
            for p2 in particles[i+1:]:
                dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                if dist < 100:
                    alpha = int(255 * (1 - dist/100))
                    pygame.draw.line(screen, (255, 255, 255, alpha), 
                                    (int(p1.x), int(p1.y)), 
                                    (int(p2.x), int(p2.y)))
        
        # Display particle count
        font = pygame.font.Font(None, 36)
        text = font.render(f"Particles: {len(particles)}", True, WHITE)
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

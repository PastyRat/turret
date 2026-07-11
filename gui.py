import pygame
import time

import tkinter as tk
from tkinter import simpledialog

# Work around crash that occurs when query strength is called more than once
root = tk.Tk()
root.withdraw()
global queryonnextdraw
queryonnextdraw = False

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Select point to fire at")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# Import background image
background = pygame.image.load("background.png")
backgroundrect = background.get_rect()

# Clock for FPS
clock = pygame.time.Clock()
fps = 60

# Center of the screen (0, 0 in our coordinate system)
center_x = WIDTH // 2
center_y = HEIGHT // 2

# Grid settings
grid_spacing = 40  # pixels between grid lines
selected_point = None  # stored as (grid_x, grid_y)
pan_speed = 5  # pixels to move the viewport per key press

# Font for text
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 32)

def pixel_to_grid(pixel_x, pixel_y):
    """Convert pixel coordinates to grid coordinates (0,0 at center)"""
    global grid_x, grid_y
    grid_x = (pixel_x - center_x) / grid_spacing
    grid_y = (center_y - pixel_y) / grid_spacing  # Invert Y because pygame Y increases downward
    return grid_x, grid_y

def grid_to_pixel(grid_x, grid_y):
    """Convert grid coordinates back to pixel coordinates"""
    pixel_x = center_x + grid_x * grid_spacing
    pixel_y = center_y - grid_y * grid_spacing
    return pixel_x, pixel_y

def draw_background(background):
    bg_rect = background.get_rect(center=(center_x, center_y))
    screen.blit(background, bg_rect)

def query_strength():
    correct = False
    while correct == False:
        try:
            user_input = float(simpledialog.askstring("Input", "Enter the extension of the elastic band in meters"))
        except ValueError:
            # Yeah, I cba to create a new window to show an exception - to do later
            pass
        else:
            correct = True
    return user_input

def query_displacement():
    correct = False
    while correct == False:
        try:
            user_input = float(simpledialog.askstring("Input", "Enter the displacement of the location you are firing to from the turret"))
        except ValueError:
            # Yeah, I cba to create a new window to show an exception - to do later
            pass
        else:
            correct = True
    return user_input

def draw_grid():
    """Draw the coordinate grid"""
    # Draw vertical lines
    x = center_x
    while x < WIDTH:
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, HEIGHT), 1)
        x += grid_spacing
    
    x = center_x
    while x > 0:
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, HEIGHT), 1)
        x -= grid_spacing
    
    # Draw horizontal lines
    y = center_y
    while y < HEIGHT:
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (WIDTH, y), 1)
        y += grid_spacing
    
    y = center_y
    while y > 0:
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (WIDTH, y), 1)
        y -= grid_spacing
    
    # Draw X and Y axes (thicker, darker lines)
    pygame.draw.line(screen, BLACK, (0, center_y), (WIDTH, center_y), 2)  # X axis
    pygame.draw.line(screen, BLACK, (center_x, 0), (center_x, HEIGHT), 2)  # Y axis
    
    # Draw origin point
    pygame.draw.circle(screen, RED, (center_x, center_y), 5)

def draw_labels():
    """Draw axis labels"""
    # X-axis labels (bottom)
    x_start = int((0 - center_x) / grid_spacing) - 1
    x_end = int((WIDTH - center_x) / grid_spacing) + 1
    for i in range(x_start, x_end + 1):
        if i == 0:
            continue
        x_pixel = center_x + i * grid_spacing
        if 0 <= x_pixel < WIDTH:
            label = font_small.render(str(i), True, BLACK)
            screen.blit(label, (x_pixel - 10, center_y + 10))
    
    # Y-axis labels (left side)
    y_start = int((center_y - HEIGHT) / grid_spacing) - 1
    y_end = int(center_y / grid_spacing) + 1
    for i in range(y_start, y_end + 1):
        if i == 0:
            label = font_small.render("0", True, RED)
            screen.blit(label, (center_x - 20, center_y - 10))
            continue
        y_pixel = center_y - i * grid_spacing
        if 0 <= y_pixel < HEIGHT:
            label = font_small.render(str(i), True, BLACK)
            screen.blit(label, (center_x - 25, y_pixel - 10))

def draw_selected_point():
    """Draw the selected point and display its coordinates"""
    if selected_point is not None:
        grid_x, grid_y = selected_point
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        
        # Draw a circle at the selected point
        pygame.draw.circle(screen, BLUE, (int(pixel_x), int(pixel_y)), 6)
        pygame.draw.circle(screen, BLACK, (int(pixel_x), int(pixel_y)), 6, 2)
        
        # Draw crosshairs
        pygame.draw.line(screen, BLUE, (pixel_x, 0), (pixel_x, HEIGHT), 1)
        pygame.draw.line(screen, BLUE, (0, pixel_y), (WIDTH, pixel_y), 1)
        
        # Display coordinates
        coord_text = font_large.render(f"({grid_x:.2f}, {grid_y:.2f})", True, BLUE)
        screen.blit(coord_text, (10, 10))
        
        # Display pixel coordinates (for reference)
        pixel_text = font_small.render(f"Pixels: ({int(pixel_x)}, {int(pixel_y)})", True, GRAY)
        screen.blit(pixel_text, (10, 45))

def main():
    global selected_point
    global queryonnextdraw
    global center_x, center_y
    
    running = True
    while running:
        clock.tick(fps)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    selected_point = pixel_to_grid(*pygame.mouse.get_pos())
                    # So we can query on the next draw, so we can see coords at the same time as popup
                    queryonnextdraw = True
        keys = pygame.key.get_pressed()
        x_min = WIDTH // 2 - 12 * grid_spacing
        x_max = WIDTH // 2 + 12 * grid_spacing
        y_min = HEIGHT // 2 - 12 * grid_spacing
        y_max = HEIGHT // 2 + 12 * grid_spacing
        if keys[pygame.K_w] and center_y + pan_speed <= y_max:
            center_y += pan_speed
        if keys[pygame.K_s] and center_y - pan_speed >= y_min:
            center_y -= pan_speed
        if keys[pygame.K_a] and center_x + pan_speed <= x_max:
            center_x += pan_speed
        if keys[pygame.K_d] and center_x - pan_speed >= x_min:
            center_x -= pan_speed

        # Clear screen
        screen.fill(WHITE)
        
        # Draw everything
        draw_background(background)
        draw_grid()
        draw_labels()
        draw_selected_point()
        
        # Instructions
        instructions = font_small.render("Click to select a point. Use W/A/S/D to pan the view. Close window to continue.", True, BLACK)
        screen.blit(instructions, (10, HEIGHT - 30))
        
        pygame.display.flip()
        if queryonnextdraw == True:
            time.sleep(0.1)
            global strength
            strength = query_strength()
            global displacement
            displacement = query_displacement()
            queryonnextdraw = False
    root.destroy()
    pygame.quit()
    if __name__ != "__main__": # Allows the function to return a value when called from another .py
        list = [grid_x, grid_y, strength, displacement]
        return list

# Testing purposes
if __name__ == "__main__":
    main()
    print(grid_x)
    print(grid_y)
    print(strength)
    print(displacement)
import pygame

import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()
queryonnextdraw = False

# Start Pygame
pygame.init()

# Screen dimensions
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Select point to fire at")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREY = (230, 230, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Import background image
# Check if we have the real background image, if not use placeholder
try:
    file = open("background.png", "r") 
except FileNotFoundError:
    background = pygame.image.load("testbackground.png")
else:
    background = pygame.image.load("background.png")
    file.close()
backgroundrect = background.get_rect()

# Clock for FPS
clock = pygame.time.Clock()
fps = 60

# Center of the screen (0, 0 in our coordinate system)
center_x = width // 2
center_y = height // 2
background_offset_x = 0
background_offset_y = 0

# Grid settings
grid_spacing = 40  # pixels between grid lines
selected_point = None  # stored as (grid_x, grid_y)
pan_speed = 5  # pixels to move the view per key press

# Font for text
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 32)

def pixel_to_grid(pixel_x, pixel_y):
    #Convert pixel coordinates to grid coordinates (0,0 at center)#
    global grid_x, grid_y
    grid_x = (pixel_x - center_x) / grid_spacing
    grid_y = (center_y - pixel_y) / grid_spacing  # Invert Y because pygame Y increases downward
    return grid_x, grid_y

def grid_to_pixel(grid_x, grid_y):
    #Convert grid coordinates back to pixel coordinates
    pixel_x = center_x + grid_x * grid_spacing
    pixel_y = center_y - grid_y * grid_spacing
    return pixel_x, pixel_y

def draw_background(background):
    bg_rect = background.get_rect(center=(center_x + background_offset_x, center_y + background_offset_y))
    screen.blit(background, bg_rect)

def query_option():
    # Create dialog window
        dialog = tk.Toplevel(root)
        dialog.title("Choose an angle")
        dialog.geometry("300x150")
    
        result = [None]
    
        tk.Label(dialog, text="Pick an option:").pack(pady=10)
    
        tk.Button(dialog, text=str("Use extension to find angle"), width=30, 
              command=lambda: [result.__setitem__(0, 0), dialog.destroy()]).pack(pady=5)
        tk.Button(dialog, text=str("Use angle to find extension"), width=30, 
              command=lambda: [result.__setitem__(0, 1), dialog.destroy()]).pack(pady=5)
    
        root.wait_window(dialog)
        return result[0]

def query_strength():
    correct = False
    while correct == False:
        try:
            user_input = float(simpledialog.askstring("Input", "Enter the extension of the elastic band in meters"))
        except ValueError:
            pass #Ask again
        else:
            correct = True
    return user_input

def query_angle():
    correct = False
    while correct == False:
        try:
            user_input = float(simpledialog.askstring("Input", "Enter the angle that you want to fire the turret at"))
        except ValueError:
            pass #Ask again
        else:
            correct = True
    return user_input

def query_displacement():
    correct = False
    while correct == False:
        try:
            user_input = float(simpledialog.askstring("Input", "Enter the displacement of the location you are firing to from the turret"))
        except ValueError:
            pass #Ask again
        else:
            correct = True
    return user_input

def draw_grid():
    # Draw vertical lines
    x = center_x
    while x < width:
        pygame.draw.line(screen, LIGHT_GREY, (x, 0), (x, height), 1)
        x += grid_spacing
    
    x = center_x
    while x > 0:
        pygame.draw.line(screen, LIGHT_GREY, (x, 0), (x, height), 1)
        x -= grid_spacing
    
    # Draw horizontal lines
    y = center_y
    while y < height:
        pygame.draw.line(screen, LIGHT_GREY, (0, y), (width, y), 1)
        y += grid_spacing
    
    y = center_y
    while y > 0:
        pygame.draw.line(screen, LIGHT_GREY, (0, y), (width, y), 1)
        y -= grid_spacing
    
    # Draw X and Y axes (thicker, darker lines)
    pygame.draw.line(screen, BLACK, (0, center_y), (width, center_y), 2)  # X axis
    pygame.draw.line(screen, BLACK, (center_x, 0), (center_x, height), 2)  # Y axis
    
    # Draw origin point
    pygame.draw.circle(screen, RED, (center_x, center_y), 5)

def draw_labels():
    # Draw axis labels
    # X-axis labels (bottom)
    x_start = int((0 - center_x) / grid_spacing) - 1
    x_end = int((width - center_x) / grid_spacing) + 1
    for i in range(x_start, x_end + 1):
        if i == 0:
            continue
        x_pixel = center_x + i * grid_spacing
        if 0 <= x_pixel < width:
            label = font_small.render(str(i), True, BLACK)
            screen.blit(label, (x_pixel - 10, center_y + 10))
    
    # Y-axis labels (left side)
    y_start = int((center_y - height) / grid_spacing) - 1
    y_end = int(center_y / grid_spacing) + 1
    for i in range(y_start, y_end + 1):
        if i == 0:
            label = font_small.render("0", True, RED)
            screen.blit(label, (center_x - 20, center_y - 10))
            continue
        y_pixel = center_y - i * grid_spacing
        if 0 <= y_pixel < height:
            label = font_small.render(str(i), True, BLACK)
            screen.blit(label, (center_x - 25, y_pixel - 10))

def draw_selected_point():
    #Draw the selected point and display its coordinates
    if selected_point != None:
        grid_x, grid_y = selected_point
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        
        # Draw a circle at the selected point
        pygame.draw.circle(screen, BLUE, (int(pixel_x), int(pixel_y)), 6)
        pygame.draw.circle(screen, BLACK, (int(pixel_x), int(pixel_y)), 6, 2)
        
        # Draw crosshairs
        pygame.draw.line(screen, BLUE, (pixel_x, 0), (pixel_x, height), 1)
        pygame.draw.line(screen, BLUE, (0, pixel_y), (width, pixel_y), 1)
        
        # Display coordinates
        coord_text = font_large.render(f"({grid_x:.2f}, {grid_y:.2f})", True, BLUE)
        screen.blit(coord_text, (10, 10))
        
        # Display pixel coordinates (for reference)
        pixel_text = font_small.render(f"Pixels: ({int(pixel_x)}, {int(pixel_y)})", True, GREY)
        screen.blit(pixel_text, (10, 45))

def main():
    global selected_point
    global queryonnextdraw
    global center_x, center_y, background_offset_x, background_offset_y
    
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
        # Pan the grid with WASD keys
        if keys[pygame.K_w]:
            center_y += pan_speed
        if keys[pygame.K_s]:
            center_y -= pan_speed
        if keys[pygame.K_a]:
            center_x += pan_speed
        if keys[pygame.K_d]:
            center_x -= pan_speed
        # Pan the background with arrow keys
        if keys[pygame.K_UP]:
            background_offset_y += pan_speed
        if keys[pygame.K_DOWN]:
            background_offset_y -= pan_speed
        if keys[pygame.K_LEFT]:
            background_offset_x += pan_speed
        if keys[pygame.K_RIGHT]:
            background_offset_x -= pan_speed

        # Clear screen
        screen.fill(GREY)
        
        # Draw everything in order
        draw_background(background)
        draw_grid()
        draw_labels()
        draw_selected_point()
        
        # Instructions
        instructions = font_small.render("Click to select a point and close the window to continue.", True, BLACK)
        instructions2 = font_small.render("Use WASD to pan the grid and arrow keys to pan the background.", True, BLACK)
        screen.blit(instructions2, (10, height - 50))
        screen.blit(instructions, (10, height - 30))
        
        pygame.display.flip()
        if queryonnextdraw == True:
            #answer = query_option() From now only we use a predetermined extension only
            global displacement
            displacement = query_displacement()
            queryonnextdraw = False
    root.destroy()
    pygame.quit()
    if __name__ != "__main__": # Allows the function to return a value when called from another .py
        list = [grid_x, grid_y, displacement]
        return list

# Testing
if __name__ == "__main__":
    main()
    print("X: " + str(grid_x))
    print("Y: " + str(grid_y))
    print("Displacement: " + str(displacement))
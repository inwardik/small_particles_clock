#!/usr/bin/env python3
"""
Simple Paint Tool
A minimalistic drawing application that allows users to draw light blue points
on a black canvas and save the coordinates to a JSON file.

Controls:
- Left mouse click: Draw a 2x2 pixel light blue point
- 'c' key: Clear the canvas
- 's' key: Save points to out.json
- 'esc' key: Exit the application
"""

import pygame
import json
import sys

# Colors
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Point settings
POINT_SIZE = 2


class PaintTool:
    """Main class for the Paint Tool application"""

    def __init__(self):
        """Initialize pygame and create the drawing surface"""
        pygame.init()

        # Get display info and create fullscreen window
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Paint Tool")

        # List to store all drawn points
        self.points = []

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Fill screen with black
        self.screen.fill(BLACK)
        pygame.display.flip()

    def add_point(self, pos):
        """
        Add a point at the given position

        Args:
            pos: Tuple of (x, y) coordinates
        """
        x, y = pos
        self.points.append([x, y])

        # Draw the point on screen (2x2 pixels)
        pygame.draw.rect(self.screen, LIGHT_BLUE, (x, y, POINT_SIZE, POINT_SIZE))
        pygame.display.flip()

    def clear_canvas(self):
        """Clear all points from the canvas"""
        self.points = []
        self.screen.fill(BLACK)
        pygame.display.flip()

    def save_points(self):
        """Save all points to out.json file"""
        output_data = {
            "type": "geo",
            "data": self.points
        }

        try:
            with open('out.json', 'w') as f:
                json.dump(output_data, f)
            print(f"Saved {len(self.points)} points to out.json")
        except Exception as e:
            print(f"Error saving file: {e}")

    def run(self):
        """Main application loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.add_point(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_c:
                        self.clear_canvas()
                    elif event.key == pygame.K_s:
                        self.save_points()

            # Control frame rate
            self.clock.tick(60)

        # Cleanup
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the application"""
    paint_tool = PaintTool()
    paint_tool.run()


if __name__ == "__main__":
    main()

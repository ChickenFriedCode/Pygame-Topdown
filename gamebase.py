"""
    Base Class for the game loop and window creation.
"""
import pygame
import sys

from typing import Callable


class GameBase:
    """ Game class with the main game loop and core
    methods and functions to have the game run. """

    # Static properties:
    # List of functions to be called during the 'Ready' phase.
    ready_functions = []
    # List of functions to be called during the 'Update" loop.
    update_functions = []
    # List of functions to be called in 'Update' with events.
    update_event_functions = []
    # List of functions to be called last.
    update_late_functions = []
    # list of functions to be called early.
    update_early_functions = []

    # static propertie for the window
    window = None
    window_width = None
    window_height = None
    window_title = None
    window_size = None
    bg_color = (120, 120, 120)

    def __init__(
            self,
            window_width: int = 400,
            window_height: int = 400,
            window_title: str = "Default Title"
    ):
        """ Init for the class. Calls window creation method """
        self.create_window(window_width, window_height, window_title)

    def create_window(
            self, window_width, window_height, window_title):
        """ Creates the game window if none exists."""
        if GameBase.window:
            return
            # sets up values:
        GameBase.window_size = (window_width, window_height)
        GameBase.window_width = window_width
        GameBase.window_height = window_height
        GameBase.window_title = window_title

        # sets clock propertie
        self.clock = pygame.time.Clock()

        # sets window title:
        pygame.display.set_caption(self.window_title)
        # Creates window:
        self.s_s_size = 2  # Screen Scale Size
        self.display = pygame.Surface((GameBase.window_width/self.s_s_size, GameBase.window_height/self.s_s_size))  # noqa
        self.dis_cent_x = self.display.get_width() / 2
        self.dis_cent_y = self.display.get_height() / 2
        self.dis_center = [self.dis_cent_x, self.dis_cent_y]
        self.surf = pygame.transform.scale(self.display, GameBase.window_size)
        GameBase.window = pygame.display.set_mode(GameBase.window_size, 0, 32)

    def check_if_window_close_pressed(self, event) -> None:
        """ Checks if window close button was pressed """
        if event.type == pygame.QUIT:
            self.quit_game()

    def quit_game(self):
        "Exits the game."
        pygame.quit()
        sys.exit()

    # Add methods or functions to the ready list
    def add_to_ready_functions(self, funct: Callable):
        """ Adds new functions to the list of ready list """
        GameBase.ready_functions.append(funct)

    # Calls methds or functions in the ready list
    def call_ready(self):
        """ Calls the ready functions in the list before game loop. """
        for f in GameBase.ready_functions:
            f()

    # Adds methods or functions to update list
    def add_to_update_functions(self, funct: Callable):
        """ Adds new functions to the list of update functions
            To be called each frame.
        """
        GameBase.update_functions.append(funct)

    # Calls methods or functions in the update list
    def update_loop(self, delta):
        """ Calls each function in the update function list """
        # -- Need to test if while is faster then the for in this set up:
        i = -1
        end = len(GameBase.update_functions) - 1
        while i < end:
            i += 1
            GameBase.update_functions[i](delta)

        # ---- Here just incase While is slower ---
        # for f in GameBase.update_functions:
        #     f(delta)

    # Adds methods or functions to event update list
    def add_to_update_event_functions(self, funct: Callable):
        """ Adds functions to even list"""
        GameBase.update_event_functions.append(funct)

    # Calls methods or functiosn to event update list
    def update_event_loop(self, delta, event):
        """ Calls each function in the update loop with events passed """
        for f in GameBase.update_event_functions:
            f(delta, event)

    # Adds methods or functions to late update list
    def add_to_update_late_functions(self, funct: Callable):
        """ Adds functions to late update list"""
        GameBase.update_late_functions.append(funct)

    # Calls methods or functiosn in late update list
    def update_late_loop(self, delta):
        """ Calls each function in the late update loop """
        for f in GameBase.update_late_functions:
            f(delta)

    # Adds methods or functiosn to early update list
    def add_to_update_early_functions(self, funct: Callable):
        """ Adds functions to early update list"""
        GameBase.update_early_functions.append(funct)

    # Calls methods or functions in early update list
    def update_early_loop(self, delta):
        """ Calls each function in the early update loop """
        for f in GameBase.update_early_functions:
            f(delta)

    # Method used to load images in to game.
    def load_image(self, path: str):
        """ Loads image in to pygame """
        return pygame.image.load(path)

    # Returns the displayed unscaled center point:
    def get_screen_center(self) -> list:
        """ Returns the game display center point """
        return self.dis_center

    # The main game loop
    def main_game_loop(self):
        """ Main game loop. """

        # ready phase before the loop starts:
        self.call_ready()

        # initial tick time
        getTicksLastFrame = 1

        # Main loop
        while True:
            # Clear Screen: AKA, Override screen with single color:
            self.display.fill(self.bg_color)

            # Delta time:
            t = pygame.time.get_ticks()
            # deltaTime in seconds.
            delta = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t

            # Update phase:
            # Call Early Update method
            self.update_early_loop(delta)

            # Event loop to call Update loops needing events
            for event in pygame.event.get():
                self.check_if_window_close_pressed(event)
                self.update_event_loop(delta, event)

            # Standard update to be called:
            self.update_loop(delta)

            # Late update
            self.update_late_loop(delta)

            # Scale the game screen to fit the window:
            self.surf = pygame.transform.scale(
                self.display, GameBase.window_size)
            # Draw the scaled game to the window:
            GameBase.window.blit(self.surf, (0, 0))
            # Updates every thing in the display
            pygame.display.update()

            # print(self.clock.get_fps()) # Uncomment to show FPS in console.
            self.clock.tick(120)  # Max FPS # Probably shouldn't be hard coded.

    # Initiates the game system
    def start_main(self):
        """ Method to initiate game """
        pygame.init()
        self.main_game_loop()


# Used for testing:
if __name__ == "__main__":
    test = GameBase(1000, 1000, 'Testing Game Window')

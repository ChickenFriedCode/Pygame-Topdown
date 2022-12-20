"""
    A test file for the game.
    --
    This is just something I slapped together seeing how much
    pygame I can learn in about 3 or so days of time.

    Also something I made to help show some of my coding style.
    --
    I made a lot of the functions in this thing my self instead
    of using all of the built in functions in pygame as I didn't
    want to spend to much time learning another framework
    I may or may not use in the future.

    If I do need to learn pygame properly in the future
    I can go in to more detail in to the frame work then.
    --
    WASD, LShift, ESC are the only keys working.
"""

# Imports:
import pygame
from gamebase import GameBase
from user_input import UserInputs
from loadmap import MapLoader
from detect_col import CollisionDetection


# Default Final screen size
SCREEN_SIZE = [1240, 760]


# The center of the original display before inlarged final screen size.
# The game is set at half the final resolution,
# so I devide by 4 to get the center of that.
SCREEN_CENTER = [SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/4]


# A test class for the game:
class TestGame:
    """ Testing game """

    def __init__(self):
        """ Initialize game """
        # TODO: Use a config file for some of these settings:

        # Initialize game screen
        self.game = GameBase(
            SCREEN_SIZE[0], SCREEN_SIZE[1], 'Pygame Game')

        # Load map
        self.loaded_map = MapLoader(self.game, 'assets/map1.png')
        # Path for player img.
        self.player_img = 'assets/box_character_16.png'
        # Player input:
        self.player_input = UserInputs(self.game)

        # The collisionDection class would be
        # inharited to a player class eventually
        self.player = CollisionDetection(game=self.game,
                                         char_img_path=self.player_img,
                                         tag=CollisionDetection.TAG_PLAYER
                                         )
        # Sets the starting position in game:
        self.player.set_position([100, 100])
        # Defaults player jump setting:
        self.jump_ressed = False

        # Adds update_loop method to game loop
        self.game.add_to_update_functions(self.update_loop)
        self.game.start_main()  # Starts the game

    # Teleport method for anyone that needs it:
    # This could be added to the player, NPC, or
    # skill kit class. If I continue the project.
    def teleport_location(self, character) -> list:
        """ returns location to teleport to """
        # Makes sure the position is not a refrence
        port_pos = character.get_position().copy()
        port_pos[0] += character.get_last_dir_moved()[0] * 100
        port_pos[1] += character.get_last_dir_moved()[1] * 100
        return port_pos

    def update_loop(self, delta):
        """ Update loop for the game mechanics """

        # ==================
        # - Player Inputs --
        # ==================

        # Quits game:
        if self.player_input.key_pressed('MENU'):
            self.game.quit_game()

        # Jump statments:
        if self.player_input.key_pressed('JUMP'):
            self.jump_ressed = True
        # If jump_pressed:
        if self.jump_ressed:
            self.jump_ressed = False
            # then teleport:
            self.player.set_position(self.teleport_location(self.player))

        # get player move input:
        move_dir = self.player_input.get_movement_dir()

        # ===================
        # - player movement -
        # ===================

        # Set player move direction based in player input:
        self.player.set_input_direction(move_dir)

        # ==================
        # --  Raycasting  --
        # ==================

        # Vars used for raycasting:
        # Because I use lists for vector2 I convert the tuple to a list:
        rect_center = [self.player.rect.center[0], self.player.rect.center[1]]
        # The direction angle the raycast should shoot from
        direction = self.player.get_last_angle_moved()

        # Raycasting :
        # raycast line using last direction moved
        # as the direction for the ray direction:
        hit_info = self.player.ray_cast_from_point(
            rect_center, direction, 40, 1)

        # TODO: Remove Hard coding:
        # Min and max dist before pushback and wall hitting begins.
        min_d = 10  # slightly more then half the size of player
        max_d = 30  # Arbitary number that feels interesting

        # Draws the line to visualize the raycast:
        pygame.draw.line(self.game.display, (200, 50, 50),
                         rect_center, hit_info['hit_point'], 2)

        # If raycast hit something do things:
        if hit_info['has_hit']:

            # Placing condistions in to vars so it's not to long:
            is_hit_dist_less_max_d = hit_info['hit_distance'] <= max_d
            is_hit_dist_more_min_d = hit_info['hit_distance'] >= min_d
            # Gives Pushback / bounce befor hitting walls.
            # Not needed it just gives a more interesting feel to the movement.
            if is_hit_dist_more_min_d and is_hit_dist_less_max_d:
                # More placing things in to vars so it's not to long:
                position = self.player.get_reversed_last_dir_moved()
                position[0] += self.player.get_position()[0]
                position[1] += self.player.get_position()[1]
                self.player.set_position(position)

            # Putting conditions in to vars so it's not to long:
            player_last_angle = self.player.get_last_angle_moved()
            is_same_direct = (player_last_angle == hit_info['hit_direction:'])
            # Stops the player from walking in to the walls.
            if hit_info['hit_distance'] < min_d and is_same_direct:
                self.player.set_input_direction([0, 0])


# Initiates the game:
test_game = TestGame()

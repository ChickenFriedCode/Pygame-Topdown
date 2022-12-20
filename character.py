"""
Character Class

The base class for all characters or entities in the game.
Even for the simple images.

This class handles the movement of all items in the game
including the movement to simulate camera movement.

All other entitiy or game objects in the game would
inharit from this class.

This class should probably be called 'GameObject'
But, this is what we get with no planning from the start.

If I do continue on with the project, I'll refactor
the game to call this GameObject class or something.
"""
# imports
import pygame
import gamebase
import math
from typing import Callable


class CharacterClass:
    """ Character Class """
    # The game property so only 1 game class for all classes.
    game: gamebase.GameBase = None

    # Static properties for all instances:
    # Constant Vars:
    CAM_SMOOTH_AMT = 20
    # Tags: Can probably be used an an enum. But I like it this way.
    TAG_WORLD = 'world'
    TAG_PLAYER = 'player'
    TAG_ENEMY = 'enemy'
    TAG_PROJECTILE = 'projectile'

    DEFAULT_SPEED = 200

    # Statics properties:
    # Instance Counter for how many characters there are:
    s_instance_counter = -1
    s_cam_pos_relitve_to_target = [0, 0]
    s_cam_target = None

    # Information about the player for all to have access to:
    s_player_position = [0, 0]
    s_player = None
    s_chars_near_player = {}
    s_chars_near_projectile = {}
    s_chars_hitting_player = {}
    s_chars_near_target = {}
    s_player_dist_max = 50

    def __init__(
            self,
            game: gamebase.GameBase,
            char_img_path: str,
            **kwargs
    ):
        """ Class Initilizer """
        # Make sure all instances use same game object:
        if CharacterClass.game is None:
            CharacterClass.game = game
        # Adds to instance counter:
        CharacterClass.s_instance_counter += 1
        # Set up defaults:
        defaults = {
            'pos_x': 0,
            'pos_y': 0,
            'name': "",
            'tag': None,
            'speed': self.DEFAULT_SPEED,
            'is_collidable': False
        }
        defaults.update(kwargs)

        pos_x: int = defaults['pos_x']
        pos_y: int = defaults['pos_y']
        name: str = defaults['name']
        tag: str = defaults['tag']
        speed: int = defaults['speed']
        is_collidable: bool = defaults['is_collidable']

        self.tag = tag
        self.name = name
        self.id = CharacterClass.s_instance_counter

        # Set up player static protperties:
        if self.tag == CharacterClass.TAG_PLAYER:
            if CharacterClass.s_cam_target is None:
                CharacterClass.s_cam_target = self
            if CharacterClass.s_player is None:
                CharacterClass.s_player = self

        self.character_pos: list = [pos_x, pos_y]
        self.character_velocity = [0, 0]
        self.last_dir_moved = [1, 0]  # defaults last direction pressed to right # noqa
        self.last_angle_moved = 0
        self.character_speed = speed
        self.view_distance = 300
        self.draw_rect = False
        self.is_force_stop_on = False
        self.input_direction = [0, 0]

        self.is_movable = True
        self.is_collidable = is_collidable

        # Load character Img and set vars acordingly
        self.img = game.load_image(char_img_path)
        self.img_half_width = self.img.get_width() / 2
        self.img_half_height = self.img.get_height() / 2
        self.hit_box_walls_size = self.img_half_width
        self.hit_box_dmg_size = self.hit_box_walls_size * 0.75
        self.rect = pygame.Rect(
            self.character_pos[0],
            self.character_pos[1],
            self.img.get_width(),
            self.img.get_height()
        )

        # Adds the update method to game loop:
        self.add_method_to_update_early_game_loop(self.early_update)
        self.add_method_to_update_game_loop(self.update)

    # =============================
    # --- Setters and Getters : ---
    # =============================

    def set_last_angle_moved(self, angle: float) -> None:
        """ Sets the last_angle_moved property """
        self.last_angle_moved = angle

    def set_last_angle_moved_by_vector(self, vector: list) -> None:
        """ Sets the last_angle_moved property with a vector """
        # Incase vector is a tuple:
        vector = self.convert_tuple_list(vector)
        self.last_angle_moved = math.degrees(math.atan2(vector[1], vector[0]))

    def set_force_stop(self, b: bool) -> None:
        """ Sets the is_force_stop_on property """
        self.is_force_stop_on = b

    def set_cam_target(self, target):
        """ Sets the target object for the camera to follow """
        CharacterClass.s_cam_target = target

    def set_draw_rect(self, b: bool) -> None:
        """ Sets bool to either draw rect or not over img. """
        self.draw_rect = b

    def set_position(self, pos_vector: list) -> None:
        """ manually sets character position
            Good for teleports or placing something.
        """
        pos_vector = self.convert_tuple_list(pos_vector)
        self.character_pos = pos_vector
        self.rect.x = pos_vector[0]
        self.rect.y = pos_vector[1]

    def set_speed(self, speed: int) -> None:
        """ Sets character speed """
        self.character_speed = speed

    def set_name(self, name: str) -> None:
        """ Gives the character a name """
        self.name = name

    def set_tag(self, tag: str) -> None:
        """ Gives the character a Tag """
        self.tag = tag

    def set_is_movable(self, b: bool) -> None:
        """ Set if character is movable """
        self.is_movable = b

    def set_is_collidable(self, b: bool) -> None:
        """ Set if character is collidable """
        self.is_collidable = b

    def set_use_center(self, b: bool) -> None:
        """ Set if Use Center Point for Movement """
        self.use_center = b

    def set_last_dir_moved(self, vector: list) -> None:
        """ Sets the last direction moved property """
        # incase tuple is sent
        vector = self.convert_tuple_list(vector)
        self.last_dir_moved = vector

    def set_input_direction(self, vector: list) -> None:
        """ Sets the input direction """
        # sets input to 0,0 if no movement is allowed:
        if not self.is_movable:
            self.input_direction = [0, 0]
            return

        # incase a tuple is entered:
        vector = self.convert_tuple_list(vector)
        # Normalizes the directinal vector:
        norm = self.normalize(vector)
        # Setting direction last pressed:
        if (norm[0] != 0 and norm[1] != 0) or (norm[0] != 0 or norm[1] != 0):
            self.last_dir_moved = norm.copy()
            self.set_last_angle_moved_by_vector(norm.copy())
        # Sets sets direction:
        self.input_direction = norm.copy()

    def get_last_angle_moved(self) -> list:
        """ Returns the last_angle_moved property """
        return self.last_angle_moved

    def get_force_stop(self) -> bool:
        """ Returns the is_force_stop_on property """
        return self.is_force_stop_on

    def get_position(self) -> list:
        """ returns characters position """
        return self.character_pos

    def get_last_dir_moved(self) -> list:
        """ gets the last_dir_moved property """
        return self.last_dir_moved

    def get_reversed_last_dir_moved(self):
        """ returned the reversed of last_dir_moved """
        return [self.last_dir_moved[0] * -1, self.last_dir_moved[1] * -1]

    def get_input_direction(self) -> list:
        """ gets the input_direction property """
        return self.input_direction

    # =============================
    # ---  Movement Methods  ------
    # =============================

    def normalize(self, vector) -> list:
        """ Normalizes the x and y input """
        # This normalize method only works for
        # keyboard or on and off buttons.
        # It's good for speed but
        # Not for analog joy sticks.

        # any case a tuple is sent through:
        vector = self.convert_tuple_list(vector)

        # Saves on Sqr math
        hyp_of_1 = 1.41421356
        hyp_x = hyp_of_1 if vector[1] else 1
        hyp_y = hyp_of_1 if vector[0] else 1
        norm_vect = [vector[0]/hyp_x, vector[1]/hyp_y]
        return norm_vect

    def set_velocity(self, vector: list) -> None:
        """ sets the velocity or 'Move' direction """
        # Any case a tuple is sent through:
        vector = self.convert_tuple_list(vector)
        self.character_velocity[0] = vector[0]
        self.character_velocity[1] = vector[1]

    # =============================
    # ---  Camera Methods  ------
    # =============================

    def _adujust_pos_to_sim_cam(self, pos: list, delta) -> list:
        """ The Final xy coords to be sent to display.blitz """
        # Tweens the camera movement in a linier tween

        # any case a tuple is sent through:
        pos = self.convert_tuple_list(pos)

        pos[0] = pos[0] + CharacterClass.s_cam_pos_relitve_to_target[0] / \
            self.CAM_SMOOTH_AMT
        pos[1] = pos[1] + CharacterClass.s_cam_pos_relitve_to_target[1] / \
            self.CAM_SMOOTH_AMT

        # I did not write to pos var cause it was causing odd bugs
        pos_x = pos[0]
        pos_y = pos[1]
        # This helps from tile tearing and collapsing
        px = math.floor(pos_x)
        py = math.floor(pos_y)
        return [px, py]

    def simple_dist_b_sub_a(self, a, b, near_0: int = 5) -> list:
        """ Checks Distance of a to b """
        x = b[0] - a[0]
        y = b[1] - a[1]

        # if x and y are close enough to zero just set it to zero.
        x = 0 if x <= near_0 and x >= -near_0 else x
        y = 0 if y <= near_0 and y >= -near_0 else y
        return [x, y]

    def move_cam_to_target(self) -> None:
        """ Moves the camera to the target object """
        if self == CharacterClass.s_cam_target:
            CharacterClass.s_cam_pos_relitve_to_target = self.simple_dist_b_sub_a(  # noqa
                self.get_position(),
                self.game.dis_center
            )

    def input_to_velocity(self):
        """ Directly adding input direction in to velocity"""
        # Should probably change this to use physics and things.
        self.set_velocity(self.get_input_direction())

    # =============================
    # --  Other Random Methods  ---
    # =============================

    def convert_tuple_list(self, item) -> list:
        """ Converts a tuple to a list
        to be used with the rest of the code"""
        if isinstance(item, list):
            return item
        x = item[0]
        y = item[0]
        return [x, y]

    # =============================
    # --  Update loop for game  ---
    # =============================

    def update(self, delta) -> None:
        """ The function that gets sent to the game loop """

        # While it's possible to change later for physics,
        # I'm just directly making velocity vector equal to input vector
        self.input_to_velocity()

        # setting character position based on speed, delta, and velocity:
        self.character_pos[0] += self.character_velocity[0] * self.character_speed * delta  # noqa
        self.character_pos[1] += self.character_velocity[1] * self.character_speed * delta  # noqa
        self.rect.x = self.character_pos[0]
        self.rect.y = self.character_pos[1]

        # Updates images based on 'Camera Movement'
        pos_to_blit = self._adujust_pos_to_sim_cam(
            self.character_pos, delta)

        # Send image to be drawn on screen.
        self.game.display.blit(
            self.img, (pos_to_blit[0], pos_to_blit[1]))

        # Updating Cam to follow target:
        self.move_cam_to_target()

        # Updateing static Player position for all to see:
        if self.tag == CharacterClass.TAG_PLAYER:
            CharacterClass.s_player_position = self.get_position()

        # Color over the object with a rect
        # Used more as a debuger to see if object was hit:
        if self.draw_rect:
            pygame.draw.rect(self.game.display, (20, 200, 20), self.rect)

    # These are here if it's needed later.
    # Probably will delete them though.
    def early_update(self, delta) -> None:
        """ add these methods to game early update loop """
        pass

    def late_update(self, delta) -> None:
        """ add these methods to game late update loop """
        pass

    # =============================
    # ---  Send To Game Loop  -----
    # =============================

    def add_method_to_update_early_game_loop(self, method: Callable):
        """ Adds methods to the early update loop """
        self.game.add_to_update_early_functions(method)

    def add_method_to_update_game_loop(self, method: Callable):
        """ Adds methods to a list to be sent to the gameloop """
        self.game.add_to_update_functions(method)

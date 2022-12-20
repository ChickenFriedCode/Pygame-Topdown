"""
Adds hit detection to the characters.
inhearits from the Character Class
Eventually would be inharited to
Player, NPC, and projectile classes.
"""

# Imports:
import math
import pygame
from character import CharacterClass


class CollisionDetection(CharacterClass):
    """ Collision and Hit Detection class """

    # static properties:
    s_hitables = []
    s_player_hit_rect = False

    def __init__(self, game, char_img_path, **kwargs):
        super().__init__(game, char_img_path, **kwargs)
        """ Initializer method """
        # Send self to collision detection list:
        CollisionDetection.s_hitables.append(self)

        # Set defaults
        self.set_is_collidable(True)
        self._is_being_hit = False
        self._is_ray_hit = False
        self._is_overlap = False
        self._hit_info = {}

        # Sends the method to the game loop
        self.add_method_to_update_game_loop(self.methods_to_send_to_loop)

    # Getters and setters:
    def _set_is_ray_hit(self, b: bool):
        """ Sets _is_ray_hit var  """
        self._is_ray_hit = b

    def _set_is_overlap(self, b: bool):
        """ sets _is_overlap var """
        self._is_overlap = b

    def _set_is_being_hit(self, b: bool):
        """ sets _is_being_hit Var """
        self._is_being_hit = b

    def _get_is_ray_hit(self):
        """ Returns _is_ray_hit var """
        return self._is_ray_hit

    def _get_is_overlap(self):
        """ Returns _is_overlap var """
        return self._is_overlap

    def _get_is_being_hit(self):
        """ Returns _is_being_hit var """
        return self._is_being_hit

    def _test_hit_vars(self):
        """ Test ray hit and overlap """
        if self._get_is_overlap() or self._get_is_ray_hit():
            self._set_is_being_hit(True)
        else:
            self._set_is_being_hit(False)

    def being_hit(self):
        if self._is_being_hit:
            self.set_draw_rect(True)
        else:
            self.set_draw_rect(False)

    def point_in_circle_cir(self, radius, angle, offset: list = [0, 0]):
        """ Math to get points along cercomfrence of a circle """
        x = (radius * math.cos(math.radians(angle))) + offset[0]
        y = (radius * math.sin(math.radians(angle))) + offset[1]
        return [x, y]

    def direction_reverse(self, directtion):
        """ Returns the opisit direction """
        output = directtion - 180
        return output

    # Detection methods:
    def rect_detect(self, delta):
        """ Detects if current object has hit the player """
        if self.tag == CollisionDetection.TAG_PLAYER:
            return

        is_hit = self.rect.colliderect(CollisionDetection.s_player.rect)
        if is_hit:
            self._set_is_overlap(True)
        else:
            self._set_is_overlap(False)

    def ray_cast_from_point(self, from_point: list, direction: int, distance: int, steps: int = 4) -> dict:  # noqa
        """Ray cast method to be called by the object it's attached to:

        Args:
            from_point (list): location the ray is casting from.
            direction (int): The direction in angle degrees
            distance (int): how far should the ray shoot out too.
            steps (int, optional): each set the ray should check for a
            hit. Defaults to 4.

        Returns:
            dictionary: Information based on the hit detection.
        """

        # Direction placed in a variable so as to keep the line short:
        vector2D = self.point_in_circle_cir(distance, direction, from_point)

        # initial set up of the hit_info output
        # Placing the max dist of the ray as the end point
        self._hit_info = self._ray_hit_info(hit_point=vector2D)

        # used to skip raycast check if one has been found.
        # But still allows the loop to complete to finish other work.
        has_hit = False

        # Using nested while loop cause it tested faster on my PC.
        i = -1
        j = -1
        # The loop for each step of the ray
        while i < distance - 1:
            i += steps  # The gap between each test before reaching the end.

            # get point at the step based on direction of the circle.
            cir_point = self.point_in_circle_cir(i, direction, from_point)  # noqa
            x = cir_point[0]  # Sets the x
            y = cir_point[1]  # sets the y

            j = -1
            # the loop for each collidable object in the list:
            while j < len(CollisionDetection.s_hitables) - 1:
                j += 1

                # Gets the object that is iterated in the list:
                hit_obj = CollisionDetection.s_hitables[j]

                # Tests if the object is it's self:
                if hit_obj.id == self.id:
                    continue

                # tests if the object currently iterated to is hit:
                if hit_obj.id == self._hit_info['hit_id']:
                    hit_obj._set_is_ray_hit(True)
                else:
                    hit_obj._set_is_ray_hit(False)

                # If one of the previus objects was hit,
                # don't calc hit object again.
                if has_hit:
                    continue

                # Calculate hit objects
                if pygame.Rect.collidepoint(hit_obj.rect, x, y):

                    # Sets var to skip this test next iteration of loops:
                    has_hit = True

                    # Sets the hit by ray tag for the hit object
                    hit_obj._set_is_ray_hit(True)

                    # Collects information of the hit object for use
                    self._hit_info = {
                        'has_hit': True,
                        'hit_point': [x, y],
                        'hit_object': hit_obj,
                        'hit_object_pos': hit_obj.get_position(),
                        'hit_tag': hit_obj.tag,
                        'hit_id': hit_obj.id,
                        'hit_name': hit_obj.name,
                        'hit_rect_overlap': hit_obj._get_is_overlap(),
                        'hit_has': True,
                        'hit_direction:': direction,
                        'hit_direction_oppisit': self.direction_reverse(direction),  # noqa
                        'hit_from': [from_point[0], from_point[1]],
                        'hit_distance': i,
                    }

        return self._hit_info

    # Method for setting up the ray hit information:
    def _ray_hit_info(self, **kwargs):
        defaults = {
            'has_hit': False,
            'hit_point': None,
            'hit_object': None,
            'hit_object_pos': None,
            'hit_tag': None,
            'hit_id': None,
            'hit_name': None,
            'hit_rect_overlap': None,
            'hit_has': None,
            'hit_direction:': None,
            'hit_direction_oppisit': None,  # noqa
            'hit_from': None,
            'hit_distance': None,
        }
        defaults.update(kwargs)
        return defaults.copy()

    # Method to hold all looped methods to be sent to game loop update
    def methods_to_send_to_loop(self, delta):
        """ All methods to add to loop to be called """
        self._test_hit_vars()
        self.being_hit()
        self.rect_detect(delta)

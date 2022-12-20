"""
Get User inputs
"""

# imports
from pygame import locals as pgl
from gamebase import GameBase


class UserInputs:
    """ Class for handling user Input: """

    # Makes sure there is only a single instance of this class
    TOTAL_INSTANCES = 0

    # Make sure there is only a single instance of the GameBase class
    game: GameBase = None

    # Constants to use so I don't have to have typos
    MOVE_LEFT = "MOVE_LEFT"
    MOVE_RIGHT = "MOVE_RIGHT"
    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    JUMP = "JUMP"
    ATTACK = "ATTACK"
    ALT_ATTACK = "ALT_ATTACK"
    MENU = "MENU"
    SELECT = "SELECT"

    # Placed in a list for iteritive abilities:
    key_list = [
        MOVE_LEFT,
        MOVE_RIGHT,
        MOVE_UP,
        MOVE_DOWN,
        JUMP,
        ATTACK,
        ALT_ATTACK,
        MENU,
        SELECT,
    ]

    last_key_state = {}
    is_key_just_pressed = {}
    is_key_pressed = {}
    is_key_just_released = {}

    key_codes = None
    move_direction = [0, 0]

    # game: GameBase
    def __init__(self, game: GameBase):
        """ Class Initilization method """
        # Makes sure only single instance
        if UserInputs.TOTAL_INSTANCES >= 1:
            return
        UserInputs.TOTAL_INSTANCES += 1
        UserInputs.game = game
        self.set_keys()

    def set_keys(self):
        """ Sets up initial key setup"""
        # TODO: Set up a load key set from config file
        # But right now it's being hard coded:
        UserInputs.key_codes = {
            UserInputs.key_list[0]: pgl.K_a,
            UserInputs.key_list[1]: pgl.K_d,
            UserInputs.key_list[2]: pgl.K_w,
            UserInputs.key_list[3]: pgl.K_s,
            UserInputs.key_list[4]: pgl.K_LSHIFT,
            UserInputs.key_list[5]: pgl.K_SPACE,
            UserInputs.key_list[6]: pgl.K_q,
            UserInputs.key_list[7]: pgl.K_ESCAPE,
            UserInputs.key_list[8]: pgl.K_TAB
        }
        # Initiate all key states to False
        for key in UserInputs.key_list:
            UserInputs.is_key_pressed[key] = False
            UserInputs.last_key_state[key] = False
            UserInputs.is_key_just_pressed[key] = False
            UserInputs.is_key_just_released[key] = False

        # Sends key Input methods to game loop:
        UserInputs.game.add_to_update_event_functions(self.send_to_update)
        UserInputs.game.add_to_update_late_functions(self.send_to_late_update)

    def set_key_is_down(self, event):
        """ Check if key is down, then sets the value if it is or isn't. """
        if event.type == pgl.KEYDOWN:
            for key in UserInputs.is_key_pressed:
                if event.key == UserInputs.key_codes[key]:
                    UserInputs.is_key_pressed[key] = True
        if event.type == pgl.KEYUP:
            for key in UserInputs.is_key_pressed:
                if event.key == UserInputs.key_codes[key]:
                    UserInputs.is_key_pressed[key] = False

    # Consumes the flags. Turns them from True to False:
    def consume_just_pressed_key(self, key):
        """ Consumes the key is just pressed flag. """
        UserInputs.is_key_just_pressed[key] = False

    def consume_just_released_key(self, key):
        """ Consumes the Key is Just Released flag. """
        UserInputs.is_key_just_released[key] = False

    def consume_all_keys(self):
        """ Consumes all Key is pressed and released flags """
        for key in UserInputs.key_list:
            UserInputs.is_key_just_pressed[key] = False
            UserInputs.is_key_just_released[key] = False

    # Checks key is pressed or released event methods:
    def key_held(self, key):
        """ Returns if key is held down. """
        return UserInputs.is_key_pressed[key]

    def key_pressed(self, key):
        """ Returns if the key was just pressed this frame """
        if not UserInputs.last_key_state[key] and UserInputs.is_key_pressed[key]:  # noqa
            UserInputs.is_key_just_pressed[key] = True
        return UserInputs.is_key_just_pressed[key]

    def key_released(self, key):
        """ Checks if the key was just released this frame """
        if UserInputs.last_key_state[key] and not UserInputs.is_key_pressed[key]:  # noqa
            UserInputs.is_key_just_released[key] = True
        return UserInputs.is_key_just_pressed[key]

    # Set key states:
    def set_last_key_state(self):
        """ Sets all key states at the end of the loop """
        for key in UserInputs.key_list:
            UserInputs.last_key_state[key] = UserInputs.is_key_pressed[key]

    # sets movement information for the player
    def move_keys_pressed(self) -> list:
        """ Sets direction for X and Y based on pressed keys """
        UserInputs.move_direction = [0, 0]
        if UserInputs.is_key_pressed[UserInputs.MOVE_LEFT]:
            UserInputs.move_direction[0] -= 1
        if UserInputs.is_key_pressed[UserInputs.MOVE_RIGHT]:
            UserInputs.move_direction[0] += 1
        if UserInputs.is_key_pressed[UserInputs.MOVE_DOWN]:
            UserInputs.move_direction[1] += 1
        if UserInputs.is_key_pressed[UserInputs.MOVE_UP]:
            UserInputs.move_direction[1] -= 1

    # Returns movement information for the player
    def get_movement_dir(self) -> list:
        """ Returns direction to be used in game """
        return UserInputs.move_direction

    def get_inverted_movement_dir(self):
        """ Returns Inverted directions """
        inv = [UserInputs.move_direction[0] * -
               1, UserInputs.move_direction[1] * -1]
        return inv

    # Sends methods to update in game loop:
    def send_to_update(self, delta, event):
        """ Sends the listed methods to game update. """
        self.set_key_is_down(event)
        self.move_keys_pressed()

    def send_to_late_update(self, delta):
        """ Sends the listed methods to game late update """
        self.set_last_key_state()
        self.consume_all_keys()


# Used for testing the input system:
if __name__ == "__main__":
    test = UserInputs()

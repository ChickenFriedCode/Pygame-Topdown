"""
Loads a map from an image
and places tiles for map in game.
"""

# Imports:
from gamebase import GameBase
from character import CharacterClass
from detect_col import CollisionDetection


class MapLoader:
    """ Loads a map layout made in an image. """
    # --- TODO: Need to change this to a random generation system ---
    # --- Maybe have a system that randomly gens maps to a bmp or png?

    # Make sure only a single gamebase is loaded:
    game: GameBase = None

    # TODO: Set colors for tile from tile file
    # Constant for which color is which tile.
    GROUND_COLOR = (125, 125, 125)
    WALL_COLOR = (0, 0, 0)

    # TODO: Remove hard coding of the tile files:
    # Maybe use a Json or something?
    GROUND_TILE_IMG_PATH = 'assets/purple_ground_4_64.png'
    WALL_TILE_IMG_PATH = 'assets/wall_2.png'
    TILE_SIZE = 64  # TODO make it auto get from tile files.

    def __init__(self, game: GameBase, map_img_path: str):
        """ Class initilizer """
        # so only 1 game can be used in all instances:
        if MapLoader.game is None:
            MapLoader.game = game

        # Loads map image and get colors from map:
        self.map_img = game.load_image(map_img_path)

        # Initilizte defaults based on map
        self.map_size_x = self.map_img.get_width()
        self.map_size_y = self.map_img.get_height()
        self.color_for_tiles = self.add_colors_to_list(self.map_img)
        # Create empty tile list:
        self.tile_list = []
        # Spawn the tiles:
        self.spawn_tiles()

    # set each pixel color to a list
    def add_colors_to_list(self, map_img):
        """ loop though img pixels to get tile colors for map"""

        # Normally people do left to right, top to bottom
        # But i wanted to keep X first and Y second
        # So I did Top to bottom then Left to right.
        # There is no difference in looks, and while not tested
        # Shouldn't be any difference in preformance.

        # new empty list:
        pixel_colors_all = []

        # Nested loops was faster then single loop with math:
        # Look at bottom of file for details.
        for x in range(map_img.get_width()):
            pixel_colors_y = []
            for y in range(map_img.get_height()):
                pixel_colors_y.append(map_img.get_at((x, y))[:3])
            pixel_colors_all.append(pixel_colors_y)
        return pixel_colors_all

    # Spawn the tiles to the world:
    def spawn_tiles(self):
        """ Spawns tiles to game """
        # Spawns tiles as either character classes for bg image
        # Or as colidable  objects for walls:
        tile: CharacterClass = None
        self.tile_list.clear()

        # Nested while loops was the fast of all.
        # Lool at the bottom of the file for details.
        x = -1
        y = -1
        while x < self.map_size_x - 1:
            x += 1
            y = -1  # Resets nested loop var
            while y < self.map_size_y - 1:
                y += 1

                # Sets x and y pos for the map tiles:
                x_pos = x * MapLoader.TILE_SIZE
                y_pos = y * MapLoader.TILE_SIZE

                # Grabs the color to select which tile to place:
                col = self.color_for_tiles[x][y]

                # Selects and places the tiles based on color:
                if col == self.WALL_COLOR:
                    tile = self.create_wall_tile()
                elif col == self.GROUND_COLOR:
                    tile = self.create_ground_tile()
                tile.set_position([x_pos, y_pos])
                self.tile_list.append(tile)  # Adds to tile list

    # Creates and returns the ground tile
    def create_ground_tile(self) -> CharacterClass:
        ''' Makes ground tiles from character class '''
        t = CharacterClass(self.game, self.GROUND_TILE_IMG_PATH,
                           tag=CharacterClass.TAG_WORLD)
        t.set_is_collidable(False)
        return t

    # Creates and returns the wall tiles:
    def create_wall_tile(self) -> CharacterClass:
        ''' Makes Wall Tiles from character class '''
        return CollisionDetection(self.game, self.WALL_TILE_IMG_PATH,
                                  tag=CollisionDetection.TAG_WORLD)


# Used for testing:
if __name__ == '__main__':
    pass
    # test = MapLoader(GameBase(), 'assets/map1.png')

# While it seems nested while loops are the fastest.
# Depending on the use it could be slowest.
# More testing is needed....

# ---  Test Nested Loop vs Math loop speed:
# - Result: Nested loop won by 1/3 the speed
# - Nested loop: 2.160943499999121
# - Math loop: 3.770416099985596
# import timeit
# runs = 100000

# code = '''x = 0
# y = 0
# for i in range(32):
#     y += 1
#     x = 0
#     for j in range(32):
#         x += 1
#         '''
# print(timeit.timeit(stmt=code, number=runs))
# code = '''x = 0
# y = 0
# for i in range(1024):
#     x += 1
#     if (i % 32) == 0:
#         x = 0
#         y += 1
# '''
# print(timeit.timeit(stmt=code, number=runs))


# --- Test with while loops:
# -- While loops are faster
# - Nested while loops are fastest:
# - Nested While Loop : 0.36966220001340844
# - Single While Loop : 5.744047299987869
#
# runs = 100000
# code = '''x = 0
# y = 0
# i = 0
# j = 0
# while i < 32:
#     i += 1
#     y += 1
#     x = 0
#     while j < 32:
#         j += 1
#         x += 1
#         '''
# print(timeit.timeit(stmt=code, number=runs))
# code = '''x = 0
# y = 0
# i = 0
# while i < 1024:
#     i += 1
#     x += 1
#     if (i % 32) == 0:
#         x = 0
#         y += 1
# '''
# print(timeit.timeit(stmt=code, number=runs))

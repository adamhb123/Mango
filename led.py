from pprint import pprint


# Dummy LED class
class LED:
    def __init__(self):
        self.brightness = 0

    def __repr__(self):
        return str(self.brightness)


class Display:
    def __init__(self, led_array=None):
        self.led_array = led_array if led_array is not None else [[LED() for _ in range(0, 16)] for x in range(0, 16)]
        self.size_y = len(self.led_array)
        self.size_x = len(self.led_array[0])
        #   Assertion tests:
        #   Test: array is even both vertically and horizontal
        assert self.size_y % 2 == 0 and self.size_x % 2 == 0
        for y in self.led_array:
            for led in y:
                assert isinstance(led, LED)

    def __repr__(self):
        pout = ""
        for y in range(0, self.size_y - 1):
            for x in range(0, self.size_x - 1):
                pout += f"{str(self.led_array[y][x])}  "
            pout += '\n'
        return pout

    def draw_line(self, xa, ya, xb, yb):
        """
        Draws a line by implementing Xiaolin Wu's line algorithm

        :param xa: starting point x index
        :param ya: starting point y index
        :param xb: endpoint x index
        :param yb: endpoint y index
        :return:
        """
        dx = xb - xa
        dy = yb - ya

    def draw_smile(self):
        #   Eyes
        for y in range(int((3 / 16) * self.size_y), int((9 / 16) * self.size_y)):
            x = int((5 / 16) * self.size_x)
            self.led_array[y][x - 1].brightness = 1
            self.get_led_mirror(y, x).brightness = 1

    def invert(self):
        for y in range(0, self.size_y - 1):
            for x in range(0, self.size_x - 1):
                self.led_array[y][x].brightness = 1 - self.led_array[y][x].brightness

    def get_led_mirror(self, y_index: int, x_index: int):
        return self.led_array[y_index][len(self.led_array) - 1 - x_index]


# 16x16 array

a = MangoDisplay()
a.draw_smile()
print(a)

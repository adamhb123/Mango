from pprint import pprint


# Dummy LED class
class LED:
    def __init__(self):
        self.brightness = 0

    def __repr__(self):
        return str(self.brightness)


class LEDDisplay:
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

    @staticmethod
    def _swap_point_x(point_a: tuple, point_b: tuple) -> tuple:
        return (point_b[0], point_a[1]), (point_a[0], point_b[1])

    def draw_line(self, point_a: tuple, point_b: tuple, brightness: int = 1):
        """
        Draws a solid line using Bresenham's algorithm

        :param point_a: line starting point
        :param point_b: line end point
        :param brightness: brightness to set activated leds to
        :return:
        """
        if point_a[0] > point_b[0]:
            point_a, point_b = self._swap_point_x(point_a, point_b)

        dx = point_b[0] - point_a[0]
        dy = point_b[1] - point_a[1]
        slope = dy / dx if dx != 0 else None
        print(slope)
        if slope is None:
            for y in range(point_a[1], point_b[1]):
                x = point_a[0]
                self.led_array[y][x].brightness = brightness
        elif slope == 1:
            for y in range(point_a[1], point_b[1]):
                self.led_array[y][y].brightness = brightness
        elif slope > 1:
            for y in range(point_a[1], point_b[1] + 1):
                x = round(y / slope)
                self.led_array[y][x].brightness = brightness
        elif 0 < slope < 1:
            for x in range(point_a[0], point_b[0] + 1):
                self.led_array[round(x * slope)][x].brightness = brightness
        elif slope == -1:
            for y in range(point_b[1], point_a[1]):
                x = round(y / slope) + point_b[0] - 1
                self.led_array[y][x].brightness = brightness
        elif -1 < slope < 0:
            for x in range(point_a[0], point_b[0] + 1):
                y = round(x * slope)
                self.led_array[y][x].brightness = brightness

    def draw_smile(self, brightness: int = 1):
        #   Eyes
        for y in range(int((3 / 16) * self.size_y), int((9 / 16) * self.size_y) + 1):
            x = int((5 / 16) * self.size_x)
            self.led_array[y][x - 1].brightness = brightness
            self.get_led_mirror(y, x).brightness = brightness

    def invert(self):
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                self.led_array[y][x].brightness = 1 - self.led_array[y][x].brightness

    def get_led_mirror(self, y_index: int, x_index: int):
        return self.led_array[y_index][len(self.led_array) - 1 - x_index]

    def reset(self):
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                self.led_array[y][x].brightness = 0

    def fill(self, brightness: int = 1):
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                self.led_array[y][x].brightness = brightness


def tests():
    # 16x16 array

    a = LEDDisplay()
    #   Test cases
    #   Slope of 1
    print("Slope of 1:")
    a.draw_line((0, 0), (5, 5))
    print(a)
    a.reset()
    #   Slope of -1
    print("Slope of -1:")
    a.draw_line((1, 5), (6, 0))
    print(a)
    a.reset()
    #   0 < slope < 1
    print("0 < Slope < 1: ")
    a.draw_line((0, 0), (5, 3))
    print(a)
    a.reset()
    #   -1 < slope < 0
    print("-1 < Slope < 0: ")
    a.draw_line((1, 5), (6, 1))
    print(a)
    a.reset()


if __name__ == "__main__":
    tests()

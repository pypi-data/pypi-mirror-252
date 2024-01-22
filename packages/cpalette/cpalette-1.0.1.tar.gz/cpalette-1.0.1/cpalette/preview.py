from PIL import Image
from scripts.colors import *


class Previewer:

    @staticmethod
    def preview(color: HEX | RGB) -> None:
        Image.new("RGB", (500, 500), color.color).show()
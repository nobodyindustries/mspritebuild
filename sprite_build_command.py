import PIL
from cleo import Command
from os.path import exists
from PIL import Image


class SpriteBuildCommand(Command):
    """
    Converts a BMP file to a MEngine Sprite file (MDT)

    mdt:build
        {file : file to process}
        {tcolor : transparent color in hexadecimal with '0x' prefix, ex. 0xAABBCC}
        {output : file to output to}
    """

    def handle(self):

        input_file = self.argument('file')
        if not exists(input_file):
            self.line(f'<error>Input file does not exist ({input_file})</error>')
            return

        try:
            tcolor = int(self.argument('tcolor'), 0)
        except ValueError:
            self.line(f'<error>Invalid value for transparent color ({self.argument("tcolor")})</error>')

        try:
            image_in = Image.open(input_file).convert('RGB')
        except FileNotFoundError:
            self.line(f'<error>Input file does not exist ({input_file})</error>')
            return
        except PIL.UnidentifiedImageError:
            self.line('<error>Input file can not be opened</error>')
            return

        output_file = self.argument('output')
        try:
            with open(output_file, 'wb') as image_out:
                # Write marker
                image_out.write(bytearray([0x00, 0x4D, 0x44, 0x54]))
                # Version
                image_out.write(bytearray([0x00, 0x00, 0x00, 0x01]))
                # Dimensions
                width, height = image_in.size
                image_out.write(width.to_bytes(4, 'big'))
                image_out.write(height.to_bytes(4, 'big'))
                # Transparent color
                image_out.write(tcolor.to_bytes(4, 'big'))
                # Pixel data
                pixels = image_in.load()
                for y in range(height):
                    for x in range(width):
                        r, g, b = pixels[x, y]
                        image_out.write(bytearray([0x00]))
                        image_out.write(r.to_bytes(1, 'big'))
                        image_out.write(g.to_bytes(1, 'big'))
                        image_out.write(b.to_bytes(1, 'big'))
        except OverflowError:
            self.line('<error>Image is too wide, too high or transparent color is invalid</error>')
            return
        except IOError:
            self.line('<error>Output file can not be opened</error>')
            return

        image_in.close()


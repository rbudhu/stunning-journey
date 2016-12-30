import sys
import math
from PIL import Image, ImageFont, ImageDraw


class Tenso(object):
    def __init__(self, im, box, w = 350, num_panels = 4,
                 text='TENSO', text_pos='top', font_path='impact.ttf'):
        self.im = im
        self.box = box
        self.w = w
        self.num_panels = num_panels
        self.text = text
        self.text_pos = text_pos
        self.font_path = font_path

    def resize(self, im):
        scale = float(self.w) / float(im.width)
        h = int(im.height * scale)
        return im.resize((self.w, h))

    def generate(self):
        # First scale the image to self.w pixels wide
        # maintaining aspect ratio
        first = self.resize(self.im)
        # Make every other panel this height
        h = first.height

        # Create the last image that is self.w wide and whatever height
        last = self.im.crop(self.box)
        last = self.resize(last)

        # Create the final image
        tenso = Image.new('RGB', (self.w, h * (self.num_panels - 2) + 
                                  first.height + last.height))

        # Paste first image
        tenso.paste(first, (0, 0))
        
        # Where to paste the new images
        y = first.height

        # Compute the scale factor
        w = self.box[2] - self.box[0]
        scale = math.ceil(self.w / w) / (self.num_panels + 2)

        # The magic number 2 is used because we've already
        # manually generated 2 panels: the first and the last ones

        for panel in range(self.num_panels - 2):
            z = scale * (panel + 2)
            zoom = self.im.resize((int(self.im.width * z),
                                   int(self.im.height * z)))
            # Center of zoomed image
            zc = zoom.width / 2
            # Scale the input box
            box = [x * z for x in self.box]
            # Get center of box
            cxr, cyr = int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)
            # Create a self.w x self.w crop region
            box = [cxr - self.w / 2, cyr - h / 2,
                    cxr + self.w / 2, cyr + h / 2]
            # Make sure we don't go outside image bounds
            if box[0] < 0:
                box[2] = self.w
                box[0] = 0
            if box[1] < 0:
                box[3] = h
                box[1] = 0
            if box[2] > zoom.width:
                box[0] = zoom.width - self.w
                box[2] = zoom.width
            if box[3] > zoom.height:
                box[1] = zoom.height - h
                box[3] = zoom.height
            # Crop the image
            zoom = zoom.crop(box)
            tenso.paste(zoom, (0, y))
            y = y + zoom.height
        
        # Paste the final image
        tenso.paste(last, (0, y))

        # Do texty stuff
        if self.text is not None:
            draw = ImageDraw.Draw(tenso)
            font = ImageFont.truetype(self.font_path, 48)
            fw, fh = font.getsize(self.text)
            tx = (self.w - fw) / 2
            ty = y + 10
            if self.text_pos == 'bottom':
                ty = tenso.height - fh - 10
            draw.text((tx, ty), self.text, font=font)
        return tenso

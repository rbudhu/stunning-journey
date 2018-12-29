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

    def generate(self):
        # First compute the maximum height for each panel
        h = int(self.im.height * (float(self.w) / float(self.im.width)))
        # In order to get the original crop box width to span self.w pixels,
        # we have to compute the crop box scaling factor
        cbsf = self.w / (self.box[2] - self.box[0])
        # We multiply the original image by the crop box scaling factor
        # such that the crop box and the pixels within it will fill up
        # a self.w panel
        self.im = self.im.resize((int(self.im.width * cbsf),
                                  int(self.im.height * cbsf)))
        # We have to compute the new crop box dimensions based on
        # the new image size
        self.box = [i * cbsf for i in self.box]

        # Create the final image
        tenso = Image.new('RGB', (self.w, h * self.num_panels + 1))

        # Where to paste the new images
        y = 0

        # Now we figure out the scale factor necessary to shrink (or grow)
        # the resized image to the width of a panel
        scale = self.w / self.im.width
        # And then figure out what scale factor we need to apply such that
        # we scale each image in a panel by a fixed factor
        scale = scale ** (1 / (self.num_panels - 1))
        for panel in range(self.num_panels - 1, -1, -1):
            z = round(math.pow(scale, panel), 8)
            zoom = self.im.resize((int(self.im.width * z),
                                   int(self.im.height * z)),
                                  Image.ANTIALIAS)
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
        
        # Do texty stuff
        if self.text is not None:
            draw = ImageDraw.Draw(tenso)
            font_size = 48
            if len(self.text) > 10:
                font_size = 24
            font = ImageFont.truetype(self.font_path, font_size)
            fw, fh = font.getsize(self.text)
            tx = (self.w - fw) / 2
            ty = y - h + 10
            if self.text_pos == 'bottom':
                ty = tenso.height - fh - 10
            draw.text((tx, ty), self.text, font=font)
        return tenso

    def generate_gif(self):
        # First compute the maximum height for each panel
        h = int(self.im.height * (float(self.w) / float(self.im.width)))
        # In order to get the original crop box width to span self.w pixels,
        # we have to compute the crop box scaling factor
        cbsf = self.w / (self.box[2] - self.box[0])
        # We multiply the original image by the crop box scaling factor
        # such that the crop box and the pixels within it will fill up
        # a self.w panel
        self.im = self.im.resize((int(self.im.width * cbsf),
                                  int(self.im.height * cbsf)))
        # We have to compute the new crop box dimensions based on
        # the new image size
        self.box = [i * cbsf for i in self.box]

        # Frame holder
        frames = []

        # Now we figure out the scale factor necessary to shrink (or grow)
        # the resized image to the width of a panel
        scale = self.w / self.im.width
        # And then figure out what scale factor we need to apply such that
        # we scale each image in a panel by a fixed factor
        scale = scale ** (1 / (self.num_panels - 1))
        for panel in range(self.num_panels - 1, -1, -1):
            z = round(math.pow(scale, panel), 8)
            zoom = self.im.resize((int(self.im.width * z),
                                   int(self.im.height * z)),
                                  Image.ANTIALIAS)
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

            # Add any text to the last panel
            if self.text is not None and panel == 0:
                draw = ImageDraw.Draw(zoom)
                font_size = 48
                if len(self.text) > 10:
                    font_size = 24
                font = ImageFont.truetype(self.font_path, font_size)
                fw, fh = font.getsize(self.text)
                tx = (self.w - fw) / 2
                ty = 10
                if self.text_pos == 'bottom':
                    ty = h - fh - 10
                draw.text((tx, ty), self.text, font=font)

            frames.append(zoom)

        return frames

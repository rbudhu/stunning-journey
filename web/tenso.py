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
        return scale, im.resize((self.w, h))

    def generate(self):
        # This is the last image
        print('Original image dims:')
        print(self.im.width, self.im.height)
        # Make the image a multiple of self.w
        new_width = math.ceil(self.im.width/self.w) * self.w
        scale = float(new_width) / float(self.im.width)
        new_height = int(scale * self.im.height)
        # Overwrite the original image with the resized image
        self.im = self.im.resize((new_width, new_height))
        print('New image dims:' )
        print(self.im.width, self.im.height)

        # Scale the crop box to match the new image dims
        self.box = [i * scale for i in self.box]
        last = self.im.crop(self.box)
        print('Original box dims: ')
        print(self.box[2] - self.box[0], self.box[3] - self.box[1])
        last_scale, last = self.resize(last)
        print('New box dims: ')
        print(last.width, last.height)
        first_scale, first = self.resize(self.im)
        final_scale = last.width / (self.box[2] - self.box[0])
        print('Scale factor: {}'.format(final_scale))
        
        h = first.height
        
        # Create the final image
        tenso_height = (first.height if first.height > last.height else
                        last.height)
        tenso = Image.new('RGB', (self.w, tenso_height * self.num_panels))

        # Paste first image
        tenso.paste(first, (0, 0))

        # Where to paste the new images
        y = first.height

        zoo = final_scale / (self.num_panels)
        
        for panel in range(1, self.num_panels):
            z = zoo * panel
            print(z)
            zoom = self.im.resize((int(self.im.width * z),
                                   int(self.im.height * z)),
                                  Image.ANTIALIAS)
            if zoom.height < last.height:
                pppp = last.height / zoom.height
                zoom = zoom.resize((int(zoom.width * pppp), last.height),
                                   Image.ANTIALIAS)
            if zoom.width < last.width:
                pppp = last.width / zoom.width
                zoom = zoom.resize((last.width, int(zoom.height * pppp)),
                                    Image.ANTIALIAS)
            print(zoom.width, zoom.height)
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

        # tenso.paste(last, (0, y))
        print(tenso.height)
        print(y)
        tenso = tenso.crop([0, 0, tenso.width, y])
        '''
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
        '''
        return tenso


    def generate_gif(self):
        # First scale the image to self.w pixels wide
        # maintaining aspect ratio
        scale, first = self.resize(self.im)
        # Make every other panel this height
        h = first.height

        # Store the frames
        frames = [first]
        
        # Compute the scale factor
        self.box = [i * scale for i in self.box]
        w = (self.box[2] - self.box[0])
        final_scale = self.w / w
        scale = math.pow(final_scale, 1.0 / (self.num_panels - 1))

        for panel in range(1, self.num_panels):
            z = math.pow(scale, panel)
            # If we're not zooming IN, just set the zoom factor
            # to the final_scale to match the last panel
            if z < 1.0:
                z = final_scale
            zoom = first.resize((int(first.width * z),
                                 int(first.height * z)),
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
            if self.text is not None and panel == self.num_panels - 1:
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


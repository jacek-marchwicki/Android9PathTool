import Image
import math


class ImageResizer:
  def create_scaled_icon(self):
    width,height = self.image.size
    left = 1
    upper = 1
    right = width - 1
    lower = height - 1

    icon = self.image.crop((left,upper,right,lower))
    #icon.save("icon.png")

    scaled_icon_size = [(int)(math.floor(self.scale_factor * x)) for x in icon.size]
    self.scaled_icon = icon.resize(scaled_icon_size, Image.BILINEAR)
    #self.scaled_icon.save("scaled.png")

  def create_left_margin(self):
    width,height = self.image.size
    left_margin = self.image.crop((0,0,1,height))
    
    scaled_height = (int)(math.floor(height * self.scale_factor))
    scaled_left_margin_size = (1, scaled_height)
    self.scaled_left_margin = left_margin.resize(scaled_left_margin_size, Image.NEAREST)
    #self.scaled_left_margin.save("left_margin.png")

  def create_right_margin(self):
    height,width = self.image.size
    right_margin = self.image.crop((width-1,0,width,height))
    
    scaled_height = (int)(math.floor(height * self.scale_factor))
    scaled_right_margin_size = (1, scaled_height)

    self.scaled_right_margin = right_margin.resize(scaled_right_margin_size, Image.NEAREST)
    #self.scaled_right_margin.save("right_margin.png")

  def create_top_margin(self):
    height,width = self.image.size
    top_margin = self.image.crop((0,0,width,1))
    
    scaled_width = (int)(math.floor(width * self.scale_factor))
    scaled_top_margin_size = (scaled_width, 1)

    self.scaled_top_margin = top_margin.resize(scaled_top_margin_size, Image.NEAREST)
    #self.scaled_top_margin.save("top_margin.png")

  def create_bottom_margin(self):
    height,width = self.image.size
    bottom_margin = self.image.crop((0,height-1,width,height))
    
    scaled_width = (int)(math.floor(width * self.scale_factor))
    scaled_bottom_margin_size = (scaled_width, 1)

    self.scaled_bottom_margin = bottom_margin.resize(scaled_bottom_margin_size, Image.NEAREST)
    #self.scaled_bottom_margin.save("bottom_margin.png")

  def create_final_image(self):
    final_size = [x + 2 for x in self.scaled_icon.size]

    width,height = self.image.size
    final_width,final_height = final_size

    self.final_image = Image.new(self.image.mode, final_size, None)

    self.final_image.paste(self.scaled_left_margin, (0,0))
    self.final_image.paste(self.scaled_right_margin, (final_width-1,0))
    self.final_image.paste(self.scaled_top_margin, (0, 0))
    self.final_image.paste(self.scaled_bottom_margin, (0, final_height-1))
    self.final_image.paste(self.scaled_icon, (1,1))

  def scale(self, src_file, dst_file, scale_factor):
    self.scale_factor = scale_factor
    self.image = Image.open(src_file)
    self.create_scaled_icon()
    self.create_left_margin()
    self.create_right_margin()
    self.create_top_margin()
    self.create_bottom_margin()
    self.create_final_image()
    self.final_image.save(dst_file)

if __name__ == "__main__":
  image_resizer = ImageResizer()
  image_resizer.scale("example.9.png", "new.9.png", 0.5)

import Image
import math
import sys
from optparse import OptionParser
import os
import os.path

class ImageResizer:

  def scale(self, src_file, dst_file, scale_factor):
    image = Image.open(src_file)

    scaled_icon_size = [(int)(math.floor(scale_factor * x)) for x in image.size]

    scaled_image = image.resize(scaled_icon_size, Image.BILINEAR)
    scaled_image.save(dst_file)

class Image9Resizer:
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
    
    scaled_left_margin_size = (1, self.final_height)

    self.scaled_left_margin = left_margin.resize(scaled_left_margin_size, Image.NEAREST)
    #self.scaled_left_margin.save("left_margin.png")

  def create_right_margin(self):
    width,height = self.image.size
    right_margin = self.image.crop((width-1,0,width,height))
    
    scaled_right_margin_size = (1, self.final_height)

    self.scaled_right_margin = right_margin.resize(scaled_right_margin_size, Image.NEAREST)
    self.scaled_right_margin.save("right_margin.png")

  def create_top_margin(self):
    width,height = self.image.size
    top_margin = self.image.crop((0,0,width,1))
    
    scaled_top_margin_size = (self.final_width, 1)

    self.scaled_top_margin = top_margin.resize(scaled_top_margin_size, Image.NEAREST)
    #self.scaled_top_margin.save("top_margin.png")

  def create_bottom_margin(self):
    width,height = self.image.size
    bottom_margin = self.image.crop((0,height-1,width,height))
    
    scaled_bottom_margin_size = (self.final_width, 1)

    self.scaled_bottom_margin = bottom_margin.resize(scaled_bottom_margin_size, Image.NEAREST)
    #self.scaled_bottom_margin.save("bottom_margin.png")

  def create_final_image(self):

    width,height = self.image.size

    self.final_image = Image.new(self.image.mode, self.final_size, None)

    self.final_image.paste(self.scaled_left_margin, (0,0))
    self.final_image.paste(self.scaled_right_margin, (self.final_width-1,0))
    self.final_image.paste(self.scaled_top_margin, (0, 0))
    self.final_image.paste(self.scaled_bottom_margin, (0, self.final_height-1))
    self.final_image.paste(self.scaled_icon, (1,1))

  def scale(self, src_file, dst_file, scale_factor):
    self.scale_factor = scale_factor
    self.image = Image.open(src_file)
    self.create_scaled_icon()

    self.final_size = [x + 2 for x in self.scaled_icon.size]
    self.final_width,self.final_height = self.final_size

    self.create_left_margin()
    self.create_right_margin()
    self.create_top_margin()
    self.create_bottom_margin()
    self.create_final_image()
    self.final_image.save(dst_file)

resolutions = ["ldpi", "mdpi", "hdpi", "xhdpi"]
resolutions_values = [120.0, 160.0, 240.0, 320.0]

class ImageFinder:
  def __init__(self):
    self.image_9_resizer = Image9Resizer()
    self.image_resizer = ImageResizer()

  def find(self, file_path):
    print "Processing file: %s" % file_path
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    last_dir_path = os.path.basename(file_dir)
    rest_dir = os.path.dirname(file_dir)
    parts = last_dir_path.split("-")
    if parts[0] != "drawable":
      raise ValueError("there are no \"drawable\" in parent directory")
    found = -1
    for i in range(len(parts)):
      value = parts[i]
      if value in resolutions:
        found = i
    if found < 0:
      raise ValueError("there are no resolution specyffic value (ldpi, mdpi, hdpi, xhdpi) in directory")
    resolution_index = resolutions.index(parts[found])
    resolution_value = resolutions_values[resolution_index]

    for i in range(len(resolutions_values)):
      dest_resolution_value = resolutions_values[i]
      dest_resolution = resolutions[i]
      if dest_resolution_value == resolution_value:
        continue
      new_parts = parts[:found] + [dest_resolution] + parts[found+1:]
      directory = "-".join(new_parts)
      new_file_path = os.path.join(rest_dir, directory, file_name)
      scale_factor = dest_resolution_value / resolution_value
      self.process(file_path, new_file_path, scale_factor)

  def process(self, file_path, new_file_path, scale_factor):
    file_exist = os.path.exists(new_file_path)
    if file_exist:
      print " destination file exists %s" % new_file_path
      return
    print " Creating file: %s (scale factor: %f)" % (new_file_path, scale_factor)

    directory = os.path.dirname(new_file_path)
    if not os.path.exists(directory):
      print " directory: %s does not exists, creating it" % directory
      os.makedirs(directory)

    file_exts = file_path.split(".")
    nine_path_indicator = file_exts[-2]
    is_nine_path = nine_path_indicator == "9"
    if is_nine_path:
      self.image_9_resizer.scale(file_path, new_file_path, scale_factor)
    else:
      self.image_resizer.scale(file_path, new_file_path, scale_factor)
    print " Image created"



        

if __name__ == "__main__":
  parser = OptionParser()
  (options, args) = parser.parse_args()

  image_finder = ImageFinder()
  for file in args:
    image_finder.find(file)

from config import Full, Small

"""
Artist is a class that allows us to override the drawing logic more easily and by just specifying a new draw function
to any child class, as well as overriding the svg XML tag template with custom strings,
without having to change the entire structure of draw code.
"""
class Artist:
  def __init__(self, sample_list, config)
    self.sample_list = sample_list
    self.align = config.align
    self.config = config
    self.height = config.height
    self.width = config.step_width
    self.elements = None
  
  """
  The default artist's svg template which rounds up the creation of drawing
  """
  def template(self):
    return f'<svg baseProfile="tiny" height="100%" preserveAspectRatio="none" version="1.2" viewBox="0 0 {self.width} {self.height}" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs/>{self.elements}</svg>'

  """
  The default artist's draw function. Creates a simple bar waveform, nothing too complicated
  """
  def draw(self):  
    """bottom position bar helper function to calculate size and position"""
    def bottom(sample, i, c):
      pos = (i * (c.width),  (1 - sample) * c.height)
      size = (c.width - c.gap, sample * c.height)
      return Position(pos[0], pos[1]), Size(size[0], size[1])
    """center position bar helper function to calculate size and position"""
    def center(sample, i, c):
      pos =  (i * (c.width), (0.5 * c.height) - (0.5 * sample * c.height))
      size = (c.width - c.gap, sample * c.height)
      return Position(pos[0], pos[1]), Size(size[0], size[1])
    def per_sample(s, i, align_callable, config):
      pos, size = align_callable(s, i, config)
      return f'<rect width="{size.w}" height="{size.w}" x="{pos.x}" y="{pos.y}" rx="{config.rounded}" ry="{config.rounded}" fill="{config.color}" />'

    if self.align == "bottom":
      align_callable = bottom
    elif self.align == "center":
      align_callable = center
    else:
      Logger.warn("Missing alignment, using 'center' alignment as default")
      align_callable = center
    self.elements = ""
    for s,i in enumerate(self.sample_list):
      elements += per_sample(s, i, align_callable, self.config)
    return self
  
  """
  To be called to finish the drawing, after draw is finished, to print the loose svg string into a
  conforming svg XML tag.
  Note that both self.template and self.draw can be overriden by child classes, hence they both can deviate
  from the default draw function (and template, respectively), but this function serves as the common basis
  all children to call in order to finish the drawing
  """
  def to_string(self):
    return self.draw().template()

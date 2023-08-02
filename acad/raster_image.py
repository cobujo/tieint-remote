from dataclasses import dataclass
from acad.entity import AcadEntity


@dataclass
class AcadRasterImage(AcadEntity):
    """
    autoscript generated USING ACDBWIPEOUT AS OBJECT (CHILD TO RASTERIMAGE)
    """

    @property
    def brightness(self):
        return self.obj.Brightness

    @property
    def clipping_enabled(self):
        return self.obj.ClippingEnabled

    @property
    def contrast(self):
        return self.obj.Contrast

    @property
    def fade(self):
        return self.obj.Fade

    @property
    def height(self):
        return self.obj.Height

    @property
    def image_file(self):
        return self.obj.ImageFile

    @property
    def image_height(self):
        return self.obj.ImageHeight

    @property
    def image_visibility(self):
        return self.obj.ImageVisibility

    @property
    def image_width(self):
        return self.obj.ImageWidth

    # Name prop in docs but throwing exception, key not found?
    @property
    def name(self):
        return self.obj.Name

    @property
    def origin(self):
        return self.obj.Origin

    @property
    def rotation(self):
        return self.obj.Rotation

    @property
    def scale_factor(self):
        return self.obj.ScaleFactor

    @property
    def show_rotation(self):
        return self.obj.ShowRotation

    @property
    def transparency(self):
        return self.obj.Transparency

    @property
    def width(self):
        return self.obj.Width

    def clip_boundary(self, points_array):
        return self.obj.ClipBoundary(PointsArray=points_array)

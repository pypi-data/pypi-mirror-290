﻿from aspose.words.drawing import charts
from aspose.words.drawing import ole
import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List
from enum import Enum

class Adjustment:
    """Represents adjustment values that are applied to the specified shape."""
    
    @property
    def name(self) -> str:
        """Gets the name of the adjustment."""
        ...
    
    @property
    def value(self) -> int:
        """Gets or sets the raw value of the adjustment.
        
        An adjust value is simply a guide that has a value based formula specified.
        That is, no calculation takes place for an adjust value guide.
        Instead, this guide specifies a parameter value that is used for calculations within the shape guides."""
        ...
    
    @value.setter
    def value(self, value: int):
        ...
    
    ...

class AdjustmentCollection:
    """Represents a read-only collection of :class:`Adjustment` adjust values that are applied to the specified shape."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.Adjustment:
        """Returns an adjustment at the specified index.
        
        :param index: An index into the collection."""
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of elements contained in the collection."""
        ...
    
    ...

class Fill:
    """Represents fill formatting for an object.
    To learn more, visit the `Working with Graphic Elements <https://docs.aspose.com/words/python-net/working-with-graphic-elements/>` documentation article.
    
    Use the :attr:`ShapeBase.fill` or :attr:`aspose.words.Font.fill` property to access fill properties of an object.
    You do not create instances of the :class:`Fill` class directly."""
    
    @overload
    def solid(self) -> None:
        """Sets the fill to a uniform color.
        
        Use this method to convert any of the fills back to solid fill."""
        ...
    
    @overload
    def solid(self, color: aspose.pydrawing.Color) -> None:
        """Sets the fill to a specified uniform color.
        
        Use this method to convert any of the fills back to solid fill."""
        ...
    
    @overload
    def patterned(self, pattern_type: aspose.words.drawing.PatternType) -> None:
        """Sets the specified fill to a pattern.
        
        :param pattern_type: :class:`PatternType`"""
        ...
    
    @overload
    def patterned(self, pattern_type: aspose.words.drawing.PatternType, fore_color: aspose.pydrawing.Color, back_color: aspose.pydrawing.Color) -> None:
        """Sets the specified fill to a pattern.
        
        :param pattern_type: :class:`PatternType`
        :param fore_color: The color of the foreground fill.
        :param back_color: The color of the background fill."""
        ...
    
    @overload
    def one_color_gradient(self, style: aspose.words.drawing.GradientStyle, variant: aspose.words.drawing.GradientVariant, degree: float) -> None:
        """Sets the specified fill to a one-color gradient.
        
        :param style: The gradient style :class:`GradientStyle`
        :param variant: The gradient variant :class:`GradientVariant`
        :param degree: The gradient degree. Can be a value from 0.0 (dark) to 1.0 (light)."""
        ...
    
    @overload
    def one_color_gradient(self, color: aspose.pydrawing.Color, style: aspose.words.drawing.GradientStyle, variant: aspose.words.drawing.GradientVariant, degree: float) -> None:
        """Sets the specified fill to a one-color gradient using the specified color.
        
        :param color: The color to build the gradient.
        :param style: The gradient style :class:`GradientStyle`
        :param variant: The gradient variant :class:`GradientVariant`
        :param degree: The gradient degree. Can be a value from 0.0 (dark) to 1.0 (light)."""
        ...
    
    @overload
    def two_color_gradient(self, style: aspose.words.drawing.GradientStyle, variant: aspose.words.drawing.GradientVariant) -> None:
        """Sets the specified fill to a two-color gradient.
        
        :param style: The gradient style :class:`GradientStyle`.
        :param variant: The gradient variant :class:`GradientVariant`"""
        ...
    
    @overload
    def two_color_gradient(self, color1: aspose.pydrawing.Color, color2: aspose.pydrawing.Color, style: aspose.words.drawing.GradientStyle, variant: aspose.words.drawing.GradientVariant) -> None:
        """Sets the specified fill to a two-color gradient.
        
        :param color1: The first color to build the gradient.
        :param color2: The second color to build the gradient.
        :param style: The gradient style :class:`GradientStyle`.
        :param variant: The gradient variant :class:`GradientVariant`"""
        ...
    
    @overload
    def set_image(self, file_name: str) -> None:
        """Changes the fill type to single image.
        
        :param file_name: The path to the image file."""
        ...
    
    @overload
    def set_image(self, stream: io.BytesIO) -> None:
        """Changes the fill type to single image.
        
        :param stream: The stream that contains the image bytes."""
        ...
    
    @overload
    def set_image(self, image_bytes: bytes) -> None:
        """Changes the fill type to single image.
        
        :param image_bytes: The image bytes array."""
        ...
    
    def preset_textured(self, preset_texture: aspose.words.drawing.PresetTexture) -> None:
        """Sets the fill to a preset texture.
        
        :param preset_texture: :class:`PresetTexture`"""
        ...
    
    @property
    def preset_texture(self) -> aspose.words.drawing.PresetTexture:
        """Gets a :class:`PresetTexture` for the fill."""
        ...
    
    @property
    def pattern(self) -> aspose.words.drawing.PatternType:
        """Gets a :class:`PatternType` for the fill."""
        ...
    
    @property
    def texture_alignment(self) -> aspose.words.drawing.TextureAlignment:
        """Gets or sets the alignment for tile texture fill."""
        ...
    
    @texture_alignment.setter
    def texture_alignment(self, value: aspose.words.drawing.TextureAlignment):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Gets or sets a Color object that represents the foreground color for the fill.
        
        This property preserves the alpha component of the aspose.pydrawing.Color,
        unlike the :attr:`Fill.fore_color` property, which resets it to fully opaque color."""
        ...
    
    @color.setter
    def color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def opacity(self) -> float:
        """Gets or sets the degree of opacity of the specified fill as a value between 0.0 (clear) and 1.0 (opaque).
        
        This property is the opposite of property :attr:`Fill.transparency`."""
        ...
    
    @opacity.setter
    def opacity(self, value: float):
        ...
    
    @property
    def image_bytes(self) -> bytes:
        """Gets the raw bytes of the fill texture or pattern.
        
        The default value is ``None``."""
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        """Gets or sets a Color object that represents the foreground color for the fill.
        
        This property resets the alpha component of the aspose.pydrawing.Color
        to fully opaque color unlike the :attr:`Fill.color` property, which preserves it."""
        ...
    
    @fore_color.setter
    def fore_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def base_fore_color(self) -> aspose.pydrawing.Color:
        """Gets a Color object that represents the base foreground color for the fill
        without any modifiers."""
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        """Gets or sets a Color object that represents the background color for the fill."""
        ...
    
    @back_color.setter
    def back_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def fore_theme_color(self) -> aspose.words.themes.ThemeColor:
        """Gets or sets a ThemeColor object that represents the foreground color for the fill."""
        ...
    
    @fore_theme_color.setter
    def fore_theme_color(self, value: aspose.words.themes.ThemeColor):
        ...
    
    @property
    def back_theme_color(self) -> aspose.words.themes.ThemeColor:
        """Gets or sets a ThemeColor object that represents the background color for the fill."""
        ...
    
    @back_theme_color.setter
    def back_theme_color(self, value: aspose.words.themes.ThemeColor):
        ...
    
    @property
    def fore_tint_and_shade(self) -> float:
        """Gets or sets a double value that lightens or darkens the foreground color.
        
        The allowed values are in the range from -1 (the darkest) to 1 (the lightest) for this property.
        
        Zero (0) is neutral.
        
        :raises RuntimeError (Proxy error(ArgumentOutOfRangeException)): Throw if set this property to a value less than -1 or more than 1."""
        ...
    
    @fore_tint_and_shade.setter
    def fore_tint_and_shade(self, value: float):
        ...
    
    @property
    def back_tint_and_shade(self) -> float:
        """Gets or sets a double value that lightens or darkens the background color.
        
        The allowed values are in the range from -1 (the darkest) to 1 (the lightest) for this property.
        
        Zero (0) is neutral.
        
        :raises RuntimeError (Proxy error(ArgumentOutOfRangeException)): Throw if set this property to a value less than -1 or more than 1."""
        ...
    
    @back_tint_and_shade.setter
    def back_tint_and_shade(self, value: float):
        ...
    
    @property
    def visible(self) -> bool:
        """Gets or sets value that is ``True`` if the formatting applied to this instance, is visible."""
        ...
    
    @visible.setter
    def visible(self, value: bool):
        ...
    
    @property
    def transparency(self) -> float:
        """Gets or sets the degree of transparency of the specified fill as a value between 0.0 (opaque) and 1.0 (clear).
        
        This property is the opposite of property :attr:`Fill.opacity`."""
        ...
    
    @transparency.setter
    def transparency(self, value: float):
        ...
    
    @property
    def rotate_with_object(self) -> bool:
        """Gets or sets whether the fill rotates with the specified object."""
        ...
    
    @rotate_with_object.setter
    def rotate_with_object(self, value: bool):
        ...
    
    @property
    def fill_type(self) -> aspose.words.drawing.FillType:
        """Gets a fill type."""
        ...
    
    @property
    def gradient_angle(self) -> float:
        """Gets or sets the angle of the gradient fill."""
        ...
    
    @gradient_angle.setter
    def gradient_angle(self, value: float):
        ...
    
    @property
    def gradient_variant(self) -> aspose.words.drawing.GradientVariant:
        """Gets the gradient variant :class:`GradientVariant` for the fill."""
        ...
    
    @property
    def gradient_style(self) -> aspose.words.drawing.GradientStyle:
        """Gets the gradient style :class:`GradientStyle` for the fill."""
        ...
    
    @property
    def gradient_stops(self) -> aspose.words.drawing.GradientStopCollection:
        """Gets a collection of :class:`GradientStop` objects for the fill."""
        ...
    
    ...

class GlowFormat:
    """Represents the glow formatting for an object.
    
    Use the :attr:`ShapeBase.glow` property to access glow properties of an object.
    You do not create instances of the :class:`GlowFormat` class directly."""
    
    def remove(self) -> None:
        """Removes :class:`GlowFormat` from the parent object."""
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Gets or sets a aspose.pydrawing.Color object that represents the color for a glow effect.
        The default value is aspose.pydrawing.Color.black."""
        ...
    
    @color.setter
    def color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def transparency(self) -> float:
        """Gets or sets the degree of transparency for the glow effect as a value between 0.0 (opaque) and 1.0 (clear).
        The default value is 0.0."""
        ...
    
    @transparency.setter
    def transparency(self, value: float):
        ...
    
    @property
    def radius(self) -> float:
        """Gets or sets a double value that represents the length of the radius for a glow effect in points (pt).
        The default value is 0.0."""
        ...
    
    @radius.setter
    def radius(self, value: float):
        ...
    
    ...

class GradientStop:
    """Represents one gradient stop.
    To learn more, visit the `Working with Graphic Elements <https://docs.aspose.com/words/python-net/working-with-graphic-elements/>` documentation article."""
    
    @overload
    def __init__(self, color: aspose.pydrawing.Color, position: float):
        """Initializes a new instance of the :class:`GradientStop` class.
        
        :param color: Represents the color of the gradient stop.
        :param position: Represents the position of a stop within
                         the gradient expressed as a percent in range 0.0 to 1.0."""
        ...
    
    @overload
    def __init__(self, color: aspose.pydrawing.Color, position: float, transparency: float):
        """Initializes a new instance of the :class:`GradientStop` class.
        
        :param color: Represents the color of the gradient stop.
        :param position: Represents the position of a stop within
                         the gradient expressed as a percent in range 0.0 to 1.0.
        :param transparency: Represents the transparency of a stop within
                             the gradient expressed as a percent in range 0.0 to 1.0."""
        ...
    
    def remove(self) -> None:
        """Removes the gradient stop from the parent :class:`GradientStopCollection`."""
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Gets or sets a value representing the color of the gradient stop."""
        ...
    
    @color.setter
    def color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def base_color(self) -> aspose.pydrawing.Color:
        """Gets a value representing the color of the gradient stop without any modifiers."""
        ...
    
    @property
    def position(self) -> float:
        """Gets or sets a value representing the position of a stop within the gradient
        expressed as a percent in range 0.0 to 1.0."""
        ...
    
    @position.setter
    def position(self, value: float):
        ...
    
    @property
    def transparency(self) -> float:
        """Gets or sets a value representing the transparency of the gradient fill
        expressed as a percent in range 0.0 to 1.0."""
        ...
    
    @transparency.setter
    def transparency(self, value: float):
        ...
    
    ...

class GradientStopCollection:
    """Contains a collection of :class:`GradientStop` objects.
    To learn more, visit the `Working with Graphic Elements <https://docs.aspose.com/words/python-net/working-with-graphic-elements/>` documentation article.
    
    You do not create instances of this class directly.
    Use the :attr:`Fill.gradient_stops` property to access gradient stops of fill objects."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.GradientStop:
        """Gets or sets a :class:`GradientStop` object in the collection."""
        ...
    
    def __setitem__(self, index: int, value: aspose.words.drawing.GradientStop):
        ...
    
    def insert(self, index: int, gradient_stop: aspose.words.drawing.GradientStop) -> aspose.words.drawing.GradientStop:
        """Inserts a :class:`GradientStop` to the collection at a specified index."""
        ...
    
    def add(self, gradient_stop: aspose.words.drawing.GradientStop) -> aspose.words.drawing.GradientStop:
        """Adds a specified :class:`GradientStop` to a gradient."""
        ...
    
    def remove_at(self, index: int) -> aspose.words.drawing.GradientStop:
        """Removes a :class:`GradientStop` from the collection at a specified index.
        
        :returns: Removed :class:`GradientStop`."""
        ...
    
    def remove(self, gradient_stop: aspose.words.drawing.GradientStop) -> bool:
        """Removes a specified :class:`GradientStop` from the collection.
        
        :returns: ``True`` if gradient stop was successfully removed, otherwise ``False``."""
        ...
    
    @property
    def count(self) -> int:
        """Gets an integer value indicating the number of items in the collection."""
        ...
    
    ...

class GroupShape(aspose.words.drawing.ShapeBase):
    """Represents a group of shapes in a document.
    To learn more, visit the `How to Add Group Shape into a Word Document <https://docs.aspose.com/words/python-net/how-to-add-group-shape-into-a-word-document/>` documentation article.
    
    A :class:`GroupShape` is a composite node and can have :class:`Shape` and
    :class:`GroupShape` nodes as children.
    
    Each :class:`GroupShape` defines a new coordinate system for its child shapes.
    The coordinate system is defined using the :attr:`ShapeBase.coord_size` and
    :attr:`ShapeBase.coord_origin` properties."""
    
    def __init__(self, doc: aspose.words.DocumentBase):
        """Creates a new group shape.
        
        :param doc: The owner document.
        
        By default, the shape is floating and has default location and size.
        
        You should specify desired shape properties after you created a shape."""
        ...
    
    def accept(self, visitor: aspose.words.DocumentVisitor) -> bool:
        """Accepts a visitor.
        
        Enumerates over this node and all of its children. Each node calls a corresponding method on :class:`aspose.words.DocumentVisitor`.
        
        For more info see the Visitor design pattern.
        
        :param visitor: The visitor that will visit the nodes.
        :returns: True if all nodes were visited; false if :class:`aspose.words.DocumentVisitor` stopped the operation before visiting all nodes.
        
        Calls :meth:`aspose.words.DocumentVisitor.visit_group_shape_start`, then calls :meth:`aspose.words.Node.accept` for all
        child shapes of this group shape and calls :meth:`aspose.words.DocumentVisitor.visit_group_shape_end` at the end."""
        ...
    
    def accept_start(self, visitor: aspose.words.DocumentVisitor) -> aspose.words.VisitorAction:
        """Accepts a visitor for visiting the start of the GroupShape.
        
        :param visitor: The document visitor.
        :returns: The action to be taken by the visitor."""
        ...
    
    def accept_end(self, visitor: aspose.words.DocumentVisitor) -> aspose.words.VisitorAction:
        """Accepts a visitor for visiting the end of the GroupShape.
        
        :param visitor: The document visitor.
        :returns: The action to be taken by the visitor."""
        ...
    
    @property
    def node_type(self) -> aspose.words.NodeType:
        """Returns :attr:`aspose.words.NodeType.GROUP_SHAPE`."""
        ...
    
    ...

class HorizontalRuleFormat:
    """Represents horizontal rule formatting.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article."""
    
    @property
    def width_percent(self) -> float:
        """Gets or sets the length of the specified horizontal rule expressed as a percentage of the window width.
        
        Valid values ​​range from 1 to 100 inclusive.
        
        The default value is 100.
        
        :raises RuntimeError (Proxy error(ArgumentOutOfRangeException)): Throws when argument was out of the range of valid values."""
        ...
    
    @width_percent.setter
    def width_percent(self, value: float):
        ...
    
    @property
    def height(self) -> float:
        """Gets or sets the height of the horizontal rule.
        
        This is a shortcut to the :attr:`ShapeBase.height` property.
        
        Valid values ​​range from 0 to 1584 inclusive.
        
        The default value is 1.5.
        
        :raises RuntimeError (Proxy error(ArgumentOutOfRangeException)): Throws when argument was out of the range of valid values."""
        ...
    
    @height.setter
    def height(self, value: float):
        ...
    
    @property
    def no_shade(self) -> bool:
        """Indicates the presence of 3D shading for the horizontal rule.
        If ``True``, then the horizontal rule is without 3D shading and solid color is used.
        
        The default value is ``False``."""
        ...
    
    @no_shade.setter
    def no_shade(self, value: bool):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Gets or sets the brush color that fills the horizontal rule.
        
        This is a shortcut to the :attr:`Fill.color` property.
        
        The default value is
        aspose.pydrawing.Color.gray."""
        ...
    
    @color.setter
    def color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def alignment(self) -> aspose.words.drawing.HorizontalRuleAlignment:
        """Gets or sets the alignment of the horizontal rule.
        
        The default value is :attr:`HorizontalRuleAlignment.LEFT`."""
        ...
    
    @alignment.setter
    def alignment(self, value: aspose.words.drawing.HorizontalRuleAlignment):
        ...
    
    ...

class ImageData:
    """Defines an image for a shape.
    To learn more, visit the `Working with Images <https://docs.aspose.com/words/python-net/working-with-images/>` documentation article.
    
    Use the :attr:`Shape.image_data` property to access and modify the image inside a shape.
    You do not create instances of the :class:`ImageData` class directly.
    
    An image can be stored inside a shape, linked to external file or both (linked and stored in the document).
    
    Regardless of whether the image is stored inside the shape or linked, you can always access the actual
    image using the :meth:`ImageData.to_byte_array`, :meth:`ImageData.to_stream` or :meth:`ImageData.save` methods.
    If the image is stored inside the shape, you can also directly access it using the :attr:`ImageData.image_bytes` property.
    
    To store an image inside a shape use the :meth:`ImageData.set_image` method. To link an image to a shape, set the :attr:`ImageData.source_full_name` property."""
    
    @overload
    def set_image(self, stream: io.BytesIO) -> None:
        """Sets the image that the shape displays.
        
        :param stream: The stream that contains the image."""
        ...
    
    @overload
    def set_image(self, file_name: str) -> None:
        """Sets the image that the shape displays.
        
        :param file_name: The image file. Can be a file name or a URL."""
        ...
    
    @overload
    def save(self, stream: io.BytesIO) -> None:
        """Saves the image into the specified stream.
        
        :param stream: The stream where to save the image to.
        
        Is it the responsibility of the caller to dispose the stream object."""
        ...
    
    @overload
    def save(self, file_name: str) -> None:
        """Saves the image into a file.
        
        :param file_name: The file name where to save the image."""
        ...
    
    def to_stream(self) -> io.BytesIO:
        """Creates and returns a stream that contains the image bytes.
        
        If the image bytes are stored in the shape, creates and returns a io.BytesIO object.
        
        If the image is linked and stored in a file, opens the file and returns a io.BytesIO object.
        
        If the image is linked and stored in an external URL, downloads the file and returns a io.BytesIO object.
        
        Is it the responsibility of the caller to dispose the stream object."""
        ...
    
    def to_byte_array(self) -> bytes:
        """Returns image bytes for any image regardless whether the image is stored or linked.
        
        :returns:
        
        If the image is linked, downloads the image every time it is called."""
        ...
    
    def fit_image_to_shape(self) -> None:
        """Fits the image data to Shape frame so that the aspect ratio of the image data matches the aspect ratio of Shape frame."""
        ...
    
    @property
    def image_bytes(self) -> bytes:
        """Gets or sets the raw bytes of the image stored in the shape.
        
        Setting the value to ``None`` or an empty array will remove the image from the shape.
        
        Returns ``None`` if the image is not stored in the document (e.g the image is probably linked in this case)."""
        ...
    
    @image_bytes.setter
    def image_bytes(self, value: bytes):
        ...
    
    @property
    def has_image(self) -> bool:
        """Returns ``True`` if the shape has image bytes or links an image."""
        ...
    
    @property
    def image_size(self) -> aspose.words.drawing.ImageSize:
        """Gets the information about image size and resolution.
        
        If the image is linked only and not stored in the document, returns zero size."""
        ...
    
    @property
    def image_type(self) -> aspose.words.drawing.ImageType:
        """Gets the type of the image."""
        ...
    
    @property
    def is_link(self) -> bool:
        """Returns ``True`` if the image is linked to the shape (when :attr:`ImageData.source_full_name` is specified)."""
        ...
    
    @property
    def is_link_only(self) -> bool:
        """Returns ``True`` if the image is linked and not stored in the document."""
        ...
    
    @property
    def source_full_name(self) -> str:
        """Gets or sets the path and name of the source file for the linked image.
        
        The default value is an empty string.
        
        If :attr:`ImageData.source_full_name` is not an empty string, the image is linked."""
        ...
    
    @source_full_name.setter
    def source_full_name(self, value: str):
        ...
    
    @property
    def title(self) -> str:
        """Defines the title of an image.
        
        The default value is an empty string."""
        ...
    
    @title.setter
    def title(self, value: str):
        ...
    
    @property
    def crop_top(self) -> float:
        """Defines the fraction of picture removal from the top side.
        
        The amount of cropping can range from -1.0 to 1.0. The default value is 0. Note
        that a value of 1 will display no picture at all. Negative values will result in
        the picture being squeezed inward from the edge being cropped (the empty space
        between the picture and the cropped edge will be filled by the fill color of the
        shape). Positive values less than 1 will result in the remaining picture being
        stretched to fit the shape.
        
        The default value is 0."""
        ...
    
    @crop_top.setter
    def crop_top(self, value: float):
        ...
    
    @property
    def crop_bottom(self) -> float:
        """Defines the fraction of picture removal from the bottom side.
        
        The amount of cropping can range from -1.0 to 1.0. The default value is 0. Note
        that a value of 1 will display no picture at all. Negative values will result in
        the picture being squeezed inward from the edge being cropped (the empty space
        between the picture and the cropped edge will be filled by the fill color of the
        shape). Positive values less than 1 will result in the remaining picture being
        stretched to fit the shape.
        
        The default value is 0."""
        ...
    
    @crop_bottom.setter
    def crop_bottom(self, value: float):
        ...
    
    @property
    def crop_left(self) -> float:
        """Defines the fraction of picture removal from the left side.
        
        The amount of cropping can range from -1.0 to 1.0. The default value is 0. Note
        that a value of 1 will display no picture at all. Negative values will result in
        the picture being squeezed inward from the edge being cropped (the empty space
        between the picture and the cropped edge will be filled by the fill color of the
        shape). Positive values less than 1 will result in the remaining picture being
        stretched to fit the shape.
        
        The default value is 0."""
        ...
    
    @crop_left.setter
    def crop_left(self, value: float):
        ...
    
    @property
    def crop_right(self) -> float:
        """Defines the fraction of picture removal from the right side.
        
        The amount of cropping can range from -1.0 to 1.0. The default value is 0. Note
        that a value of 1 will display no picture at all. Negative values will result in
        the picture being squeezed inward from the edge being cropped (the empty space
        between the picture and the cropped edge will be filled by the fill color of the
        shape). Positive values less than 1 will result in the remaining picture being
        stretched to fit the shape.
        
        The default value is 0."""
        ...
    
    @crop_right.setter
    def crop_right(self, value: float):
        ...
    
    @property
    def borders(self) -> aspose.words.BorderCollection:
        """Gets the collection of borders of the image. Borders only have effect for inline images."""
        ...
    
    @property
    def chroma_key(self) -> aspose.pydrawing.Color:
        """Defines the color value of the image that will be treated as transparent.
        
        The default value is 0."""
        ...
    
    @chroma_key.setter
    def chroma_key(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def brightness(self) -> float:
        """Gets or sets the brightness of the picture.
        The value for this property must be a number from 0.0 (dimmest) to 1.0 (brightest).
        
        The default value is 0.5."""
        ...
    
    @brightness.setter
    def brightness(self, value: float):
        ...
    
    @property
    def contrast(self) -> float:
        """Gets or sets the contrast for the specified picture. The value
        for this property must be a number from 0.0 (the least contrast) to 1.0 (the greatest contrast).
        
        The default value is 0.5."""
        ...
    
    @contrast.setter
    def contrast(self, value: float):
        ...
    
    @property
    def bi_level(self) -> bool:
        """Determines whether an image will be displayed in black and white.
        
        The default value is ``False``."""
        ...
    
    @bi_level.setter
    def bi_level(self, value: bool):
        ...
    
    @property
    def gray_scale(self) -> bool:
        """Determines whether a picture will display in grayscale mode.
        
        The default value is ``False``."""
        ...
    
    @gray_scale.setter
    def gray_scale(self, value: bool):
        ...
    
    ...

class ImageSize:
    """Contains information about image size and resolution.
    To learn more, visit the `Working with Images <https://docs.aspose.com/words/python-net/working-with-images/>` documentation article."""
    
    @overload
    def __init__(self, width_pixels: int, height_pixels: int):
        """Initializes width and height to the given values in pixels. Initializes resolution to 96 dpi.
        
        :param width_pixels: Width in pixels.
        :param height_pixels: Height in pixels."""
        ...
    
    @overload
    def __init__(self, width_pixels: int, height_pixels: int, horizontal_resolution: float, vertical_resolution: float):
        """Initializes width, height and resolution to the given values.
        
        :param width_pixels: Width in pixels.
        :param height_pixels: Height in pixels.
        :param horizontal_resolution: Horizontal resolution in DPI.
        :param vertical_resolution: Vertical resolution in DPI."""
        ...
    
    @property
    def width_pixels(self) -> int:
        """Gets the width of the image in pixels."""
        ...
    
    @property
    def height_pixels(self) -> int:
        """Gets the height of the image in pixels."""
        ...
    
    @property
    def horizontal_resolution(self) -> float:
        """Gets the horizontal resolution in DPI."""
        ...
    
    @property
    def vertical_resolution(self) -> float:
        """Gets the vertical resolution in DPI."""
        ...
    
    @property
    def width_points(self) -> float:
        """Gets the width of the image in points. 1 point is 1/72 inch."""
        ...
    
    @property
    def height_points(self) -> float:
        """Gets the height of the image in points. 1 point is 1/72 inch."""
        ...
    
    ...

class OleFormat:
    """Provides access to the data of an OLE object or ActiveX control.
    To learn more, visit the `Working with Ole Objects <https://docs.aspose.com/words/python-net/working-with-ole-objects/>` documentation article.
    
    Use the :attr:`Shape.ole_format` property to access the data of an OLE object.
    You do not create instances of the :class:`OleFormat` class directly."""
    
    @overload
    def save(self, stream: io.BytesIO) -> None:
        """Saves the data of the embedded object into the specified stream.
        
        It is the responsibility of the caller to dispose the stream.
        
        :raises RuntimeError (Proxy error(InvalidOperationException)): Throws if you attempt to save a linked object.
        :param stream: Where to save the object data."""
        ...
    
    @overload
    def save(self, file_name: str) -> None:
        """Saves the data of the embedded object into a file with the specified name.
        
        :raises RuntimeError (Proxy error(InvalidOperationException)): Throws if you attempt to save a linked object.
        :param file_name: Name of the file to save the OLE object data."""
        ...
    
    def get_ole_entry(self, ole_entry_name: str) -> io.BytesIO:
        """Gets OLE object data entry.
        
        :param ole_entry_name: Case-sensitive name of the OLE data stream.
        :returns: An OLE data stream or ``None``."""
        ...
    
    def get_raw_data(self) -> bytes:
        """Gets OLE object raw data."""
        ...
    
    @property
    def icon_caption(self) -> str:
        """Gets icon caption of OLE object.
        In case if the OLE object does not have an icon or a caption cannot be retrieved, returns an empty
        string."""
        ...
    
    @property
    def suggested_extension(self) -> str:
        """Gets the file extension suggested for the current embedded object if you want to save it into a file."""
        ...
    
    @property
    def suggested_file_name(self) -> str:
        """Gets the file name suggested for the current embedded object if you want to save it into a file."""
        ...
    
    @property
    def prog_id(self) -> str:
        """Gets or sets the ProgID of the OLE object.
        
        The ProgID property is not always present in Microsoft Word documents and cannot be relied upon.
        
        Cannot be ``None``.
        
        The default value is an empty string."""
        ...
    
    @prog_id.setter
    def prog_id(self, value: str):
        ...
    
    @property
    def is_link(self) -> bool:
        """Returns ``True`` if the OLE object is linked (when :attr:`OleFormat.source_full_name` is specified)."""
        ...
    
    @property
    def source_full_name(self) -> str:
        """Gets or sets the path and name of the source file for the linked OLE object.
        
        The default value is an empty string.
        
        If :attr:`OleFormat.source_full_name` is not an empty string, the OLE object is linked."""
        ...
    
    @source_full_name.setter
    def source_full_name(self, value: str):
        ...
    
    @property
    def source_item(self) -> str:
        """Gets or sets a string that is used to identify the portion of the source file that is being linked.
        
        The default value is an empty string.
        
        For example, if the source file is a Microsoft Excel workbook, the :attr:`OleFormat.source_item`
        property might return "Workbook1!R3C1:R4C2" if the OLE object contains only a few cells from
        the worksheet."""
        ...
    
    @source_item.setter
    def source_item(self, value: str):
        ...
    
    @property
    def auto_update(self) -> bool:
        """Specifies whether the link to the OLE object is automatically updated or not in Microsoft Word.
        
        The default value is ``False``."""
        ...
    
    @auto_update.setter
    def auto_update(self, value: bool):
        ...
    
    @property
    def ole_icon(self) -> bool:
        """Gets the draw aspect of the OLE object. When ``True``, the OLE object is displayed as an icon.
        When ``False``, the OLE object is displayed as content.
        
        Aspose.Words does not allow to set this property to avoid confusion. If you were able to change
        the draw aspect in Aspose.Words, Microsoft Word would still display the OLE object in its original
        draw aspect until you edit or update the OLE object in Microsoft Word."""
        ...
    
    @property
    def is_locked(self) -> bool:
        """Specifies whether the link to the OLE object is locked from updates.
        
        The default value is ``False``."""
        ...
    
    @is_locked.setter
    def is_locked(self, value: bool):
        ...
    
    @property
    def clsid(self) -> uuid.UUID:
        """Gets the CLSID of the OLE object."""
        ...
    
    @property
    def ole_package(self) -> aspose.words.drawing.OlePackage:
        """Provide access to :class:`OlePackage` if OLE object is an OLE Package.
        Returns ``None`` otherwise.
        
        OLE Package is a legacy technology that allows to wrap any file format not present in the OLE registry of
        a Windows system into a generic package allowing to embed almost anything into a document.
        See :class:`OlePackage` type for more info."""
        ...
    
    @property
    def ole_control(self) -> aspose.words.drawing.ole.OleControl:
        """Gets :attr:`OleFormat.ole_control` objects if this OLE object is an ActiveX control. Otherwise this property is null."""
        ...
    
    ...

class OlePackage:
    """Allows to access OLE Package properties.
    To learn more, visit the `Working with Ole Objects <https://docs.aspose.com/words/python-net/working-with-ole-objects/>` documentation article.
    
    OLE package is a legacy and "undocumented" way to store embedded object if OLE handler is unknown.
    Early Windows versions such as Windows 3.1, 95 and 98 had Packager.exe application which could be used to embed any type of data into document.
    Now this application is excluded from Windows but MS Word and other applications still use it to embed data if OLE handler is missing or unknown."""
    
    @property
    def file_name(self) -> str:
        """Gets or sets OLE Package file name."""
        ...
    
    @file_name.setter
    def file_name(self, value: str):
        ...
    
    @property
    def display_name(self) -> str:
        """Gets or sets OLE Package display name."""
        ...
    
    @display_name.setter
    def display_name(self, value: str):
        ...
    
    ...

class ReflectionFormat:
    """Represents the reflection formatting for an object.
    
    Use the :attr:`ShapeBase.reflection` property to access reflection properties of an object.
    You do not create instances of the :class:`ReflectionFormat` class directly."""
    
    def remove(self) -> None:
        """Removes :class:`ReflectionFormat` from the parent object."""
        ...
    
    @property
    def blur(self) -> float:
        """Gets or sets a double value that specifies the degree of blur effect applied to the reflection effect in points.
        The default value is 0.0."""
        ...
    
    @blur.setter
    def blur(self, value: float):
        ...
    
    @property
    def distance(self) -> float:
        """Gets or sets a double value that specifies the amount of separation of the reflected image from the object in points.
        The default value is 0.0."""
        ...
    
    @distance.setter
    def distance(self, value: float):
        ...
    
    @property
    def size(self) -> float:
        """Gets or sets a double value between 0.0 and 1.0 representing the size of the reflection
        as a percentage of the reflected object.
        The default value is 0.0."""
        ...
    
    @size.setter
    def size(self, value: float):
        ...
    
    @property
    def transparency(self) -> float:
        """Gets or sets a double value between 0.0 (opaque) and 1.0 (clear) representing the degree
        of transparency for the reflection effect.
        The default value is 0.0."""
        ...
    
    @transparency.setter
    def transparency(self, value: float):
        ...
    
    ...

class ShadowFormat:
    """Represents shadow formatting for an object.
    To learn more, visit the `Working with Graphic Elements <https://docs.aspose.com/words/python-net/working-with-graphic-elements/>` documentation article."""
    
    def clear(self) -> None:
        """Clears shadow format."""
        ...
    
    @property
    def type(self) -> aspose.words.drawing.ShadowType:
        """Gets or sets the specified :class:`ShadowType` for ShadowFormat."""
        ...
    
    @type.setter
    def type(self, value: aspose.words.drawing.ShadowType):
        ...
    
    @property
    def visible(self) -> bool:
        """Returns ``True`` if the formatting applied to this instance is visible.
        
        Unlike :meth:`ShadowFormat.clear`, assigning ``False`` to Visible does not clear the formatting,
        it only hides the shape effect."""
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Gets a aspose.pydrawing.Color object that represents the color for the shadow.
        The default value is aspose.pydrawing.Color.black."""
        ...
    
    ...

class Shape(aspose.words.drawing.ShapeBase):
    """Represents an object in the drawing layer, such as an AutoShape, textbox, freeform, OLE object, ActiveX control, or picture.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article.
    
    Using the :class:`Shape` class you can create or modify shapes in a Microsoft Word document.
    
    An important property of a shape is its :attr:`ShapeBase.shape_type`. Shapes of different
    types can have different capabilities in a Word document. For example, only image and OLE shapes
    can have images inside them. Most of the shapes can have text, but not all.
    
    Shapes that can have text, can contain :class:`aspose.words.Paragraph` and
    :class:`aspose.words.tables.Table` nodes as children."""
    
    def __init__(self, doc: aspose.words.DocumentBase, shape_type: aspose.words.drawing.ShapeType):
        """Creates a new shape object.
        
        You should specify desired shape properties after you created a shape.
        
        :param doc: The owner document.
        :param shape_type: The type of the shape to create."""
        ...
    
    def accept(self, visitor: aspose.words.DocumentVisitor) -> bool:
        """Accepts a visitor.
        
        Enumerates over this node and all of its children. Each node calls a corresponding method on :class:`aspose.words.DocumentVisitor`.
        
        For more info see the Visitor design pattern.
        
        :param visitor: The visitor that will visit the nodes.
        :returns: True if all nodes were visited; false if :class:`aspose.words.DocumentVisitor` stopped the operation before visiting all nodes.
        
        Calls :meth:`aspose.words.DocumentVisitor.visit_shape_start`, then calls :meth:`aspose.words.Node.accept`
        for all child nodes of the shape and calls :meth:`aspose.words.DocumentVisitor.visit_shape_end` at the end."""
        ...
    
    def accept_start(self, visitor: aspose.words.DocumentVisitor) -> aspose.words.VisitorAction:
        """Accepts a visitor for visiting the start of the shape.
        
        :param visitor: The document visitor.
        :returns: The action to be taken by the visitor."""
        ...
    
    def accept_end(self, visitor: aspose.words.DocumentVisitor) -> aspose.words.VisitorAction:
        """Accepts a visitor for visiting the end of the shape.
        
        :param visitor: The document visitor.
        :returns: The action to be taken by the visitor."""
        ...
    
    def update_smart_art_drawing(self) -> None:
        """Updates SmartArt pre-rendered drawing by using Aspose.Words's SmartArt cold rendering engine.
        
        Microsoft Word generates and saves the pre-rendered drawing along with SmartArt object. However,
        if the document is saved by other applications, the pre-rendered SmartArt drawing may be missing or incorrect.
        If pre-rendered drawing is available then Aspose.Words uses it to render the SmartArt object.
        If pre-rendered drawing is missing then Aspose.Words uses its own SmartArt cold rendering engine to render the
        SmartArt object.
        If pre-rendered drawing is incorrect then it is required to call this method to invoke the SmartArt cold
        rendering engine."""
        ...
    
    @property
    def node_type(self) -> aspose.words.NodeType:
        """Returns :attr:`aspose.words.NodeType.SHAPE`."""
        ...
    
    @property
    def story_type(self) -> aspose.words.StoryType:
        """Returns :attr:`aspose.words.StoryType.TEXTBOX`."""
        ...
    
    @property
    def extrusion_enabled(self) -> bool:
        """Returns ``True`` if an extrusion effect is enabled."""
        ...
    
    @property
    def shadow_enabled(self) -> bool:
        """Returns ``True`` if a shadow effect is enabled."""
        ...
    
    @property
    def stroke(self) -> aspose.words.drawing.Stroke:
        """Defines a stroke for a shape."""
        ...
    
    @property
    def stroked(self) -> bool:
        """Defines whether the path will be stroked.
        
        This is a shortcut to the :attr:`Stroke.on` property.
        
        The default value is ``True``."""
        ...
    
    @stroked.setter
    def stroked(self, value: bool):
        ...
    
    @property
    def stroke_weight(self) -> float:
        """Defines the brush thickness that strokes the path of a shape in points.
        
        This is a shortcut to the :attr:`Stroke.weight` property.
        
        The default value is 0.75."""
        ...
    
    @stroke_weight.setter
    def stroke_weight(self, value: float):
        ...
    
    @property
    def stroke_color(self) -> aspose.pydrawing.Color:
        """Defines the color of a stroke.
        
        This is a shortcut to the :attr:`Stroke.color` property.
        
        The default value is
        aspose.pydrawing.Color.black."""
        ...
    
    @stroke_color.setter
    def stroke_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def filled(self) -> bool:
        """Determines whether the closed path of the shape will be filled.
        
        This is a shortcut to the :attr:`Fill.visible` property.
        
        The default value is ``True``."""
        ...
    
    @filled.setter
    def filled(self, value: bool):
        ...
    
    @property
    def fill_color(self) -> aspose.pydrawing.Color:
        """Defines the brush color that fills the closed path of the shape.
        
        This is a shortcut to the :attr:`Fill.color` property.
        
        The default value is
        aspose.pydrawing.Color.white."""
        ...
    
    @fill_color.setter
    def fill_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def has_image(self) -> bool:
        """Returns ``True`` if the shape has image bytes or links an image."""
        ...
    
    @property
    def image_data(self) -> aspose.words.drawing.ImageData:
        """Provides access to the image of the shape.
        Returns ``None`` if the shape cannot have an image."""
        ...
    
    @property
    def ole_format(self) -> aspose.words.drawing.OleFormat:
        """Provides access to the OLE data of a shape. For a shape that is not an OLE object or ActiveX control, returns ``None``."""
        ...
    
    @property
    def text_box(self) -> aspose.words.drawing.TextBox:
        """Defines attributes that specify how text is displayed in a shape."""
        ...
    
    @property
    def text_path(self) -> aspose.words.drawing.TextPath:
        """Defines the text of the text path (of a WordArt object)."""
        ...
    
    @property
    def first_paragraph(self) -> aspose.words.Paragraph:
        """Gets the first paragraph in the shape."""
        ...
    
    @property
    def last_paragraph(self) -> aspose.words.Paragraph:
        """Gets the last paragraph in the shape."""
        ...
    
    @property
    def horizontal_rule_format(self) -> aspose.words.drawing.HorizontalRuleFormat:
        """Provides access to the properties of the horizontal rule shape.
        For a shape that is not a horizontal rule, returns ``None``."""
        ...
    
    @property
    def adjustments(self) -> aspose.words.drawing.AdjustmentCollection:
        """Provides access to the adjustment raw values of a shape.
        For a shape that does not contain any adjustment raw values, it returns an empty collection."""
        ...
    
    @property
    def signature_line(self) -> aspose.words.drawing.SignatureLine:
        """Gets :class:`SignatureLine` object if the shape is a signature line. Returns ``None`` otherwise.
        
        You can insert new :class:`SignatureLine` into the document using :meth:`aspose.words.DocumentBuilder.insert_signature_line` and"""
        ...
    
    @property
    def has_chart(self) -> bool:
        """Returns ``True`` if this :class:`Shape` has a :class:`aspose.words.drawing.charts.Chart`."""
        ...
    
    @property
    def has_smart_art(self) -> bool:
        """Returns ``True`` if this :class:`Shape` has a SmartArt object."""
        ...
    
    @property
    def chart(self) -> aspose.words.drawing.charts.Chart:
        """Provides access to the chart properties if this shape has a :class:`aspose.words.drawing.charts.Chart`.
        
        This property will return the :class:`aspose.words.drawing.charts.Chart` object only if :attr:`Shape.has_chart`
        property is ``True`` for this :class:`Shape`, and will throw an exception otherwise."""
        ...
    
    ...

class ShapeBase(aspose.words.CompositeNode):
    """Base class for objects in the drawing layer, such as an AutoShape, freeform, OLE object, ActiveX control, or picture.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article.
    
    This is an abstract class. The two derived classes that you can instantiate
    are :class:`Shape` and :class:`GroupShape`.
    
    A shape is a node in the document tree.
    
    If the shape is a child of a :class:`aspose.words.Paragraph` object, then the shape is said to be "top-level".
    Top-level shapes are measured and positioned in points.
    
    A shape can also occur as a child of a :class:`GroupShape` object when several shapes
    are grouped. Child shapes of a group shape are positioned in the coordinate space and units
    defined by the :attr:`ShapeBase.coord_size` and :attr:`ShapeBase.coord_origin` properties of the parent
    group shape.
    
    A shape can be positioned inline with text or floating. The positioning method is controlled
    using the :attr:`ShapeBase.wrap_type` property.
    
    When a shape is floating, it is positioned relative to something (e.g the current paragraph,
    the margin or the page). The relative positioning of the shape is specified using the
    :attr:`ShapeBase.relative_horizontal_position` and :attr:`ShapeBase.relative_vertical_position` properties.
    
    A floating shape be positioned explicitly using the :attr:`ShapeBase.left` and :attr:`ShapeBase.top`
    properties or aligned relative to some other object using the :attr:`ShapeBase.horizontal_alignment`
    and :attr:`ShapeBase.vertical_alignment` properties."""
    
    def get_shape_renderer(self) -> aspose.words.rendering.ShapeRenderer:
        """Creates and returns an object that can be used to render this shape into an image.
        
        This method just invokes the :class:`aspose.words.rendering.ShapeRenderer` constructor and passes
        this object as a parameter.
        
        :returns: The renderer object for this shape."""
        ...
    
    def local_to_parent(self, value: aspose.pydrawing.PointF) -> aspose.pydrawing.PointF:
        """Converts a value from the local coordinate space into the coordinate space of the parent shape."""
        ...
    
    def adjust_with_effects(self, source: aspose.pydrawing.RectangleF) -> aspose.pydrawing.RectangleF:
        """Adds to the source rectangle values of the effect extent and returns the final rectangle."""
        ...
    
    @property
    def fill(self) -> aspose.words.drawing.Fill:
        """Gets fill formatting for the shape."""
        ...
    
    @property
    def shadow_format(self) -> aspose.words.drawing.ShadowFormat:
        """Gets shadow formatting for the shape."""
        ...
    
    @property
    def glow(self) -> aspose.words.drawing.GlowFormat:
        """Gets glow formatting for the shape."""
        ...
    
    @property
    def reflection(self) -> aspose.words.drawing.ReflectionFormat:
        """Gets reflection formatting for the shape."""
        ...
    
    @property
    def soft_edge(self) -> aspose.words.drawing.SoftEdgeFormat:
        """Gets soft edge formatting for the shape."""
        ...
    
    @property
    def screen_tip(self) -> str:
        """Defines the text displayed when the mouse pointer moves over the shape.
        
        The default value is an empty string."""
        ...
    
    @screen_tip.setter
    def screen_tip(self, value: str):
        ...
    
    @property
    def href(self) -> str:
        """Gets or sets the full hyperlink address for a shape.
        
        The default value is an empty string.
        
        Below are examples of valid values for this property:
        
        Full URI: ``https://www.aspose.com/``.
        
        Full file name: ``C:\\\\My Documents\\\\SalesReport.doc``.
        
        Relative URI: ``../../../resource.txt``
        
        Relative file name: ``..\\\\My Documents\\\\SalesReport.doc``.
        
        Bookmark within another document: ``https://www.aspose.com/Products/Default.aspx#Suites``
        
        Bookmark within this document: ``#BookmakName``."""
        ...
    
    @href.setter
    def href(self, value: str):
        ...
    
    @property
    def target(self) -> str:
        """Gets or sets the target frame for the shape hyperlink.
        
        The default value is an empty string."""
        ...
    
    @target.setter
    def target(self, value: str):
        ...
    
    @property
    def alternative_text(self) -> str:
        """Defines alternative text to be displayed instead of a graphic.
        
        The default value is an empty string."""
        ...
    
    @alternative_text.setter
    def alternative_text(self, value: str):
        ...
    
    @property
    def is_decorative(self) -> bool:
        """Gets or sets the flag that specifies whether the shape is decorative in the document.
        
        Note that shape having not empty :attr:`ShapeBase.alternative_text` cannot be decorative."""
        ...
    
    @is_decorative.setter
    def is_decorative(self, value: bool):
        ...
    
    @property
    def title(self) -> str:
        """Gets or sets the title (caption) of the current shape object.
        
        Default is empty string.
        
        Cannot be ``None``, but can be an empty string."""
        ...
    
    @title.setter
    def title(self, value: str):
        ...
    
    @property
    def name(self) -> str:
        """Gets or sets the optional shape name.
        
        Default is empty string.
        
        Cannot be ``None``, but can be an empty string."""
        ...
    
    @name.setter
    def name(self, value: str):
        ...
    
    @property
    def is_insert_revision(self) -> bool:
        """Returns true if this object was inserted in Microsoft Word while change tracking was enabled."""
        ...
    
    @property
    def is_delete_revision(self) -> bool:
        """Returns true if this object was deleted in Microsoft Word while change tracking was enabled."""
        ...
    
    @property
    def is_move_from_revision(self) -> bool:
        """Returns ``True`` if this object was moved (deleted) in Microsoft Word while change tracking was enabled."""
        ...
    
    @property
    def is_move_to_revision(self) -> bool:
        """Returns ``True`` if this object was moved (inserted) in Microsoft Word while change tracking was enabled."""
        ...
    
    @property
    def is_top_level(self) -> bool:
        """Returns ``True`` if this shape is not a child of a group shape."""
        ...
    
    @property
    def is_group(self) -> bool:
        """Returns ``True`` if this is a group shape."""
        ...
    
    @property
    def is_image(self) -> bool:
        """Returns ``True`` if this shape is an image shape."""
        ...
    
    @property
    def is_horizontal_rule(self) -> bool:
        """Returns ``True`` if this shape is a horizontal rule."""
        ...
    
    @property
    def is_word_art(self) -> bool:
        """Returns ``True`` if this shape is a WordArt object.
        
        Works till 2007 compatibility mode.
        In 2010 and higher compatibility mode WordArt is just a TextBox with fancy fonts."""
        ...
    
    @property
    def can_have_image(self) -> bool:
        """Returns ``True`` if the shape type allows the shape to have an image.
        
        Although Microsoft Word has a special shape type for images, it appears that in Microsoft Word documents any shape
        except a group shape can have an image, therefore this property returns ``True`` for all shapes except :class:`GroupShape`."""
        ...
    
    @property
    def anchor_locked(self) -> bool:
        """Specifies whether the shape's anchor is locked.
        
        The default value is ``False``.
        
        Has effect only for top level shapes.
        
        This property affects behavior of the shape's anchor in Microsoft Word.
        When the anchor is not locked, moving the shape in Microsoft Word can move
        the shape's anchor too."""
        ...
    
    @anchor_locked.setter
    def anchor_locked(self, value: bool):
        ...
    
    @property
    def aspect_ratio_locked(self) -> bool:
        """Specifies whether the shape's aspect ratio is locked.
        
        The default value depends on the :class:`ShapeType`, for the :attr:`ShapeType.IMAGE` it is ``True``
        but for the other shape types it is ``False``.
        
        Has effect for top level shapes only."""
        ...
    
    @aspect_ratio_locked.setter
    def aspect_ratio_locked(self, value: bool):
        ...
    
    @property
    def allow_overlap(self) -> bool:
        """Gets or sets a value that specifies whether this shape can overlap other shapes.
        
        This property affects behavior of the shape in Microsoft Word.
        Aspose.Words ignores the value of this property.
        
        This property is applicable only to top level shapes.
        
        The default value is ``True``."""
        ...
    
    @allow_overlap.setter
    def allow_overlap(self, value: bool):
        ...
    
    @property
    def behind_text(self) -> bool:
        """Specifies whether the shape is below or above text.
        
        Has effect only for top level shapes.
        
        The default value is ``False``."""
        ...
    
    @behind_text.setter
    def behind_text(self, value: bool):
        ...
    
    @property
    def is_inline(self) -> bool:
        """A quick way to determine if this shape is positioned inline with text.
        
        Has effect only for top level shapes."""
        ...
    
    @property
    def left(self) -> float:
        """Gets or sets the position of the left edge of the containing block of the shape.
        
        For a top-level shape, the value is in points and relative to the shape anchor.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group.
        
        The default value is 0.
        
        Has effect only for floating shapes."""
        ...
    
    @left.setter
    def left(self, value: float):
        ...
    
    @property
    def top(self) -> float:
        """Gets or sets the position of the top edge of the containing block of the shape.
        
        For a top-level shape, the value is in points and relative to the shape anchor.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group.
        
        The default value is 0.
        
        Has effect only for floating shapes."""
        ...
    
    @top.setter
    def top(self, value: float):
        ...
    
    @property
    def right(self) -> float:
        """Gets the position of the right edge of the containing block of the shape.
        
        For a top-level shape, the value is in points and relative to the shape anchor.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group."""
        ...
    
    @property
    def bottom(self) -> float:
        """Gets the position of the bottom edge of the containing block of the shape.
        
        For a top-level shape, the value is in points and relative to the shape anchor.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group."""
        ...
    
    @property
    def width(self) -> float:
        """Gets or sets the width of the containing block of the shape.
        
        For a top-level shape, the value is in points.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group.
        
        The default value is 0."""
        ...
    
    @width.setter
    def width(self, value: float):
        ...
    
    @property
    def height(self) -> float:
        """Gets or sets the height of the containing block of the shape.
        
        For a top-level shape, the value is in points.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group.
        
        The default value is 0."""
        ...
    
    @height.setter
    def height(self, value: float):
        ...
    
    @property
    def distance_top(self) -> float:
        """Returns or sets the distance (in points) between the document text and the top edge of the shape.
        
        The default value is 0.
        
        Has effect only for top level shapes."""
        ...
    
    @distance_top.setter
    def distance_top(self, value: float):
        ...
    
    @property
    def distance_bottom(self) -> float:
        """Returns or sets the distance (in points) between the document text and the bottom edge of the shape.
        
        The default value is 0.
        
        Has effect only for top level shapes."""
        ...
    
    @distance_bottom.setter
    def distance_bottom(self, value: float):
        ...
    
    @property
    def distance_left(self) -> float:
        """Returns or sets the distance (in points) between the document text and the left edge of the shape.
        
        The default value is 1/8 inch.
        
        Has effect only for top level shapes."""
        ...
    
    @distance_left.setter
    def distance_left(self, value: float):
        ...
    
    @property
    def distance_right(self) -> float:
        """Returns or sets the distance (in points) between the document text and the right edge of the shape.
        
        The default value is 1/8 inch.
        
        Has effect only for top level shapes."""
        ...
    
    @distance_right.setter
    def distance_right(self, value: float):
        ...
    
    @property
    def rotation(self) -> float:
        """Defines the angle (in degrees) that a shape is rotated.
        Positive value corresponds to clockwise rotation angle.
        
        The default value is 0."""
        ...
    
    @rotation.setter
    def rotation(self, value: float):
        ...
    
    @property
    def z_order(self) -> int:
        """Determines the display order of overlapping shapes.
        
        Has effect only for top level shapes.
        
        The default value is 0.
        
        The number represents the stacking precedence. A shape with a higher number will be displayed
        as if it were overlapping (in "front" of) a shape with a lower number.
        
        The order of overlapping shapes is independent for shapes in the header and in the main
        text of the document.
        
        The display order of child shapes in a group shape is determined by their order
        inside the group shape."""
        ...
    
    @z_order.setter
    def z_order(self, value: int):
        ...
    
    @property
    def parent_paragraph(self) -> aspose.words.Paragraph:
        """Returns the immediate parent paragraph.
        
        For child shapes of a group shape and child shapes of an Office Math object always returns ``None``."""
        ...
    
    @property
    def bounds(self) -> aspose.pydrawing.RectangleF:
        """Gets or sets the location and size of the containing block of the shape.
        
        Ignores aspect ratio lock upon setting.
        
        For a top-level shape, the value is in points and relative to the shape anchor.
        
        For shapes in a group, the value is in the coordinate space and units of the parent group."""
        ...
    
    @bounds.setter
    def bounds(self, value: aspose.pydrawing.RectangleF):
        ...
    
    @property
    def bounds_in_points(self) -> aspose.pydrawing.RectangleF:
        """Gets the location and size of the containing block of the shape in points, relative to the anchor of the topmost shape."""
        ...
    
    @property
    def bounds_with_effects(self) -> aspose.pydrawing.RectangleF:
        """Gets final extent that this shape object has after applying drawing effects.
        Value is measured in points."""
        ...
    
    @property
    def shape_type(self) -> aspose.words.drawing.ShapeType:
        """Gets the shape type."""
        ...
    
    @property
    def markup_language(self) -> aspose.words.drawing.ShapeMarkupLanguage:
        """Gets MarkupLanguage used for this graphic object."""
        ...
    
    @property
    def size_in_points(self) -> aspose.pydrawing.SizeF:
        """Gets the size of the shape in points."""
        ...
    
    @property
    def flip_orientation(self) -> aspose.words.drawing.FlipOrientation:
        """Switches the orientation of a shape.
        
        The default value is :attr:`FlipOrientation.NONE`."""
        ...
    
    @flip_orientation.setter
    def flip_orientation(self, value: aspose.words.drawing.FlipOrientation):
        ...
    
    @property
    def relative_horizontal_position(self) -> aspose.words.drawing.RelativeHorizontalPosition:
        """Specifies relative to what the shape is positioned horizontally.
        
        The default value is :attr:`RelativeHorizontalPosition.COLUMN`.
        
        Has effect only for top level floating shapes."""
        ...
    
    @relative_horizontal_position.setter
    def relative_horizontal_position(self, value: aspose.words.drawing.RelativeHorizontalPosition):
        ...
    
    @property
    def relative_vertical_position(self) -> aspose.words.drawing.RelativeVerticalPosition:
        """Specifies relative to what the shape is positioned vertically.
        
        The default value is :attr:`RelativeVerticalPosition.PARAGRAPH`.
        
        Has effect only for top level floating shapes."""
        ...
    
    @relative_vertical_position.setter
    def relative_vertical_position(self, value: aspose.words.drawing.RelativeVerticalPosition):
        ...
    
    @property
    def relative_horizontal_size(self) -> aspose.words.drawing.RelativeHorizontalSize:
        """Gets or sets the value of shape's relative size in horizontal direction.
        
        The default value is :class:`RelativeHorizontalSize`.
        
        Has effect only if :attr:`ShapeBase.width_relative` is set."""
        ...
    
    @relative_horizontal_size.setter
    def relative_horizontal_size(self, value: aspose.words.drawing.RelativeHorizontalSize):
        ...
    
    @property
    def relative_vertical_size(self) -> aspose.words.drawing.RelativeVerticalSize:
        """Gets or sets the value of shape's relative size in vertical direction.
        
        The default value is :attr:`RelativeVerticalSize.MARGIN`.
        
        Has effect only if :attr:`ShapeBase.height_relative` is set."""
        ...
    
    @relative_vertical_size.setter
    def relative_vertical_size(self, value: aspose.words.drawing.RelativeVerticalSize):
        ...
    
    @property
    def left_relative(self) -> float:
        """Gets or sets the value that represents shape's relative left position in percent."""
        ...
    
    @left_relative.setter
    def left_relative(self, value: float):
        ...
    
    @property
    def top_relative(self) -> float:
        """Gets or sets the value that represents shape's relative top position in percent."""
        ...
    
    @top_relative.setter
    def top_relative(self, value: float):
        ...
    
    @property
    def height_relative(self) -> float:
        """Gets or sets the value that represents the percentage of shape's relative height."""
        ...
    
    @height_relative.setter
    def height_relative(self, value: float):
        ...
    
    @property
    def width_relative(self) -> float:
        """Gets or sets the value that represents the percentage of shape's relative width."""
        ...
    
    @width_relative.setter
    def width_relative(self, value: float):
        ...
    
    @property
    def horizontal_alignment(self) -> aspose.words.drawing.HorizontalAlignment:
        """Specifies how the shape is positioned horizontally.
        
        The default value is :attr:`HorizontalAlignment.NONE`.
        
        Has effect only for top level floating shapes."""
        ...
    
    @horizontal_alignment.setter
    def horizontal_alignment(self, value: aspose.words.drawing.HorizontalAlignment):
        ...
    
    @property
    def vertical_alignment(self) -> aspose.words.drawing.VerticalAlignment:
        """Specifies how the shape is positioned vertically.
        
        The default value is :attr:`VerticalAlignment.NONE`.
        
        Has effect only for top level floating shapes."""
        ...
    
    @vertical_alignment.setter
    def vertical_alignment(self, value: aspose.words.drawing.VerticalAlignment):
        ...
    
    @property
    def wrap_type(self) -> aspose.words.drawing.WrapType:
        """Defines whether the shape is inline or floating. For floating shapes defines the wrapping mode for text around the shape.
        
        The default value is :attr:`WrapType.NONE`.
        
        Has effect only for top level shapes."""
        ...
    
    @wrap_type.setter
    def wrap_type(self, value: aspose.words.drawing.WrapType):
        ...
    
    @property
    def wrap_side(self) -> aspose.words.drawing.WrapSide:
        """Specifies how the text is wrapped around the shape.
        
        The default value is :attr:`WrapSide.BOTH`.
        
        Has effect only for top level shapes."""
        ...
    
    @wrap_side.setter
    def wrap_side(self, value: aspose.words.drawing.WrapSide):
        ...
    
    @property
    def coord_origin(self) -> aspose.pydrawing.Point:
        """The coordinates at the top-left corner of the containing block of this shape.
        
        The default value is (0,0)."""
        ...
    
    @coord_origin.setter
    def coord_origin(self, value: aspose.pydrawing.Point):
        ...
    
    @property
    def coord_size(self) -> aspose.pydrawing.Size:
        """The width and height of the coordinate space inside the containing block of this shape.
        
        The default value is (1000, 1000)."""
        ...
    
    @coord_size.setter
    def coord_size(self, value: aspose.pydrawing.Size):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of this object."""
        ...
    
    @property
    def is_signature_line(self) -> bool:
        """Indicates that shape is a :class:`SignatureLine`."""
        ...
    
    @property
    def is_layout_in_cell(self) -> bool:
        """Gets or sets a flag indicating whether the shape is displayed inside a table or outside of it.
        
        The default value is ``True``.
        
        Has effect only for top level shapes, the property :attr:`ShapeBase.wrap_type` of which is set to value
        other than :class:`aspose.words.Inline`."""
        ...
    
    @is_layout_in_cell.setter
    def is_layout_in_cell(self, value: bool):
        ...
    
    ...

class SignatureLine:
    """Provides access to signature line properties.
    To learn more, visit the `Work with Digital Signatures <https://docs.aspose.com/words/python-net/working-with-digital-signatures/>` documentation article."""
    
    @property
    def signer(self) -> str:
        """Gets or sets suggested signer of the signature line.
        Default value for this property is **empty string** ()."""
        ...
    
    @signer.setter
    def signer(self, value: str):
        ...
    
    @property
    def signer_title(self) -> str:
        """Gets or sets suggested signer's title (for example, Manager).
        Default value for this property is **empty string** ()."""
        ...
    
    @signer_title.setter
    def signer_title(self, value: str):
        ...
    
    @property
    def email(self) -> str:
        """Gets or sets suggested signer's e-mail address.
        Default value for this property is **empty string** ()."""
        ...
    
    @email.setter
    def email(self, value: str):
        ...
    
    @property
    def default_instructions(self) -> bool:
        """Gets or sets a value indicating that default instructions is shown in the Sign dialog.
        Default value for this property is ``True``."""
        ...
    
    @default_instructions.setter
    def default_instructions(self, value: bool):
        ...
    
    @property
    def instructions(self) -> str:
        """Gets or sets instructions to the signer that are displayed on signing the signature line.
        This property is ignored if :attr:`SignatureLine.default_instructions` is set.
        Default value for this property is **empty string** ()."""
        ...
    
    @instructions.setter
    def instructions(self, value: str):
        ...
    
    @property
    def allow_comments(self) -> bool:
        """Gets or sets a value indicating that the signer can add comments in the Sign dialog.
        Default value for this property is ``False``."""
        ...
    
    @allow_comments.setter
    def allow_comments(self, value: bool):
        ...
    
    @property
    def show_date(self) -> bool:
        """Gets or sets a value indicating that sign date is shown in the signature line.
        Default value for this property is ``True``."""
        ...
    
    @show_date.setter
    def show_date(self, value: bool):
        ...
    
    @property
    def id(self) -> uuid.UUID:
        """Gets or sets identifier for this signature line.
        This identifier can be associated with a digital signature, when signing document using :class:`aspose.words.digitalsignatures.DigitalSignatureUtil`.
        This value must be unique and by default it is randomly generated new Guid
        ()."""
        ...
    
    @id.setter
    def id(self, value: uuid.UUID):
        ...
    
    @property
    def provider_id(self) -> uuid.UUID:
        """Gets or sets signature provider identifier for this signature line.
        Default value is "{00000000-0000-0000-0000-000000000000}".
        
        The cryptographic service provider (CSP) is an independent software module that actually performs
        cryptography algorithms for authentication, encoding, and encryption. MS Office reserves the value
        of {00000000-0000-0000-0000-000000000000} for its default signature provider.
        
        The GUID of the additionally installed provider should be obtained from the documentation shipped with the provider.
        
        In addition, all the installed cryptographic providers are enumerated in windows registry.
        It can be found in the following path: HKLM\\SOFTWARE\\Microsoft\\Cryptography\\Defaults\\Provider.
        There is a key name "CP Service UUID" which corresponds to a GUID of signature provider."""
        ...
    
    @provider_id.setter
    def provider_id(self, value: uuid.UUID):
        ...
    
    @property
    def is_signed(self) -> bool:
        """Indicates that signature line is signed by digital signature."""
        ...
    
    @property
    def is_valid(self) -> bool:
        """Indicates that signature line is signed by digital signature and this digital signature is valid."""
        ...
    
    ...

class SoftEdgeFormat:
    """Represents the soft edge formatting for an object.
    
    Use the :attr:`ShapeBase.soft_edge` property to access soft edge properties of an object.
    You do not create instances of the :class:`SoftEdgeFormat` class directly."""
    
    def remove(self) -> None:
        """Removes :class:`SoftEdgeFormat` from the parent object."""
        ...
    
    @property
    def radius(self) -> float:
        """Gets or sets a double value that represents the length of the radius for a soft edge effect in points (pt).
        The default value is 0.0."""
        ...
    
    @radius.setter
    def radius(self, value: float):
        ...
    
    ...

class Stroke:
    """Defines a stroke for a shape.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article.
    
    Use the :attr:`Shape.stroke` property to access stroke properties of a shape.
    You do not create instances of the :class:`Stroke` class directly."""
    
    @property
    def on(self) -> bool:
        """Defines whether the path will be stroked.
        
        The default value for a :class:`Shape` is ``True``."""
        ...
    
    @on.setter
    def on(self, value: bool):
        ...
    
    @property
    def color(self) -> aspose.pydrawing.Color:
        """Defines the color of a stroke.
        
        The default value for a :class:`Shape` is
        aspose.pydrawing.Color.black."""
        ...
    
    @color.setter
    def color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def color2(self) -> aspose.pydrawing.Color:
        """Defines a second color for a stroke.
        
        The default value for a :class:`Shape` is
        aspose.pydrawing.Color.white."""
        ...
    
    @color2.setter
    def color2(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def fore_color(self) -> aspose.pydrawing.Color:
        """Gets or sets the foreground color of the stroke.
        
        The default value for a :class:`Shape` is
        aspose.pydrawing.Color.black."""
        ...
    
    @fore_color.setter
    def fore_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def base_fore_color(self) -> aspose.pydrawing.Color:
        """Gets the base foreground color of the stroke without any modifiers.
        
        The default value for a :class:`Shape` is
        aspose.pydrawing.Color.black."""
        ...
    
    @property
    def back_color(self) -> aspose.pydrawing.Color:
        """Gets or sets the background color of the stroke.
        
        The default value for a :class:`Shape` is
        aspose.pydrawing.Color.white."""
        ...
    
    @back_color.setter
    def back_color(self, value: aspose.pydrawing.Color):
        ...
    
    @property
    def fore_theme_color(self) -> aspose.words.themes.ThemeColor:
        """Gets or sets a ThemeColor object that represents the stroke foreground color."""
        ...
    
    @fore_theme_color.setter
    def fore_theme_color(self, value: aspose.words.themes.ThemeColor):
        ...
    
    @property
    def back_theme_color(self) -> aspose.words.themes.ThemeColor:
        """Gets or sets a ThemeColor object that represents the stroke background color."""
        ...
    
    @back_theme_color.setter
    def back_theme_color(self, value: aspose.words.themes.ThemeColor):
        ...
    
    @property
    def fore_tint_and_shade(self) -> float:
        """Gets or sets a double value that lightens or darkens the stroke foreground color.
        
        The allowed values are within the range from -1 (the darkest) to 1 (the lightest) for this property.
        Zero (0) is neutral. Attempting to set this property to a value less than -1 or more than 1
        results in System.ArgumentOutOfRangeException."""
        ...
    
    @fore_tint_and_shade.setter
    def fore_tint_and_shade(self, value: float):
        ...
    
    @property
    def back_tint_and_shade(self) -> float:
        """Gets or sets a double value that lightens or darkens the stroke background color.
        
        The allowed values are within the range from -1 (the darkest) to 1 (the lightest) for this property.
        Zero (0) is neutral. Attempting to set this property to a value less than -1 or more than 1
        results in System.ArgumentOutOfRangeException."""
        ...
    
    @back_tint_and_shade.setter
    def back_tint_and_shade(self, value: float):
        ...
    
    @property
    def visible(self) -> bool:
        """Gets or sets a flag indicating whether the stroke is visible.
        
        The default value for a :class:`Shape` is ``True``."""
        ...
    
    @visible.setter
    def visible(self, value: bool):
        ...
    
    @property
    def transparency(self) -> float:
        """Gets or sets a value between 0.0 (opaque) and 1.0 (clear) representing the degree of transparency
        of the stroke.
        
        The default value is 0."""
        ...
    
    @transparency.setter
    def transparency(self, value: float):
        ...
    
    @property
    def weight(self) -> float:
        """Defines the brush thickness that strokes the path of a shape in points.
        
        The default value for a :class:`Shape` is 0.75."""
        ...
    
    @weight.setter
    def weight(self, value: float):
        ...
    
    @property
    def dash_style(self) -> aspose.words.drawing.DashStyle:
        """Specifies the dot and dash pattern for a stroke.
        
        The default value is :attr:`DashStyle.SOLID`."""
        ...
    
    @dash_style.setter
    def dash_style(self, value: aspose.words.drawing.DashStyle):
        ...
    
    @property
    def join_style(self) -> aspose.words.drawing.JoinStyle:
        """Defines the join style of a polyline.
        
        The default value is :attr:`JoinStyle.ROUND`."""
        ...
    
    @join_style.setter
    def join_style(self, value: aspose.words.drawing.JoinStyle):
        ...
    
    @property
    def end_cap(self) -> aspose.words.drawing.EndCap:
        """Defines the cap style for the end of a stroke.
        
        The default value is :attr:`EndCap.FLAT`."""
        ...
    
    @end_cap.setter
    def end_cap(self, value: aspose.words.drawing.EndCap):
        ...
    
    @property
    def line_style(self) -> aspose.words.drawing.ShapeLineStyle:
        """Defines the line style of the stroke.
        
        The default value is :attr:`ShapeLineStyle.SINGLE`."""
        ...
    
    @line_style.setter
    def line_style(self, value: aspose.words.drawing.ShapeLineStyle):
        ...
    
    @property
    def start_arrow_type(self) -> aspose.words.drawing.ArrowType:
        """Defines the arrowhead for the start of a stroke.
        
        The default value is :attr:`ArrowType.NONE`."""
        ...
    
    @start_arrow_type.setter
    def start_arrow_type(self, value: aspose.words.drawing.ArrowType):
        ...
    
    @property
    def end_arrow_type(self) -> aspose.words.drawing.ArrowType:
        """Defines the arrowhead for the end of a stroke.
        
        The default value is :attr:`ArrowType.NONE`."""
        ...
    
    @end_arrow_type.setter
    def end_arrow_type(self, value: aspose.words.drawing.ArrowType):
        ...
    
    @property
    def start_arrow_width(self) -> aspose.words.drawing.ArrowWidth:
        """Defines the arrowhead width for the start of a stroke.
        
        The default value is :attr:`ArrowWidth.MEDIUM`."""
        ...
    
    @start_arrow_width.setter
    def start_arrow_width(self, value: aspose.words.drawing.ArrowWidth):
        ...
    
    @property
    def start_arrow_length(self) -> aspose.words.drawing.ArrowLength:
        """Defines the arrowhead length for the start of a stroke.
        
        The default value is :attr:`ArrowLength.MEDIUM`."""
        ...
    
    @start_arrow_length.setter
    def start_arrow_length(self, value: aspose.words.drawing.ArrowLength):
        ...
    
    @property
    def end_arrow_width(self) -> aspose.words.drawing.ArrowWidth:
        """Defines the arrowhead width for the end of a stroke.
        
        The default value is :attr:`ArrowWidth.MEDIUM`."""
        ...
    
    @end_arrow_width.setter
    def end_arrow_width(self, value: aspose.words.drawing.ArrowWidth):
        ...
    
    @property
    def end_arrow_length(self) -> aspose.words.drawing.ArrowLength:
        """Defines the arrowhead length for the end of a stroke.
        
        The default value is :attr:`ArrowLength.MEDIUM`."""
        ...
    
    @end_arrow_length.setter
    def end_arrow_length(self, value: aspose.words.drawing.ArrowLength):
        ...
    
    @property
    def opacity(self) -> float:
        """Defines the amount of transparency of a stroke. Valid range is from 0 to 1.
        
        The default value is 1."""
        ...
    
    @opacity.setter
    def opacity(self, value: float):
        ...
    
    @property
    def image_bytes(self) -> bytes:
        """Defines the image for a stroke image or pattern fill."""
        ...
    
    @property
    def fill(self) -> aspose.words.drawing.Fill:
        """Gets fill formatting for the :class:`Stroke`."""
        ...
    
    ...

class TextBox:
    """Defines attributes that specify how a text is displayed inside a shape.
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article.
    
    Use the :attr:`Shape.text_box` property to access text properties of a shape.
    You do not create instances of the :class:`TextBox` class directly."""
    
    def is_valid_link_target(self, target: aspose.words.drawing.TextBox) -> bool:
        """Determines whether this :class:`TextBox` can be linked to the target :class:`TextBox`."""
        ...
    
    def break_forward_link(self) -> None:
        """Breaks the link to the next :class:`TextBox`.
        
        :meth:`TextBox.break_forward_link` doesn't break all other links in the current sequence of shapes.
        For example: 1-2-3-4 sequence and :meth:`TextBox.break_forward_link` at the 2-nd textbox will create
        two sequences 1-2, 3-4."""
        ...
    
    @property
    def internal_margin_left(self) -> float:
        """Specifies the inner left margin in points for a shape.
        
        The default value is 1/10 inch."""
        ...
    
    @internal_margin_left.setter
    def internal_margin_left(self, value: float):
        ...
    
    @property
    def internal_margin_right(self) -> float:
        """Specifies the inner right margin in points for a shape.
        
        The default value is 1/10 inch."""
        ...
    
    @internal_margin_right.setter
    def internal_margin_right(self, value: float):
        ...
    
    @property
    def internal_margin_top(self) -> float:
        """Specifies the inner top margin in points for a shape.
        
        The default value is 1/20 inch."""
        ...
    
    @internal_margin_top.setter
    def internal_margin_top(self, value: float):
        ...
    
    @property
    def internal_margin_bottom(self) -> float:
        """Specifies the inner bottom margin in points for a shape.
        
        The default value is 1/20 inch."""
        ...
    
    @internal_margin_bottom.setter
    def internal_margin_bottom(self, value: float):
        ...
    
    @property
    def fit_shape_to_text(self) -> bool:
        """Determines whether Microsoft Word will grow the shape to fit text.
        
        The default value is ``False``."""
        ...
    
    @fit_shape_to_text.setter
    def fit_shape_to_text(self, value: bool):
        ...
    
    @property
    def layout_flow(self) -> aspose.words.drawing.LayoutFlow:
        """Determines the flow of the text layout in a shape.
        
        The default value is :attr:`LayoutFlow.HORIZONTAL`."""
        ...
    
    @layout_flow.setter
    def layout_flow(self, value: aspose.words.drawing.LayoutFlow):
        ...
    
    @property
    def text_box_wrap_mode(self) -> aspose.words.drawing.TextBoxWrapMode:
        """Determines how text wraps inside a shape.
        
        The default value is :attr:`TextBoxWrapMode.SQUARE`."""
        ...
    
    @text_box_wrap_mode.setter
    def text_box_wrap_mode(self, value: aspose.words.drawing.TextBoxWrapMode):
        ...
    
    @property
    def no_text_rotation(self) -> bool:
        """Gets or sets a boolean value indicating either text of the TextBox should not rotate when the shape is rotated.
        
        The default value is ``False``"""
        ...
    
    @no_text_rotation.setter
    def no_text_rotation(self, value: bool):
        ...
    
    @property
    def vertical_anchor(self) -> aspose.words.drawing.TextBoxAnchor:
        """Specifies the vertical alignment of the text within a shape.
        
        The default value is :attr:`TextBoxAnchor.TOP`."""
        ...
    
    @vertical_anchor.setter
    def vertical_anchor(self, value: aspose.words.drawing.TextBoxAnchor):
        ...
    
    @property
    def next(self) -> aspose.words.drawing.TextBox:
        """Returns or sets a :class:`TextBox` that represents the next :class:`TextBox` in a sequence of shapes."""
        ...
    
    @next.setter
    def next(self, value: aspose.words.drawing.TextBox):
        ...
    
    @property
    def previous(self) -> aspose.words.drawing.TextBox:
        """Returns a :class:`TextBox` that represents the previous :class:`TextBox` in a sequence of shapes."""
        ...
    
    @property
    def parent(self) -> aspose.words.drawing.Shape:
        """Gets a parent shape for the :class:`TextBox`."""
        ...
    
    ...

class TextPath:
    """Defines the text and formatting of the text path (of a WordArt object).
    To learn more, visit the `Working with Shapes <https://docs.aspose.com/words/python-net/working-with-shapes/>` documentation article.
    
    Use the :attr:`Shape.text_path` property to access WordArt properties of a shape.
    You do not create instances of the :class:`TextPath` class directly."""
    
    @property
    def on(self) -> bool:
        """Defines whether the text is displayed.
        
        The default value is ``False``."""
        ...
    
    @on.setter
    def on(self, value: bool):
        ...
    
    @property
    def fit_path(self) -> bool:
        """Defines whether the text fits the path of a shape.
        
        The default value is ``False``."""
        ...
    
    @fit_path.setter
    def fit_path(self, value: bool):
        ...
    
    @property
    def fit_shape(self) -> bool:
        """Defines whether the text fits bounding box of a shape.
        
        The default value is ``False``."""
        ...
    
    @fit_shape.setter
    def fit_shape(self, value: bool):
        ...
    
    @property
    def font_family(self) -> str:
        """Defines the family of the textpath font.
        
        The default value is Arial."""
        ...
    
    @font_family.setter
    def font_family(self, value: str):
        ...
    
    @property
    def size(self) -> float:
        """Defines the size of the font in points.
        
        The default value is 36."""
        ...
    
    @size.setter
    def size(self, value: float):
        ...
    
    @property
    def bold(self) -> bool:
        """True if the font is formatted as bold.
        
        The default value is ``False``."""
        ...
    
    @bold.setter
    def bold(self, value: bool):
        ...
    
    @property
    def italic(self) -> bool:
        """True if the font is formatted as italic.
        
        The default value is ``False``."""
        ...
    
    @italic.setter
    def italic(self, value: bool):
        ...
    
    @property
    def small_caps(self) -> bool:
        """True if the font is formatted as small capital letters.
        
        The default value is ``False``."""
        ...
    
    @small_caps.setter
    def small_caps(self, value: bool):
        ...
    
    @property
    def rotate_letters(self) -> bool:
        """Determines whether the letters of the text are rotated.
        
        The default value is ``False``."""
        ...
    
    @rotate_letters.setter
    def rotate_letters(self, value: bool):
        ...
    
    @property
    def trim(self) -> bool:
        """Determines whether extra space is removed above and below the text.
        
        The default value is ``False``."""
        ...
    
    @trim.setter
    def trim(self, value: bool):
        ...
    
    @property
    def kerning(self) -> bool:
        """Determines whether kerning is turned on.
        
        The default value is ``False``."""
        ...
    
    @kerning.setter
    def kerning(self, value: bool):
        ...
    
    @property
    def shadow(self) -> bool:
        """Defines whether a shadow is applied to the text on a text path.
        
        The default value is ``False``."""
        ...
    
    @shadow.setter
    def shadow(self, value: bool):
        ...
    
    @property
    def underline(self) -> bool:
        """True if the font is underlined.
        
        The default value is ``False``."""
        ...
    
    @underline.setter
    def underline(self, value: bool):
        ...
    
    @property
    def strike_through(self) -> bool:
        """True if the font is formatted as strikethrough text.
        
        The default value is ``False``."""
        ...
    
    @strike_through.setter
    def strike_through(self, value: bool):
        ...
    
    @property
    def same_letter_heights(self) -> bool:
        """Determines whether all letters will be the same height regardless of initial case.
        
        The default value is ``False``."""
        ...
    
    @same_letter_heights.setter
    def same_letter_heights(self, value: bool):
        ...
    
    @property
    def text(self) -> str:
        """Defines the text of the text path.
        
        The default value is an empty string."""
        ...
    
    @text.setter
    def text(self, value: str):
        ...
    
    @property
    def text_path_alignment(self) -> aspose.words.drawing.TextPathAlignment:
        """Defines the alignment of text.
        
        The default value is :attr:`TextPathAlignment.CENTER`."""
        ...
    
    @text_path_alignment.setter
    def text_path_alignment(self, value: aspose.words.drawing.TextPathAlignment):
        ...
    
    @property
    def reverse_rows(self) -> bool:
        """Determines whether the layout order of rows is reversed.
        
        The default value is ``False``.
        
        If ``True``, the layout order of rows is reversed. This attribute is used for vertical text layout."""
        ...
    
    @reverse_rows.setter
    def reverse_rows(self, value: bool):
        ...
    
    @property
    def spacing(self) -> float:
        """Defines the amount of spacing for text. 1 means 100%.
        
        The default value is 1."""
        ...
    
    @spacing.setter
    def spacing(self, value: float):
        ...
    
    @property
    def x_scale(self) -> bool:
        """Determines whether a straight textpath will be used instead of the shape path.
        
        The default value is ``False``.
        
        If ``True``, the text runs along a path from left to right along the x value of
        the lower boundary of the shape."""
        ...
    
    @x_scale.setter
    def x_scale(self, value: bool):
        ...
    
    ...

class ArrowLength(Enum):
    """Length of the arrow at the end of a line."""
    
    SHORT: int
    
    MEDIUM: int
    
    LONG: int
    
    """Same as :attr:`ArrowLength.SHORT`."""
    DEFAULT: int
    

class ArrowType(Enum):
    """Specifies the type of an arrow at a line end."""
    
    """The line does not have an arrow at the end."""
    NONE: int
    
    """The arrow is a solid triangle."""
    ARROW: int
    
    """The arrow is a "stealth" arrow."""
    STEALTH: int
    
    """The line end is a solid diamond."""
    DIAMOND: int
    
    """The line end is a solid oval."""
    OVAL: int
    
    """The arrow is an open arrow."""
    OPEN: int
    
    """Same as :attr:`ArrowType.NONE`."""
    DEFAULT: int
    

class ArrowWidth(Enum):
    """Width of the arrow at the end of a line."""
    
    NARROW: int
    
    MEDIUM: int
    
    WIDE: int
    
    """Same as :attr:`ArrowWidth.NARROW`."""
    DEFAULT: int
    

class DashStyle(Enum):
    """Dashed line style."""
    
    """Solid (continuous) pen."""
    SOLID: int
    
    """System dash style."""
    SHORT_DASH: int
    
    """System dash style."""
    SHORT_DOT: int
    
    """System dash style."""
    SHORT_DASH_DOT: int
    
    """System dash style."""
    SHORT_DASH_DOT_DOT: int
    
    """Square dot style."""
    DOT: int
    
    """Dash style."""
    DASH: int
    
    """Long dash style."""
    LONG_DASH: int
    
    """Dash short dash."""
    DASH_DOT: int
    
    """Long dash short dash."""
    LONG_DASH_DOT: int
    
    """Long dash short dash short dash."""
    LONG_DASH_DOT_DOT: int
    
    """Same as :attr:`DashStyle.SOLID`."""
    DEFAULT: int
    

class EndCap(Enum):
    """Specifies line cap style."""
    
    """Rounded ends."""
    ROUND: int
    
    """Square protrudes by half line width."""
    SQUARE: int
    
    """Line ends at end point."""
    FLAT: int
    
    """Default value is :attr:`EndCap.FLAT`."""
    DEFAULT: int
    

class FillType(Enum):
    """Specifies fill type for a fillable object."""
    
    """Solid fill."""
    SOLID: int
    
    """Patterned fill."""
    PATTERNED: int
    
    """Gradient fill."""
    GRADIENT: int
    
    """Textured fill."""
    TEXTURED: int
    
    """Fill is the same as the background."""
    BACKGROUND: int
    
    """Picture fill."""
    PICTURE: int
    

class FlipOrientation(Enum):
    """Possible values for the orientation of a shape."""
    
    """Coordinates are not flipped."""
    NONE: int
    
    """Flip along the y-axis, reversing the x-coordinates."""
    HORIZONTAL: int
    
    """Flip along the x-axis, reversing the y-coordinates."""
    VERTICAL: int
    
    """Flip along both the y- and x-axis."""
    BOTH: int
    

class GradientStyle(Enum):
    """Specifies the style for a gradient fill."""
    
    """No gradient."""
    NONE: int
    
    """Gradient running horizontally across an object."""
    HORIZONTAL: int
    
    """Gradient running vertically down an object."""
    VERTICAL: int
    
    """Diagonal gradient moving from a bottom corner up to the opposite corner."""
    DIAGONAL_UP: int
    
    """Diagonal gradient moving from a top corner down to the opposite corner."""
    DIAGONAL_DOWN: int
    
    """Gradient running from a corner to the other three corners."""
    FROM_CORNER: int
    
    """Gradient running from the center out to the corners."""
    FROM_CENTER: int
    

class GradientVariant(Enum):
    """Specifies the variant for a gradient fill.
    
    Corresponds to the four variants on the Gradient tab in the Fill Effects dialog box in Word."""
    
    """Gradient variant 'None'."""
    NONE: int
    
    """Gradient variant 1."""
    VARIANT1: int
    
    """Gradient variant 2."""
    VARIANT2: int
    
    """Gradient variant 3.
    
    This variant is not applicable to gradient fill with the style :attr:`GradientStyle.FROM_CENTER`,
    if object has markup language :attr:`ShapeMarkupLanguage.VML`."""
    VARIANT3: int
    
    """Gradient variant 4.
    
    This variant is not applicable to gradient fill with the style :attr:`GradientStyle.FROM_CENTER`,
    if object has markup language :attr:`ShapeMarkupLanguage.VML`."""
    VARIANT4: int
    

class HorizontalAlignment(Enum):
    """Specifies horizontal alignment of a floating shape, text frame or floating table."""
    
    """The object is explicitly positioned, usually using its **Left** property."""
    NONE: int
    
    """Same as :attr:`HorizontalAlignment.NONE`."""
    DEFAULT: int
    
    """Specifies that the object shall be left aligned to the horizontal alignment base."""
    LEFT: int
    
    """Specifies that the object shall be centered with respect to the horizontal alignment base."""
    CENTER: int
    
    """Specifies that the object shall be right aligned to the horizontal alignment base."""
    RIGHT: int
    
    """Specifies that the object shall be inside of the horizontal alignment base."""
    INSIDE: int
    
    """Specifies that the object shall be outside of the horizontal alignment base."""
    OUTSIDE: int
    

class HorizontalRuleAlignment(Enum):
    """Represents the alignment for the specified horizontal rule."""
    
    """Aligned to the left."""
    LEFT: int
    
    """Aligned to the center."""
    CENTER: int
    
    """Aligned to the right."""
    RIGHT: int
    

class ImageType(Enum):
    """Specifies the type (format) of an image in a Microsoft Word document."""
    
    """The is no image data."""
    NO_IMAGE: int
    
    """An unknown image type or image type that cannot be directly stored inside a Microsoft Word document."""
    UNKNOWN: int
    
    """Windows Enhanced Metafile."""
    EMF: int
    
    """Windows Metafile."""
    WMF: int
    
    """Macintosh PICT. An existing image will be preserved in a document, but inserting new
    PICT images into a document is not supported."""
    PICT: int
    
    """JPEG JFIF."""
    JPEG: int
    
    """Portable Network Graphics."""
    PNG: int
    
    """Windows Bitmap."""
    BMP: int
    
    """Encapsulated PostScript."""
    EPS: int
    
    """WebP."""
    WEB_P: int
    
    """GIF"""
    GIF: int
    

class JoinStyle(Enum):
    """Line join style."""
    
    """Join edges by a straight line."""
    BEVEL: int
    
    """Extend edges until they join."""
    MITER: int
    
    """Draw an arc between the two edges."""
    ROUND: int
    

class LayoutFlow(Enum):
    """Determines the flow of the text layout in a textbox."""
    
    """Text is displayed horizontally."""
    HORIZONTAL: int
    
    """Ideographic text is displayed vertically."""
    TOP_TO_BOTTOM_IDEOGRAPHIC: int
    
    """Text is displayed vertically."""
    BOTTOM_TO_TOP: int
    
    """Text is displayed vertically."""
    TOP_TO_BOTTOM: int
    
    """Ideographic text is displayed horizontally."""
    HORIZONTAL_IDEOGRAPHIC: int
    
    """Text is displayed vertically."""
    VERTICAL: int
    

class PatternType(Enum):
    """Specifies the fill pattern to be used to fill a shape."""
    
    """No pattern."""
    NONE: int
    
    """10% of the foreground color."""
    PERCENT10: int
    
    """20% of the foreground color."""
    PERCENT20: int
    
    """25% of the foreground color."""
    PERCENT25: int
    
    """30% of the foreground color."""
    PERCENT30: int
    
    """40% of the foreground color"""
    PERCENT40: int
    
    """50% of the foreground color"""
    PERCENT50: int
    
    """5% of the foreground color."""
    PERCENT5: int
    
    """60% of the foreground color."""
    PERCENT60: int
    
    """70% of the foreground color."""
    PERCENT70: int
    
    """75% of the foreground color."""
    PERCENT75: int
    
    """80% of the foreground color."""
    PERCENT80: int
    
    """90% of the foreground color."""
    PERCENT90: int
    
    """Cross."""
    CROSS: int
    
    """Dark downward diagonal."""
    DARK_DOWNWARD_DIAGONAL: int
    
    """Dark horizontal."""
    DARK_HORIZONTAL: int
    
    """Dark upward diagonal."""
    DARK_UPWARD_DIAGONAL: int
    
    """Dark vertical."""
    DARK_VERTICAL: int
    
    """Dashed downward diagonal."""
    DASHED_DOWNWARD_DIAGONAL: int
    
    """Dashed horizontal."""
    DASHED_HORIZONTAL: int
    
    """Dashed upward diagonal."""
    DASHED_UPWARD_DIAGONAL: int
    
    """Dashed vertical."""
    DASHED_VERTICAL: int
    
    """Diagonal brick."""
    DIAGONAL_BRICK: int
    
    """Diagonal cross."""
    DIAGONAL_CROSS: int
    
    """Pattern divot."""
    DIVOT: int
    
    """Dotted diamond."""
    DOTTED_DIAMOND: int
    
    """Dotted grid."""
    DOTTED_GRID: int
    
    """Downward diagonal."""
    DOWNWARD_DIAGONAL: int
    
    """Horizontal."""
    HORIZONTAL: int
    
    """Horizontal brick."""
    HORIZONTAL_BRICK: int
    
    """Large checker board."""
    LARGE_CHECKER_BOARD: int
    
    """Large confetti."""
    LARGE_CONFETTI: int
    
    """Large grid."""
    LARGE_GRID: int
    
    """Light downward diagonal."""
    LIGHT_DOWNWARD_DIAGONAL: int
    
    """Light horizontal."""
    LIGHT_HORIZONTAL: int
    
    """Light upward diagonal."""
    LIGHT_UPWARD_DIAGONAL: int
    
    """Light vertical."""
    LIGHT_VERTICAL: int
    
    """Narrow horizontal."""
    NARROW_HORIZONTAL: int
    
    """Narrow vertical."""
    NARROW_VERTICAL: int
    
    """Outlined diamond."""
    OUTLINED_DIAMOND: int
    
    """Plaid."""
    PLAID: int
    
    """Shingle."""
    SHINGLE: int
    
    """Small checker board."""
    SMALL_CHECKER_BOARD: int
    
    """Small confetti."""
    SMALL_CONFETTI: int
    
    """Small grid."""
    SMALL_GRID: int
    
    """Solid diamond."""
    SOLID_DIAMOND: int
    
    """Sphere."""
    SPHERE: int
    
    """Trellis."""
    TRELLIS: int
    
    """Upward diagonal."""
    UPWARD_DIAGONAL: int
    
    """Vertical."""
    VERTICAL: int
    
    """Wave."""
    WAVE: int
    
    """Weave."""
    WEAVE: int
    
    """Wide downward diagonal."""
    WIDE_DOWNWARD_DIAGONAL: int
    
    """Wide upward diagonal."""
    WIDE_UPWARD_DIAGONAL: int
    
    """Zig zag."""
    ZIG_ZAG: int
    

class PresetTexture(Enum):
    """Specifies texture to be used to fill a shape."""
    
    """No Texture."""
    NONE: int
    
    """Blue tissue paper texture."""
    BLUE_TISSUE_PAPER: int
    
    """Bouquet texture."""
    BOUQUET: int
    
    """Brown marble texture."""
    BROWN_MARBLE: int
    
    """Canvas texture."""
    CANVAS: int
    
    """Cork texture."""
    CORK: int
    
    """Denim texture."""
    DENIM: int
    
    """Fish fossil texture."""
    FISH_FOSSIL: int
    
    """Granite texture."""
    GRANITE: int
    
    """Green marble texture."""
    GREEN_MARBLE: int
    
    """Medium wood texture."""
    MEDIUM_WOOD: int
    
    """Newsprint texture."""
    NEWSPRINT: int
    
    """Oak texture."""
    OAK: int
    
    """Paper bag texture."""
    PAPER_BAG: int
    
    """Papyrus texture."""
    PAPYRUS: int
    
    """Parchment texture."""
    PARCHMENT: int
    
    """Pink tissue paper texture."""
    PINK_TISSUE_PAPER: int
    
    """Purple mesh texture."""
    PURPLE_MESH: int
    
    """Recycled paper texture."""
    RECYCLED_PAPER: int
    
    """Sand texture."""
    SAND: int
    
    """Stationery texture."""
    STATIONERY: int
    
    """Walnut texture."""
    WALNUT: int
    
    """Water droplets texture."""
    WATER_DROPLETS: int
    
    """White marble texture."""
    WHITE_MARBLE: int
    
    """Woven mat texture."""
    WOVEN_MAT: int
    

class RelativeHorizontalPosition(Enum):
    """Specifies to what the horizontal position of a shape or text frame is relative."""
    
    """Specifies that the horizontal positioning shall be relative to the page margins."""
    MARGIN: int
    
    """The object is positioned relative to the left edge of the page."""
    PAGE: int
    
    """The object is positioned relative to the left side of the column."""
    COLUMN: int
    
    """The object is positioned relative to the left side of the paragraph."""
    CHARACTER: int
    
    """Specifies that the horizontal positioning shall be relative to the left margin of the page."""
    LEFT_MARGIN: int
    
    """Specifies that the horizontal positioning shall be relative to the right margin of the page."""
    RIGHT_MARGIN: int
    
    """Specifies that the horizontal positioning shall be relative to the inside margin of the
    current page (the left margin on odd pages, right on even pages)."""
    INSIDE_MARGIN: int
    
    """Specifies that the horizontal positioning shall be relative to the outside margin of the
    current page (the right margin on odd pages, left on even pages)."""
    OUTSIDE_MARGIN: int
    
    """Default value is :attr:`RelativeHorizontalPosition.COLUMN`."""
    DEFAULT: int
    

class RelativeHorizontalSize(Enum):
    """Specifies relatively to what the width of a shape or a text frame is calculated horizontally."""
    
    """Specifies that the width is calculated relatively to the space between the left and the right margins."""
    MARGIN: int
    
    """Specifies that the width is calculated relatively to the page width."""
    PAGE: int
    
    """Specifies that the width is calculated relatively to the left margin area size."""
    LEFT_MARGIN: int
    
    """Specifies that the width is calculated relatively to the right margin area size."""
    RIGHT_MARGIN: int
    
    """Specifies that the width is calculated relatively to the inside margin area size,
    to the left margin area size for odd pages and to the right margin area size for even pages."""
    INNER_MARGIN: int
    
    """Specifies that the width is calculated relatively to the outside margin area size,
    to the right margin area size for odd pages and to the left margin area size for even pages."""
    OUTER_MARGIN: int
    
    """Default value is :attr:`RelativeHorizontalSize.MARGIN`."""
    DEFAULT: int
    

class RelativeVerticalPosition(Enum):
    """Specifies to what the vertical position of a shape or text frame is relative."""
    
    """Specifies that the vertical positioning shall be relative to the page margins."""
    MARGIN: int
    
    """The object is positioned relative to the top edge of the page."""
    PAGE: int
    
    """The object is positioned relative to the top of the paragraph that contains the anchor."""
    PARAGRAPH: int
    
    """Undocumented."""
    LINE: int
    
    """Specifies that the vertical positioning shall be relative to the top margin of the current page."""
    TOP_MARGIN: int
    
    """Specifies that the vertical positioning shall be relative to the bottom margin of the current page."""
    BOTTOM_MARGIN: int
    
    """Specifies that the vertical positioning shall be relative to the inside margin of the current page."""
    INSIDE_MARGIN: int
    
    """Specifies that the vertical positioning shall be relative to the outside margin of the current page."""
    OUTSIDE_MARGIN: int
    
    """Default value is :attr:`RelativeVerticalPosition.MARGIN`."""
    TABLE_DEFAULT: int
    
    """Default value is :attr:`RelativeVerticalPosition.PARAGRAPH`."""
    TEXT_FRAME_DEFAULT: int
    

class RelativeVerticalSize(Enum):
    """Specifies relatively to what the height of a shape or a text frame is calculated vertically."""
    
    """Specifies that the height is calculated relatively to the space between the top and the bottom margins."""
    MARGIN: int
    
    """Specifies that the height is calculated relatively to the page height."""
    PAGE: int
    
    """Specifies that the height is calculated relatively to the top margin area size."""
    TOP_MARGIN: int
    
    """Specifies that the height is calculated relatively to the bottom margin area size."""
    BOTTOM_MARGIN: int
    
    """Specifies that the height is calculated relatively to the inside margin area size,
    to the top margin area size for odd pages and to the bottom margin area size for even pages."""
    INNER_MARGIN: int
    
    """Specifies that the height is calculated relatively to the outside margin area size,
    to the bottom margin area size for odd pages and to the top margin area size for even pages."""
    OUTER_MARGIN: int
    
    """Default value is :attr:`RelativeVerticalSize.MARGIN`."""
    DEFAULT: int
    

class ShadowType(Enum):
    """Specifies the type of a shape shadow.
    
    ShadowType is not a simple attribute, but a preset that sets at once several attributes which form the
    shadow appearance."""
    
    """None of predefined shadow presets."""
    SHADOW_MIXED: int
    
    """First shadow type."""
    SHADOW1: int
    
    """Tenth shadow type."""
    SHADOW10: int
    
    """Eleventh shadow type."""
    SHADOW11: int
    
    """Twelfth shadow type."""
    SHADOW12: int
    
    """Thirteenth shadow type."""
    SHADOW13: int
    
    """Fourteenth shadow type."""
    SHADOW14: int
    
    """Fifteenth shadow type."""
    SHADOW15: int
    
    """Sixteenth shadow type."""
    SHADOW16: int
    
    """Seventeenth shadow type."""
    SHADOW17: int
    
    """Eighteenth shadow type."""
    SHADOW18: int
    
    """Nineteenth shadow type."""
    SHADOW19: int
    
    """Second shadow type."""
    SHADOW2: int
    
    """Twentieth shadow type."""
    SHADOW20: int
    
    """Twenty first shadow type."""
    SHADOW21: int
    
    """Twenty second shadow type."""
    SHADOW22: int
    
    """Twenty third shadow type."""
    SHADOW23: int
    
    """Twenty forth shadow type."""
    SHADOW24: int
    
    """Twenty fifth shadow type."""
    SHADOW25: int
    
    """Twenty sixth shadow type."""
    SHADOW26: int
    
    """Twenty seventh shadow type."""
    SHADOW27: int
    
    """Twenty eighth shadow type."""
    SHADOW28: int
    
    """Twenty ninth shadow type."""
    SHADOW29: int
    
    """Third shadow type."""
    SHADOW3: int
    
    """Thirtieth shadow type."""
    SHADOW30: int
    
    """Thirty first shadow type."""
    SHADOW31: int
    
    """Thirty second shadow type."""
    SHADOW32: int
    
    """Thirty third shadow type."""
    SHADOW33: int
    
    """Thirty forth shadow type."""
    SHADOW34: int
    
    """Thirty fifth shadow type."""
    SHADOW35: int
    
    """Thirty sixth shadow type."""
    SHADOW36: int
    
    """Thirty seventh shadow type."""
    SHADOW37: int
    
    """Thirty eighth shadow type."""
    SHADOW38: int
    
    """Thirty ninth shadow type."""
    SHADOW39: int
    
    """Fourth shadow type."""
    SHADOW4: int
    
    """Fortieth shadow type."""
    SHADOW40: int
    
    """Forty first shadow type."""
    SHADOW41: int
    
    """Forty second shadow type."""
    SHADOW42: int
    
    """Forty third shadow type."""
    SHADOW43: int
    
    """Fifth shadow type."""
    SHADOW5: int
    
    """Sixth shadow type."""
    SHADOW6: int
    
    """Seventh shadow type."""
    SHADOW7: int
    
    """Eighth shadow type."""
    SHADOW8: int
    
    """Ninth shadow type."""
    SHADOW9: int
    

class ShapeLineStyle(Enum):
    """Specifies the compound line style of a :class:`Shape`."""
    
    """Single line."""
    SINGLE: int
    
    """Double lines of equal width."""
    DOUBLE: int
    
    """Double lines, one thick, one thin."""
    THICK_THIN: int
    
    """Double lines, one thin, one thick."""
    THIN_THICK: int
    
    """Three lines, thin, thick, thin."""
    TRIPLE: int
    
    """Default value is :attr:`ShapeLineStyle.SINGLE`."""
    DEFAULT: int
    

class ShapeMarkupLanguage(Enum):
    """Specifies Markup language used for the shape."""
    
    """Drawing Markup Language is used to define the shape.
    
    This is the new standard for drawing for Office Open XML which has appeared first in ECMA-376 1st edition (2006), first appeared in MS Word 2007."""
    DML: int
    
    """Vector Markup Language is used to define the shape.
    
    A deprecated format included in Office Open XML for legacy reasons only."""
    VML: int
    

class ShapeTextOrientation(Enum):
    """Specifies orientation of text in shapes."""
    
    """Text is arranged horizontally (lr-tb)."""
    HORIZONTAL: int
    
    """Text is rotated 90 degrees to the right to appear from top to bottom (tb-rl)."""
    DOWNWARD: int
    
    """Text is rotated 90 degrees to the left to appear from bottom to top (bt-lr)."""
    UPWARD: int
    
    """Far East characters appear vertical, other text is rotated 90 degrees
    to the right to appear from top to bottom (tb-rl-v)."""
    VERTICAL_FAR_EAST: int
    
    """Far East characters appear vertical, other text is rotated 90 degrees
    to the right to appear from top to bottom vertically, then left to right horizontally  (tb-lr-v)."""
    VERTICAL_ROTATED_FAR_EAST: int
    
    """Text is vertical, with one letter on top of the other."""
    WORD_ART_VERTICAL: int
    
    """Text is vertical, with one letter on top of the other, then right to left horizontally."""
    WORD_ART_VERTICAL_RIGHT_TO_LEFT: int
    

class ShapeType(Enum):
    """Specifies the type of shape in a Microsoft Word document."""
    
    """The shape is an image."""
    IMAGE: int
    
    """The shape is a textbox. Note that shapes of many other types can also have text inside them too.
    A shape does not have to have this type to contain text."""
    TEXT_BOX: int
    
    """The shape is a group shape."""
    GROUP: int
    
    """The shape is an OLE object.
    You cannot create shapes of this type in the document."""
    OLE_OBJECT: int
    
    """The shape is an ActiveX control.
    You cannot create shapes of this type in the document."""
    OLE_CONTROL: int
    
    """A shape drawn by user and consisting of multiple segments and/or vertices (curve, freeform or scribble).
    You cannot create shapes of this type in the document."""
    NON_PRIMITIVE: int
    
    """Rectangle."""
    RECTANGLE: int
    
    """Round rectangle."""
    ROUND_RECTANGLE: int
    
    """Ellipse."""
    ELLIPSE: int
    
    """Diamond."""
    DIAMOND: int
    
    """Triangle."""
    TRIANGLE: int
    
    """Right triangle."""
    RIGHT_TRIANGLE: int
    
    """Parallelogram."""
    PARALLELOGRAM: int
    
    """Trapezoid."""
    TRAPEZOID: int
    
    """Hexagon."""
    HEXAGON: int
    
    """Octagon."""
    OCTAGON: int
    
    """Plus."""
    PLUS: int
    
    """Star."""
    STAR: int
    
    """Arrow."""
    ARROW: int
    
    """Thick arrow."""
    THICK_ARROW: int
    
    """Home plate."""
    HOME_PLATE: int
    
    """Cube."""
    CUBE: int
    
    """Balloon."""
    BALLOON: int
    
    """Seal."""
    SEAL: int
    
    """Arc."""
    ARC: int
    
    """Line."""
    LINE: int
    
    """Plaque."""
    PLAQUE: int
    
    """Can."""
    CAN: int
    
    """Donut."""
    DONUT: int
    
    """Text simple."""
    TEXT_SIMPLE: int
    
    """Text octagon."""
    TEXT_OCTAGON: int
    
    """Text hexagon."""
    TEXT_HEXAGON: int
    
    """Text curve."""
    TEXT_CURVE: int
    
    """Text wave."""
    TEXT_WAVE: int
    
    """Text ring."""
    TEXT_RING: int
    
    """Text on curve."""
    TEXT_ON_CURVE: int
    
    """Text on ring."""
    TEXT_ON_RING: int
    
    """A straight connector shape."""
    STRAIGHT_CONNECTOR1: int
    
    """A bent connector shape with two segments."""
    BENT_CONNECTOR2: int
    
    """A bent connector shape with three segments."""
    BENT_CONNECTOR3: int
    
    """A bent connector shape with four segments."""
    BENT_CONNECTOR4: int
    
    """A bent connector shape with five segments."""
    BENT_CONNECTOR5: int
    
    """A curved connector shape with two segments."""
    CURVED_CONNECTOR2: int
    
    """A curved connector shape with three segments."""
    CURVED_CONNECTOR3: int
    
    """A curved connector shape with four segments."""
    CURVED_CONNECTOR4: int
    
    """A curved connector shape with five segments."""
    CURVED_CONNECTOR5: int
    
    """A callout shape with one arrow."""
    CALLOUT1: int
    
    """A callout shape with two arrows."""
    CALLOUT2: int
    
    """A callout shape with three arrows."""
    CALLOUT3: int
    
    """An accent callout shape with one arrow."""
    ACCENT_CALLOUT1: int
    
    """An accent callout shape with two arrows."""
    ACCENT_CALLOUT2: int
    
    """An accent callout shape with three arrows."""
    ACCENT_CALLOUT3: int
    
    """Border callout 1."""
    BORDER_CALLOUT1: int
    
    """Border callout 2."""
    BORDER_CALLOUT2: int
    
    """Border callout 3."""
    BORDER_CALLOUT3: int
    
    """Accent border callout 1."""
    ACCENT_BORDER_CALLOUT1: int
    
    """Accent border callout 2."""
    ACCENT_BORDER_CALLOUT2: int
    
    """Accent border callout 3."""
    ACCENT_BORDER_CALLOUT3: int
    
    """Ribbon."""
    RIBBON: int
    
    """Ribbon 2."""
    RIBBON2: int
    
    """Chevron."""
    CHEVRON: int
    
    """Pentagon."""
    PENTAGON: int
    
    """NoSmoking."""
    NO_SMOKING: int
    
    """Eight-pointed star."""
    SEAL8: int
    
    """16-pointed star."""
    SEAL16: int
    
    """32-pointed star."""
    SEAL32: int
    
    """Wedge rect callout."""
    WEDGE_RECT_CALLOUT: int
    
    """Wedge R rect callout."""
    WEDGE_R_RECT_CALLOUT: int
    
    """Wedge ellipse callout."""
    WEDGE_ELLIPSE_CALLOUT: int
    
    """Wave."""
    WAVE: int
    
    """Folded corner."""
    FOLDED_CORNER: int
    
    """Left arrow."""
    LEFT_ARROW: int
    
    """Down arrow."""
    DOWN_ARROW: int
    
    """Up arrow."""
    UP_ARROW: int
    
    """Left right arrow."""
    LEFT_RIGHT_ARROW: int
    
    """Up down arrow."""
    UP_DOWN_ARROW: int
    
    """Irregular seal 1."""
    IRREGULAR_SEAL1: int
    
    """Irregular seal 2."""
    IRREGULAR_SEAL2: int
    
    """Lightning bolt."""
    LIGHTNING_BOLT: int
    
    """Heart."""
    HEART: int
    
    """Quad arrow."""
    QUAD_ARROW: int
    
    """Left arrow callout."""
    LEFT_ARROW_CALLOUT: int
    
    """Right arrow callout"""
    RIGHT_ARROW_CALLOUT: int
    
    """Up arrow callout."""
    UP_ARROW_CALLOUT: int
    
    """Down arrow callout."""
    DOWN_ARROW_CALLOUT: int
    
    """Left right arrow callout."""
    LEFT_RIGHT_ARROW_CALLOUT: int
    
    """Up down arrow callout."""
    UP_DOWN_ARROW_CALLOUT: int
    
    """Quad arrow callout."""
    QUAD_ARROW_CALLOUT: int
    
    """Bevel."""
    BEVEL: int
    
    """Left bracket."""
    LEFT_BRACKET: int
    
    """Right bracket."""
    RIGHT_BRACKET: int
    
    """Left brace."""
    LEFT_BRACE: int
    
    """Right brace."""
    RIGHT_BRACE: int
    
    """Left up arrow."""
    LEFT_UP_ARROW: int
    
    """Bent up arrow."""
    BENT_UP_ARROW: int
    
    """Bent arrow."""
    BENT_ARROW: int
    
    """24-pointed star."""
    SEAL24: int
    
    """Striped right arrow."""
    STRIPED_RIGHT_ARROW: int
    
    """Notched right arrow."""
    NOTCHED_RIGHT_ARROW: int
    
    """Block arc."""
    BLOCK_ARC: int
    
    """Smiley face."""
    SMILEY_FACE: int
    
    """Vertical scroll."""
    VERTICAL_SCROLL: int
    
    """Horizontal scroll."""
    HORIZONTAL_SCROLL: int
    
    """Circular arrow."""
    CIRCULAR_ARROW: int
    
    """This shape type seems to be set for shapes that are not part of the standard set of the
    auto shapes in Microsoft Word. For example, if you insert a new auto shape from ClipArt.
    You cannot create shapes of this type in the document."""
    CUSTOM_SHAPE: int
    
    """Uturn arrow."""
    UTURN_ARROW: int
    
    """Curved right arrow."""
    CURVED_RIGHT_ARROW: int
    
    """Curved left arrow."""
    CURVED_LEFT_ARROW: int
    
    """Curved up arrow"""
    CURVED_UP_ARROW: int
    
    """Curved down arrow."""
    CURVED_DOWN_ARROW: int
    
    """Cloud callout."""
    CLOUD_CALLOUT: int
    
    """Ellipse ribbon."""
    ELLIPSE_RIBBON: int
    
    """Ellipse ribbon 2."""
    ELLIPSE_RIBBON2: int
    
    """Flow chart process."""
    FLOW_CHART_PROCESS: int
    
    """Flow chart decision."""
    FLOW_CHART_DECISION: int
    
    """Flow chart input output."""
    FLOW_CHART_INPUT_OUTPUT: int
    
    """Flow chart predefined process"""
    FLOW_CHART_PREDEFINED_PROCESS: int
    
    """Flow chart internal storage."""
    FLOW_CHART_INTERNAL_STORAGE: int
    
    """Flow chart document."""
    FLOW_CHART_DOCUMENT: int
    
    """Flow chart multi document."""
    FLOW_CHART_MULTIDOCUMENT: int
    
    """Flow chart terminator."""
    FLOW_CHART_TERMINATOR: int
    
    """Flow chart preparation."""
    FLOW_CHART_PREPARATION: int
    
    """Flow chart manual input."""
    FLOW_CHART_MANUAL_INPUT: int
    
    """Flow chart manual operation."""
    FLOW_CHART_MANUAL_OPERATION: int
    
    """Flow chart connector."""
    FLOW_CHART_CONNECTOR: int
    
    """Flow chart punched card."""
    FLOW_CHART_PUNCHED_CARD: int
    
    """Flow chart punched tape."""
    FLOW_CHART_PUNCHED_TAPE: int
    
    """Flow chart summing junction."""
    FLOW_CHART_SUMMING_JUNCTION: int
    
    """Flow chart or."""
    FLOW_CHART_OR: int
    
    """Flow chart collate."""
    FLOW_CHART_COLLATE: int
    
    """Flow chart sort."""
    FLOW_CHART_SORT: int
    
    """Flow chart extract."""
    FLOW_CHART_EXTRACT: int
    
    """Flow chart merge."""
    FLOW_CHART_MERGE: int
    
    """Flow chart off-line storage."""
    FLOW_CHART_OFFLINE_STORAGE: int
    
    """Flow chart on-line storage."""
    FLOW_CHART_ONLINE_STORAGE: int
    
    """Flow char magnetic tape."""
    FLOW_CHART_MAGNETIC_TAPE: int
    
    """Flow chart magnetic disk."""
    FLOW_CHART_MAGNETIC_DISK: int
    
    """Flow chart magnetic drum."""
    FLOW_CHART_MAGNETIC_DRUM: int
    
    """Flow chart display."""
    FLOW_CHART_DISPLAY: int
    
    """Flow chart delay."""
    FLOW_CHART_DELAY: int
    
    """Plain-text, WordArt object."""
    TEXT_PLAIN_TEXT: int
    
    """Stop, WordArt object."""
    TEXT_STOP: int
    
    """Triangle, WordArt object."""
    TEXT_TRIANGLE: int
    
    """Triangle inverted, WordArt object."""
    TEXT_TRIANGLE_INVERTED: int
    
    """Chevron, WordArt object."""
    TEXT_CHEVRON: int
    
    """Chevron inverted, WordArt object."""
    TEXT_CHEVRON_INVERTED: int
    
    """Ring inside, WordArt object."""
    TEXT_RING_INSIDE: int
    
    """Ring outside, WordArt object."""
    TEXT_RING_OUTSIDE: int
    
    """Arch up curve, WordArt object."""
    TEXT_ARCH_UP_CURVE: int
    
    """Arch down curve, WordArt object."""
    TEXT_ARCH_DOWN_CURVE: int
    
    """Circle curve, WordArt object."""
    TEXT_CIRCLE_CURVE: int
    
    """Button curve, WordArt object."""
    TEXT_BUTTON_CURVE: int
    
    """Arch up pour, WordArt object."""
    TEXT_ARCH_UP_POUR: int
    
    """Arch down pour, WordArt object."""
    TEXT_ARCH_DOWN_POUR: int
    
    """Circle pour, WordArt object."""
    TEXT_CIRCLE_POUR: int
    
    """Button pour, WordArt object."""
    TEXT_BUTTON_POUR: int
    
    """Curve up, WordArt object."""
    TEXT_CURVE_UP: int
    
    """Curve down, WordArt object."""
    TEXT_CURVE_DOWN: int
    
    """Cascade up, WordArt object."""
    TEXT_CASCADE_UP: int
    
    """Cascade down, WordArt object."""
    TEXT_CASCADE_DOWN: int
    
    """Wave 1, WordArt object."""
    TEXT_WAVE1: int
    
    """Wave 2, WordArt object."""
    TEXT_WAVE2: int
    
    """Wave 3, WordArt object."""
    TEXT_WAVE3: int
    
    """Wave 4, WordArt object."""
    TEXT_WAVE4: int
    
    """Inflate, WordArt object."""
    TEXT_INFLATE: int
    
    """Deflate, WordArt object."""
    TEXT_DEFLATE: int
    
    """Inflate bottom, WordArt object."""
    TEXT_INFLATE_BOTTOM: int
    
    """Deflate bottom, WordArt object."""
    TEXT_DEFLATE_BOTTOM: int
    
    """Inflate top, WordArt object."""
    TEXT_INFLATE_TOP: int
    
    """Deflate top, WordArt object."""
    TEXT_DEFLATE_TOP: int
    
    """Deflate inflate, WordArt object."""
    TEXT_DEFLATE_INFLATE: int
    
    """Deflate inflate deflate, WordArt object."""
    TEXT_DEFLATE_INFLATE_DEFLATE: int
    
    """Fade right, WordArt object."""
    TEXT_FADE_RIGHT: int
    
    """Fade left, WordArt object."""
    TEXT_FADE_LEFT: int
    
    """Fade up, WordArt object."""
    TEXT_FADE_UP: int
    
    """Fade down, WordArt object."""
    TEXT_FADE_DOWN: int
    
    """Slant up, WordArt object."""
    TEXT_SLANT_UP: int
    
    """Slant down, WordArt object."""
    TEXT_SLANT_DOWN: int
    
    """Can up, WordArt object."""
    TEXT_CAN_UP: int
    
    """Can down, WordArt object."""
    TEXT_CAN_DOWN: int
    
    """Flow chart alternate process."""
    FLOW_CHART_ALTERNATE_PROCESS: int
    
    """Flow chart off page connector."""
    FLOW_CHART_OFFPAGE_CONNECTOR: int
    
    """Callout 90."""
    CALLOUT90: int
    
    """Accent callout 90."""
    ACCENT_CALLOUT90: int
    
    """Border callout 90."""
    BORDER_CALLOUT90: int
    
    """Accent border callout 90."""
    ACCENT_BORDER_CALLOUT90: int
    
    """Left right up arrow."""
    LEFT_RIGHT_UP_ARROW: int
    
    """Sun."""
    SUN: int
    
    """Moon."""
    MOON: int
    
    """Bracket pair."""
    BRACKET_PAIR: int
    
    """Brace pair"""
    BRACE_PAIR: int
    
    """Four-pointed star."""
    SEAL4: int
    
    """Double wave."""
    DOUBLE_WAVE: int
    
    """Action button blank."""
    ACTION_BUTTON_BLANK: int
    
    """Action button home."""
    ACTION_BUTTON_HOME: int
    
    """Action button help."""
    ACTION_BUTTON_HELP: int
    
    """Action button information."""
    ACTION_BUTTON_INFORMATION: int
    
    """Action button forward next."""
    ACTION_BUTTON_FORWARD_NEXT: int
    
    """Action button back previous."""
    ACTION_BUTTON_BACK_PREVIOUS: int
    
    """Action button end."""
    ACTION_BUTTON_END: int
    
    """Action button beginning."""
    ACTION_BUTTON_BEGINNING: int
    
    """Action button return."""
    ACTION_BUTTON_RETURN: int
    
    """Action button document."""
    ACTION_BUTTON_DOCUMENT: int
    
    """Action button sound."""
    ACTION_BUTTON_SOUND: int
    
    """Action button movie."""
    ACTION_BUTTON_MOVIE: int
    
    """Snip single corner rectangle object.
    
    Applicable only for DML shapes."""
    SINGLE_CORNER_SNIPPED: int
    
    """Snip same side corner rectangle.
    
    Applicable only for DML shapes."""
    TOP_CORNERS_SNIPPED: int
    
    """Snip diagonal corner rectangle.
    
    Applicable only for DML shapes."""
    DIAGONAL_CORNERS_SNIPPED: int
    
    """Snip and round single corner rectangle.
    
    Applicable only for DML shapes."""
    TOP_CORNERS_ONE_ROUNDED_ONE_SNIPPED: int
    
    """Round single corner rectangle.
    
    Applicable only for DML shapes."""
    SINGLE_CORNER_ROUNDED: int
    
    """Round same side corner rectangle.
    
    Applicable only for DML shapes."""
    TOP_CORNERS_ROUNDED: int
    
    """Round diagonal corner rectangle.
    
    Applicable only for DML shapes."""
    DIAGONAL_CORNERS_ROUNDED: int
    
    """Heptagon.
    
    Applicable only for DML shapes."""
    HEPTAGON: int
    
    """Cloud.
    
    Applicable only for DML shapes."""
    CLOUD: int
    
    """Six-pointed star.
    
    Applicable only for DML shapes."""
    SEAL6: int
    
    """Seven-pointed star.
    
    Applicable only for DML shapes."""
    SEAL7: int
    
    """Ten-pointed star.
    
    Applicable only for DML shapes."""
    SEAL10: int
    
    """Twelve-pointed star.
    
    Applicable only for DML shapes."""
    SEAL12: int
    
    """Swoosh arrow.
    
    Applicable only for DML shapes."""
    SWOOSH_ARROW: int
    
    """Teardrop.
    
    Applicable only for DML shapes."""
    TEARDROP: int
    
    """Square tabs.
    
    Applicable only for DML shapes."""
    SQUARE_TABS: int
    
    """Plaque tabs.
    
    Applicable only for DML shapes."""
    PLAQUE_TABS: int
    
    """Pie.
    
    Applicable only for DML shapes."""
    PIE: int
    
    """Wedge pie.
    
    Applicable only for DML shapes."""
    WEDGE_PIE: int
    
    """Inverse line.
    
    Applicable only for DML shapes."""
    INVERSE_LINE: int
    
    """Math plus.
    
    Applicable only for DML shapes."""
    MATH_PLUS: int
    
    """Math minus.
    
    Applicable only for DML shapes."""
    MATH_MINUS: int
    
    """Math multiply.
    
    Applicable only for DML shapes."""
    MATH_MULTIPLY: int
    
    """Math divide.
    
    Applicable only for DML shapes."""
    MATH_DIVIDE: int
    
    """Math equal.
    
    Applicable only for DML shapes."""
    MATH_EQUAL: int
    
    """Math not equal.
    
    Applicable only for DML shapes."""
    MATH_NOT_EQUAL: int
    
    """Non-isosceles trapezoid.
    
    Applicable only for DML shapes."""
    NON_ISOSCELES_TRAPEZOID: int
    
    """Left-right circular arrow.
    
    Applicable only for DML shapes."""
    LEFT_RIGHT_CIRCULAR_ARROW: int
    
    """Left-right ribbon.
    
    Applicable only for DML shapes."""
    LEFT_RIGHT_RIBBON: int
    
    """Left circular arrow.
    
    Applicable only for DML shapes."""
    LEFT_CIRCULAR_ARROW: int
    
    """Frame.
    
    Applicable only for DML shapes."""
    FRAME: int
    
    """Half frame.
    
    Applicable only for DML shapes."""
    HALF_FRAME: int
    
    """Funnel.
    
    Applicable only for DML shapes."""
    FUNNEL: int
    
    """Six-tooth gear.
    
    Applicable only for DML shapes."""
    GEAR6: int
    
    """Nine-tooth gear.
    
    Applicable only for DML shapes."""
    GEAR9: int
    
    """Decagon.
    
    Applicable only for DML shapes."""
    DECAGON: int
    
    """Dodecagon.
    
    Applicable only for DML shapes."""
    DODECAGON: int
    
    """Diagonal stripe.
    
    Applicable only for DML shapes."""
    DIAGONAL_STRIPE: int
    
    """Corner.
    
    Applicable only for DML shapes."""
    CORNER: int
    
    """Corner tabs.
    
    Applicable only for DML shapes."""
    CORNER_TABS: int
    
    """Chord.
    
    Applicable only for DML shapes."""
    CHORD: int
    
    """Chart plus.
    
    Applicable only for DML shapes."""
    CHART_PLUS: int
    
    """Chart star.
    
    Applicable only for DML shapes."""
    CHART_STAR: int
    
    """Chart X.
    
    Applicable only for DML shapes."""
    CHART_X: int
    
    """Reserved for the system use."""
    MIN_VALUE: int
    

class TextBoxAnchor(Enum):
    """Specifies values used for shape text vertical alignment."""
    
    """Text is aligned to the top of the textbox."""
    TOP: int
    
    """Text is aligned to the middle of the textbox."""
    MIDDLE: int
    
    """Text is aligned to the bottom of the textbox."""
    BOTTOM: int
    
    """Text is aligned to the top centered of the textbox."""
    TOP_CENTERED: int
    
    """Text is aligned to the middle centered of the textbox."""
    MIDDLE_CENTERED: int
    
    """Text is aligned to the bottom centered of the textbox."""
    BOTTOM_CENTERED: int
    
    """Text is aligned to the top baseline of the textbox."""
    TOP_BASELINE: int
    
    """Text is aligned to the bottom baseline of the textbox."""
    BOTTOM_BASELINE: int
    
    """Text is aligned to the top centered baseline of the textbox."""
    TOP_CENTERED_BASELINE: int
    
    """Text is aligned to the bottom centered baseline of the textbox."""
    BOTTOM_CENTERED_BASELINE: int
    

class TextBoxWrapMode(Enum):
    """Specifies how text wraps inside a shape."""
    
    """Text wraps inside a shape."""
    SQUARE: int
    
    """Text does not wrap inside a shape."""
    NONE: int
    

class TextPathAlignment(Enum):
    """WordArt alignment."""
    
    """Stretch each line of text to fit width."""
    STRETCH: int
    
    """Center text on width."""
    CENTER: int
    
    """Left justify."""
    LEFT: int
    
    """Right justify."""
    RIGHT: int
    
    """Spread letters out to fit width."""
    LETTER_JUSTIFY: int
    
    """Spread words out to fit width."""
    WORD_JUSTIFY: int
    

class TextureAlignment(Enum):
    """Specifies the alignment for the tiling of the texture fill."""
    
    """Top left texture alignment."""
    TOP_LEFT: int
    
    """Top texture alignment."""
    TOP: int
    
    """Top right texture alignment."""
    TOP_RIGHT: int
    
    """Left texture alignment."""
    LEFT: int
    
    """Center texture alignment."""
    CENTER: int
    
    """Right texture alignment."""
    RIGHT: int
    
    """Bottom left texture alignment."""
    BOTTOM_LEFT: int
    
    """Bottom texture alignment."""
    BOTTOM: int
    
    """Bottom right texture alignment."""
    BOTTOM_RIGHT: int
    
    """None texture alignment."""
    NONE: int
    

class VerticalAlignment(Enum):
    """Specifies vertical alignment of a floating shape, text frame or a floating table."""
    
    """The object is explicitly positioned, usually using its **Top** property."""
    NONE: int
    
    """Specifies that the object shall be at the top of the vertical alignment base."""
    TOP: int
    
    """Specifies that the object shall be centered with respect to the vertical alignment base."""
    CENTER: int
    
    """Specifies that the object shall be at the bottom of the vertical alignment base."""
    BOTTOM: int
    
    """Specifies that the object shall be inside of the horizontal alignment base."""
    INSIDE: int
    
    """Specifies that the object shall be outside of the vertical alignment base."""
    OUTSIDE: int
    
    """Not documented. Seems to be a possible value for floating paragraphs and tables."""
    INLINE: int
    
    """Same as :attr:`VerticalAlignment.NONE`."""
    DEFAULT: int
    

class WrapSide(Enum):
    """Specifies what side(s) of the shape or picture the text wraps around."""
    
    """The document text wraps on both sides of the shape."""
    BOTH: int
    
    """The document text wraps on the left side of the shape only. There is a text free area on the right of the shape."""
    LEFT: int
    
    """The document text wraps on the right side of the shape only. There is a text free area on the left side of the shape."""
    RIGHT: int
    
    """The document text wraps on the side of the shape that is farthest from the page margin, leaving text free area on the other side of the shape."""
    LARGEST: int
    
    """Default value is :attr:`WrapSide.BOTH`."""
    DEFAULT: int
    

class WrapType(Enum):
    """Specifies how text is wrapped around a shape or picture."""
    
    """No text wrapping around the shape. The shape is placed behind or in front of text."""
    NONE: int
    
    """The shape remains on the same layer as text and treated as a character."""
    INLINE: int
    
    """The text stops at the top of the shape and restarts on the line below the shape."""
    TOP_BOTTOM: int
    
    """Wraps text around all sides of the square bounding box of the shape."""
    SQUARE: int
    
    """Wraps tightly around the edges of the shape, instead of wrapping around the bounding box."""
    TIGHT: int
    
    """Same as Tight, but wraps inside any parts of the shape that are open."""
    THROUGH: int
    


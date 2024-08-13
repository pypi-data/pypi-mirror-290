﻿import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable, List
from enum import Enum

class AxisBound:
    """Represents minimum or maximum bound of axis values.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article.
    
    Bound can be specified as a numeric, datetime or a special "auto" value.
    
    The instances of this class are immutable."""
    
    @overload
    def __init__(self):
        """Creates a new instance indicating that axis bound should be determined automatically by a word-processing
        application."""
        ...
    
    @overload
    def __init__(self, value: float):
        """Creates an axis bound represented as a number."""
        ...
    
    @overload
    def __init__(self, datetime: datetime.datetime):
        """Creates an axis bound represented as datetime value."""
        ...
    
    @property
    def is_auto(self) -> bool:
        """Returns a flag indicating that axis bound should be determined automatically."""
        ...
    
    @property
    def value(self) -> float:
        """Returns numeric value of axis bound."""
        ...
    
    @property
    def value_as_date(self) -> datetime.datetime:
        """Returns value of axis bound represented as datetime."""
        ...
    
    ...

class AxisDisplayUnit:
    """Provides access to the scaling options of the display units for the value axis.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __init__(self):
        ...
    
    @property
    def unit(self) -> aspose.words.drawing.charts.AxisBuiltInUnit:
        """Gets or sets the scaling value of the display units as one of the predefined values.
        
        Default value is :attr:`AxisBuiltInUnit.NONE`. The :attr:`AxisBuiltInUnit.CUSTOM` and
        :attr:`AxisBuiltInUnit.PERCENTAGE` values are not available in some chart types; see
        :class:`AxisBuiltInUnit` for more information."""
        ...
    
    @unit.setter
    def unit(self, value: aspose.words.drawing.charts.AxisBuiltInUnit):
        ...
    
    @property
    def custom_unit(self) -> float:
        """Gets or sets a user-defined divisor to scale display units on the value axis.
        
        The property is not supported by MS Office 2016 new charts. Default value is 1.
        
        Setting this property sets the :attr:`AxisDisplayUnit.unit` property to
        :attr:`AxisBuiltInUnit.CUSTOM`."""
        ...
    
    @custom_unit.setter
    def custom_unit(self, value: float):
        ...
    
    @property
    def document(self) -> aspose.words.DocumentBase:
        """Returns the document containing the parent chart."""
        ...
    
    ...

class AxisScaling:
    """Represents the scaling options of the axis.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __init__(self):
        ...
    
    @property
    def type(self) -> aspose.words.drawing.charts.AxisScaleType:
        """Gets or sets scaling type of the axis.
        
        The :attr:`AxisScaleType.LINEAR` value is the only that is allowed in MS Office 2016 new charts."""
        ...
    
    @type.setter
    def type(self, value: aspose.words.drawing.charts.AxisScaleType):
        ...
    
    @property
    def log_base(self) -> float:
        """Gets or sets the logarithmic base for a logarithmic axis.
        
        The property is not supported by MS Office 2016 new charts.
        
        Valid range of a floating point value is greater than or equal to 2 and less than or
        equal to 1000. The property has effect only if :attr:`AxisScaling.type` is set to
        :attr:`AxisScaleType.LOGARITHMIC`.
        
        Setting this property sets the :attr:`AxisScaling.type` property to :attr:`AxisScaleType.LOGARITHMIC`."""
        ...
    
    @log_base.setter
    def log_base(self, value: float):
        ...
    
    @property
    def minimum(self) -> aspose.words.drawing.charts.AxisBound:
        """Gets or sets minimum value of the axis.
        
        The default value is "auto"."""
        ...
    
    @minimum.setter
    def minimum(self, value: aspose.words.drawing.charts.AxisBound):
        ...
    
    @property
    def maximum(self) -> aspose.words.drawing.charts.AxisBound:
        """Gets or sets the maximum value of the axis.
        
        The default value is "auto"."""
        ...
    
    @maximum.setter
    def maximum(self, value: aspose.words.drawing.charts.AxisBound):
        ...
    
    ...

class AxisTickLabels:
    """Represents properties of axis tick mark labels."""
    
    @property
    def position(self) -> aspose.words.drawing.charts.AxisTickLabelPosition:
        """Gets or sets the position of the tick labels on the axis.
        
        The property is not supported by MS Office 2016 new charts."""
        ...
    
    @position.setter
    def position(self, value: aspose.words.drawing.charts.AxisTickLabelPosition):
        ...
    
    @property
    def offset(self) -> int:
        """Gets or sets the distance of the tick labels from the axis.
        
        The property represents a percentage of the default label offset.
        
        Valid range is from 0 to 1000 percent inclusive. The default value is 100%.
        
        The property has effect only for category axes. It is not supported by MS Office 2016 new charts."""
        ...
    
    @offset.setter
    def offset(self, value: int):
        ...
    
    @property
    def spacing(self) -> int:
        """Gets or sets the interval at which the tick labels are drawn.
        
        The property has effect for text category and series axes. It is not supported by MS Office 2016
        new charts. Valid range of a value is greater than or equal to 1.
        
        Setting this property sets the :attr:`AxisTickLabels.is_auto_spacing` property to ``False``."""
        ...
    
    @spacing.setter
    def spacing(self, value: int):
        ...
    
    @property
    def is_auto_spacing(self) -> bool:
        """Gets or sets a flag indicating whether to use automatic interval for drawing the tick labels.
        
        The default value is ``True``.
        
        The property has effect for text category and series axes. It is not supported by MS Office 2016
        new charts."""
        ...
    
    @is_auto_spacing.setter
    def is_auto_spacing(self, value: bool):
        ...
    
    @property
    def alignment(self) -> aspose.words.ParagraphAlignment:
        """Gets or sets text alignment of the axis tick labels.
        
        This property has effect only for multi-line labels.
        
        The default value is :attr:`aspose.words.ParagraphAlignment.CENTER`.
        
        ."""
        ...
    
    @alignment.setter
    def alignment(self, value: aspose.words.ParagraphAlignment):
        ...
    
    @property
    def orientation(self) -> aspose.words.drawing.ShapeTextOrientation:
        """Gets or sets the orientation of the tick label text.
        
        The default value is :attr:`aspose.words.drawing.ShapeTextOrientation.HORIZONTAL`.
        
        Note that some :class:`aspose.words.drawing.ShapeTextOrientation` values do not affect the orientation of tick label text
        in value axes."""
        ...
    
    @orientation.setter
    def orientation(self, value: aspose.words.drawing.ShapeTextOrientation):
        ...
    
    @property
    def rotation(self) -> int:
        """Gets or sets the rotation of the tick labels in degrees.
        
        The range of acceptable values is from -180 to 180 inclusive. The default value is 0."""
        ...
    
    @rotation.setter
    def rotation(self, value: int):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to font formatting of the tick labels."""
        ...
    
    ...

class BubbleSizeCollection:
    """Represents a collection of bubble sizes for a chart series.
    
    The collection allows only changing bubble sizes. To add or insert new values to a chart series, or remove
    values, the appropriate methods of the :class:`ChartSeries` class can be used.
    
    Empty bubble size values are represented as None."""
    
    def __getitem__(self, index: int) -> float:
        """Gets or sets the bubble size value at the specified index."""
        ...
    
    def __setitem__(self, index: int, value: float):
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of items in this collection."""
        ...
    
    ...

class Chart:
    """Provides access to the chart shape properties.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def series(self) -> aspose.words.drawing.charts.ChartSeriesCollection:
        """Provides access to series collection."""
        ...
    
    @property
    def series_groups(self) -> aspose.words.drawing.charts.ChartSeriesGroupCollection:
        """Provides access to a series group collection of this chart."""
        ...
    
    @property
    def title(self) -> aspose.words.drawing.charts.ChartTitle:
        """Provides access to the chart title properties."""
        ...
    
    @property
    def legend(self) -> aspose.words.drawing.charts.ChartLegend:
        """Provides access to the chart legend properties."""
        ...
    
    @property
    def data_table(self) -> aspose.words.drawing.charts.ChartDataTable:
        """Provides access to properties of a data table of this chart.
        The data table can be shown using the :attr:`ChartDataTable.show` property."""
        ...
    
    @property
    def axis_x(self) -> aspose.words.drawing.charts.ChartAxis:
        """Provides access to properties of the primary X axis of the chart."""
        ...
    
    @property
    def axis_y(self) -> aspose.words.drawing.charts.ChartAxis:
        """Provides access to properties of the primary Y axis of the chart."""
        ...
    
    @property
    def axis_z(self) -> aspose.words.drawing.charts.ChartAxis:
        """Provides access to properties of the Z axis of the chart."""
        ...
    
    @property
    def axes(self) -> aspose.words.drawing.charts.ChartAxisCollection:
        """Gets a collection of all axes of this chart."""
        ...
    
    @property
    def source_full_name(self) -> str:
        """Gets the path and name of an xls/xlsx file this chart is linked to."""
        ...
    
    @source_full_name.setter
    def source_full_name(self, value: str):
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the chart."""
        ...
    
    ...

class ChartAxis:
    """Represents the axis options of the chart.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def type(self) -> aspose.words.drawing.charts.ChartAxisType:
        """Returns type of the axis."""
        ...
    
    @property
    def category_type(self) -> aspose.words.drawing.charts.AxisCategoryType:
        """Gets or sets type of the category axis.
        
        Only text categories (:attr:`AxisCategoryType.CATEGORY`) are allowed in MS Office 2016 new charts."""
        ...
    
    @category_type.setter
    def category_type(self, value: aspose.words.drawing.charts.AxisCategoryType):
        ...
    
    @property
    def crosses(self) -> aspose.words.drawing.charts.AxisCrosses:
        """Specifies how this axis crosses the perpendicular axis.
        
        Default value is :attr:`AxisCrosses.AUTOMATIC`.
        
        The property is not supported by MS Office 2016 new charts."""
        ...
    
    @crosses.setter
    def crosses(self, value: aspose.words.drawing.charts.AxisCrosses):
        ...
    
    @property
    def crosses_at(self) -> float:
        """Specifies where on the perpendicular axis the axis crosses.
        
        The property has effect only if :attr:`ChartAxis.crosses` are set to :attr:`AxisCrosses.CUSTOM`.
        It is not supported by MS Office 2016 new charts.
        
        The units are determined by the type of axis. When the axis is a value axis, the value of the property
        is a decimal number on the value axis. When the axis is a time category axis, the value is defined as
        an integer number of days relative to the base date (30/12/1899). For a text category axis, the value is
        an integer category number, starting with 1 as the first category."""
        ...
    
    @crosses_at.setter
    def crosses_at(self, value: float):
        ...
    
    @property
    def reverse_order(self) -> bool:
        """Returns or sets a flag indicating whether values of axis should be displayed in reverse order, i.e.
        from max to min.
        
        The property is not supported by MS Office 2016 new charts. Default value is ``False``."""
        ...
    
    @reverse_order.setter
    def reverse_order(self, value: bool):
        ...
    
    @property
    def major_tick_mark(self) -> aspose.words.drawing.charts.AxisTickMark:
        """Returns or sets the major tick marks."""
        ...
    
    @major_tick_mark.setter
    def major_tick_mark(self, value: aspose.words.drawing.charts.AxisTickMark):
        ...
    
    @property
    def minor_tick_mark(self) -> aspose.words.drawing.charts.AxisTickMark:
        """Returns or sets the minor tick marks for the axis."""
        ...
    
    @minor_tick_mark.setter
    def minor_tick_mark(self, value: aspose.words.drawing.charts.AxisTickMark):
        ...
    
    @property
    def tick_label_position(self) -> aspose.words.drawing.charts.AxisTickLabelPosition:
        """Returns or sets the position of the tick labels on the axis.
        
        The property is not supported by MS Office 2016 new charts."""
        ...
    
    @tick_label_position.setter
    def tick_label_position(self, value: aspose.words.drawing.charts.AxisTickLabelPosition):
        ...
    
    @property
    def major_unit(self) -> float:
        """Returns or sets the distance between major tick marks.
        
        Valid range of a value is greater than zero. The property has effect for time category and
        value axes.
        
        Setting this property sets the :attr:`ChartAxis.major_unit_is_auto` property to ``False``."""
        ...
    
    @major_unit.setter
    def major_unit(self, value: float):
        ...
    
    @property
    def major_unit_is_auto(self) -> bool:
        """Gets or sets a flag indicating whether default distance between major tick marks shall be used.
        
        The property has effect for time category and value axes."""
        ...
    
    @major_unit_is_auto.setter
    def major_unit_is_auto(self, value: bool):
        ...
    
    @property
    def major_unit_scale(self) -> aspose.words.drawing.charts.AxisTimeUnit:
        """Returns or sets the scale value for major tick marks on the time category axis.
        
        The property has effect only for time category axes."""
        ...
    
    @major_unit_scale.setter
    def major_unit_scale(self, value: aspose.words.drawing.charts.AxisTimeUnit):
        ...
    
    @property
    def minor_unit(self) -> float:
        """Returns or sets the distance between minor tick marks.
        
        Valid range of a value is greater than zero. The property has effect for time category and
        value axes.
        
        Setting this property sets the :attr:`ChartAxis.minor_unit_is_auto` property to ``False``."""
        ...
    
    @minor_unit.setter
    def minor_unit(self, value: float):
        ...
    
    @property
    def minor_unit_is_auto(self) -> bool:
        """Gets or sets a flag indicating whether default distance between minor tick marks shall be used.
        
        The property has effect for time category and value axes."""
        ...
    
    @minor_unit_is_auto.setter
    def minor_unit_is_auto(self, value: bool):
        ...
    
    @property
    def minor_unit_scale(self) -> aspose.words.drawing.charts.AxisTimeUnit:
        """Returns or sets the scale value for minor tick marks on the time category axis.
        
        The property has effect only for time category axes."""
        ...
    
    @minor_unit_scale.setter
    def minor_unit_scale(self, value: aspose.words.drawing.charts.AxisTimeUnit):
        ...
    
    @property
    def base_time_unit(self) -> aspose.words.drawing.charts.AxisTimeUnit:
        """Returns or sets the smallest time unit that is represented on the time category axis.
        
        The property has effect only for time category axes."""
        ...
    
    @base_time_unit.setter
    def base_time_unit(self, value: aspose.words.drawing.charts.AxisTimeUnit):
        ...
    
    @property
    def number_format(self) -> aspose.words.drawing.charts.ChartNumberFormat:
        """Returns a :class:`ChartNumberFormat` object that allows defining number formats for the axis."""
        ...
    
    @property
    def tick_label_offset(self) -> int:
        """Gets or sets the distance of labels from the axis.
        
        The property represents a percentage of the default label offset.
        
        Valid range is from 0 to 1000 percent inclusive. Default value is 100%.
        
        The property has effect only for category axes. It is not supported by MS Office 2016 new charts."""
        ...
    
    @tick_label_offset.setter
    def tick_label_offset(self, value: int):
        ...
    
    @property
    def display_unit(self) -> aspose.words.drawing.charts.AxisDisplayUnit:
        """Specifies the scaling value of the display units for the value axis.
        
        The property has effect only for value axes."""
        ...
    
    @property
    def axis_between_categories(self) -> bool:
        """Gets or sets a flag indicating whether the value axis crosses the category axis between categories.
        
        The property has effect only for value axes. It is not supported by MS Office 2016 new charts."""
        ...
    
    @axis_between_categories.setter
    def axis_between_categories(self, value: bool):
        ...
    
    @property
    def scaling(self) -> aspose.words.drawing.charts.AxisScaling:
        """Provides access to the scaling options of the axis."""
        ...
    
    @property
    def tick_label_spacing(self) -> int:
        """Gets or sets the interval, at which tick labels are drawn.
        
        The property has effect for text category and series axes. It is not supported by MS Office 2016
        new charts. Valid range of a value is greater than or equal to 1.
        
        Setting this property sets the :attr:`AxisTickLabels.is_auto_spacing` property to ``False``."""
        ...
    
    @tick_label_spacing.setter
    def tick_label_spacing(self, value: int):
        ...
    
    @property
    def tick_label_spacing_is_auto(self) -> bool:
        """Gets or sets a flag indicating whether automatic interval of drawing tick labels shall be used.
        
        Default value is ``True``.
        
        The property has effect for text category and series axes. It is not supported by MS Office 2016
        new charts."""
        ...
    
    @tick_label_spacing_is_auto.setter
    def tick_label_spacing_is_auto(self, value: bool):
        ...
    
    @property
    def tick_label_alignment(self) -> aspose.words.ParagraphAlignment:
        """Gets or sets text alignment of axis tick labels.
        
        This property has effect only for multi-line labels.
        
        Default value is :attr:`aspose.words.ParagraphAlignment.CENTER`.
        
        ."""
        ...
    
    @tick_label_alignment.setter
    def tick_label_alignment(self, value: aspose.words.ParagraphAlignment):
        ...
    
    @property
    def tick_mark_spacing(self) -> int:
        """Gets or sets the interval, at which tick marks are drawn.
        
        The property has effect for text category and series axes. It is not supported by MS Office 2016
        new charts.
        
        Valid range of a value is greater than or equal to 1."""
        ...
    
    @tick_mark_spacing.setter
    def tick_mark_spacing(self, value: int):
        ...
    
    @property
    def hidden(self) -> bool:
        """Gets or sets a flag indicating whether this axis is hidden or not.
        
        Default value is ``False``."""
        ...
    
    @hidden.setter
    def hidden(self, value: bool):
        ...
    
    @property
    def has_major_gridlines(self) -> bool:
        """Gets or sets a flag indicating whether the axis has major gridlines."""
        ...
    
    @has_major_gridlines.setter
    def has_major_gridlines(self, value: bool):
        ...
    
    @property
    def has_minor_gridlines(self) -> bool:
        """Gets or sets a flag indicating whether the axis has minor gridlines."""
        ...
    
    @has_minor_gridlines.setter
    def has_minor_gridlines(self, value: bool):
        ...
    
    @property
    def title(self) -> aspose.words.drawing.charts.ChartAxisTitle:
        """Provides access to the axis title properties."""
        ...
    
    @property
    def tick_labels(self) -> aspose.words.drawing.charts.AxisTickLabels:
        """Provides access to the properties of the axis tick mark labels."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to line formatting of the axis and fill of the tick labels.
        
        Fill of chart tick marks can be changed only for pre Word 2016 charts. Word 2016 charts do not support this."""
        ...
    
    @property
    def document(self) -> aspose.words.DocumentBase:
        """Returns the document containing the parent chart."""
        ...
    
    ...

class ChartAxisCollection:
    """Represents a collection of chart axes."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartAxis:
        """Gets the axis at the specified index."""
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of axes in this collection."""
        ...
    
    ...

class ChartAxisTitle:
    """Provides access to the axis title properties.
    To learn more, visit the `Working with
                Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def text(self) -> str:
        """Gets or sets the text of the axis title.
        If ``None`` or empty value is specified, auto generated title will be shown.
        
        Use :attr:`ChartAxisTitle.show` option if you need to show the title."""
        ...
    
    @text.setter
    def text(self, value: str):
        ...
    
    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap the title.
        The default value is ``False``."""
        ...
    
    @overlay.setter
    def overlay(self, value: bool):
        ...
    
    @property
    def show(self) -> bool:
        """Determines whether the title shall be shown for the axis.
        The default value is ``False``."""
        ...
    
    @show.setter
    def show(self, value: bool):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of the axis title."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the axis title."""
        ...
    
    ...

class ChartDataLabel:
    """Represents data label on a chart point or trendline.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article.
    
    On a series, the :class:`ChartDataLabel` object is a member of the :class:`ChartDataLabelCollection`.
    The :class:`ChartDataLabelCollection` contains a :class:`ChartDataLabel` object for each point."""
    
    def clear_format(self) -> None:
        """Clears format of this data label. The properties are set to the default values defined in the parent data
        label collection."""
        ...
    
    @property
    def index(self) -> int:
        """Specifies the index of the containing element.
        This index shall determine which of the parent's children collection this element applies to.
        Default value is 0."""
        ...
    
    @property
    def show_category_name(self) -> bool:
        """Allows to specify if category name is to be displayed for the data labels on a chart.
        Default value is ``False``."""
        ...
    
    @show_category_name.setter
    def show_category_name(self, value: bool):
        ...
    
    @property
    def show_bubble_size(self) -> bool:
        """Allows to specify if bubble size is to be displayed for the data labels on a chart.
        Applies only to Bubble charts.
        Default value is ``False``."""
        ...
    
    @show_bubble_size.setter
    def show_bubble_size(self, value: bool):
        ...
    
    @property
    def show_legend_key(self) -> bool:
        """Allows to specify if legend key is to be displayed for the data labels on a chart.
        Default value is ``False``."""
        ...
    
    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        ...
    
    @property
    def show_percentage(self) -> bool:
        """Allows to specify if percentage value is to be displayed for the data labels on a chart.
        Default value is ``False``."""
        ...
    
    @show_percentage.setter
    def show_percentage(self, value: bool):
        ...
    
    @property
    def show_series_name(self) -> bool:
        """Returns or sets a Boolean to indicate the series name display behavior for the data labels on a chart.
        ``True`` to show the series name; ``False`` to hide. By default ``False``."""
        ...
    
    @show_series_name.setter
    def show_series_name(self, value: bool):
        ...
    
    @property
    def show_value(self) -> bool:
        """Allows to specify if values are to be displayed in the data labels.
        Default value is ``False``."""
        ...
    
    @show_value.setter
    def show_value(self, value: bool):
        ...
    
    @property
    def show_leader_lines(self) -> bool:
        """Allows to specify if data label leader lines need be shown.
        Default value is ``False``.
        
        Applies to Pie charts only.
        Leader lines create a visual connection between a data label and its corresponding data point."""
        ...
    
    @show_leader_lines.setter
    def show_leader_lines(self, value: bool):
        ...
    
    @property
    def show_data_labels_range(self) -> bool:
        """Allows to specify if values from data labels range to be displayed in the data labels.
        Default value is ``False``."""
        ...
    
    @show_data_labels_range.setter
    def show_data_labels_range(self, value: bool):
        ...
    
    @property
    def separator(self) -> str:
        """Gets or sets string separator used for the data labels on a chart.
        The default is a comma, except for pie charts showing only category name and percentage, when a line break
        shall be used instead."""
        ...
    
    @separator.setter
    def separator(self, value: str):
        ...
    
    @property
    def orientation(self) -> aspose.words.drawing.ShapeTextOrientation:
        """Gets or sets the orientation of the label text.
        
        The default value is :attr:`aspose.words.drawing.ShapeTextOrientation.HORIZONTAL`."""
        ...
    
    @orientation.setter
    def orientation(self, value: aspose.words.drawing.ShapeTextOrientation):
        ...
    
    @property
    def rotation(self) -> int:
        """Gets or sets the rotation of the label in degrees.
        
        The range of acceptable values is from -180 to 180 inclusive. The default value is 0.
        
        If the :attr:`ChartDataLabel.orientation` value is :attr:`aspose.words.drawing.ShapeTextOrientation.HORIZONTAL`, the
        label shape, if it exists, is rotated along with the label text. Otherwise, only the label text is rotated."""
        ...
    
    @rotation.setter
    def rotation(self, value: int):
        ...
    
    @property
    def is_visible(self) -> bool:
        """Returns ``True`` if this data label has something to display."""
        ...
    
    @property
    def number_format(self) -> aspose.words.drawing.charts.ChartNumberFormat:
        """Returns number format of the parent element."""
        ...
    
    @property
    def is_hidden(self) -> bool:
        """Gets/sets a flag indicating whether this label is hidden.
        The default value is ``False``."""
        ...
    
    @is_hidden.setter
    def is_hidden(self, value: bool):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of this data label."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the data label."""
        ...
    
    ...

class ChartDataLabelCollection:
    """Represents a collection of :class:`ChartDataLabel`.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartDataLabel:
        """Returns :class:`ChartDataLabel` for the specified index."""
        ...
    
    def clear_format(self) -> None:
        """Clears format of all :class:`ChartDataLabel` in this collection."""
        ...
    
    @property
    def count(self) -> int:
        """Returns the number of :class:`ChartDataLabel` in this collection."""
        ...
    
    @property
    def show_category_name(self) -> bool:
        """Allows to specify whether category name is to be displayed for the data labels of the entire series.
        Default value is ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_category_name` property."""
        ...
    
    @show_category_name.setter
    def show_category_name(self, value: bool):
        ...
    
    @property
    def show_bubble_size(self) -> bool:
        """Allows to specify whether bubble size is to be displayed for the data labels of the entire series.
        Applies only to Bubble charts.
        Default value is ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_bubble_size` property."""
        ...
    
    @show_bubble_size.setter
    def show_bubble_size(self, value: bool):
        ...
    
    @property
    def show_legend_key(self) -> bool:
        """Allows to specify whether legend key is to be displayed for the data labels of the entire series.
        Default value is ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_legend_key` property."""
        ...
    
    @show_legend_key.setter
    def show_legend_key(self, value: bool):
        ...
    
    @property
    def show_percentage(self) -> bool:
        """Allows to specify whether percentage value is to be displayed for the data labels of the entire series.
        Default value is ``False``. Applies only to Pie charts.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_percentage` property."""
        ...
    
    @show_percentage.setter
    def show_percentage(self, value: bool):
        ...
    
    @property
    def show_series_name(self) -> bool:
        """Returns or sets a Boolean to indicate the series name display behavior for the data labels of the entire series.
        ``True`` to show the series name; ``False`` to hide. By default ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_series_name` property."""
        ...
    
    @show_series_name.setter
    def show_series_name(self, value: bool):
        ...
    
    @property
    def show_value(self) -> bool:
        """Allows to specify whether values are to be displayed in the data labels of the entire series.
        Default value is ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_value` property."""
        ...
    
    @show_value.setter
    def show_value(self, value: bool):
        ...
    
    @property
    def show_leader_lines(self) -> bool:
        """Allows to specify whether data label leader lines need be shown for the data labels of the entire series.
        Default value is ``False``.
        
        Applies to Pie charts only.
        Leader lines create a visual connection between a data label and its corresponding data point.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_leader_lines` property."""
        ...
    
    @show_leader_lines.setter
    def show_leader_lines(self, value: bool):
        ...
    
    @property
    def show_data_labels_range(self) -> bool:
        """Allows to specify whether values from data labels range to be displayed in the data labels of the entire series.
        Default value is ``False``.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.show_data_labels_range` property."""
        ...
    
    @show_data_labels_range.setter
    def show_data_labels_range(self, value: bool):
        ...
    
    @property
    def separator(self) -> str:
        """Gets or sets string separator used for the data labels of the entire series.
        The default is a comma, except for pie charts showing only category name and percentage, when a line break
        shall be used instead.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.separator` property."""
        ...
    
    @separator.setter
    def separator(self, value: str):
        ...
    
    @property
    def orientation(self) -> aspose.words.drawing.ShapeTextOrientation:
        """Gets or sets the text orientation of the data labels of the entire series.
        
        The default value is :attr:`aspose.words.drawing.ShapeTextOrientation.HORIZONTAL`."""
        ...
    
    @orientation.setter
    def orientation(self, value: aspose.words.drawing.ShapeTextOrientation):
        ...
    
    @property
    def rotation(self) -> int:
        """Gets or sets the rotation of the data labels of the entire series in degrees.
        
        The range of acceptable values is from -180 to 180 inclusive. The default value is 0.
        
        If the :attr:`ChartDataLabelCollection.orientation` value is :attr:`aspose.words.drawing.ShapeTextOrientation.HORIZONTAL`, label shapes,
        if they exist, are rotated along with the label text. Otherwise, only the label text is rotated."""
        ...
    
    @rotation.setter
    def rotation(self, value: int):
        ...
    
    @property
    def number_format(self) -> aspose.words.drawing.charts.ChartNumberFormat:
        """Gets an :class:`ChartNumberFormat` instance allowing to set number format for the data labels of the
        entire series."""
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of the data labels of the entire series.
        
        Value defined for this property can be overridden for an individual data label with using the
        :attr:`ChartDataLabel.font` property."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the data labels."""
        ...
    
    ...

class ChartDataPoint:
    """Allows to specify formatting of a single data point on the chart.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article.
    
    On a series, the :class:`ChartDataPoint` object is a member of the :class:`ChartDataPointCollection`.
    The :class:`ChartDataPointCollection` contains a :class:`ChartDataPoint` object for each point."""
    
    def clear_format(self) -> None:
        """Clears format of this data point. The properties are set to the default values defined in the parent series."""
        ...
    
    @property
    def index(self) -> int:
        """Index of the data point this object applies formatting to."""
        ...
    
    @property
    def explosion(self) -> int:
        """Specifies the amount the data point shall be moved from the center of the pie.
        Can be negative, negative means that property is not set and no explosion should be applied.
        Applies only to Pie charts."""
        ...
    
    @explosion.setter
    def explosion(self, value: int):
        ...
    
    @property
    def invert_if_negative(self) -> bool:
        """Specifies whether the parent element shall inverts its colors if the value is negative."""
        ...
    
    @invert_if_negative.setter
    def invert_if_negative(self, value: bool):
        ...
    
    @property
    def bubble_3d(self) -> bool:
        """Specifies whether the bubbles in Bubble chart should have a 3-D effect applied to them."""
        ...
    
    @bubble_3d.setter
    def bubble_3d(self, value: bool):
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of this data point."""
        ...
    
    @property
    def marker(self) -> aspose.words.drawing.charts.ChartMarker:
        """Specifies chart data marker."""
        ...
    
    ...

class ChartDataPointCollection:
    """Represents collection of a :class:`ChartDataPoint`.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartDataPoint:
        """Returns :class:`ChartDataPoint` for the specified index."""
        ...
    
    def clear_format(self) -> None:
        """Clears format of all :class:`ChartDataPoint` in this collection."""
        ...
    
    def has_default_format(self, data_point_index: int) -> bool:
        """Gets a flag indicating whether the data point at the specified index has default format."""
        ...
    
    def copy_format(self, source_index: int, destination_index: int) -> None:
        """Copies format from the source data point to the destination data point."""
        ...
    
    @property
    def count(self) -> int:
        """Returns the number of :class:`ChartDataPoint` in this collection."""
        ...
    
    ...

class ChartDataTable:
    """Allows to specify properties of a chart data table."""
    
    @property
    def show(self) -> bool:
        """Gets or sets a flag indicating whether the data table will be shown for the chart.
        Default value is ``False``.
        
        The following chart types do not support data tables: Scatter, Pie, Doughnut, Surface, Radar, Treemap,
        Sunburst, Histogram, Pareto, Box and Whisker, Waterfall, Funnel, Combo charts that include series of
        these types. Showing a data table for the chart types throws a System.InvalidOperationException
        exception."""
        ...
    
    @show.setter
    def show(self, value: bool):
        ...
    
    @property
    def has_legend_keys(self) -> bool:
        """Gets or sets a flag indicating whether legend keys are displayed in the data table.
        The default value is ``True``."""
        ...
    
    @has_legend_keys.setter
    def has_legend_keys(self, value: bool):
        ...
    
    @property
    def has_horizontal_border(self) -> bool:
        """Gets or sets a flag indicating whether a horizontal border of the data table is displayed.
        The default value is ``True``."""
        ...
    
    @has_horizontal_border.setter
    def has_horizontal_border(self, value: bool):
        ...
    
    @property
    def has_vertical_border(self) -> bool:
        """Gets or sets a flag indicating whether a vertical border of the data table is displayed.
        The default value is ``True``."""
        ...
    
    @has_vertical_border.setter
    def has_vertical_border(self, value: bool):
        ...
    
    @property
    def has_outline_border(self) -> bool:
        """Gets or sets a flag indicating whether an outline border, that is, a border around series and category names,
        is displayed.
        The default value is ``True``."""
        ...
    
    @has_outline_border.setter
    def has_outline_border(self, value: bool):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to font formatting of the data table."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill of text background and border formatting of the data table."""
        ...
    
    ...

class ChartFormat:
    """Represents the formatting of a chart element.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def set_default_fill(self) -> None:
        """Resets the fill of the chart element to have the default value."""
        ...
    
    @property
    def fill(self) -> aspose.words.drawing.Fill:
        """Gets fill formatting for the parent chart element."""
        ...
    
    @property
    def stroke(self) -> aspose.words.drawing.Stroke:
        """Gets line formatting for the parent chart element."""
        ...
    
    @property
    def shape_type(self) -> aspose.words.drawing.charts.ChartShapeType:
        """Gets or sets the shape type of the parent chart element.
        
        Currently, the property can only be used for data labels."""
        ...
    
    @shape_type.setter
    def shape_type(self, value: aspose.words.drawing.charts.ChartShapeType):
        ...
    
    @property
    def is_defined(self) -> bool:
        """Gets a flag indicating whether any format is defined."""
        ...
    
    ...

class ChartLegend:
    """Represents chart legend properties.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def legend_entries(self) -> aspose.words.drawing.charts.ChartLegendEntryCollection:
        """Returns a collection of legend entries for all series and trendlines of the parent chart."""
        ...
    
    @property
    def position(self) -> aspose.words.drawing.charts.LegendPosition:
        """Specifies the position of the legend on a chart.
        
        The default value is :attr:`LegendPosition.RIGHT` for pre-Word 2016 charts and
        :attr:`LegendPosition.TOP` for Word 2016 charts."""
        ...
    
    @position.setter
    def position(self, value: aspose.words.drawing.charts.LegendPosition):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the default font formatting of legend entries. To override the font formatting for
        a specific legend entry, use the:attr:`ChartLegendEntry.font` property."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the legend."""
        ...
    
    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap legend.
        Default value is ``False``."""
        ...
    
    @overlay.setter
    def overlay(self, value: bool):
        ...
    
    ...

class ChartLegendEntry:
    """Represents a chart legend entry.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article.
    
    A legend entry corresponds to a specific chart series or trendline.
    
    The text of the entry is the name of the series or trendline. The text cannot be changed."""
    
    @property
    def is_hidden(self) -> bool:
        """Gets or sets a value indicating whether this entry is hidden in the chart legend.
        The default value is **false**.
        
        When a chart legend entry is hidden, it does not affect the corresponding chart series or trendline that
        is still displayed on the chart."""
        ...
    
    @is_hidden.setter
    def is_hidden(self, value: bool):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of this legend entry."""
        ...
    
    ...

class ChartLegendEntryCollection:
    """Represents a collection of chart legend entries.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartLegendEntry:
        """Returns :class:`ChartLegendEntry` for the specified index."""
        ...
    
    @property
    def count(self) -> int:
        """Returns the number of :class:`ChartLegendEntry` in this collection."""
        ...
    
    ...

class ChartMarker:
    """Represents a chart data marker.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def symbol(self) -> aspose.words.drawing.charts.MarkerSymbol:
        """Gets or sets chart marker symbol."""
        ...
    
    @symbol.setter
    def symbol(self, value: aspose.words.drawing.charts.MarkerSymbol):
        ...
    
    @property
    def size(self) -> int:
        """Gets or sets chart marker size.
        Default value is 7."""
        ...
    
    @size.setter
    def size(self, value: int):
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of this marker."""
        ...
    
    ...

class ChartMultilevelValue:
    """Represents a value for charts that display multilevel data."""
    
    @overload
    def __init__(self, level1: str, level2: str, level3: str):
        """Initializes a new instance of this class that represents a three-level value."""
        ...
    
    @overload
    def __init__(self, level1: str, level2: str):
        """Initializes a new instance of this class that represents a two-level value."""
        ...
    
    @overload
    def __init__(self, level1: str):
        """Initializes a new instance of this class that represents a single-level value."""
        ...
    
    @property
    def level1(self) -> str:
        """Gets the name of the chart top level that this value refers to."""
        ...
    
    @property
    def level2(self) -> str:
        """Gets the name of the chart intermediate level that this value refers to."""
        ...
    
    @property
    def level3(self) -> str:
        """Gets the name of the chart bottom level that this value refers to."""
        ...
    
    ...

class ChartNumberFormat:
    """Represents number formatting of the parent element.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def format_code(self) -> str:
        """Gets or sets the format code applied to a data label.
        
        Number formatting is used to change the way a value appears in data label and can be used in some very creative ways.
        The examples of number formats:
        Number - "#,##0.00"
        
        Currency - "\\"$\\"#,##0.00"
        
        Time - "[$-x-systime]h:mm:ss AM/PM"
        
        Date - "d/mm/yyyy"
        
        Percentage - "0.00%"
        
        Fraction - "# ?/?"
        
        Scientific - "0.00E+00"
        
        Text - "@"
        
        Accounting - "_-\\"$\\"\* #,##0.00_-;-\\"$\\"\* #,##0.00_-;_-\\"$\\"\* \\"-\\"??_-;_-@_-"
        
        Custom with color - "[Red]-#,##0.0""""
        ...
    
    @format_code.setter
    def format_code(self, value: str):
        ...
    
    @property
    def is_linked_to_source(self) -> bool:
        """Specifies whether the format code is linked to a source cell.
        Default is true.
        
        The NumberFormat will be reset to general if format code is linked to source."""
        ...
    
    @is_linked_to_source.setter
    def is_linked_to_source(self, value: bool):
        ...
    
    ...

class ChartSeries:
    """Represents chart series properties.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @overload
    def add(self, x_value: aspose.words.drawing.charts.ChartXValue) -> None:
        """Adds the specified X value to the chart series. If the series supports Y values and bubble sizes, they will
        be empty for the X value."""
        ...
    
    @overload
    def add(self, x_value: aspose.words.drawing.charts.ChartXValue, y_value: aspose.words.drawing.charts.ChartYValue) -> None:
        """Adds the specified X and Y values to the chart series."""
        ...
    
    @overload
    def add(self, x_value: aspose.words.drawing.charts.ChartXValue, y_value: aspose.words.drawing.charts.ChartYValue, bubble_size: float) -> None:
        """Adds the specified X value, Y value and bubble size to the chart series."""
        ...
    
    @overload
    def insert(self, index: int, x_value: aspose.words.drawing.charts.ChartXValue) -> None:
        """Inserts the specified X value into the chart series at the specified index. If the series supports Y values
        and bubble sizes, they will be empty for the X value.
        
        The corresponding data point with default formatting will be inserted into the data point collection. And,
        if data labels are displayed, the corresponding data label with default formatting will be inserted too."""
        ...
    
    @overload
    def insert(self, index: int, x_value: aspose.words.drawing.charts.ChartXValue, y_value: aspose.words.drawing.charts.ChartYValue) -> None:
        """Inserts the specified X and Y values into the chart series at the specified index.
        
        The corresponding data point with default formatting will be inserted into the data point collection. And,
        if data labels are displayed, the corresponding data label with default formatting will be inserted too."""
        ...
    
    @overload
    def insert(self, index: int, x_value: aspose.words.drawing.charts.ChartXValue, y_value: aspose.words.drawing.charts.ChartYValue, bubble_size: float) -> None:
        """Inserts the specified X value, Y value and bubble size into the chart series at the specified index.
        
        The corresponding data point with default formatting will be inserted into the data point collection. And,
        if data labels are displayed, the corresponding data label with default formatting will be inserted too."""
        ...
    
    def remove(self, index: int) -> None:
        """Removes the X value, Y value, and bubble size, if supported, from the chart series at the specified index.
        The corresponding data point and data label are also removed."""
        ...
    
    def clear(self) -> None:
        """Removes all data values from the chart series. Format of all individual data points and data labels is cleared."""
        ...
    
    def clear_values(self) -> None:
        """Removes all data values from the chart series with preserving the format of the data points and data labels."""
        ...
    
    def copy_format_from(self, data_point_index: int) -> None:
        """Copies default data point format from the data point with the specified index."""
        ...
    
    @property
    def explosion(self) -> int:
        """Specifies the amount the data point shall be moved from the center of the pie.
        Can be negative, negative means that property is not set and no explosion should be applied.
        Applies only to Pie charts."""
        ...
    
    @explosion.setter
    def explosion(self, value: int):
        ...
    
    @property
    def invert_if_negative(self) -> bool:
        """Specifies whether the parent element shall inverts its colors if the value is negative."""
        ...
    
    @invert_if_negative.setter
    def invert_if_negative(self, value: bool):
        ...
    
    @property
    def marker(self) -> aspose.words.drawing.charts.ChartMarker:
        """Specifies a data marker. Marker is automatically created when requested."""
        ...
    
    @property
    def bubble_3d(self) -> bool:
        """Specifies whether the bubbles in Bubble chart should have a 3-D effect applied to them."""
        ...
    
    @bubble_3d.setter
    def bubble_3d(self, value: bool):
        ...
    
    @property
    def data_points(self) -> aspose.words.drawing.charts.ChartDataPointCollection:
        """Returns a collection of formatting objects for all data points in this series."""
        ...
    
    @property
    def name(self) -> str:
        """Gets or sets the name of the series, if name is not set explicitly it is generated using index.
        By default returns Series plus one based index."""
        ...
    
    @name.setter
    def name(self, value: str):
        ...
    
    @property
    def smooth(self) -> bool:
        """Allows to specify whether the line connecting the points on the chart shall be smoothed using Catmull-Rom splines."""
        ...
    
    @smooth.setter
    def smooth(self, value: bool):
        ...
    
    @property
    def has_data_labels(self) -> bool:
        """Gets or sets a flag indicating whether data labels are displayed for the series."""
        ...
    
    @has_data_labels.setter
    def has_data_labels(self, value: bool):
        ...
    
    @property
    def data_labels(self) -> aspose.words.drawing.charts.ChartDataLabelCollection:
        """Specifies the settings for the data labels for the entire series."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the series."""
        ...
    
    @property
    def legend_entry(self) -> aspose.words.drawing.charts.ChartLegendEntry:
        """Gets a legend entry for this chart series."""
        ...
    
    @property
    def series_type(self) -> aspose.words.drawing.charts.ChartSeriesType:
        """Gets the type of this chart series."""
        ...
    
    @property
    def x_values(self) -> aspose.words.drawing.charts.ChartXValueCollection:
        """Gets a collection of X values for this chart series."""
        ...
    
    @property
    def y_values(self) -> aspose.words.drawing.charts.ChartYValueCollection:
        """Gets a collection of Y values for this chart series."""
        ...
    
    @property
    def bubble_sizes(self) -> aspose.words.drawing.charts.BubbleSizeCollection:
        """Gets a collection of bubble sizes for this chart series."""
        ...
    
    ...

class ChartSeriesCollection:
    """Represents collection of a :class:`ChartSeries`.
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartSeries:
        """Returns a :class:`ChartSeries` at the specified index.
        
        The index is zero-based.
        
        Negative indexes are allowed and indicate access from the back of the collection.
        For example -1 means the last item, -2 means the second before last and so on.
        
        If index is greater than or equal to the number of items in the list, this returns a null reference.
        
        If index is negative and its absolute value is greater than the number of items in the list, this returns a null reference.
        
        :param index: An index into the collection."""
        ...
    
    @overload
    def add(self, series_name: str, categories: List[str], values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Bar, Column, Line and Surface charts.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @overload
    def add(self, series_name: str, x_values: List[float], y_values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Scatter charts.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @overload
    def add(self, series_name: str, dates: List[datetime.datetime], values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Area, Radar and Stock charts."""
        ...
    
    @overload
    def add(self, series_name: str, x_values: List[float], y_values: List[float], bubble_sizes: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Bubble charts.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @overload
    def add(self, series_name: str, categories: List[aspose.words.drawing.charts.ChartMultilevelValue], values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series that have multi-level data categories.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @overload
    def add(self, series_name: str, x_values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to Histogram charts.
        
        For chart types other than Histogram, this method adds a series with empty Y values.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @overload
    def add(self, series_name: str, categories: List[str], values: List[float], is_subtotal: List[bool]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to Waterfall charts.
        
        For chart types other than Waterfall, *isSubtotal* values are ignored.
        
        :param series_name: A name of the series to be added.
        :param categories: Category names for the X axis.
        :param values: Y-axis values.
        :param is_subtotal: Values indicating whether the corresponding Y value is a subtotal.
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    def remove_at(self, index: int) -> None:
        """Removes a :class:`ChartSeries` at the specified index.
        
        :param index: The zero-based index of the :class:`ChartSeries` to remove."""
        ...
    
    def clear(self) -> None:
        """Removes all :class:`ChartSeries` from this collection."""
        ...
    
    def add_double(self, series_name: str, x_values: List[float], y_values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Scatter charts.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    def add_date(self, series_name: str, dates: List[datetime.datetime], values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series to any type of Area, Radar and Stock charts."""
        ...
    
    def add_multilevel_value(self, series_name: str, categories: List[aspose.words.drawing.charts.ChartMultilevelValue], values: List[float]) -> aspose.words.drawing.charts.ChartSeries:
        """Adds new :class:`ChartSeries` to this collection.
        Use this method to add series that have multi-level data categories.
        
        :returns: Recently added :class:`ChartSeries` object."""
        ...
    
    @property
    def count(self) -> int:
        """Returns the number of :class:`ChartSeries` in this collection."""
        ...
    
    ...

class ChartSeriesGroup:
    """Represents properties of a chart series group, that is, the properties of chart series of the same type
    associated with the same axes.
    
    Combo charts contains multiple chart series groups, with a separate group for each series type.
    
    Also, you can create a chart series group to assign secondary axes to one or more chart series.
    
    To learn more, visit the `
                Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def series_type(self) -> aspose.words.drawing.charts.ChartSeriesType:
        """Gets the type of chart series included in this group."""
        ...
    
    @property
    def axis_group(self) -> aspose.words.drawing.charts.AxisGroup:
        """Gets or sets the axis group to which this series group belongs."""
        ...
    
    @axis_group.setter
    def axis_group(self, value: aspose.words.drawing.charts.AxisGroup):
        ...
    
    @property
    def axis_x(self) -> aspose.words.drawing.charts.ChartAxis:
        """Provides access to properties of the X axis of this series group."""
        ...
    
    @property
    def axis_y(self) -> aspose.words.drawing.charts.ChartAxis:
        """Provides access to properties of the Y axis of this series group."""
        ...
    
    @property
    def series(self) -> aspose.words.drawing.charts.ChartSeriesCollection:
        """Gets a collection of series that belong to this series group."""
        ...
    
    @property
    def overlap(self) -> int:
        """Gets or sets the percentage of how much the series bars or columns overlap.
        
        Applies to series groups of all bar and column types.
        
        The range of acceptable values is from -100 to 100 inclusive. A value of 0 indicates that there is no
        space between bars/columns. If the value is -100, the distance between bars/columns is equal to their width.
        A value of 100 means that the bars/columns overlap completely."""
        ...
    
    @overlap.setter
    def overlap(self, value: int):
        ...
    
    @property
    def gap_width(self) -> int:
        """Gets or sets the percentage of gap width between chart elements.
        
        Applies only to series groups of the bar, column, pie-of-bar, pie-of-pie, histogram, box&whisker,
        waterfall and funnel types.
        
        The range of acceptable values is from 0 to 500 inclusive. For bar/column-based series groups, the
        property represents the space between bar clusters as a percentage of their width. For pie-of-pie and
        bar-of-pie charts, this is the space between the primary and secondary sections of the chart."""
        ...
    
    @gap_width.setter
    def gap_width(self, value: int):
        ...
    
    @property
    def bubble_scale(self) -> int:
        """Gets or sets the size of the bubbles as a percentage of their default size.
        
        Applies only to series groups of the :attr:`ChartSeriesType.BUBBLE` and
        :attr:`ChartSeriesType.BUBBLE_3D` types.
        
        The range of acceptable values is from 0 to 300 inclusive."""
        ...
    
    @bubble_scale.setter
    def bubble_scale(self, value: int):
        ...
    
    ...

class ChartSeriesGroupCollection:
    """Represents a collection of :class:`ChartSeriesGroup` objects.
    
    To learn more, visit the `Working with Charts <https://docs.aspose.com/words/python-net/working-with-charts/>`
    documentation article."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartSeriesGroup:
        """Returns a :class:`ChartSeriesGroup` at the specified index."""
        ...
    
    def remove_at(self, index: int) -> None:
        """Removes a series group at the specified index. All child series will be removed from the chart."""
        ...
    
    def add(self, series_type: aspose.words.drawing.charts.ChartSeriesType) -> aspose.words.drawing.charts.ChartSeriesGroup:
        """Adds a new series group of the specified series type to this collection.
        
        Combo charts can contain series groups only of the following types: area, bar, column, line, pie, scatter,
        radar and stock types (except the corresponding 3D series types)."""
        ...
    
    @property
    def count(self) -> int:
        """Returns the number of series groups in this collection."""
        ...
    
    ...

class ChartTitle:
    """Provides access to the chart title properties.
    To learn more, visit the `Working with
                Charts <https://docs.aspose.com/words/python-net/working-with-charts/>` documentation article."""
    
    @property
    def text(self) -> str:
        """Gets or sets the text of the chart title.
        If ``None`` or empty value is specified, auto generated title will be shown.
        
        Use :attr:`ChartTitle.show` option if you need to hide the Title."""
        ...
    
    @text.setter
    def text(self, value: str):
        ...
    
    @property
    def overlay(self) -> bool:
        """Determines whether other chart elements shall be allowed to overlap title.
        By default overlay is ``False``."""
        ...
    
    @overlay.setter
    def overlay(self, value: bool):
        ...
    
    @property
    def show(self) -> bool:
        """Determines whether the title shall be shown for this chart.
        Default value is ``True``."""
        ...
    
    @show.setter
    def show(self, value: bool):
        ...
    
    @property
    def font(self) -> aspose.words.Font:
        """Provides access to the font formatting of the chart title."""
        ...
    
    @property
    def format(self) -> aspose.words.drawing.charts.ChartFormat:
        """Provides access to fill and line formatting of the chart title."""
        ...
    
    ...

class ChartXValue:
    """Represents an X value for a chart series.
    
    This class contains a number of static methods for creating an X value of a particular type. The
    :attr:`ChartXValue.value_type` property allows you to determine the type of an existing X value.
    
    All non-null X values of a chart series must be of the same :class:`ChartXValueType` type."""
    
    @staticmethod
    def from_string(value: str) -> aspose.words.drawing.charts.ChartXValue:
        """Creates a :class:`ChartXValue` instance of the :attr:`ChartXValueType.STRING` type."""
        ...
    
    @staticmethod
    def from_double(value: float) -> aspose.words.drawing.charts.ChartXValue:
        """Creates a :class:`ChartXValue` instance of the :attr:`ChartXValueType.DOUBLE` type."""
        ...
    
    @staticmethod
    def from_date_time(value: datetime.datetime) -> aspose.words.drawing.charts.ChartXValue:
        """Creates a :class:`ChartXValue` instance of the :attr:`ChartXValueType.DATE_TIME` type."""
        ...
    
    @staticmethod
    def from_time_span(value: datetime.timespan) -> aspose.words.drawing.charts.ChartXValue:
        """Creates a :class:`ChartXValue` instance of the :attr:`ChartXValueType.TIME` type."""
        ...
    
    @staticmethod
    def from_multilevel_value(value: aspose.words.drawing.charts.ChartMultilevelValue) -> aspose.words.drawing.charts.ChartXValue:
        """Creates a :class:`ChartXValue` instance of the :attr:`ChartXValueType.MULTILEVEL` type."""
        ...
    
    @property
    def value_type(self) -> aspose.words.drawing.charts.ChartXValueType:
        """Gets the type of the X value stored in the object."""
        ...
    
    @property
    def string_value(self) -> str:
        """Gets the stored string value."""
        ...
    
    @property
    def double_value(self) -> float:
        """Gets the stored numeric value."""
        ...
    
    @property
    def date_time_value(self) -> datetime.datetime:
        """Gets the stored datetime value."""
        ...
    
    @property
    def time_value(self) -> datetime.timespan:
        """Gets the stored time value."""
        ...
    
    @property
    def multilevel_value(self) -> aspose.words.drawing.charts.ChartMultilevelValue:
        """Gets the stored multilevel value."""
        ...
    
    ...

class ChartXValueCollection:
    """Represents a collection of X values for a chart series.
    
    All items of the collection other than **null** must have the same :attr:`ChartXValue.value_type`.
    
    The collection allows only changing X values. To add or insert new values to a chart series, or remove values,
    the appropriate methods of the :class:`ChartSeries` class can be used."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartXValue:
        """Gets or sets the X value at the specified index.
        
        Empty values are represented as **null**."""
        ...
    
    def __setitem__(self, index: int, value: aspose.words.drawing.charts.ChartXValue):
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of items in this collection."""
        ...
    
    ...

class ChartYValue:
    """Represents an Y value for a chart series.
    
    This class contains a number of static methods for creating an Y value of a particular type. The
    :attr:`ChartYValue.value_type` property allows you to determine the type of an existing Y value.
    
    All non-null Y values of a chart series must be of the same :class:`ChartYValueType` type."""
    
    @staticmethod
    def from_double(value: float) -> aspose.words.drawing.charts.ChartYValue:
        """Creates a :class:`ChartYValue` instance of the :attr:`ChartYValueType.DOUBLE` type."""
        ...
    
    @staticmethod
    def from_date_time(value: datetime.datetime) -> aspose.words.drawing.charts.ChartYValue:
        """Creates a :class:`ChartYValue` instance of the :attr:`ChartYValueType.DATE_TIME` type."""
        ...
    
    @staticmethod
    def from_time_span(value: datetime.timespan) -> aspose.words.drawing.charts.ChartYValue:
        """Creates a :class:`ChartYValue` instance of the :attr:`ChartYValueType.TIME` type."""
        ...
    
    @property
    def value_type(self) -> aspose.words.drawing.charts.ChartYValueType:
        """Gets the type of the Y value stored in the object."""
        ...
    
    @property
    def double_value(self) -> float:
        """Gets the stored numeric value."""
        ...
    
    @property
    def date_time_value(self) -> datetime.datetime:
        """Gets the stored datetime value."""
        ...
    
    @property
    def time_value(self) -> datetime.timespan:
        """Gets the stored time value."""
        ...
    
    ...

class ChartYValueCollection:
    """Represents a collection of Y values for a chart series.
    
    All items of the collection other than **null** must have the same :attr:`ChartYValue.value_type`.
    
    The collection allows only changing Y values. To add or insert new values to a chart series, or remove values,
    the appropriate methods of the :class:`ChartSeries` class can be used."""
    
    def __getitem__(self, index: int) -> aspose.words.drawing.charts.ChartYValue:
        """Gets or sets the Y value at the specified index.
        
        Empty values are represented as **null**."""
        ...
    
    def __setitem__(self, index: int, value: aspose.words.drawing.charts.ChartYValue):
        ...
    
    @property
    def count(self) -> int:
        """Gets the number of items in this collection."""
        ...
    
    ...

class IChartDataPoint:
    """Contains properties of a single data point on the chart."""
    
    @property
    def explosion(self) -> int:
        """Specifies the amount the data point shall be moved from the center of the pie.
        Can be negative, negative means that property is not set and no explosion should be applied.
        Applies only to Pie charts."""
        ...
    
    @explosion.setter
    def explosion(self, value: int):
        ...
    
    @property
    def invert_if_negative(self) -> bool:
        """Specifies whether the parent element shall inverts its colors if the value is negative."""
        ...
    
    @invert_if_negative.setter
    def invert_if_negative(self, value: bool):
        ...
    
    @property
    def marker(self) -> aspose.words.drawing.charts.ChartMarker:
        """Specifies a data marker. Marker is automatically created when requested."""
        ...
    
    @property
    def bubble_3d(self) -> bool:
        """Specifies whether the bubbles in Bubble chart should have a 3-D effect applied to them."""
        ...
    
    @bubble_3d.setter
    def bubble_3d(self, value: bool):
        ...
    
    ...

class AxisBuiltInUnit(Enum):
    """Specifies the display units for an axis."""
    
    """Specifies the values on the chart shall displayed as is."""
    NONE: int
    
    """Specifies the values on the chart shall be divided by a user-defined divisor. This value is not supported
    by the new chart types of MS Office 2016."""
    CUSTOM: int
    
    """Specifies the values on the chart shall be divided by 1,000,000,000."""
    BILLIONS: int
    
    """Specifies the values on the chart shall be divided by 100,000,000."""
    HUNDRED_MILLIONS: int
    
    """Specifies the values on the chart shall be divided by 100."""
    HUNDREDS: int
    
    """Specifies the values on the chart shall be divided by 100,000."""
    HUNDRED_THOUSANDS: int
    
    """Specifies the values on the chart shall be divided by 1,000,000."""
    MILLIONS: int
    
    """Specifies the values on the chart shall be divided by 10,000,000."""
    TEN_MILLIONS: int
    
    """Specifies the values on the chart shall be divided by 10,000."""
    TEN_THOUSANDS: int
    
    """Specifies the values on the chart shall be divided by 1,000."""
    THOUSANDS: int
    
    """Specifies the values on the chart shall be divided by 1,000,000,000,0000."""
    TRILLIONS: int
    
    """Specifies the values on the chart shall be divided by 0.01. This value is supported only by the new chart
    types of MS Office 2016."""
    PERCENTAGE: int
    

class AxisCategoryType(Enum):
    """Specifies type of a category axis."""
    
    """Specifies that type of a category axis is determined automatically based on data."""
    AUTOMATIC: int
    
    """Specifies an axis of an arbitrary set of categories."""
    CATEGORY: int
    
    """Specifies a time category axis."""
    TIME: int
    

class AxisCrosses(Enum):
    """Specifies the possible crossing points for an axis."""
    
    """The category axis crosses at the zero point of the value axis (if possible), or at the minimum value
    if the minimum is greater than zero, or at the maximum if the maximum is less than zero."""
    AUTOMATIC: int
    
    """A perpendicular axis crosses at the maximum value of the axis."""
    MAXIMUM: int
    
    """A perpendicular axis crosses at the minimum value of the axis."""
    MINIMUM: int
    
    """A perpendicular axis crosses at the specified value of the axis."""
    CUSTOM: int
    

class AxisGroup(Enum):
    """Represents a type of a chart axis group."""
    
    """Specifies the primary axis group."""
    PRIMARY: int
    
    """Specifies the secondary axis group."""
    SECONDARY: int
    

class AxisScaleType(Enum):
    """Specifies the possible scale types for an axis."""
    
    """Linear scaling."""
    LINEAR: int
    
    """Logarithmic scaling."""
    LOGARITHMIC: int
    

class AxisTickLabelPosition(Enum):
    """Specifies the possible positions for tick labels."""
    
    """Specifies the axis labels shall be at the high end of the perpendicular axis."""
    HIGH: int
    
    """Specifies the axis labels shall be at the low end of the perpendicular axis."""
    LOW: int
    
    """Specifies the axis labels shall be next to the axis."""
    NEXT_TO_AXIS: int
    
    """Specifies the axis labels are not drawn."""
    NONE: int
    
    """Specifies default value of tick labels position."""
    DEFAULT: int
    

class AxisTickMark(Enum):
    """Specifies the possible positions for tick marks."""
    
    """Specifies that the tick marks shall cross the axis."""
    CROSS: int
    
    """Specifies that the tick marks shall be inside the plot area."""
    INSIDE: int
    
    """Specifies that the tick marks shall be outside the plot area."""
    OUTSIDE: int
    
    """Specifies that there shall be no tick marks."""
    NONE: int
    

class AxisTimeUnit(Enum):
    """Specifies the unit of time for axes."""
    
    """Specifies that unit was not set explicitly and default value should be used."""
    AUTOMATIC: int
    
    """Specifies that the chart data shall be shown in days."""
    DAYS: int
    
    """Specifies that the chart data shall be shown in months."""
    MONTHS: int
    
    """Specifies that the chart data shall be shown in years."""
    YEARS: int
    

class ChartAxisType(Enum):
    """Specifies type of chart axis."""
    
    """Category axis of a chart."""
    CATEGORY: int
    
    """Series axis of a chart."""
    SERIES: int
    
    """Value axis of a chart."""
    VALUE: int
    

class ChartSeriesType(Enum):
    """Specifies a type of a chart series."""
    
    """Represents an Area chart series."""
    AREA: int
    
    """Represents a Stacked Area chart series."""
    AREA_STACKED: int
    
    """Represents a 100% Stacked Area chart series."""
    AREA_PERCENT_STACKED: int
    
    """Represents a 3D Area chart series."""
    AREA_3D: int
    
    """Represents a 3D Stacked Area chart series."""
    AREA_3D_STACKED: int
    
    """Represents a 3D 100% Stacked Area chart series."""
    AREA_3D_PERCENT_STACKED: int
    
    """Represents a Bar chart series."""
    BAR: int
    
    """Represents a Stacked Bar chart series."""
    BAR_STACKED: int
    
    """Represents a 100% Stacked Bar chart series."""
    BAR_PERCENT_STACKED: int
    
    """Represents a 3D Bar chart series."""
    BAR_3D: int
    
    """Represents a 3D Stacked Bar chart series."""
    BAR_3D_STACKED: int
    
    """Represents a 3D 100% Stacked Bar chart series."""
    BAR_3D_PERCENT_STACKED: int
    
    """Represents a Bubble chart series."""
    BUBBLE: int
    
    """Represents a 3D Bubble chart series."""
    BUBBLE_3D: int
    
    """Represents a Column chart series."""
    COLUMN: int
    
    """Represents a Stacked Column chart series."""
    COLUMN_STACKED: int
    
    """Represents a 100% Stacked Column chart series."""
    COLUMN_PERCENT_STACKED: int
    
    """Represents a 3D Column chart series."""
    COLUMN_3D: int
    
    """Represents a 3D Stacked Column chart series."""
    COLUMN_3D_STACKED: int
    
    """Represents a 3D 100% Stacked Column chart series."""
    COLUMN_3D_PERCENT_STACKED: int
    
    """Represents a 3D Clustered Column chart series."""
    COLUMN_3D_CLUSTERED: int
    
    """Represents a Doughnut chart series."""
    DOUGHNUT: int
    
    """Represents a Line chart series."""
    LINE: int
    
    """Represents a Stacked Line chart series."""
    LINE_STACKED: int
    
    """Represents a 100% Stacked Line chart series."""
    LINE_PERCENT_STACKED: int
    
    """Represents a 3D Line chart series."""
    LINE_3D: int
    
    """Represents a Pie chart series."""
    PIE: int
    
    """Represents a 3D Pie chart series."""
    PIE_3D: int
    
    """Represents a Pie of Bar chart series."""
    PIE_OF_BAR: int
    
    """Represents a Pie of Pie chart series."""
    PIE_OF_PIE: int
    
    """Represents a Radar chart series."""
    RADAR: int
    
    """Represents a Scatter chart series."""
    SCATTER: int
    
    """Represents a Stock chart series."""
    STOCK: int
    
    """Represents a Surface chart series."""
    SURFACE: int
    
    """Represents a 3D Surface chart series."""
    SURFACE_3D: int
    
    """Represents a Treemap chart series."""
    TREEMAP: int
    
    """Represents a Sunburst chart series."""
    SUNBURST: int
    
    """Represents a Histogram chart series."""
    HISTOGRAM: int
    
    """Represents a Pareto chart series."""
    PARETO: int
    
    """Represents a Pareto Line chart series."""
    PARETO_LINE: int
    
    """Represents a Box and Whisker chart series."""
    BOX_AND_WHISKER: int
    
    """Represents a Waterfall chart series."""
    WATERFALL: int
    
    """Represents a Funnel chart series."""
    FUNNEL: int
    
    """Represents a Region Map chart series."""
    REGION_MAP: int
    

class ChartShapeType(Enum):
    """Specifies the shape type of chart elements."""
    
    """Indicates that a shape is not defined for the chart element."""
    DEFAULT: int
    
    """Rectangle."""
    RECTANGLE: int
    
    """Rounded rectangle."""
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
    
    """Home plate."""
    HOME_PLATE: int
    
    """Cube."""
    CUBE: int
    
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
    
    """Straight connector 1."""
    STRAIGHT_CONNECTOR1: int
    
    """Bent connector 2."""
    BENT_CONNECTOR2: int
    
    """Bent connector 3."""
    BENT_CONNECTOR3: int
    
    """Bent connector 4."""
    BENT_CONNECTOR4: int
    
    """Bent connector 5."""
    BENT_CONNECTOR5: int
    
    """Curved connector 2."""
    CURVED_CONNECTOR2: int
    
    """Curved connector 3."""
    CURVED_CONNECTOR3: int
    
    """Curved connector 4."""
    CURVED_CONNECTOR4: int
    
    """Curved connector 5."""
    CURVED_CONNECTOR5: int
    
    """Callout 1."""
    CALLOUT1: int
    
    """Callout 2."""
    CALLOUT2: int
    
    """Callout 3."""
    CALLOUT3: int
    
    """Accent callout 1."""
    ACCENT_CALLOUT1: int
    
    """Accent callout 2."""
    ACCENT_CALLOUT2: int
    
    """Accent callout 3."""
    ACCENT_CALLOUT3: int
    
    """Callout with border 1."""
    BORDER_CALLOUT1: int
    
    """Callout with border 2."""
    BORDER_CALLOUT2: int
    
    """Callout with border 3."""
    BORDER_CALLOUT3: int
    
    """Accent callout with border 1."""
    ACCENT_BORDER_CALLOUT1: int
    
    """Accent callout with border 2."""
    ACCENT_BORDER_CALLOUT2: int
    
    """Accent callout with border 3."""
    ACCENT_BORDER_CALLOUT3: int
    
    """Ribbon."""
    RIBBON: int
    
    """Ribbon 2."""
    RIBBON2: int
    
    """Chevron."""
    CHEVRON: int
    
    """Pentagon."""
    PENTAGON: int
    
    """No smoking."""
    NO_SMOKING: int
    
    """Four pointed star."""
    SEAL4: int
    
    """Six pointed star."""
    SEAL6: int
    
    """Seven pointed star."""
    SEAL7: int
    
    """Eight pointed star."""
    SEAL8: int
    
    """Ten pointed star."""
    SEAL10: int
    
    """Twelve pointed star."""
    SEAL12: int
    
    """Sixteen pointed star."""
    SEAL16: int
    
    """Twenty-four pointed star."""
    SEAL24: int
    
    """Thirty-two pointed star."""
    SEAL32: int
    
    """Callout wedge rectangle."""
    WEDGE_RECT_CALLOUT: int
    
    """Callout wedge round rectangle."""
    WEDGE_R_RECT_CALLOUT: int
    
    """Callout wedge ellipse."""
    WEDGE_ELLIPSE_CALLOUT: int
    
    """Wave."""
    WAVE: int
    
    """Folded corner."""
    FOLDED_CORNER: int
    
    """Left arrow."""
    LEFT_ARROW: int
    
    """Down arrow."""
    DOWN_ARROW: int
    
    """Up  arrow."""
    UP_ARROW: int
    
    """Left and right arrow."""
    LEFT_RIGHT_ARROW: int
    
    """Up and down arrow."""
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
    
    """Callout left arrow."""
    LEFT_ARROW_CALLOUT: int
    
    """Callout right arrow."""
    RIGHT_ARROW_CALLOUT: int
    
    """Callout up arrow."""
    UP_ARROW_CALLOUT: int
    
    """Callout down arrow."""
    DOWN_ARROW_CALLOUT: int
    
    """Callout left and right arrow."""
    LEFT_RIGHT_ARROW_CALLOUT: int
    
    """Callout up and down arrow."""
    UP_DOWN_ARROW_CALLOUT: int
    
    """Callout quad arrow."""
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
    
    """U-turn arrow."""
    UTURN_ARROW: int
    
    """Curved right arrow."""
    CURVED_RIGHT_ARROW: int
    
    """Curved left arrow."""
    CURVED_LEFT_ARROW: int
    
    """Curved up arrow."""
    CURVED_UP_ARROW: int
    
    """Curved down arrow."""
    CURVED_DOWN_ARROW: int
    
    """Callout cloud."""
    CLOUD_CALLOUT: int
    
    """Ellipse ribbon."""
    ELLIPSE_RIBBON: int
    
    """Ellipse ribbon 2."""
    ELLIPSE_RIBBON2: int
    
    """Process flow."""
    FLOW_CHART_PROCESS: int
    
    """Decision flow."""
    FLOW_CHART_DECISION: int
    
    """Input output flow."""
    FLOW_CHART_INPUT_OUTPUT: int
    
    """Predefined process flow."""
    FLOW_CHART_PREDEFINED_PROCESS: int
    
    """Internal storage flow."""
    FLOW_CHART_INTERNAL_STORAGE: int
    
    """Document flow."""
    FLOW_CHART_DOCUMENT: int
    
    """Multi-document flow."""
    FLOW_CHART_MULTIDOCUMENT: int
    
    """Terminator flow."""
    FLOW_CHART_TERMINATOR: int
    
    """Preparation flow."""
    FLOW_CHART_PREPARATION: int
    
    """Manual input flow."""
    FLOW_CHART_MANUAL_INPUT: int
    
    """Manual operation flow."""
    FLOW_CHART_MANUAL_OPERATION: int
    
    """Connector flow."""
    FLOW_CHART_CONNECTOR: int
    
    """Punched card flow."""
    FLOW_CHART_PUNCHED_CARD: int
    
    """Punched tape flow."""
    FLOW_CHART_PUNCHED_TAPE: int
    
    """Summing junction flow."""
    FLOW_CHART_SUMMING_JUNCTION: int
    
    """Or flow."""
    FLOW_CHART_OR: int
    
    """Collate flow."""
    FLOW_CHART_COLLATE: int
    
    """Sort flow."""
    FLOW_CHART_SORT: int
    
    """Extract flow."""
    FLOW_CHART_EXTRACT: int
    
    """Merge flow."""
    FLOW_CHART_MERGE: int
    
    """Offline storage flow."""
    FLOW_CHART_OFFLINE_STORAGE: int
    
    """Online storage flow."""
    FLOW_CHART_ONLINE_STORAGE: int
    
    """Magnetic tape flow."""
    FLOW_CHART_MAGNETIC_TAPE: int
    
    """Magnetic disk flow."""
    FLOW_CHART_MAGNETIC_DISK: int
    
    """Magnetic drum flow."""
    FLOW_CHART_MAGNETIC_DRUM: int
    
    """Display flow."""
    FLOW_CHART_DISPLAY: int
    
    """Delay flow."""
    FLOW_CHART_DELAY: int
    
    """Alternate process flow."""
    FLOW_CHART_ALTERNATE_PROCESS: int
    
    """Off-page connector flow."""
    FLOW_CHART_OFFPAGE_CONNECTOR: int
    
    """Left right up arrow."""
    LEFT_RIGHT_UP_ARROW: int
    
    """Sun."""
    SUN: int
    
    """Moon."""
    MOON: int
    
    """Bracket pair."""
    BRACKET_PAIR: int
    
    """Brace pair."""
    BRACE_PAIR: int
    
    """Double wave."""
    DOUBLE_WAVE: int
    
    """Blank button."""
    ACTION_BUTTON_BLANK: int
    
    """Home button."""
    ACTION_BUTTON_HOME: int
    
    """Help button."""
    ACTION_BUTTON_HELP: int
    
    """Information button."""
    ACTION_BUTTON_INFORMATION: int
    
    """Forward or next button."""
    ACTION_BUTTON_FORWARD_NEXT: int
    
    """Back or previous button."""
    ACTION_BUTTON_BACK_PREVIOUS: int
    
    """End button."""
    ACTION_BUTTON_END: int
    
    """Beginning button."""
    ACTION_BUTTON_BEGINNING: int
    
    """Return button."""
    ACTION_BUTTON_RETURN: int
    
    """Document button."""
    ACTION_BUTTON_DOCUMENT: int
    
    """Sound button."""
    ACTION_BUTTON_SOUND: int
    
    """Movie button."""
    ACTION_BUTTON_MOVIE: int
    
    """Snip single corner rectangle object."""
    SINGLE_CORNER_SNIPPED: int
    
    """Snip same side corner rectangle."""
    TOP_CORNERS_SNIPPED: int
    
    """Snip diagonal corner rectangle."""
    DIAGONAL_CORNERS_SNIPPED: int
    
    """Snip and round single corner rectangle."""
    TOP_CORNERS_ONE_ROUNDED_ONE_SNIPPED: int
    
    """Rounded single corner rectangle."""
    SINGLE_CORNER_ROUNDED: int
    
    """Rounded same side corner rectangle."""
    TOP_CORNERS_ROUNDED: int
    
    """Rounded diagonal corner rectangle."""
    DIAGONAL_CORNERS_ROUNDED: int
    
    """Heptagon."""
    HEPTAGON: int
    
    """Cloud."""
    CLOUD: int
    
    """Swoosh arrow."""
    SWOOSH_ARROW: int
    
    """Teardrop."""
    TEARDROP: int
    
    """Square tabs."""
    SQUARE_TABS: int
    
    """Plaque tabs."""
    PLAQUE_TABS: int
    
    """Pie."""
    PIE: int
    
    """Wedge pie."""
    WEDGE_PIE: int
    
    """Inverse line."""
    INVERSE_LINE: int
    
    """Math plus."""
    MATH_PLUS: int
    
    """Math minus."""
    MATH_MINUS: int
    
    """Math multiply."""
    MATH_MULTIPLY: int
    
    """Math divide."""
    MATH_DIVIDE: int
    
    """Math equal."""
    MATH_EQUAL: int
    
    """Math not equal."""
    MATH_NOT_EQUAL: int
    
    """Non-isosceles trapezoid."""
    NON_ISOSCELES_TRAPEZOID: int
    
    """Left-right circular arrow."""
    LEFT_RIGHT_CIRCULAR_ARROW: int
    
    """Left-right ribbon."""
    LEFT_RIGHT_RIBBON: int
    
    """Left circular arrow."""
    LEFT_CIRCULAR_ARROW: int
    
    """Frame."""
    FRAME: int
    
    """Half frame."""
    HALF_FRAME: int
    
    """Funnel."""
    FUNNEL: int
    
    """Six-tooth gear."""
    GEAR6: int
    
    """Nine-tooth gear."""
    GEAR9: int
    
    """Decagon."""
    DECAGON: int
    
    """Dodecagon."""
    DODECAGON: int
    
    """Diagonal stripe."""
    DIAGONAL_STRIPE: int
    
    """Corner."""
    CORNER: int
    
    """Corner tabs."""
    CORNER_TABS: int
    
    """Chord."""
    CHORD: int
    
    """Chart plus."""
    CHART_PLUS: int
    
    """Chart star."""
    CHART_STAR: int
    
    """Chart X."""
    CHART_X: int
    

class ChartType(Enum):
    """Specifies type of a chart."""
    
    """Area chart."""
    AREA: int
    
    """Stacked Area chart."""
    AREA_STACKED: int
    
    """100% Stacked Area chart."""
    AREA_PERCENT_STACKED: int
    
    """3D Area chart."""
    AREA_3D: int
    
    """3D Stacked Area chart."""
    AREA_3D_STACKED: int
    
    """3D 100% Stacked Area chart."""
    AREA_3D_PERCENT_STACKED: int
    
    """Bar chart."""
    BAR: int
    
    """Stacked Bar chart."""
    BAR_STACKED: int
    
    """100% Stacked Bar chart."""
    BAR_PERCENT_STACKED: int
    
    """3D Bar chart."""
    BAR_3D: int
    
    """3D Stacked Bar chart."""
    BAR_3D_STACKED: int
    
    """3D 100% Stacked Bar chart."""
    BAR_3D_PERCENT_STACKED: int
    
    """Bubble chart."""
    BUBBLE: int
    
    """3D Bubble chart."""
    BUBBLE_3D: int
    
    """Column chart."""
    COLUMN: int
    
    """Stacked Column chart."""
    COLUMN_STACKED: int
    
    """100% Stacked Column chart."""
    COLUMN_PERCENT_STACKED: int
    
    """3D Column chart."""
    COLUMN_3D: int
    
    """3D Stacked Column chart."""
    COLUMN_3D_STACKED: int
    
    """3D 100% Stacked Column chart."""
    COLUMN_3D_PERCENT_STACKED: int
    
    """3D Clustered Column chart."""
    COLUMN_3D_CLUSTERED: int
    
    """Doughnut chart."""
    DOUGHNUT: int
    
    """Line chart."""
    LINE: int
    
    """Stacked Line chart."""
    LINE_STACKED: int
    
    """100% Stacked Line chart."""
    LINE_PERCENT_STACKED: int
    
    """3D Line chart."""
    LINE_3D: int
    
    """Pie chart."""
    PIE: int
    
    """3D Pie chart."""
    PIE_3D: int
    
    """Pie of Bar chart."""
    PIE_OF_BAR: int
    
    """Pie of Pie chart."""
    PIE_OF_PIE: int
    
    """Radar chart."""
    RADAR: int
    
    """Scatter chart."""
    SCATTER: int
    
    """Stock chart."""
    STOCK: int
    
    """Surface chart."""
    SURFACE: int
    
    """3D Surface chart."""
    SURFACE_3D: int
    
    """Treemap chart."""
    TREEMAP: int
    
    """Sunburst chart."""
    SUNBURST: int
    
    """Histogram chart."""
    HISTOGRAM: int
    
    """Pareto chart."""
    PARETO: int
    
    """Box and Whisker chart."""
    BOX_AND_WHISKER: int
    
    """Waterfall chart."""
    WATERFALL: int
    
    """Funnel chart."""
    FUNNEL: int
    

class ChartXValueType(Enum):
    """Allows to specify type of an X value of a chart series."""
    
    """Specifies that an X value is a string category."""
    STRING: int
    
    """Specifies that an X value is a double-precision floating-point number."""
    DOUBLE: int
    
    """Specifies that an X value is a date and time of day."""
    DATE_TIME: int
    
    """Specifies that an X value is a time of day."""
    TIME: int
    
    """Specifies that an X value is a multilevel value."""
    MULTILEVEL: int
    

class ChartYValueType(Enum):
    """Allows to specify type of an Y value of a chart series."""
    
    """Specifies that an Y value is a double-precision floating-point number."""
    DOUBLE: int
    
    """Specifies that an Y value is a date and time of day."""
    DATE_TIME: int
    
    """Specifies that an X value is a time of day."""
    TIME: int
    

class LegendPosition(Enum):
    """Specifies the possible positions for a chart legend."""
    
    """No legend will be shown for the chart."""
    NONE: int
    
    """Specifies that the legend shall be drawn at the bottom of the chart."""
    BOTTOM: int
    
    """Specifies that the legend shall be drawn at the left of the chart."""
    LEFT: int
    
    """Specifies that the legend shall be drawn at the right of the chart."""
    RIGHT: int
    
    """Specifies that the legend shall be drawn at the top of the chart."""
    TOP: int
    
    """Specifies that the legend shall be drawn at the top right of the chart."""
    TOP_RIGHT: int
    

class MarkerSymbol(Enum):
    """Specifies marker symbol style."""
    
    """Specifies a default marker symbol shall be drawn at each data point."""
    DEFAULT: int
    
    """Specifies a circle shall be drawn at each data point."""
    CIRCLE: int
    
    """Specifies a dash shall be drawn at each data point."""
    DASH: int
    
    """Specifies a diamond shall be drawn at each data point."""
    DIAMOND: int
    
    """Specifies a dot shall be drawn at each data point."""
    DOT: int
    
    """Specifies nothing shall be drawn at each data point."""
    NONE: int
    
    """Specifies a picture shall be drawn at each data point."""
    PICTURE: int
    
    """Specifies a plus shall be drawn at each data point."""
    PLUS: int
    
    """Specifies a square shall be drawn at each data point."""
    SQUARE: int
    
    """Specifies a star shall be drawn at each data point."""
    STAR: int
    
    """Specifies a triangle shall be drawn at each data point."""
    TRIANGLE: int
    
    """Specifies an X shall be drawn at each data point."""
    X: int
    


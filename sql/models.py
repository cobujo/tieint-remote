from sqlalchemy import Column, INTEGER, REAL, TEXT, BOOLEAN, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base, declared_attr
import sqlalchemy.types as types
from ast import literal_eval
from settings import constants as cn
from dataclasses import dataclass

Base = declarative_base()
metadata = Base.metadata

# not sure of the cleanest way to create and maintain these models...
# listing all properties that belong to a class for reference, but commenting out those we see no use for
# if later on we discover need for these, will need to uncomment and add datatypes accordingly
# (and possibly classes if they're not native python types)
THREE_ARR_DOUBLES_TYPE = TEXT


class MyTuple(types.TypeDecorator):
    """
    into db as text, out of db as tuple
    """
    impl = types.TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            return literal_eval(value)
        return value


class MyIntOrText(types.TypeDecorator):
    """
    Using this for enum properties that typically use ints but may use certain constants
    """
    impl = types.TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        try:
            return int(value)
        except ValueError:
            return value


class MyDocument(types.TypeDecorator):
    """
    into db as document name
    """
    impl = types.TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        # if isinstance(value, AcadDocument)  # importing AcadDocument was causing a circular import, not a hard requirement to use the class
        from acad.document import AcadDocument
        # if hasattr(value, 'name'):
        if isinstance(value, AcadDocument):
            return value.name
        return value


class ObjectBase(Base):
    """
    Must be a real table in order to establish coordinates -> object relationship*,
    however will be autofilled on object entry; records should not be directly added here.
    Although this isn't an Acad native table, still adding the '_' to the end of the field
    because it will be inherited by native Acad tables (to indicate this isn't a native property)

    *this is currently one directional, as we don't want to set up relationships back to coordinates
    for every AcDb table; expecting to query coordinates to get objects, not the other way around
    """
    __tablename__ = 'objects_mapper'
    id_ = Column(INTEGER, primary_key=True)
    tablename_ = Column(TEXT)

    coordinates_ = relationship('ObjectCoordinates', back_populates='object')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': tablename_
    }


class ObjectBoundingBoxBase(Base):
    """
    modeled after ObjectBase
    """
    __tablename__ = 'objects_bounding_box_mapper'
    id_ = Column(INTEGER, primary_key=True)
    tablename_ = Column(TEXT)

    bounding_box_ = relationship('ObjectBoundingBox', back_populates='object')
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': tablename_
    }


class AcadObjectBase(ObjectBase):
    __abstract__ = True
    id_ = Column(INTEGER, ForeignKey('objects_mapper.id_'), primary_key=True)
    # application
    document = Column(MyDocument(), primary_key=True)
    handle = Column(TEXT, primary_key=True)
    # has_extension_dictionary
    object_id = Column(INTEGER)
    object_name = Column(TEXT)
    owner_id = Column(INTEGER)
    space_ = Column(cn.SPACE_ATTR_NAME, TEXT)

    def __repr__(self):
        return f'<{self.__class__.__name__}: ({self.handle})>'


class AcadEntityBase(AcadObjectBase):
    __abstract__ = True
    entity_transparency = Column(TEXT)
    # hyperlinks
    layer = Column(TEXT)
    linetype = Column(TEXT)
    linetype_scale = Column(REAL)
    lineweight = Column(TEXT)
    material = Column(TEXT)
    plot_style_name = Column(TEXT)
    # true_color
    visible = Column(BOOLEAN)


class AcDbArcBase(AcadEntityBase):
    __tablename__ = 'acdb_arcs'
    arc_length = Column(REAL)
    area = Column(REAL)
    center = Column(MyTuple())
    end_angle = Column(REAL)
    end_point = Column(MyTuple())
    normal = Column(MyTuple())
    radius = Column(REAL)
    start_angle = Column(REAL)
    start_point = Column(MyTuple())
    thickness = Column(REAL)
    total_angle = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbBlockReferenceBase(AcadEntityBase):
    __tablename__ = 'acdb_block_references'
    effective_name = Column(TEXT)
    has_attributes = Column(BOOLEAN)
    insertion_point = Column(MyTuple())
    ins_units = Column(TEXT)
    ins_units_factor = Column(REAL)
    is_dynamic_block = Column(BOOLEAN)
    name = Column(TEXT)
    normal = Column(MyTuple())
    rotation = Column(REAL)
    x_effective_scale_factor = Column(REAL)
    x_scale_factor = Column(REAL)
    y_effective_scale_factor = Column(REAL)
    y_scale_factor = Column(REAL)
    z_effective_scale_factor = Column(REAL)
    z_scale_factor = Column(REAL)
    block_attributes_ = relationship('AcDbAttributeBase', back_populates='block_reference_', primaryjoin='AcDbBlockReferenceBase.handle==AcDbAttributeBase.block_reference_handle_')
    dynamic_properties_ = relationship('AcadDynamicBlockReferencePropertyBase', back_populates='block_reference_')

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbAttributeBase(AcadEntityBase):
    __tablename__ = 'acdb_attributes'
    alignment = Column(INTEGER)  # docs show this as enum (text) but testing shows int?
    backward = Column(BOOLEAN)
    constant = Column(BOOLEAN)
    field_length = Column(INTEGER)
    height = Column(REAL)
    insertion_point = Column(MyTuple())
    invisible = Column(BOOLEAN)
    lock_position = Column(BOOLEAN)
    m_text_attribute = Column(BOOLEAN)
    m_text_attribute_content = Column(TEXT)
    m_text_boundary_width = Column(REAL)
    m_text_drawing_direction = Column(INTEGER)
    normal = Column(MyTuple())
    oblique_angle = Column(REAL)
    rotation = Column(REAL)
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    tag_string = Column(TEXT)
    text_alignment_point = Column(MyTuple())
    text_generation_flag = Column(INTEGER)
    text_string = Column(TEXT)
    thickness = Column(REAL)
    upside_down = Column(BOOLEAN)
    # added from acdb object
    block_reference_handle_ = Column(TEXT, ForeignKey('acdb_block_references.handle', onupdate='CASCADE', ondelete='CASCADE'))
    block_reference_ = relationship('AcDbBlockReferenceBase', back_populates='block_attributes_', primaryjoin='AcDbAttributeBase.block_reference_handle_==AcDbBlockReferenceBase.handle')

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbAttributeDefinitionBase(AcadEntityBase):
    __tablename__ = 'acdb_attribute_definitions'
    alignment = Column(INTEGER)  # docs show this as enum (text) but testing shows int?
    backward = Column(BOOLEAN)
    constant = Column(BOOLEAN)
    field_length = Column(INTEGER)
    height = Column(REAL)
    insertion_point = Column(MyTuple())
    invisible = Column(BOOLEAN)
    lock_position = Column(BOOLEAN)
    mode = Column(INTEGER)  # docs show this as enum (text) but testing shows int?
    m_text_attribute = Column(BOOLEAN)
    m_text_attribute_content = Column(TEXT)
    m_text_boundary_width = Column(REAL)
    m_text_drawing_direction = Column(INTEGER)
    normal = Column(MyTuple())
    oblique_angle = Column(REAL)
    preset = Column(BOOLEAN)
    prompt_string = Column(TEXT)
    rotation = Column(REAL)
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    tag_string = Column(TEXT)
    text_alignment_point = Column(MyTuple())
    text_generation_flag = Column(INTEGER)
    text_string = Column(TEXT)
    thickness = Column(REAL)
    upside_down = Column(BOOLEAN)
    verify = Column(BOOLEAN)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcadDynamicBlockReferencePropertyBase(Base):
    __tablename__ = 'acad_dynamic_block_ref_properties'
    block_reference_handle_ = Column(TEXT, ForeignKey('acdb_block_references.handle', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    block_reference_ = relationship('AcDbBlockReferenceBase', back_populates='dynamic_properties_')
    allowed_values = Column(MyTuple())
    description = Column(TEXT)
    property_name = Column(TEXT, primary_key=True)
    read_only = Column(BOOLEAN)
    show = Column(BOOLEAN)
    units_type = Column(INTEGER)
    value = Column(TEXT)


class AcDbCircleBase(AcadEntityBase):
    __tablename__ = 'acdb_circles'
    area = Column(REAL)
    center = Column(MyTuple())
    circumference = Column(REAL)
    diameter = Column(REAL)
    normal = Column(MyTuple())
    radius = Column(REAL)
    thickness = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbEllipseBase(AcadEntityBase):
    __tablename__ = 'acdb_ellipses'
    area = Column(REAL)
    center = Column(MyTuple())
    end_angle = Column(REAL)
    end_parameter = Column(REAL)
    end_point = Column(MyTuple())
    major_axis = Column(MyTuple())
    major_radius = Column(REAL)
    minor_axis = Column(MyTuple())
    minor_radius = Column(REAL)
    normal = Column(MyTuple())
    radius_ratio = Column(REAL)
    start_angle = Column(REAL)
    start_parameter = Column(REAL)
    start_point = Column(MyTuple())

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbHatchBase(AcadEntityBase):
    __tablename__ = 'acdb_hatches'
    area = Column(REAL)
    associative_hatch = Column(BOOLEAN)
    background_color_id_ = Column(TEXT, ForeignKey('acad_true_colors.id_', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    elevation = Column(REAL)
    gradient_angle = Column(TEXT)  # type in docs is ACAD_ANGLE, no link to object properties
    gradient_centered = Column(BOOLEAN)
    gradient_color1_id_ = Column(TEXT, ForeignKey('acad_true_colors.id_', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    gradient_color2_id_ = Column(TEXT, ForeignKey('acad_true_colors.id_', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    gradient_name = Column(TEXT)
    hatch_object_type = Column(TEXT)
    hatch_style = Column(TEXT)
    iso_pen_width = Column(TEXT)
    normal = Column(MyTuple())
    number_of_loops = Column(INTEGER)
    origin = Column(MyTuple())
    pattern_angle = Column(REAL)
    pattern_double = Column(REAL)
    pattern_name = Column(TEXT)
    pattern_scale = Column(REAL)
    pattern_space = Column(REAL)
    pattern_type = Column(TEXT)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcadAcCmColorBase(Base):
    __tablename__ = 'acad_true_colors'
    id_ = Column(TEXT, primary_key=True)
    blue = Column(INTEGER)
    book_name = Column(TEXT)
    color_index = Column(INTEGER)
    color_method = Column(INTEGER)
    color_name = Column(TEXT)
    entity_color = Column(TEXT)
    green = Column(INTEGER)
    red = Column(INTEGER)


class AcDbLeaderBase(AcadEntityBase):
    __tablename__ = 'acdb_leaders'
    # native property is 'annotation' but can be either BockReference, Mtext, or Tolerance.  Getting entity type and handle id in case we need to reference it
    # (this entity should already exist in another table, no need to store it from this propery)
    annotation_type = Column(TEXT)
    annotation_handle_id = Column(TEXT)
    arrowhead_block = Column(TEXT)
    arrowhead_size = Column(REAL)
    arrowhead_type = Column(INTEGER)
    coordinates = Column(MyTuple())
    dimension_line_color = Column(MyIntOrText())
    dimension_line_weight = Column(MyIntOrText())
    normal = Column(MyTuple())
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    text_gap = Column(REAL)
    type = Column(TEXT)
    vertical_text_position = Column(TEXT)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbLineBase(AcadEntityBase):
    __tablename__ = 'acdb_lines'
    angle = Column(REAL)
    delta = Column(MyTuple())
    end_point = Column(MyTuple())
    length = Column(REAL)
    normal = Column(MyTuple())
    start_point = Column(MyTuple())
    thickness = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbMLeaderBase(AcadEntityBase):
    __tablename__ = 'acdb_mleaders'
    arrowhead_block = Column(TEXT)
    arrowhead_size = Column(REAL)
    arrowhead_type = Column(INTEGER)  # enum text or int?
    block_connection_type = Column(INTEGER)  # enum text or int?
    block_scale = Column(REAL)
    content_block_name = Column(TEXT)
    content_block_type = Column(INTEGER)
    content_type = Column(TEXT)
    dog_legged = Column(BOOLEAN)
    dogleg_length = Column(REAL)
    landing_gap = Column(REAL)
    leader_count = Column(INTEGER)
    leader_line_color_id_ = Column(TEXT, ForeignKey('acad_true_colors.id_', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    leader_line_type = Column(TEXT)  # ACAD_LTYPE?
    leader_line_weight = Column(INTEGER)  # ACAD_LWEIGHT?
    leader_type = Column(INTEGER)
    # normal = Column(MyTuple())
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    text_attachment_direction = Column(INTEGER)  # enum text or int?
    text_background_fill = Column(BOOLEAN)
    text_bottom_attachment_type = Column(INTEGER)
    text_direction = Column(INTEGER)
    text_frame_display = Column(BOOLEAN)
    text_height = Column(REAL)
    text_justify = Column(INTEGER)
    text_left_attachment_type = Column(INTEGER)
    text_line_spacing_distance = Column(REAL)
    text_line_spacing_factor = Column(REAL)
    text_line_spacing_style = Column(INTEGER)
    text_right_attachment_type = Column(INTEGER)
    text_rotation = Column(REAL)
    text_string = Column(TEXT)
    text_style_name = Column(TEXT)
    text_top_attachment_type = Column(INTEGER)
    text_width = Column(REAL)
    type = Column(TEXT)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbMTextBase(AcadEntityBase):
    __tablename__ = 'acdb_mtexts'
    attachment_point = Column(TEXT)
    background_fill = Column(BOOLEAN)
    drawing_direction = Column(TEXT)
    height = Column(REAL)
    insertion_point = Column(MyTuple())
    line_spacing_distance = Column(REAL)
    line_spacing_factor = Column(REAL)
    line_spacing_style = Column(TEXT)
    normal = Column(MyTuple())
    rotation = Column(REAL)
    style_name = Column(TEXT)
    text_string = Column(TEXT)
    width = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbPointBase(AcadEntityBase):
    __tablename__ = 'acdb_points'
    coordinates = Column(MyTuple())
    normal = Column(MyTuple())
    thickness = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbPolylineBase(AcadEntityBase):
    __tablename__ = 'acdb_polylines'
    area = Column(REAL)
    closed = Column(BOOLEAN)
    constant_width = Column(REAL, nullable=True)
    # coordinate = Column(INTEGER)
    coordinates = Column(MyTuple())
    elevation = Column(REAL)
    length = Column(REAL)
    linetype_generation = Column(BOOLEAN)
    normal = Column(MyTuple())
    thickness = Column(REAL)
    # type_ = Column(TEXT)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbSolidBase(AcadEntityBase):
    __tablename__ = 'acdb_solids'
    coordinate = Column(REAL)
    coordinates = Column(THREE_ARR_DOUBLES_TYPE)
    normal = Column(THREE_ARR_DOUBLES_TYPE)
    thickness = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbSplineBase(AcadEntityBase):
    __tablename__ = 'acdb_splines'
    area = Column(REAL)
    closed = Column(BOOLEAN)
    closed2 = Column(BOOLEAN)
    control_points = Column(MyTuple())
    degree = Column(INTEGER)
    degree2 = Column(INTEGER)
    end_tangent = Column(MyTuple())
    fit_points = Column(MyTuple())
    fit_tolerance = Column(REAL)
    is_periodic = Column(BOOLEAN)
    is_planar = Column(BOOLEAN)
    is_rational = Column(BOOLEAN)
    knot_parameterization = Column(TEXT)
    knots = Column(MyTuple())
    number_of_control_points = Column(INTEGER)
    number_of_fit_points = Column(INTEGER)
    spline_frame = Column(TEXT)
    spline_method = Column(TEXT)
    start_tangent = Column(MyTuple())
    # weights = Column(MyTuple())  # throwing com_error from testing 'No weights available for polynomial spline'

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbTextBase(AcadEntityBase):
    __tablename__ = 'acdb_texts'
    alignment = Column(TEXT)
    backward = Column(BOOLEAN)
    height = Column(REAL)
    insertion_point = Column(MyTuple())
    normal = Column(MyTuple())
    oblique_angle = Column(REAL)
    rotation = Column(REAL)
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    text_alignment_point = Column(MyTuple())
    text_generation_flag = Column(TEXT)
    text_string = Column(TEXT)
    thickness = Column(REAL)
    upside_down = Column(BOOLEAN)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDb2dPolylineBase(AcadEntityBase):
    __tablename__ = 'acdb_2d_polylines'
    area = Column(REAL)
    closed = Column(BOOLEAN)
    constant_width = Column(REAL)
    coordinates = Column(MyTuple())
    elevation = Column(REAL)
    length = Column(REAL)
    linetype_generation = Column(BOOLEAN)
    normal = Column(MyTuple())
    thickness = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbViewportBase(AcadObjectBase):
    __tablename__ = 'acdb_viewports'
    arc_smoothness = Column(INTEGER)
    center = Column(MyTuple())
    direction = Column(MyTuple())
    grid_on = Column(BOOLEAN)
    height = Column(REAL)
    # lower_left_corner = Column(MyTuple())  # getting attribute error on testing
    # name = Column(TEXT)  # getting attribute error on testing
    # ortho_on = Column(BOOLEAN)  # getting attribute error on testing
    snap_base_point = Column(MyTuple())
    snap_on = Column(BOOLEAN)
    snap_rotation_angle = Column(REAL)
    target = Column(MyTuple())
    ucs_icon_at_origin = Column(BOOLEAN)
    ucs_icon_on = Column(BOOLEAN)
    # upper_right_corner = Column(MyTuple())  # getting attribute error on testing
    width = Column(REAL)
    x_min_ms_ = Column(REAL)
    x_max_ms_ = Column(REAL)
    y_min_ms_ = Column(REAL)
    y_max_ms_ = Column(REAL)
    scale_ = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcDbWipeoutBase(AcadEntityBase):
    __tablename__ = 'acdb_wipeouts'
    brightness = Column(INTEGER)
    clipping_enabled = Column(BOOLEAN)
    contrast = Column(INTEGER)
    fade = Column(REAL)
    height = Column(REAL)
    image_file = Column(TEXT)
    image_height = Column(REAL)
    image_visibility = Column(BOOLEAN)
    image_width = Column(REAL)
    name = Column(TEXT)
    origin = Column(MyTuple())
    rotation = Column(REAL)
    scale_factor = Column(REAL)
    show_rotation = Column(BOOLEAN)
    transparency = Column(BOOLEAN)
    width = Column(REAL)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcadDatabaseBase(Base):
    __abstract__ = True
    # blocks
    # dictionaries
    # dim_styles
    elevation_model_space = Column(REAL)
    elevation_paper_space = Column(REAL)
    # groups
    # layers  # not what you think, does not provide list of layer names
    # layouts
    limits = Column(MyTuple())

    # linetypes
    # material = Column(TEXT)  # not getting attribute from COM object
    # model_space
    # paper_space
    # plot_configurations
    # preferences
    # registered_applications
    # section_manager
    # summary_info_id  # see declared_attr below
    # text_styles
    # user_coordinate_systems
    # viewports
    # vieww

    @declared_attr
    def summary_info_id(self):
        return Column(INTEGER, ForeignKey('acad_summary_infos.id_', onupdate='CASCADE', ondelete='CASCADE'))


class AcadSummaryInfoBase(Base):
    __tablename__ = 'acad_summary_infos'
    id_ = Column(INTEGER, primary_key=True)
    document_name_ = Column(TEXT)
    author = Column(TEXT)
    comments = Column(TEXT)
    hyperlink_base = Column(TEXT)
    keywords = Column(TEXT)
    last_saved_by = Column(TEXT)
    revision_number = Column(TEXT)
    subject = Column(TEXT)
    title = Column(TEXT)


class AcadDocumentBase(AcadDatabaseBase):
    __tablename__ = 'acad_documents'
    # active
    # active_dim_style
    # active_layer
    # active_layout
    # active_linetype
    # active_material
    # active_p_viewport
    # active_selection_set
    # active_space
    # active_text_style
    # active_ucs
    # active_viewport
    # application
    # database
    full_name = Column(TEXT)
    height = Column(REAL)
    # hwnd
    # materials
    m_space = Column(BOOLEAN)
    name = Column(TEXT, primary_key=True)
    object_snap_mode = Column(BOOLEAN)
    path = Column(TEXT)
    # pickfirst_selection_set
    # plot
    read_only = Column(BOOLEAN)
    saved = Column(BOOLEAN)
    # selection_sets
    # utility
    width = Column(REAL)
    # window_state
    window_title = Column(TEXT)
    import_complete_ = Column(BOOLEAN)

    title_block = relationship('TitleBlockEtc', uselist=False, back_populates='document')
    rev_strip = relationship('RevStrip', back_populates='document')


class TitleBlockEtc(Base):
    __tablename__ = 'titleblocks'
    document_name = Column(TEXT, ForeignKey('acad_documents.name'), primary_key=True)
    dwg = Column('DWG#', TEXT)
    name = Column(TEXT)
    title_1 = Column('TITLE-1', TEXT)
    title_2 = Column('TITLE-2', TEXT)
    title_3 = Column('TITLE-3', TEXT)
    title_4 = Column('TITLE-4', TEXT)
    scale = Column('SCALE', TEXT)
    plotscale = Column('PLOTSCALE', TEXT)
    sheet_of = Column('##__##', TEXT)
    drawn = Column('DRAWN', TEXT)
    date = Column('DATE', TEXT)
    filename = Column('FILENAME', TEXT)
    win = Column('WIN', TEXT)
    old_num = Column('OLD-NUM', TEXT)
    group_id = Column('GROUP_ID', TEXT)
    eqt_code = Column('EQT_CODE', TEXT)
    checked = Column('CHECKED', TEXT)
    c_date = Column('C_DATE', TEXT)
    croschek = Column('CROSCHEK', TEXT)
    cc_date = Column('CC_DATE', TEXT)
    safety = Column('SAFETY', TEXT)
    s_date = Column('S_DATE', TEXT)
    planchk = Column('PLANCHK', TEXT)
    p_date = Column('P_DATE', TEXT)
    engr = Column('ENGR', TEXT)
    e_date = Column('E_DATE', TEXT)
    approv = Column('APPROV', TEXT)
    a_date = Column('A_DATE', TEXT)
    rprev = Column('RPREV', TEXT)
    owned_dwg_ = Column(BOOLEAN, default=False)  # is it a SSOE drawing?
    ifr_dwg_ = Column(BOOLEAN, default=False)  # issue for reference
    nfc_dwg_ = Column(BOOLEAN, default=False)  # not for construction

    document = relationship('AcadDocumentBase', uselist=False, back_populates='title_block')


class RevStrip(Base):
    __tablename__ = 'rev_strips'
    block_reference_handle_ = Column(TEXT, primary_key=True)
    document_name = Column(TEXT, ForeignKey('acad_documents.name'))
    rank_ = Column(INTEGER)
    hash_1 = Column(TEXT)
    hash_2 = Column(TEXT)
    description = Column('DESCRIPTION', TEXT)
    approv = Column('APPROV', TEXT)
    date = Column('DATE', TEXT)
    date_1 = Column('DATE1', TEXT)

    document = relationship('AcadDocumentBase', back_populates='rev_strip')


class AcadLayerBase(AcadObjectBase):
    __tablename__ = 'acad_layers'
    description = Column(TEXT)
    freeze = Column(BOOLEAN)
    layer_on = Column(BOOLEAN)
    linetype = Column(TEXT)
    lineweight = Column(INTEGER)
    lock = Column(BOOLEAN)
    material = Column(TEXT)
    name = Column(TEXT)
    plot_style_name = Column(TEXT)
    plottable = Column(BOOLEAN)
    true_color_id_ = Column(TEXT, ForeignKey('acad_true_colors.id_', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    used = Column(BOOLEAN)
    viewport_default = Column(BOOLEAN)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }


class AcadDimensionBase(AcadEntityBase):
    __abstract__ = True
    decimal_separator = Column(TEXT)
    dim_txt_direction = Column(BOOLEAN)
    normal = Column(MyTuple())
    rotation = Column(REAL)
    scale_factor = Column(REAL)
    style_name = Column(TEXT)
    suppress_leading_zeros = Column(BOOLEAN)
    suppress_trailing_zeros = Column(BOOLEAN)
    text_color = Column(INTEGER)
    text_fill = Column(BOOLEAN)
    text_fill_color = Column(INTEGER)
    text_gap = Column(REAL)
    text_height = Column(REAL)
    text_movement = Column(INTEGER)
    text_override = Column(TEXT)
    text_position = Column(MyTuple())
    text_prefix = Column(TEXT)
    text_rotation = Column(REAL)
    text_style = Column(TEXT)
    text_suffix = Column(TEXT)
    tolerance_display = Column(INTEGER)
    tolerance_height_scale = Column(REAL)
    tolerance_justification = Column(INTEGER)
    tolerance_lower_limit = Column(REAL)
    tolerance_precision = Column(INTEGER)
    tolerance_suppress_leading_zeros = Column(BOOLEAN)
    tolerance_suppress_trailing_zeros = Column(BOOLEAN)
    tolerance_upper_limit = Column(REAL)
    vertical_text_position = Column(INTEGER)


class AcadDimRotated(AcadDimensionBase):
    __tablename__ = 'acad_dims_rotated'


class ObjectCoordinates(Base):
    """
    Table to more efficiently keep record of object and coordinates of certain attributes (i.e. center for circle, nodes for lines, etc.)
    Will allow us to better query areas of the drawing if needed
    """
    __tablename__ = 'object_coordinates'
    # originally used multiple columns as primary keys, but ran into issues when trying to use
    # order as key and nullable
    id = Column(INTEGER, primary_key=True)
    object_id = Column(INTEGER, ForeignKey('objects_mapper.id_'))  # this is the db id, does not exist in Acad
    document_name = Column(TEXT)
    handle_id = Column(TEXT)
    property = Column(TEXT)
    class_name = Column(TEXT)
    space = Column(TEXT)
    x = Column(REAL)
    y = Column(REAL)
    z = Column(REAL, nullable=True)
    order = Column(INTEGER, nullable=True)  # only used when entity has more than one coordinate for the same prop (i.e. polyline, leader)
    index = Column(INTEGER, nullable=True)  # only used for objects with multiple sub-parts, i.e. MLeader

    object = relationship('ObjectBase', back_populates='coordinates_')


class ObjectBoundingBox(Base):
    __tablename__ = 'object_bounding_boxes'
    id = Column(INTEGER, primary_key=True)
    object_id = Column(INTEGER, ForeignKey('objects_bounding_box_mapper.id_'))
    document_name = Column(TEXT)
    handle_id = Column(TEXT)
    class_name = Column(TEXT)
    space = Column(TEXT)
    x_min = Column(REAL)
    x_max = Column(REAL)
    y_min = Column(REAL)
    y_max = Column(REAL)

    object = relationship('ObjectBoundingBox', back_populates='bounding_box_')


class AcadAttributeErrorsBase(Base):
    __tablename__ = 'attribute_errors'
    id = Column(INTEGER, primary_key=True)
    document_name = Column(TEXT)
    object_id = Column(INTEGER)
    handle = Column(TEXT)
    space = Column(TEXT)
    attr_name = Column(TEXT)
    attr_error = Column(TEXT)


class AcadObjectErrorsBase(Base):
    __tablename__ = 'object_errors'
    id = Column(INTEGER, primary_key=True)
    document_name = Column(TEXT)
    object_id = Column(INTEGER)
    handle = Column(TEXT)
    space = Column(TEXT)
    object_name = Column(TEXT)
    error = Column(TEXT)


class HandleCheckBase(Base):
    __tablename__ = 'handle_checks'
    handle = Column(TEXT, primary_key=True)
    document_name = Column(TEXT, primary_key=True)
    status = Column(TEXT, nullable=True)
    message = Column(TEXT, nullable=True)


class DesignError(Base):
    __tablename__ = 'design_errors'
    id = Column(INTEGER, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    category = Column(TEXT)
    friendly = Column(TEXT)
    verbose = Column(TEXT)
    fatal = Column(BOOLEAN)

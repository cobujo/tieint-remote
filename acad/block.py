from dataclasses import dataclass
from acad.object import AcadObject
from acad.line import AcDbLine


@dataclass
class AcDbBlockTableRecord(AcadObject):
    """
    autoscript generated

    """

    @property
    def block_scaling(self):
        return self.obj.BlockScaling

    @property
    def comments(self):
        return self.obj.Comments

    @property
    def count(self):
        return self.obj.Count

    @property
    def explodable(self):
        return self.obj.Explodable

    @property
    def is_dynamic_block(self):
        return self.obj.IsDynamicBlock

    @property
    def is_layout(self):
        return self.obj.IsLayout

    @property
    def is_x_ref(self):
        return self.obj.IsXRef

    @property
    def layout(self):
        return self.obj.Layout

    @property
    def material(self):
        return self.obj.Material

    @property
    def name(self):
        return self.obj.Name

    @property
    def origin(self):
        return self.obj.Origin

    @property
    def path(self):
        return self.obj.Path

    @property
    def units(self):
        return self.obj.Units

    @property
    def x_ref_database(self):
        return self.obj.XRefDatabase

    def add3_d_face(self, point1, point2, point3, point4):
        return self.obj.Add3DFace(Point1=point1, Point2=point2, point3=point3, Point4=point4)

    def add3_d_mesh(self, m, n, points_matrix):
        return self.obj.Add3DMesh(M=m, N=n, PointsMatrix=points_matrix)

    def add3_d_poly(self, points_array):
        return self.obj.Add3DPoly(PointsArray=points_array)

    def add_arc(self, center, radius, start_angle, end_angle):
        return self.obj.AddArc(Center=center, Radius=radius, StartAngle=start_angle, EndAngle=end_angle)

    def add_attribute(self, height, mode, prompt, insertion_point, tag, value):
        return self.obj.AddAttribute(Height=height, Mode=mode, Prompt=prompt, InsertionPoint=insertion_point, Tag=tag, Value=value)

    def add_box(self, origin, length, width, height):
        return self.obj.AddBox(Origin=origin, Length=length, Width=width, Height=height)

    def add_circle(self, center, radius):
        return self.obj.AddCircle(Center=center, Radius=radius)

    def add_cone(self, center, base_radius, height):
        return self.obj.AddCone(Center=center, BaseRadius=base_radius, Height=height)

    def add_custom_object(self, class_name):
        return self.obj.AddCustomObject(ClassName=class_name)

    def add_cylinder(self, center, radius, height):
        return self.obj.AddCylinder(Center=center, Radius=radius, Height=height)

    def add_dim3_point_angular(self, angle_vertex, first_end_point, second_end_point, text_point):
        return self.obj.AddDim3PointAngular(AngleVertex=angle_vertex, FirstEndPoint=first_end_point, SecondEndPoint=second_end_point, TextPoint=text_point)

    def add_dim_aligned(self, ext_line1_point, ext_line2_point, text_position):
        return self.obj.AddDimAligned(ExtLine1Point=ext_line1_point, ExtLine2Point=ext_line2_point, TextPosition=text_position)

    def add_dim_angular(self, angle_vertex, first_end_point, second_end_point, text_point):
        return self.obj.AddDimAngular(AngleVertex=angle_vertex, FirstEndPoint=first_end_point, SecondEndPoint=second_end_point, TextPoint=text_point)

    def add_dim_arc(self, arc_center, first_end_point, second_end_point, arc_point):
        return self.obj.AddDimArc(ArcCenter=arc_center, FirstEndPoint=first_end_point, SecondEndPoint=second_end_point, ArcPoint=arc_point)

    def add_dim_diametric(self, chord_point, far_chord_point, leader_length):
        return self.obj.AddDimDiametric(ChordPoint=chord_point, FarChordPoint=far_chord_point, LeaderLength=leader_length)

    def add_dim_ordinate(self, definition_point, leader_end_point, use_x_axis):
        return self.obj.AddDimOrdinate(DefinitionPoint=definition_point, LeaderEndPoint=leader_end_point, UseXAxis=use_x_axis)

    def add_dim_radial(self, center, chord_point, leader_length):
        return self.obj.AddDimRadial(Center=center, ChordPoint=chord_point, LeaderLength=leader_length)

    def add_dim_radial_large(self, center, chord_point, override_center, jog_point, jog_angle):
        return self.obj.AddDimRadialLarge(Center=center, ChordPoint=chord_point, OverrideCenter=override_center, JogPoint=jog_point, JogAngle=jog_angle)

    def add_dim_rotated(self, ext_line1_point, ext_line2_point, dim_line_location, rotation_angle):
        return self.obj.AddDimRotated(ExtLine1Point=ext_line1_point, ExtLine2Point=ext_line2_point, DimLineLocation=dim_line_location, RotationAngle=rotation_angle)

    def add_ellipse(self, center, major_axis, radius_ratio):
        return self.obj.AddEllipse(Center=center, MajorAxis=major_axis, RadiusRatio=radius_ratio)

    def add_elliptical_cone(self, center, major_radius, minor_radius, height):
        return self.obj.AddEllipticalCone(Center=center, MajorRadius=major_radius, MinorRadius=minor_radius, Height=height)

    def add_elliptical_cylinder(self, center, major_radius, minor_radius, height):
        return self.obj.AddEllipticalCylinder(Center=center, MajorRadius=major_radius, MinorRadius=minor_radius, Height=height)

    def add_extruded_solid(self, profile, height, taper_angle):
        return self.obj.AddExtrudedSolid(Profile=profile, Height=height, TaperAngle=taper_angle)

    def add_extruded_solid_along_path(self):
        return self.obj.AddExtrudedSolidALongPath()

    def add_hatch(self, pattern_type, pattern_name, associativity, hatch_object_type):
        return self.obj.AddHatch(PatternType=pattern_type, PatternName=pattern_name, Associativity=associativity, HatchObjectType=hatch_object_type)

    def add_leader(self, points_array, annotation, type_):
        return self.obj.AddLeader(PointsArray=points_array, Annotation=annotation, Type=type_)

    def add_light_weight_polyline(self, vertices_list):
        return self.obj.AddLightWeightPolyline(VerticesList=vertices_list)

    def add_line(self, start_point, end_point):
        return AcDbLine(self.obj.AddLine(StartPoint=start_point, EndPoint=end_point))

    def add_m_insert_block(self, insertion_point, name, xscale, yscale, zscale, rotation, num_rows, num_columns, row_spacing, column_spacing, password):
        return self.obj.AddMInsertBlock(InsertionPoint=insertion_point, Name=name, Xscale=xscale, Yscale=yscale, Zscale=zscale, Rotation=rotation, NumRows=num_rows, NumColumns=num_columns, RowSpacing=row_spacing, ColumnSpacing=column_spacing, Password=password)

    def add_m_leader(self, points_array, leader_line_index):
        return self.obj.AddMLeader(PointsArray=points_array, leaderLineIndex=leader_line_index)

    def add_m_line(self, vertex_list):
        return self.obj.AddMLine(VertexList=vertex_list)

    def add_m_text(self, insertion_point, width, text):
        return self.obj.AddMText(InsertionPoint=insertion_point, Width=width, Text=text)

    def add_point(self, point):
        return self.obj.AddPoint(Point=point)

    def add_polyface_mesh(self, vertex_list, face_list):
        return self.obj.AddPolyfaceMesh(VertexList=vertex_list, FaceList=face_list)

    def add_polyline(self, vertices_list):
        return self.obj.AddPolyline(VerticesList=vertices_list)

    def add_raster(self, image_file_name, insertion_point, scale_factor, rotation_angle):
        return self.obj.AddRaster(imageFileName=image_file_name, InsertionPoint=insertion_point, ScaleFactor=scale_factor, RotationAngle=rotation_angle)

    def add_ray(self, point1, point2):
        return self.obj.AddRay(Point1=point1, Point2=point2)

    def add_region(self, object_list):
        return self.obj.AddRegion(ObjectList=object_list)

    def add_revolved_solid(self, profile, axis_point, axis_dir, angle):
        return self.obj.AddRevolvedSolid(Profile=profile, AxisPoint=axis_point, AxisDir=axis_dir, Angle=angle)

    def add_section(self, from_point, to_point, plane_vector):
        return self.obj.AddSection(FromPoint=from_point, ToPoint=to_point, planeVector=plane_vector)

    def add_shape(self, name, insertion_point, scale_factor, rotation_angle):
        return self.obj.AddShape(Name=name, InsertionPoint=insertion_point, ScaleFactor=scale_factor, RotationAngle=rotation_angle)

    def add_solid(self, point1, point2, point3, point4):
        return self.obj.AddSolid(Point1=point1, Point2=point2, point3=point3, Point4=point4)

    def add_sphere(self, center, radius):
        return self.obj.AddSphere(Center=center, Radius=radius)

    def add_spline(self, points_array, start_tangent, end_tangent):
        return self.obj.AddSpline(PointsArray=points_array, StartTangent=start_tangent, EndTangent=end_tangent)

    def add_table(self, insertion_point, num_rows, num_columns, row_height, col_width):
        return self.obj.AddTable(InsertionPoint=insertion_point, NumRows=num_rows, NumColumns=num_columns, RowHeight=row_height, ColWidth=col_width)

    def add_text(self, text_string, insertion_point, height):
        return self.obj.AddText(TextString=text_string, InsertionPoint=insertion_point, Height=height)

    def add_tolerance(self, text, insertion_point, direction):
        return self.obj.AddTolerance(Text=text, InsertionPoint=insertion_point, Direction=direction)

    def add_torus(self, center, torus_radius, tube_radius):
        return self.obj.AddTorus(Center=center, TorusRadius=torus_radius, TubeRadius=tube_radius)

    def add_trace(self, points_array):
        return self.obj.AddTrace(PointsArray=points_array)

    def add_wedge(self, center, length, width, height):
        return self.obj.AddWedge(Center=center, Length=length, Width=width, Height=height)

    def add_x_line(self):
        return self.obj.AddXLine()

    def attach_external_reference(self, path_name, name, insertion_point, xscale, yscale, zscale, rotation, b_overlay, password):
        return self.obj.AttachExternalReference(PathName=path_name, Name=name, InsertionPoint=insertion_point, Xscale=xscale, Yscale=yscale, Zscale=zscale, Rotation=rotation, bOverlay=b_overlay, Password=password)

    def bind(self, b_prefix_name):
        return self.obj.Bind(bPrefixName=b_prefix_name)

    def detach(self):
        return self.obj.Detach()

    def insert_block(self, insertion_point, name, xscale, yscale, zscale, rotation, password):
        return self.obj.InsertBlock(InsertionPoint=insertion_point, Name=name, Xscale=xscale, Yscale=yscale, Zscale=zscale, Rotation=rotation, Password=password)

    def item(self, index):
        return self.obj.Item(Index=index)

    def reload(self):
        return self.obj.Reload()

    def unload(self):
        return self.obj.Unload()


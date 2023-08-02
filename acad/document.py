from dataclasses import dataclass, field
from typing import Optional
from acad import ACAD_OBJS_KEY, NO_OBJECT_NAME_KEY, NO_DATABASE_OBJECT_KEY
from acad.database import AcadDatabase, AcadSummaryInfo
from acad.utils import AcadUtil
from acad.application import AcadApplication
from sql.models import AcadDocumentBase
from collections.abc import Iterable
from acad import Spaces, convert_raw_objs_to_acad
from mylogger import logger
from warnings import warn


@dataclass
class AcadObjectsFromSpace:
    acad_objs: Optional[list] = None
    no_db_objs: Optional[dict] = None
    no_obj_name: Optional[list] = None


@dataclass
class AcadObjectsFromPaper(AcadObjectsFromSpace):
    space: str = 'paper'


@dataclass
class AcadObjectsFromModel(AcadObjectsFromSpace):
    space: str = 'model'


@dataclass
class AcadDocument(AcadDatabase, AcadUtil):
    """
    autoscript generated **except for fields below that are not @property
    """
    acad_objs_from_paper_: AcadObjectsFromPaper = field(default_factory=AcadObjectsFromPaper)
    acad_objs_from_model_: AcadObjectsFromModel = field(default_factory=AcadObjectsFromModel)

    @property
    def active(self):
        return self.obj.Active

    @property
    def active_dim_style(self):
        return self.obj.ActiveDimStyle

    @property
    def active_layer(self):
        return self.obj.ActiveLayer

    @property
    def active_layout(self):
        return self.obj.ActiveLayout

    @property
    def active_linetype(self):
        return self.obj.ActiveLinetype

    @property
    def active_material(self):
        return self.obj.ActiveMaterial

    @property
    def active_p_viewport(self):
        return self.obj.ActivePViewport

    @property
    def active_selection_set(self):
        return self.obj.ActiveSelectionSet

    @property
    def active_space(self):
        return self.obj.ActiveSpace

    @property
    def active_text_style(self):
        return self.obj.ActiveTextStyle

    @property
    def active_ucs(self):
        return self.obj.ActiveUCS

    @property
    def active_viewport(self):
        return self.obj.ActiveViewport

    @property
    def application(self):
        return AcadApplication(self.obj.Application)

    @property
    def database(self):
        return self.obj.Database

    @property
    def full_name(self):
        return self.obj.FullName

    @property
    def height(self):
        return self.obj.Height

    @property
    def hwnd(self):
        return self.obj.HWND

    @property
    def materials(self):
        return self.obj.Materials

    @property
    def m_space(self):
        return self.obj.MSpace

    @property
    def name(self):
        return self.obj.Name

    @property
    def object_snap_mode(self):
        return self.obj.ObjectSnapMode

    @property
    def path(self):
        return self.obj.Path

    @property
    def pickfirst_selection_set(self):
        return self.obj.PickfirstSelectionSet

    @property
    def plot(self):
        return self.obj.Plot

    @property
    def read_only(self):
        return self.obj.ReadOnly

    @property
    def saved(self):
        return self.obj.Saved

    @property
    def selection_sets(self):
        return self.obj.SelectionSets

    @property
    def summary_info(self) -> AcadSummaryInfo:
        return AcadSummaryInfo(self.obj.SummaryInfo, _document_name=self.name)

    @property
    def utility(self):
        return self.obj.Utility

    @property
    def width(self):
        return self.obj.Width

    @property
    def window_state(self):
        return self.obj.WindowState

    @property
    def window_title(self):
        return self.obj.WindowTitle

    def activate(self):
        return self.obj.Activate()

    def audit_info(self, fix_err):
        return self.obj.AuditInfo(FixErr=fix_err)

    def close(self, save_changes, file_name):
        return self.obj.Close(SaveChanges=save_changes, FileName=file_name)

    def end_undo_mark(self):
        return self.obj.EndUndoMark()

    def export(self, file_name, extension, selection_set):
        return self.obj.Export(FileName=file_name, Extension=extension, SelectionSet=selection_set)

    def get_variable(self, name):
        return self.obj.GetVariable(Name=name)

    def import_(self, file_name, insertion_point, scale_factor):
        return self.obj.Import(FileName=file_name, InsertionPoint=insertion_point, ScaleFactor=scale_factor)

    def load_shape_file(self, full_name):
        return self.obj.LoadShapeFile(FullName=full_name)

    def new(self, template_file_name):
        return self.obj.New(TemplateFileName=template_file_name)

    def open(self, full_name, password):
        return self.obj.Open(FullName=full_name, Password=password)

    def post_command(self, command):
        return self.obj.PostCommand(Command=command)

    def purge_all(self):
        return self.obj.PurgeAll()

    def regen(self, which_viewports):
        return self.obj.Regen(WhichViewports=which_viewports)

    def save(self):
        return self.obj.Save()

    def save_as(self, full_file_name, save_as_type, v_security_params):
        return self.obj.SaveAs(FullFileName=full_file_name, SaveAsType=save_as_type, vSecurityParams=v_security_params)

    def send_command(self, command):
        return self.obj.SendCommand(Command=command)

    def set_variable(self, name, value):
        return self.obj.SetVariable(Name=name, Value=value)

    def start_undo_mark(self):
        return self.obj.StartUndoMark()

    def w_block(self):
        return self.obj.WBlock()

    def set_active_layout_(self, layout_name: str):
        """
        No native method for setting the active layout using VBA API, need to use send_command
        :param layout_name: str
        :return:
        """
        self.send_command(f'-LAYOUT\nS\n{layout_name}\n')

    def set_ps_layout_(self):
        layout_names = [l.name for l in self.layouts_list_]
        if layout_names == ['Model']:
            # TODO: Medium -> log this error, every drawing should have at least 1 paperspace layout
            raise ValueError(f'doc: {self.name} only has a modelspace layout; expecting at least 1 paperspace layout')

        if 'Layout1' in layout_names:
            self.set_active_layout_('Layout1')
            return 'Layout1'

        ps_layouts = [lo for lo in layout_names if lo != 'Model']
        # TODO: Medium -> along with logging no paperspace error, should also log when Layout1 doesn't exist
        logger.warning(f'expecting layout named Layout1, your layouts are named: {ps_layouts}')
        layout_guess = ps_layouts[0]
        logger.warning(f'guessing at this point, making active paperspace layout: {layout_guess}')
        self.set_active_layout_(layout_guess)
        return layout_guess

    def get_ps_layout_extents_(self) -> list:
        if self.active_layout.name != 'Layout1':
            _ = self.set_ps_layout_()

        extmax = self.get_variable('EXTMAX')
        try:
            assert (isinstance(extmax, tuple))
        except AssertionError:
            raise ValueError(
                f'Unable to get EXTMAX from doc, expecting return to be tuple but received: {type(extmax)}')

        extmin = self.get_variable('EXTMIN')
        try:
            assert (isinstance(extmin, tuple))
        except AssertionError:
            raise ValueError(
                f'Unable to get EXTMIN from doc, expecting return to be tuple but received: {type(extmin)}')

        return [extmin, extmax]

    def _raw_objects_from_paperspace(self):
        return [o for o in self.obj.Paperspace]

    def _raw_objects_from_modelspace(self):
        return [o for o in self.obj.Modelspace]

    def set_acad_objects_from_space(self, space: str):
        raw_objs = None

        if space == 'paper':
            raw_objs = self._raw_objects_from_paperspace()
            if not raw_objs:
                return

            objs_dct = convert_raw_objs_to_acad(raw_objs)
            self.acad_objs_from_paper_.acad_objs = objs_dct[ACAD_OBJS_KEY]
            self.acad_objs_from_paper_.no_obj_name = objs_dct[NO_OBJECT_NAME_KEY]
            self.acad_objs_from_paper_.no_db_objs = objs_dct[NO_DATABASE_OBJECT_KEY]

        elif space == 'model':
            raw_objs = self._raw_objects_from_modelspace()
            if not raw_objs:
                return

            objs_dct = convert_raw_objs_to_acad(raw_objs)
            self.acad_objs_from_model_.acad_objs = objs_dct[ACAD_OBJS_KEY]
            self.acad_objs_from_model_.no_obj_name = objs_dct[NO_OBJECT_NAME_KEY]
            self.acad_objs_from_model_.no_db_objs = objs_dct[NO_DATABASE_OBJECT_KEY]

        else:
            raise ValueError(f'space must be one of: {Spaces}, you put: {space}')

    def db_process_in_session_(self, session, space=None, include: Iterable = ('summary_info', 'layers')):
        self.db_add_in_session_(model=AcadDocumentBase, session=session, space=None)

        if 'summary_info' in include:
            self.summary_info.db_process_in_session_(session=session, space=None)

        if 'layers' in include:
            layers = self.layers_list_
            [layer.db_process_in_session_(session=session, space=None) for layer in layers]

    def set_get_acad_results_from_space(self, space):
        self.set_acad_objects_from_space(space=space)
        propname = f'acad_objs_from_{space}_'
        acad_results = getattr(self, propname)
        if not acad_results.acad_objs:
            logger.info(f'{self.name}: no objects found to process in {space}space')
            return

        return acad_results

    def db_process_in_session_everything_(self, session, spaces=('paper',)):
        warning = 'Not recommended; if AutoCAD crashes on a bad object there is no recovery.  Recommend to use functions in processing.getdata'
        warn(warning, DeprecationWarning, stacklevel=2)
        # first process the document
        self.db_process_in_session_(session=session, space=None)
        # then process the objects in each space
        for space in spaces:
            self.set_acad_objects_from_space(space=space)
            propname = f'acad_objs_from_{space}_'
            acad_results = getattr(self, propname)
            if acad_results.acad_objs:
                # TODO: process no_db_objs and no_obj_name, put into db table?
                [obj.db_process_in_session_(session=session, space=space) for obj in acad_results.acad_objs]

                logger.info(f'{self.name}: {len(acad_results.acad_objs)} objects processed to db from {space}space')
            else:
                logger.info(f'{self.name}: no objects found to process in {space}space')

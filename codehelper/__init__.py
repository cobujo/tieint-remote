from inflection import underscore
import inspect
from types import FunctionType
from typing import Optional

# getting errors when trying getattr on certain attributes
# right now it's only ocurring with application but there could be others
# WARNING: attributes in this set should already be in the code for parents,
# if they're new and added here they won't be included on code generation!
DISALLOWED = {'application'}


def attributes(obj: object) -> dict:
    """
    https://stackoverflow.com/a/59128615
    :param obj:
    :return:
    """
    disallowed_names = {
        name for name, value in inspect.getmembers(type(obj))
        if isinstance(value, FunctionType)}
    dir_obj = [d for d in dir(obj) if d not in DISALLOWED]
    return {
        name: getattr(obj, name) for name in dir_obj
        if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)}


def properties_methods(properties: list, methods: list, custom_parent: object = None) -> dict:
    """
    riff of above function
    :param properties:
    :param methods:
    :param custom_parent:
    :return:
    """
    parent_attrs = {}
    if custom_parent:
        parent_attrs = attributes(custom_parent)

    # get reduced attrs against parent object
    # attrs = attributes(obj)
    # if parent_attrs:
    #     attrs = {k: v for (k, v) in attrs.items() if k not in parent_attrs}

    properties_red = [p for p in properties if p not in parent_attrs]
    methods_red = [m for m in methods if m not in parent_attrs]
    # properties = [k for k, v in attrs.items() if type(v) == property]
    # methods = [k for k, v in attrs.items() if type(v) == FunctionType]

    return {
        'properties': properties_red,
        'methods': methods_red
    }


def single_method_output(orig_method_name: str, com_obj: Optional[object] = None) -> str:
    meth = orig_method_name
    meth_lower = underscore(meth)
    meth_args = ''
    meth_lower_args = 'self'
    return_str = 'return'
    if com_obj:
        try:
            meth_arg_spec = inspect.getfullargspec(getattr(com_obj, meth))
            meth_args_lst = meth_arg_spec.args
            meth_args_lst_noself = [m for m in meth_args_lst if m != 'self']
            meth_args_lst_lower = [underscore(m) for m in meth_args_lst]
            meth_args_lst_lower_noself = [m for m in meth_args_lst_lower if m != 'self']

            meth_lower_args = ', '.join(meth_args_lst_lower)
            meth_args = ', '.join([f'{x}={y}' for x, y in zip(meth_args_lst_noself, meth_args_lst_lower_noself)])
            return_str = f'return self.obj.{meth}({meth_args})'
        except AttributeError as e:
            return_str = f"warnings.warn('{meth_lower} raising AttributeError: {e}')"

    return f"""
    def {meth_lower}({meth_lower_args}):
        {return_str}
    """


def properties_methods_codestring(class_name: str, properties: list, methods: list, com_obj, custom_parent: Optional[object]) -> str:
    """
    Output the code string for the class
    :param class_name:
    :param properties: list
        expecting CamelCase as shown in ActiveX documentation
    :param methods: list
            expecting CamelCase as shown in ActiveX documentation
    :param com_obj: COMObject
        used to args for each method
    :param custom_parent: object
        NOT A COM OBJECT, expecting an Acad object from our codebase
    :return: str
    """
    custom_parent_name = custom_parent.__class__.__name__ if custom_parent else 'object'
    output = f"""
@dataclass
class {class_name}({custom_parent_name}):
    \"""
    autoscript generated
    \"""

    """
    p_m = properties_methods(properties=properties, methods=methods, custom_parent=custom_parent)
    prop_out = ""
    for prop in p_m['properties']:
        prop_lower = underscore(prop)
        prop_out = prop_out + f"""
    @property
    def {prop_lower}(self):
        return self.obj.{prop}

    """

    meth_out = ""
    # NEXT -> get params of COM object, add these (underscore these for python methods)
    for meth in p_m['methods']:
        meth_out = meth_out + single_method_output(orig_method_name=meth, com_obj=com_obj)

    return output + prop_out + meth_out

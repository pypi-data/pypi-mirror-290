"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""



from typing import Any, Callable, ClassVar, Dict, Optional, Tuple, Union, TYPE_CHECKING
from dataclasses import dataclass, fields

from mkdocs.config import config_options as C

from pyodide_mkdocs_theme.pyodide_macros.messages.fr_lang import Lang
from ..maestro_tools import CopyableConfig

if TYPE_CHECKING:
    from pyodide_mkdocs_theme.pyodide_macros.plugin.pyodide_macros_plugin import PyodideMacrosPlugin


VAR_ARGS     = -1
DEFAULT_LANG = Lang()


@dataclass
class ArgConfigDumpable:
    """
    Define a macro argument, that can be dumped as mkdocs C.OptionItem for a plugin Config.
    """

    name: str
    """
    Macro argument name.
    """

    py_type: Any
    """
    Type of the actual value, used at runtime in python (see BaseMaestro extractors).
    """


    # ------------------------------------------------------------------------
    # kwargs only:


    in_config: bool = True
    """
    If False, this argument will not be added to the Config class/objects.
    Used for things that are implemented or were, but shouldn't be visible on user's side.
    """

    conf_type: Optional[Any] = None
    """
    ConfigOption to use for this argument.
    If not given, use `C.Type(py_type, default=self.default)`.
    """

    default: Optional[Any] = None
    """
    Default value for the conf_type. Ignored if None (use is_optional for this).
    """

    is_optional: bool = False
    """
    If True, add a C.Optional wrapper around the conf_type (given are generated).
    """

    index: Optional[int] = None
    """
    Index of the argument in the `*args` tuple, if it's positional.
    If index is -1, means the argument itself is a varargs.
    """


    # ------------------------------------------------------------------------
    # Internals:


    maestro_extractor_prop: str = ''
    """
    MaestroBase property name (ConfigExtractor)
    """

    config_setter_path: Tuple[str] = ()
    """
    "Path" to access the config holding this argument in CopiableConfig objects.
    This allows to modify them on the fly if needed (Lang...).
    """


    @property
    def is_positional(self):
        """
        Is a positional argument or a varargs.
        """
        return self.index is not None


    # ------------------------------------------------------------------------


    def __post_init__(self):

        if self.in_config:

            if self.conf_type is None:
                # Reminder: "default=None" means "required" in mkdocs ConfigOptions.
                self.conf_type = C.Type(self.py_type, default=self.default)

            if self.is_optional:
                self.conf_type = C.Optional(self.conf_type)


    def copy_with(self, **kw):
        """
        Create a copy of the current instance, possibly changing some things on the fly.
        """
        args = {
            field.name: getattr(self, field.name) for field in fields( type(self) )
        }
        args.update(kw)
        return self.__class__(**args)


    def to_config(self):
        """
        Convert to the relevant mkdocs ConfigOption object.
        """
        return self.conf_type


    def get_value(self, env:'PyodideMacrosPlugin'):
        """
        Get the current config value for this argument.
        """
        return getattr(env, self.maestro_extractor_prop)


    def as_config_extractor_code(self, path:Tuple[str]):
        """
        Build the ConfigExtractor code for BaseMaestro class (use in mkdocs_hooks)
        """
        prop     = self.maestro_extractor_prop
        py_type  = self.py_type.__name__
        location = '.'.join(path[:-1])
        return f"\n    { prop }: { py_type } = ConfigExtractor('{ location }', prop='{self.name}')"











@dataclass
class ArgConfigWithDynamicLangDefault(ArgConfigDumpable):

    __LANG_DEFAULTS: ClassVar[Dict[str, 'ArgConfigWithDynamicLangDefault']] = {}

    # ------------------------------------------------------------------------
    # kwargs only:

    lang_default_access: Optional[str] = None
    """
    Path to access the wanted string in env.lang, for values depending on the theme language,
    as set in mkdocs.yml.
    """

    def __post_init__(self):

        if self.lang_default_access:
            self.__LANG_DEFAULTS[ self.lang_default_access ] = self
            self._assign_lang_default()     # To do BEFORE super().__post_init__()

        super().__post_init__()


    @classmethod
    def update_lang_defaults_with_current_lang(cls, env:'PyodideMacrosPlugin'):
        for arg in cls.__LANG_DEFAULTS.values():
            arg._assign_lang_default(env)


    def _assign_lang_default(self, env:Optional['PyodideMacrosPlugin']=None):
        lang         = env.lang if env else DEFAULT_LANG
        prop, msg    = self.lang_default_access.split('.')
        self.default = getattr( getattr(lang, prop), msg)

        if env:
            obj = env.config
            for prop in self.config_setter_path:
                obj = getattr(obj,prop)
            obj[self.name] = self.default








@dataclass
class ArgDeprecationAutoTransfer(ArgConfigDumpable):
    """
    Some macros args could replace a previously global setting in the mkdocs configuration.
    If registered as such, any value registered in the deprecated config field can be
    automatically extracted and transferred "here".
    """

    deprecated_source: Optional[Union[Tuple[str], str]] = None
    """
    Path attributes chaining of a deprecated config option: if this option is not None at
    runtime, the current option should be overridden with the one from the old option.

    NOTE: given as string at declaration time, then converted automatically to tuple.
    """

    transfer_processor: Optional[Callable[[Any],Any]] = None
    """
    Potential conversion function, used when automatically transferring the value from a
    deprecated option to it's new location (note: unused so far...)
    """

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.deprecated_source,str):
            self.deprecated_source = tuple(self.deprecated_source.split('.'))

    def process_value_from_old_location(self, value):
        """
        Extract any value given to the deprecated options matching the current argument, and apply
        it in the current config, for this argument.
        """
        return value if not self.transfer_processor else self.transfer_processor(value)









@dataclass
class ArgToDocs(ArgConfigDumpable):
    """
    Represent an argument of a macro and it's associated behaviors/config.
    """

    # ------------------------------------------------------------------------
    # kwargs only:

    docs: str = ""
    """ Text to use when building the "summary" args tables in the docs """

    docs_default_as_type: bool = True
    """ If True, use the default value instead of the type in the as_docs_table output. """

    in_docs: bool = True
    """
    If False, this argument will not be present in the docs (tables of arguments, signatures).
    """

    docs_type: str = ""
    """ String replacement for the types in the docs """

    ide_link: bool=True
    """
    If True, when generating `as_table_row`, an md link will be added at the end, pointing
    toward the equivalent argument in the IDE-details page.
    """

    line_feed_link: bool = True


    @property
    def doc_name_type_min_length(self):
        return 1 + len(self.name) + len(self.get_docs_type())


    def get_type_str(self):
        """
        Return the name of the python type, unless `self.docs_default_as_type` is true and the
        `self.default` is not None: in that case, return `repr(self.default)`.
        """
        if self.docs_default_as_type and self.default is not None:
            return repr(self.default)
        return self.py_type.__name__

    def get_docs_type(self):
        """
        Return the string to use to describe de type of this argument in the docs.
        """
        return self.docs_type or self.py_type.__name__


    def signature(self, size:int=None):
        """
        Build a prettier signature, with default values assignment vertically aligned, of the
        macro call signature.
        """
        length   = self.doc_name_type_min_length
        n_spaces = length if size is None else size - length + 1
        return f"\n    { self.name }:{ ' '*n_spaces }{ self.get_docs_type() } = {self.default!r},"


    def as_table_row(self, only=True):
        """
        Generate a md table row for this specific argument.

        @only:  Conditions what is used for arg name, type and value.
                It is `False` when building IDE "per argument tables" (aka, with
                `macro_args_table(..., only=...)`.

            only | False   | True
            col1 | type    | nom argument
            col2 | default | type (or default, depending on docs_default_as_type)
            col3 | docs    | docs + ide_link if needed
        """

        if only:
            c1, c2, doc = (
                f"#!py { self.get_docs_type() }",
                repr(self.default),
                self.docs
            )
        else:
            c1, c2, doc = (
                self.name,
                self.get_type_str(),
                self.docs,
            )
            if self.ide_link:
                doc += self.line_feed_link * "<br>" + f"_([plus d'informations](--IDE-{ self.name }))_"

        return f"| `{ c1 }` | `#!py { c2 }` | { doc } |"







@dataclass
class ArgConfig(
    ArgToDocs,
    ArgDeprecationAutoTransfer,
    ArgConfigWithDynamicLangDefault,
    ArgConfigDumpable,
):
    pass


@dataclass
class ArgConfigNotIde(ArgConfig):
    """ Just to avoid to put the argument each time... (lazy you are :p ) """

    def __post_init__(self):
        super().__post_init__()
        self.ide_link = False












class MacroConfigDumpable:
    """
    Class making the link between:
        - The actual python implementation
        - The docs content (avoiding out of synch docs)
        - The Config used for the .meta.pmt.yml features. Note that optional stuff "there" is
          different from an optionality (or it's absence) in the running macro/python layer.

    Those instances represent the config "starting point", so all defaults are applied here,
    for the Config implementation.
    When extracting meta files or meta headers, the CopyableConfig instances will receive dicts
    from the yaml content, and those will be merged in the current config. This means the dict
    itself can contain only partial configs, it's not a problem.
    The corollary of this, is that _only_ values that could be None at runtime as an actual/useful
    value should be declared as `C.Optional`.
    """

    def __init__(self, name, *args:ArgConfig, in_config=True,  in_docs=True):

        self.in_config: bool = in_config
        self.in_docs:   bool = in_docs
        self.name:      str = name
        self.args:      Dict[str,ArgConfig] = {arg.name: arg for arg in args}

        if len(self.args) != len(args):
            raise ValueError(name+": duplicate arguments names.\n"+str(args))

        positionals = tuple(arg for arg in args if isinstance(arg,ArgConfigDumpable) and arg.is_positional)
        if args[:len(positionals)] != positionals:
            names = ', '.join(arg.name for arg in positionals)
            raise ValueError(
                f"{self.name}: the positional arguments should come first ({names})"
            )
        self.i_kwarg = len(positionals) and not positionals[-1].name.startswith('*')


    def __getattr__(self, prop):
        if prop not in self.args:
            raise AttributeError(prop)
        return self.args[prop]


    def build_accessors(self):
        """
        Build all accessors for the entire Config tree, then return self.
        """
        for arg,path in self.args_with_tree_path_as_gen():
            if arg.index == VAR_ARGS:
                continue
            arg.maestro_extractor_prop = '_'.join(path)
            arg.config_setter_path = path[:-1]
        return self


    def get_sub_config_if_exist(self, name) -> Union[None, 'MacroConfig']:
        if name=='IDEv': name='IDE'
        return getattr(self, name, None)


    def args_with_tree_path_as_gen(self):
        """
        Build a generator yielding all the ArgConfig instances with their path attributes
        in the Config.
        """

        def dfs(obj: Union[MacroConfig,ArgConfig] ):
            path.append(obj.name)
            if isinstance(obj, ArgConfigDumpable):
                yield obj, tuple(path)
            else:
                for child in obj.args.values():
                    yield from dfs(child)
            path.pop()

        path = []
        return dfs(self)


    def to_config(self):
        """
        Convert recursively to the equivalent CopyableConfig object.
        """
        class_name = ''.join(map(str.title, self.name.split('_'))) + 'Config'
        extends = (CopyableConfig,)
        body = {
            name: arg.to_config()
                for name,arg in self.args.items()
                if arg.in_config
        }
        kls = type(class_name, extends, body)
        return C.SubConfig(kls)









class MacroConfigToDocs(MacroConfigDumpable):

    def as_docs_table(self):
        """
        Converts all arguments to a 3 columns table (data rows only!):  name + type + help.
        No indentation logic is added here.
        """
        return '\n'.join(
            arg.as_table_row(False) for arg in self.args.values() if arg.in_docs
        )


    def signature_for_docs(self):
        """
        Converts the MacroConfig to a python signature for the docs, ignoring arguments that
        are not "in_docs".
        """
        args = [arg for arg in self.args.values() if arg.in_docs]
        size = max( arg.doc_name_type_min_length for arg in args )
        lst  = [ arg.signature(size) for arg in args ]

        if self.i_kwarg:
            lst.insert(self.i_kwarg, "\n    *,")

        return f"""
```python
{ '{{' } { self.name }({ ''.join(lst) }
) { '}}' }
```
"""






class MacroConfig(
    MacroConfigToDocs,
    MacroConfigDumpable,
):
    pass

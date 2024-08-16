"""Parse BBF-extended ``pyproject.yaml`` and generate Sphinx ``conf.py``
etc. files.

Standard ``pyproject.toml`` keys are used as far as possible, and necessary
BBF extensions are in the ``tool.bbftools`` table.
"""

# Copyright (c) 2024, Broadband Forum
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials
#    provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The above license is used as a license under copyright only.
# Please reference the Forum IPR Policy for patent licensing terms
# <https://www.broadband-forum.org/ipr-policy>.
#
# Any moral rights which are necessary to exercise under the above
# license grant are also deemed granted under this license.

import argparse
import importlib
import logging
import os
import re
import sys
import textwrap
import time

from typing import Any, Optional, Union

# starting with python 3.11, tomllib is part of the distribution
import tomli as tomllib

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)

PYPROJECT = 'pyproject.toml'

# XXX should put this text elsewhere, e.g. lower down or in a separate file
# XXX '<YEAR>', '<COPYRIGHT HOLDER>' etc. should be substituted with info from
#     the TOML file
KNOWN_LICENSES = {
    # XXX this is currently the slightly-modified BBF version; this is pending
    #     discussion of licenses for BBF tools
    'License :: OSI Approved :: BSD License': '''
Copyright (c) 2024, Broadband Forum

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the following
conditions are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials
   provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products
   derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The above license is used as a license under copyright only.
Please reference the Forum IPR Policy for patent licensing terms
<https://www.broadband-forum.org/ipr-policy>.

Any moral rights which are necessary to exercise under the above
license grant are also deemed granted under this license.'''[1:]
}


# XXX Holder and Wrapper need further thought; do we actually need both of
#     them? or either of them?
class Holder:
    def __init__(self, value: Any):
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    def __contains__(self, item) -> bool:
        value = self._value
        if isinstance(value, Holder):
            value = value._value
        if isinstance(value, dict):
            item_dash = item.replace('_', '-')
            # this is checking the keys, which are strings
            return item in value or item_dash in value
        elif isinstance(value, list):
            # list items can (or will?) be Holder instances
            # XXX this should be handled transparently by Holder
            value_ = [val._value if isinstance(val, Holder) else val for val
                      in value]
            return item in value_
        else:
            return item in value

    # XXX this is too complicated; you have to know that it'll return Holders
    #     for dicts and lists, and actual values for the rest
    # XXX also, there's a potential name conflict with 'value'
    def __getattr__(self, item: str) -> Any:
        value = self._value
        if isinstance(value, Holder):
            value = value._value

        item_dash = item.replace('_', '-')
        if not isinstance(value, dict) or (
                item not in value and item_dash not in value):
            raise AttributeError(f'{type(value).__name__!r} has no attribute '
                                 f'{item!r}')
        value = value.get(item, value[item_dash])

        if isinstance(value, Holder) and \
                not isinstance(value._value, (dict, list)):
            value = value._value
        return value

    def __getitem__(self, item) -> Any:
        value = self._value
        if isinstance(value, Holder):
            value = value._value

        if isinstance(value, list) and isinstance(item, (int, slice)):
            value = value[item]
        elif isinstance(item, str):
            value = self.__getattr__(item)
        else:
            raise TypeError(f"{type(value).__name__!r} doesn't support "
                            f"{type(item).__name__!r} indices")

        if isinstance(value, Holder) and \
                not isinstance(value._value,(dict, list)):
            value = value._value
        return value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)


class Wrapper:
    def __init__(self, value: Optional[Any] = None):
        self._holder = self.__holder(value)

    @classmethod
    def __holder(cls, value: Optional[Any] = None) -> Holder:
        if isinstance(value, dict):
            value = {n: cls.__holder(v) for n, v in value.items()}
        elif isinstance(value, list):
            value = [cls.__holder(v) for v in value]
        return Holder(value)

    def __contains__(self, item) -> bool:
        return self._holder.__contains__(item)

    def __getattr__(self, item: str) -> Any:
        return self._holder.__getattr__(item)

    def __getitem__(self, item) -> Any:
        return self._holder.__getitem__(item)

    @property
    def holder(self) -> Any:
        return self._holder

    def __str__(self):
        return str(self._holder)

    def __repr__(self):
        return repr(self._holder)


class Config:
    """Represents a standard pyproject.toml file as documented at
    https://packaging.python.org/en/latest/guides/writing-pyproject-toml and
    https://packaging.python.org/en/latest/specifications/pyproject-toml."""

    # "JSON Schema" approximation
    _str_schema = {'type': str}

    # XXX this isn't currently used
    # _str_schema_with_default = lambda d: {'type': str, 'default': d}

    _list_of_str_schema = {
        'type': list,
        'items': _str_schema
    }

    _dict_of_str_schema = {
        'type': dict,
        'additionalProperties': False,
        'patternProperties': {
            r'^.*$': _str_schema
        }
    }

    _list_of_dict_of_str_schema = {
        'type': list,
        'items': _dict_of_str_schema
    }

    _dict_of_list_of_str_schema = {
        'type': dict,
        'additionalProperties': False,
        'patternProperties': {
            r'^.*$': _list_of_str_schema
        }
    }

    _file_or_text_schema = {
        'type': dict,
        'additionalProperties': False,
        'properties': {
            'content-type': _str_schema,
            # XXX these should be mutually exclusive
            'file': _str_schema,
            'text': _str_schema
        },
        # XXX content-type is not required for license
        'required': []
    }

    _str_file_or_text_schema = {
        'oneOf': [
            _str_schema,
            _file_or_text_schema
        ]
    }

    _list_of_name_and_email_schema = {
        'type': list,
        'items': {
            'type': dict,
            'additionalProperties': False,
            'properties': {
                'name': _str_schema,
                'email': _str_schema
            }
        }
    }

    _bbftools_schema = {
        'type': dict,
        'additionalProperties': False,
        'properties': {
            'sphinx': _dict_of_str_schema
        }
    }

    _pyproject_schema = {
        'type': dict,
        'additionalProperties': False,
        'properties': {
            'build-system': {
                'type': dict,
                'additionalProperties': False,
                'properties': {
                    'requires': _list_of_str_schema,
                    # XXX this isn't mentioned in the spec
                    'build-backend': _str_schema
                },
                'required': ['requires']
            },
            'project': {
                'type': dict,
                'additionalProperties': False,
                'properties': {
                    'authors': _list_of_name_and_email_schema,
                    'classifiers': _list_of_str_schema,
                    'dependencies': _list_of_str_schema,
                    'description': _str_schema,
                    # XXX this has additional semantics
                    'dynamic': _list_of_str_schema,
                    'entry-points': _list_of_dict_of_str_schema,
                    'gui-scripts': _dict_of_str_schema,
                    'keywords': _list_of_str_schema,
                    'license': _file_or_text_schema,
                    'maintainers': _list_of_name_and_email_schema,
                    'name': _str_schema,
                    'optional-dependencies': _dict_of_list_of_str_schema,
                    'readme': _str_file_or_text_schema,
                    'requires-python': _str_schema,
                    'scripts': _dict_of_str_schema,
                    'urls': _dict_of_str_schema,
                    'version': _str_schema,
                },
                # XXX can't require version because it might be dynamic
                'required': ['name'],
            },
            'tool': {
                'type': dict,
                'additionalProperties': True,
                'properties': {
                    'bbftools': _bbftools_schema
                }
            }
        },
        'required': []
    }

    def __init__(self, path: str = PYPROJECT):
        self._content = None
        self._is_valid = None

        # load the file
        # XXX could/should search for the file
        with open(path, 'rb') as fd:
            self._content = tomllib.load(fd)

        # validate against the schema
        self._is_valid = self.__validate(self._content, self._pyproject_schema)

    def __bool__(self) -> bool:
        return bool(self._is_valid)

    @property
    def is_valid(self) -> bool:
        return bool(self._is_valid)

    # XXX would like the content to contain entries for everything in the
    #     schema (including defaults) regardless of whether it's in the config;
    #     this means that won't have to check for existence of anything that's
    #     in the schema; either do a post-validation pass (yes?) or else pass
    #     the schema to the Wrapper() constructor (no?)
    @property
    def content(self) -> Wrapper:
        return Wrapper(self._content)

    # handle the two cases; returns an (is_file, text) tuple
    @property
    def license(self) -> tuple[bool, Optional[str]]:
        project = self.content.project
        if 'license' in project and \
                isinstance((license_ := project.license).value, dict):
            if 'file' in license_:
                return True, self.__read_file(license_.file)
            elif 'text' in license_:
                return False, license_.text

        # check for known 'License :: ' classifiers
        elif licenses := [item for item in project.classifiers.value if
                          item.value.startswith('License :: ')]:
            if len(licenses) > 1:
                logger.warning(f'multiple licenses {licenses}; will use the '
                               f'first one')
            elif (license_ := licenses[0].value) not in KNOWN_LICENSES:
                logger.error(f'ignored unknown {license_}')
            else:
                return False, KNOWN_LICENSES[license_]

        # default to file and empty (safest option)
        return True, ''

    # handle the two cases; returns an (is_file, text) tuple
    @property
    def readme(self) -> tuple[bool, Optional[str]]:
        project = self.content.project
        readme = project.readme
        if isinstance(readme, str):
            return True, self.__read_file(readme)
        elif isinstance(readme.value, dict):
            if 'file' in readme:
                return True, self.__read_file(readme.file)
            elif 'text' in readme:
                return False, readme.text

        # default to file and empty (safest option)
        return True, ''

    # try to get the version from content.project, but if marked as dynamic,
    # try to get it via tool.setuptools.dynamic.version
    # XXX ideally might want to be able to use content.tool.setuptools.version
    #     and have that trigger the dynamic access, but not yet...
    # XXX all these 'not in' checks are only temporary
    @property
    def version(self) -> Optional[str]:
        logger.debug('getting version')
        project = self.content.project
        tool = self.content.tool
        if 'version' in project:
            logger.debug(f'  defined directly -> {project.version}')
            return project.version
        elif 'version' not in project.dynamic:
            logger.debug('  not defined directly or dynamically')
            return None
        elif 'setuptools' not in tool:
            logger.debug('  no setuptools info')
            return None
        elif 'dynamic' not in tool.setuptools:
            logger.debug('  no dynamic setuptools info')
            return None
        elif 'version' not in tool.setuptools.dynamic:
            logger.debug('  no setuptools info for version')
            return None
        elif not (version_spec := tool.setuptools.dynamic.version):
            logger.debug('  empty setuptools info for version')
            return None
        elif 'attr' not in version_spec:
            logger.debug("  version info doesn't define attr")
            return None
        elif '.' not in version_spec.attr:
            logger.debug(f"  attr {version_spec.attr} doesn't contain a dot")
            return None
        else:
            module_name, attr = version_spec.attr.rsplit('.', maxsplit=1)
            try:
                module = importlib.import_module(module_name)
                logger.debug(f'  module {module}')
                value = getattr(module, attr, None)
                logger.debug(f'  attr {attr} -> {value}')
                if isinstance(value, tuple):
                    value = '.'.join(str(comp) for comp in value)
                    logger.debug(f'  tuple -> {value}')
                return value
            except ModuleNotFoundError:
                logger.debug(f'  module {module_name} not found')
                return None

    @classmethod
    def __validate(cls, value: Union[dict, list, str, int],
                   schema: Optional[dict[str, Any]] = None, *,
                   is_valid: bool = True, quiet: bool = False) -> bool:
        if schema is None:
            # XXX or allow {}
            schema = {'type': Any}

        error_func = (lambda m: None) if quiet else logger.error

        if {'allOf', 'anyOf', 'oneOf'} & set(schema):
            key = next(iter(schema))
            if len(list(schema.keys())) > 1:
                raise ValueError(f"expected single key {key} but got "
                                 f"{list(schema.keys())} (schema error)")
            if not isinstance(schema[key], list):
                raise ValueError(f'expected list but got '
                                 f'{type(schema[key]).__name__} (schema error')
            is_valids = [cls.__validate(value, item, is_valid=is_valid,
                                        quiet=True) for item in schema[key]]
            num_valid = len([v for v in is_valids if v])
            if (key == 'allOf' and num_valid < len(is_valids)) or \
                    (key == 'anyOf' and num_valid == 0) or \
                    (key == 'oneOf' and num_valid != 1):
                # XXX re-validate all so all messages are output (this can
                #     output rather confusing messages)
                [cls.__validate(value, item, is_valid=is_valid, quiet=False)
                 for item in schema[key]]
                is_valid = False
        elif 'type' not in schema:
            raise ValueError(f"expected 'type' but got {list(schema.keys())} "
                             f"(schema error)")
        elif schema['type'] in {dict, Any} and isinstance(value, dict):
            additional_properties = schema.get('additionalProperties', True)
            required = schema.get('required', [])
            if 'properties' in schema:
                properties = schema['properties']
                for key in value:
                    if key not in properties and not additional_properties:
                        error_func(f'invalid key {key!r}: expected one '
                                   f'of {list(properties.keys())} in {value}')
                        is_valid = False
                    if not cls.__validate(value[key],
                                          properties.get(key, None),
                                          is_valid=is_valid, quiet=quiet):
                        is_valid = False
            # XXX does JSON Schema allow both properties and patternProperties?
            if 'patternProperties' in schema:
                properties = schema['patternProperties']
                for key in value:
                    # note use of re.search(); patterns aren't anchored
                    matches = [(mat, sch) for patt, sch in properties.items()
                               if (mat := re.search(patt, key))]
                    if not matches and not additional_properties:
                        error_func(f'invalid pattern {key!r}: expected one '
                                   f'of {list(properties.keys())} in {value}')
                        is_valid = False
                    if len(matches) > 1:
                        patts = [m[0].re.pattern for m in matches]
                        raise ValueError(f'ambiguous patterns {patts} in '
                                         f'{value} (schema error)')
                    if not cls.__validate(value[key], matches[0][1],
                                          is_valid=is_valid, quiet=quiet):
                        is_valid = False

            if missing := set(required) - set(value):
                error_func(f'missing {sorted(missing)} in {value}')
                is_valid = False
        elif schema['type'] in {list, Any} and isinstance(value, list):
            for item in value:
                if not cls.__validate(item, schema['items'],
                                      is_valid=is_valid, quiet=quiet):
                    is_valid = False
        elif schema['type'] in {str, Any} and isinstance(value, str):
            pass
        elif schema['type'] in {int, Any} and isinstance(value, int):
            pass
        else:
            error_func(f'expected {schema["type"].__name__} in {value!r}')
            is_valid = False
        return is_valid

    @classmethod
    def __read_file(cls, file: str) -> Optional[str]:
        try:
            with open(file, 'r') as fd:
                return fd.read()
        except FileNotFoundError as e:
            logger.error(e)
            return None

    def __str__(self):
        return str(self._content)

    def __repr__(self):
        return repr(self._content)


# return a 'do not edit' line for the specified language
def do_not_edit(*, lang: str = 'markdown'):
    assert lang in {'html', 'makefile', 'markdown', 'python', 'yaml'}
    beg, end = \
        ('<!-- ', ' -->') if lang in {'html', 'markdown'} else ('# ', '')
    return '%sdo not edit! this file was created from %s by %s%s' % (
        beg, PYPROJECT, prog_basename, end)


# XXX should test this with an empty (or nearly empty) TOML file, to check that
#     all the defaulting is working correctly
def write_conf_py(config: Config) -> tuple[bool, list[str]]:
    project = config.content.project

    year = time.gmtime().tm_year

    # noinspection PyListCreation
    lines = []

    # add a 'do not edit' line
    lines.append(do_not_edit(lang='python'))
    lines.append('')

    # add top-level info
    author = project.authors[0].name
    copyright_ = f'{year}, {author}'
    version = config.version or ''
    lines.append(f'project = {project.description!r}')
    lines.append(f'# noinspection PyShadowingBuiltins')
    lines.append(f'copyright = {copyright_!r}')
    lines.append(f'author = {author!r}')
    lines.append(f'release = {version!r}')
    lines.append('')

    # add extensions
    # XXX maybe should define these defaults via an in-memory TOML instance
    # XXX should allow additional settings in tool.bbftools.sphinx
    extensions = (
        ('sphinx.ext.autodoc', None, {
            'autodoc_class_signature': 'separated',
            'autodoc_member_order': 'bysource',
            'autodoc_typehints': 'description',
            'autodoc_typehints_format': 'fully-qualified'
        }),
        ('sphinx.ext.napoleon', None, None),
        ('sphinxarg.ext', 'pip install sphinx-argparse', None),
        ('myst_parser', 'pip install myst-parser', {
            'myst_enable_extensions': [
                'colon_fence'
            ]
        }),
    )

    lines.append('extensions = [')
    for name, comment, _ in extensions:
        comment = f'  # {comment}' if comment else ''
        lines.append(f'    {name!r},{comment}')
    lines.append(']')
    lines.append('')

    for _, _, config in extensions:
        if config:
            for name, value in config.items():
                lines.append(f'{name} = {value!r}')
            lines.append('')

    # add exclusions
    excludes = [
        'README.md',
        'docs',
        'Thumbs.db',
        '.DS_Store'
    ]
    lines.append('exclude_patterns = [')
    for exclude in excludes:
        lines.append(f'    {exclude!r},')
    lines.append(']')
    lines.append('')

    # add HTML theme
    html_theme = 'furo'
    lines.append(fr'html_theme = {html_theme!r}')

    return False, lines


def write_license(config: Config) -> tuple[bool, list[str]]:
    # get the LICENSE information
    is_file, text = config.license
    if is_file and text != '':
        logger.warning(f'use of an external LICENSE file is discouraged; use '
                       f'a classifier instead')

    # if defined in an external file, we won't be removing or writing the file
    return is_file, ([] if is_file or not text else
                     textwrap.dedent(text).splitlines())


def write_readme_md(config: Config) -> tuple[bool, list[str]]:
    # get the README information
    is_file, text = config.readme
    if is_file and text != '':
        logger.warning(f'use of an external README file is discouraged; use '
                       f'project.readme instead')

    # noinspection PyListCreation
    lines = []

    # if defined in an eternal file, we won't be removing or writing the file
    if not is_file:
        # add a 'do not edit' line
        lines.append(do_not_edit(lang='markdown'))
        lines.append('')

        # add header
        project = config.content.project
        lines.append(f'# {project.description}')
        lines.append('')

        # add the README information
        if text:
            lines.extend(textwrap.dedent(text).splitlines())

    return is_file, lines


def write_index_md(config: Config) -> tuple[bool, list[str]]:
    project = config.content.project

    # noinspection PyListCreation
    lines = []

    # add a 'do not edit' line
    lines.append(do_not_edit(lang='markdown'))
    lines.append('')

    # add header
    lines.append(f'# {project.description}')
    lines.append('')

    # add toctree
    lines.append('::: {toctree}')
    lines.append('bbftools.rst')
    lines.append(':::')
    lines.append('')

    # add footer
    lines.append('## Indices and tables')
    lines.append('')
    lines.append('* [Index](genindex)')
    lines.append('* [Module Index](modindex)')
    lines.append('* [Search Page](search)')

    return False, lines


def write_makefile(config: Config) -> tuple[bool, list[str]]:
    project = config.content.project

    # noinspection PyListCreation
    lines = []

    # add a 'do not edit' line
    lines.append(do_not_edit(lang='makefile'))
    lines.append('')

    # add content
    text = f'''
        NAMESPACE = bbftools

        TARGETDIR = docs
        
        EDITABLE = --editable
        
        LOGLEVEL = 1
        
        PYTHON = python

        BBF-PYPROJECT-PARSER = $(or \\
            $(wildcard bin/bbf-pyproject-parser.py), bbf-pyproject-parser.py)

        SPHINX-APIDOC = sphinx-apidoc

        PYPI = testpypi

        all: html

        build:
        \t$(RM) -r *.egg-info/ dist/
        \t$(PYTHON) -m build

        upload:
        \t$(PYTHON) -m twine upload $(PYPI:%=-r %) --verbose dist/*

        install:
        \t$(PYTHON) -m pip install $(EDITABLE) .

        uninstall:
        \t$(PYTHON) -m pip uninstall {project.name}

        html: apidoc
        \t$(PYTHON) -m sphinx . $(TARGETDIR)

        apidoc:
        \t$(SPHINX-APIDOC) --implicit-namespaces --no-toc -o . $(NAMESPACE)

        populate:
        \t $(BBF-PYPROJECT-PARSER) --loglevel $(LOGLEVEL)

        maintainerclean: distclean
        \t$(BBF-PYPROJECT-PARSER) --clean

        distclean: clean
        \t$(RM) -r *.egg-info build dist __pycache__

        clean:
        \t$(RM) -r $(NAMESPACE)*.rst $(TARGETDIR)
    '''[1:]
    lines.extend(textwrap.dedent(text).splitlines())

    return False, lines


def get_argparser() -> argparse.ArgumentParser:
    default_loglevel = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clean', action='store_true',
                        help='clean (remove) generated files')
    parser.add_argument('-l', '--loglevel', type=int, default=default_loglevel,
                        help='logging level; default: %r' % default_loglevel)

    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # parse arguments
    parser = get_argparser()
    args = parser.parse_args(argv[1:])

    # set logging level
    loglevel_map = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
    loglevel = loglevel_map.get(args.loglevel, logging.WARNING)
    logging.basicConfig(level=loglevel)

    # parse and validate config
    # XXX should allow the file path to be specified
    config = Config()

    # details of generated files
    files = (
        ('conf.py', write_conf_py),
        ('LICENSE', write_license),
        ('README.md', write_readme_md),
        ('index.md', write_index_md),
        ('makefile', write_makefile)
    )

    # if valid, remove or write output files
    if config.is_valid:
        for name, func in files:
            # XXX these should be Config observers (somehow)
            is_file, lines = func(config)

            # report
            logger.debug(f'file {name} file? {is_file}')
            for i, line in enumerate(lines):
                logger.debug(f'{i+1:2} {line!r}')

            # never remove or write externally-defined files
            if is_file:
                operation = 'removed' if args.clean else 'written'
                logger.info(f'{name} is an external file, so not '
                            f'{operation}')

            elif args.clean:
                if not os.path.exists(name):
                    logger.debug(f"{name} doesn't exist")
                else:
                    os.remove(name)
                    logger.info(f'removed {name}')

            # ignore if no lines
            elif not lines:
                logger.info(f"nothing to write to {name}")

            # otherwise write the file
            else:
                text = '\n'.join(lines + [''])
                with open(name, 'w') as fd:
                    fd.write(text)
                # really characters, but it's the same if they're all ASCII
                logger.info(f'wrote {len(lines)} lines ({len(text)} bytes) to'
                            f' {name}')

    # return 0 on success, or 1 on failure
    # XXX could count errors
    return not config.is_valid


if __name__ == "__main__":
    sys.exit(main())

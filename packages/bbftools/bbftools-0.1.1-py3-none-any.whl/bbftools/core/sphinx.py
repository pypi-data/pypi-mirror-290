"""Replacement for the https://pypi.org/project/sphinx-autodoc-defaultargs
extension, which loses type annotations and its always_document_default_args
setting adds defaults for the class (as well as for __init__()) and
undesirably separates keyword and positional parameters."""

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

import inspect

from typing import Any

from sphinx.application import Sphinx


# XXX need to add the necessary logic (it looks straightforward)
# noinspection PyUnusedLocal
def process_docstring(app: Sphinx, what: str, name: str, obj: Any,
                      options: dict[str, Any], lines: list[str]):
    # XXX will re-enable this when ready
    if False and what in {'method'}:
        # XXX might need to consult these to decide what to do
        # autodoc_class_signature = app.config.autodoc_class_signature
        # autodoc = app.extensions['sphinx.ext.autodoc']
        print(f'process docstring {what} {name}')
        try:
            rep = lambda x: '<none>' if x is inspect.Parameter.empty else x
            signature = {n: (rep(v.annotation), rep(v.default))
                         for n, v in inspect.signature(obj).parameters.items()}
            print(f'  signature {signature}')
        except (TypeError, ValueError):
            pass
        for line in lines:
            print(f'  %r' % line)


# XXX we might also want to add some config settings
def setup(app: Sphinx):
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', process_docstring)

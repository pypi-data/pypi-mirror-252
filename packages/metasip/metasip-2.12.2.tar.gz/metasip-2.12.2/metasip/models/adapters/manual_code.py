# Copyright (c) 2023 Riverbank Computing Limited.
#
# This file is part of metasip.
#
# This file may be used under the terms of the GNU General Public License v3
# as published by the Free Software Foundation which can be found in the file
# LICENSE-GPL3.txt included in this package.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


from ..code import Code
from ..docstring import Docstring
from ..extended_access import ExtendedAccess

from .adapt import adapt
from .base_adapter import AttributeType, BaseApiAdapter


class ManualCodeAdapter(BaseApiAdapter):
    """ This is the ManualCode adapter. """

    # The map of attribute names and types.
    ATTRIBUTE_TYPE_MAP = {
        'body':     AttributeType.LITERAL,
        'methcode': AttributeType.LITERAL,
        'precis':   AttributeType.STRING,
    }

    def as_str(self):
        """ Return the standard string representation. """

        return self.model.precis

    def generate_sip(self, sip_file, output):
        """ Generate the .sip file content. """

        manual_code = self.model

        nr_ends = self.version_start(output)

        if manual_code.body != '':
            output.write(f'// {manual_code.precis}\n{manual_code.body}\n',
                    indent=False)
        elif manual_code.precis.startswith('%'):
            output.write(manual_code.precis + '\n', indent=False)
        else:
            output.write(manual_code.precis + ';\n')

        adapt(manual_code, Docstring).generate_sip_directives(output)
        output.write_code_directive('%MethodCode', manual_code.methcode)

        self.version_end(nr_ends, output)

    def load(self, element, ui):
        """ Load the model from the XML element.  An optional user interface
        may be available to inform the user of progress.
        """

        super().load(element, ui)

        adapt(self.model, Code).load(element, ui)
        adapt(self.model, Docstring).load(element, ui)
        adapt(self.model, ExtendedAccess).load(element, ui)

    def save(self, output):
        """ Save the model to an output file. """

        manual_code = self.model

        output.write('<ManualCode')
        adapt(manual_code, Code).save_attributes(output)
        adapt(manual_code, Docstring).save_attributes(output)
        adapt(manual_code, ExtendedAccess).save_attributes(output)
        self.save_attribute('precis', manual_code.precis, output)
        output.write('>\n')

        output += 1
        self.save_literal('body', output)
        adapt(manual_code, Code).save_subelements(output)
        adapt(manual_code, Docstring).save_subelements(output)
        adapt(manual_code, ExtendedAccess).save_subelements(output)
        self.save_literal('methcode', output)
        output -= 1

        output.write('</ManualCode>\n')

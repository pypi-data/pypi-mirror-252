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


from ..access import Access
from ..annos import Annos
from ..code import Code

from .adapt import adapt
from .base_adapter import AttributeType, BaseApiAdapter


class DestructorAdapter(BaseApiAdapter):
    """ This is the Destructor adapter. """

    # The map of attribute names and types.
    ATTRIBUTE_TYPE_MAP = {
        'methcode': AttributeType.LITERAL,
        'name':     AttributeType.STRING,
        'virtcode': AttributeType.LITERAL,
        'virtual':  AttributeType.BOOL,
    }

    def __eq__(self, other):
        """ Compare for C/C++ equality. """

        dtor = self.model
        other_dtor = other.model

        if type(dtor) is not type(other_dtor):
            return False

        if dtor.access != other_dtor.access:
            return False

        if dtor.name != other_dtor.name:
            return False

        if dtor.virtual != other_dtor.virtual:
            return False

        return True

    def as_str(self):
        """ Return the standard string representation. """

        dtor = self.model

        s = '~' + dtor.name + '()' + adapt(dtor, Annos).as_str()

        if dtor.virtual:
            s = 'virtual ' + s

        return s

    def generate_sip(self, sip_file, output):
        """ Generate the .sip file content. """

        dtor = self.model

        nr_ends = self.version_start(output)

        output.write(self.as_str())
        output.write(';\n')

        output.write_code_directive('%MethodCode', dtor.methcode)
        output.write_code_directive('%VirtualCatcherCode', dtor.virtcode)

        self.version_end(nr_ends, output)

    def load(self, element, ui):
        """ Load the model from the XML element.  An optional user interface
        may be available to inform the user of progress.
        """

        super().load(element, ui)

        adapt(self.model, Code).load(element, ui)
        adapt(self.model, Access).load(element, ui)

    def save(self, output):
        """ Save the model to an output file. """

        dtor = self.model

        output.write('<Destructor')
        adapt(dtor, Code).save_attributes(output)
        adapt(dtor, Access).save_attributes(output)
        self.save_attribute('name', dtor.name, output)
        self.save_bool('virtual', output)
        output.write('>\n')

        output += 1
        self.save_literal('methcode', output)
        self.save_literal('virtcode', output)
        adapt(dtor, Code).save_subelements(output)
        adapt(dtor, Access).save_subelements(output)
        output -= 1

        output.write('</Destructor>\n')

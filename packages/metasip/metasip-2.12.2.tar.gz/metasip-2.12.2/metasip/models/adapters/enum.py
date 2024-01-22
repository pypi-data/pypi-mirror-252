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
from ..enum_value import EnumValue

from .adapt import adapt
from .base_adapter import AttributeType, BaseApiAdapter


class EnumAdapter(BaseApiAdapter):
    """ This is the Enum adapter. """

    # The map of attribute names and types.
    ATTRIBUTE_TYPE_MAP = {
        'enumclass':    AttributeType.BOOL,
        'name':         AttributeType.STRING,
    }

    def __eq__(self, other):
        """ Compare for C/C++ equality. """

        enum = self.model
        other_enum = other.model

        if type(enum) is not type(other_enum):
            return False

        if enum.access != other_enum.access:
            return False

        if enum.name != other_enum.name:
            return False

        if enum.enumclass != other_enum.enumclass:
            return False

        return True

    def as_str(self):
        """ Return the standard string representation. """

        enum = self.model

        s = 'enum'

        if enum.enumclass:
            s += ' class'

        if enum.name != '':
            s += ' ' + enum.name

        s += adapt(enum, Annos).as_str()

        return s

    def generate_sip(self, sip_file, output):
        """ Generate the .sip file content. """

        enum = self.model

        nr_ends = self.version_start(output)

        output.blank()
        output.write(self.as_str())
        output.write('\n{\n')
        output += 1

        for enum_value in enum.content:
            if enum_value.status == '':
                adapt(enum_value).generate_sip(sip_file, output)

        output -= 1
        output.write('};\n')
        output.blank()

        self.version_end(nr_ends, output)

    def load(self, element, ui):
        """ Load the model from the XML element.  An optional user interface
        may be available to inform the user of progress.
        """

        super().load(element, ui)

        adapt(self.model, Code).load(element, ui)
        adapt(self.model, Access).load(element, ui)

        for subelement in element:
            if subelement.tag == 'EnumValue':
                enum_value = EnumValue()
                adapt(enum_value).load(subelement, ui)
                self.model.content.append(enum_value)

    def save(self, output):
        """ Save the model to an output file. """

        enum = self.model

        output.write('<Enum')
        adapt(enum, Code).save_attributes(output)
        adapt(enum, Access).save_attributes(output)
        self.save_bool('enumclass', output)
        self.save_attribute('name', enum.name, output)
        output.write('>\n')

        output += 1
        adapt(enum, Code).save_subelements(output)
        adapt(enum, Access).save_subelements(output)

        for enum_value in enum.content:
            adapt(enum_value).save(output)

        output -= 1

        output.write('</Enum>\n')

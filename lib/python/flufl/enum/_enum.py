# Copyright (C) 2004-2011 by Barry A. Warsaw
#
# This file is part of flufl.enum
#
# flufl.enum is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# flufl.enum is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.enum.  If not, see <http://www.gnu.org/licenses/>.

"""Python enumerations."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    b'Enum',
    b'make_enum',
    ]


COMMASPACE = ', '



# pylint: disable-msg=C0203
class EnumMetaclass(type):
    """Meta class for Enums."""

    def __init__(cls, name, bases, attributes):
        """Create an Enum class.

        :param cls: The class being defined.
        :param name: The name of the class.
        :param bases: The class's base classes.
        :param attributes: The class attributes.
        """
        super(EnumMetaclass, cls).__init__(name, bases, attributes)
        # Store EnumValues here for easy access.
        cls._enums = {}
        # Figure out the set of enum values on the base classes, to ensure
        # that we don't get any duplicate values (which would screw up
        # conversion from integer).
        for basecls in cls.__mro__:
            if hasattr(basecls, '_enums'):
                # pylint: disable-msg=W0212
                cls._enums.update(basecls._enums)
        # For each class attribute, create an EnumValue and store that back on
        # the class instead of the int.  Skip Python reserved names.  Also add
        # a mapping from the integer to the instance so we can return the same
        # object on conversion.
        for attr in attributes:
            if not (attr.startswith('__') and attr.endswith('__')):
                intval  = attributes[attr]
                enumval = EnumValue(cls, intval, attr)
                if intval in cls._enums:
                    raise TypeError('Multiple enum values: %s' % intval)
                # Store as an attribute on the class, and save the attr name
                setattr(cls, attr, enumval)
                cls._enums[intval] = attr

    def __getattr__(cls, name):
        if name == '__members__':
            return cls._enums.values()
        raise AttributeError(name)

    def __repr__(cls):
        enums = ['%s: %d' % (cls._enums[k], k) for k in sorted(cls._enums)]
        return '<%s {%s}>' % (cls.__name__, COMMASPACE.join(enums))

    def __iter__(cls):
        for i in sorted(cls._enums):
            yield getattr(cls, cls._enums[i])

    def __getitem__(cls, i):
        # i can be an integer or a string
        attr = cls._enums.get(i)
        if attr is None:
            # It wasn't an integer -- try attribute name
            try:
                return getattr(cls, i)
            except (AttributeError, TypeError):
                raise ValueError(i)
        return getattr(cls, attr)

    # Support both MyEnum[i] and MyEnum(i)
    __call__ = __getitem__



class EnumValue:
    """Class to represent an enumeration value.

    EnumValue('Color', 'red', 12) prints as 'Color.red' and can be converted
    to the integer 12.
    """
    def __init__(self, cls, value, enumname):
        self._class     = cls
        self._value     = value
        self._enumname  = enumname

    def __repr__(self):
        return '<EnumValue: %s.%s [int=%d]>' % (
            self._class.__name__, self._enumname, self._value)

    def __str__(self):
        return '%s.%s' % (self._class.__name__, self._enumname)

    def __int__(self):
        return self._value

    def __reduce__(self):
        return getattr, (self._class, self._enumname)

    @property
    def enumclass(self):
        """Return the class associated with the enum value."""
        return self._class

    @property
    def enumname(self):
        """Return the name of the enum value."""
        return self._enumname

    # Support only comparison by identity and equality.  Ordered comparisions
    # are not supported.
    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __lt__(self, other):
        raise NotImplementedError

    __gt__ = __lt__
    __le__ = __lt__
    __ge__ = __lt__
    __hash__ = object.__hash__



class Enum:
    """The public API Enum class."""

    # pylint: disable-msg=W0232
    __metaclass__ = EnumMetaclass



def make_enum(name, value_string):
    """Return an Enum class from a name and a value string.

    This is a convenience function for defining a new enumeration when you
    don't care about the values of the items.  The values are automatically
    created by splitting the value string on spaces.

    :param name: The resulting enum's class name.
    :type name: byte string (or ASCII-only unicode string)
    :param value_string: A string of enumeration item names, separated by
        spaces, e.g. 'one two three'.
    :type value_string: byte string (or ASCII-only unicode string)
    :return: The new enumeration class.
    :rtype: instance of `EnumMetaClass`
    """
    value_names = value_string.split()
    return EnumMetaclass(
        str(name), (Enum,),
        dict((str(value), i) for i, value in enumerate(value_names, 1))
        )

=========================================
flufl.enum - A Python enumeration package
=========================================

This package is called ``flufl.enum``.  It is yet another Python enumeration
package, but with a slightly different take on syntax and semantics than
earlier such packages.

The goals of ``flufl.enum`` are to produce simple, specific, concise semantics
in an easy to read and write syntax.  ``flufl.enum`` has just enough of the
features needed to make enumerations useful, but without a lot of extra
baggage to weigh them down.  This work grew out of the Mailman 3.0 project and
it is the enum package used there.  Until version 3.0, this package was called
``munepy``.


Requirements
============

``flufl.enum`` requires Python 2.6 or newer, and is compatible with Python 3
when used with ``2to3``.


Documentation
=============

A `simple guide`_ to using the library is available within this package, in
the form of doctests.   The manual is also available online in the Cheeseshop
at:

    http://package.python.org/flufl.enum


Project details
===============

The project home page is:

    http://launchpad.net/flufl.enum

You should report bugs at:

    http://bugs.launchpad.net/flufl.enum

You can download the latest version of the package either from the Cheeseshop:

    http://pypi.python.org/pypi/flufl.enum

or from the Launchpad page above.  Of course you can also just install it with
``pip`` or ``easy_install`` from the command line::

    % sudo pip flufl.enum
    % sudo easy_install flufl.enum

You can grab the latest development copy of the code using Bazaar, from the
Launchpad home page above.  See http://bazaar-vcs.org for details on the
Bazaar distributed revision control system.  If you have Bazaar installed, you
can grab your own branch of the code like this::

     bzr branch lp:flufl.enum

You may contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2004-2011 Barry A. Warsaw

This file is part of flufl.enum.

flufl.enum is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

flufl.enum is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with flufl.enum.  If not, see <http://www.gnu.org/licenses/>.


Table of Contents
=================

.. toctree::

    docs/using.txt
    NEWS.txt

.. _`simple guide`: docs/using.html

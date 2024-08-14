# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Form widgets

This module defines some custom widgets for use with WuttaWeb.

However for convenience it also makes other Deform widgets available
in the namespace:

* :class:`deform:deform.widget.Widget` (base class)
* :class:`deform:deform.widget.TextInputWidget`
* :class:`deform:deform.widget.SelectWidget`
"""

from deform.widget import Widget, TextInputWidget, SelectWidget
from webhelpers2.html import HTML


class ObjectRefWidget(SelectWidget):
    """
    Widget for use with model "object reference" fields, e.g.  foreign
    key UUID => TargetModel instance.

    While you may create instances of this widget directly, it
    normally happens automatically when schema nodes of the
    :class:`~wuttaweb.forms.schema.ObjectRef` (sub)type are part of
    the form schema; via
    :meth:`~wuttaweb.forms.schema.ObjectRef.widget_maker()`.

    .. attribute:: model_instance

       Reference to the model record instance, i.e. the "far side" of
       the foreign key relationship.

       .. note::

          You do not need to provide the ``model_instance`` when
          constructing the widget.  Rather, it is set automatically
          when the :class:`~wuttaweb.forms.schema.ObjectRef` type
          instance (associated with the node) is serialized.
    """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def serialize(self, field, cstruct, **kw):
        """
        Serialize the widget.

        In readonly mode, returns a ``<span>`` tag around the
        :attr:`model_instance` rendered as string.

        Otherwise renders via the ``deform/select`` template.
        """
        readonly = kw.get('readonly', self.readonly)
        if readonly:
            obj = field.schema.model_instance
            return HTML.tag('span', c=str(obj or ''))

        return super().serialize(field, cstruct, **kw)

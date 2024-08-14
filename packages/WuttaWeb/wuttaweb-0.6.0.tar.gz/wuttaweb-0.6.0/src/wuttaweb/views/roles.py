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
Views for roles
"""

from wuttjamaican.db.model import Role
from wuttaweb.views import MasterView
from wuttaweb.db import Session


class RoleView(MasterView):
    """
    Master view for roles.

    Notable URLs provided by this class:

    * ``/roles/``
    * ``/roles/new``
    * ``/roles/XXX``
    * ``/roles/XXX/edit``
    * ``/roles/XXX/delete``
    """
    model_class = Role

    grid_columns = [
        'name',
        'notes',
    ]

    # TODO: master should handle this, possibly via configure_form()
    def get_query(self, session=None):
        """ """
        model = self.app.model
        query = super().get_query(session=session)
        return query.order_by(model.Role.name)

    def configure_grid(self, g):
        """ """
        super().configure_grid(g)

        # name
        g.set_link('name')

    def configure_form(self, f):
        """ """
        super().configure_form(f)

        # never show these
        f.remove('permission_refs',
                 'user_refs')

        # name
        f.set_validator('name', self.unique_name)

    def unique_name(self, node, value):
        """ """
        model = self.app.model
        session = Session()

        query = session.query(model.Role)\
                       .filter(model.Role.name == value)

        if self.editing:
            uuid = self.request.matchdict['uuid']
            query = query.filter(model.Role.uuid != uuid)

        if query.count():
            node.raise_invalid("Name must be unique")


def defaults(config, **kwargs):
    base = globals()

    RoleView = kwargs.get('RoleView', base['RoleView'])
    RoleView.defaults(config)


def includeme(config):
    defaults(config)

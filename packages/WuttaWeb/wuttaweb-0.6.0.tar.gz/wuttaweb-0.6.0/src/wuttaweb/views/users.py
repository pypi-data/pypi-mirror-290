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
Views for users
"""

import colander

from wuttjamaican.db.model import User
from wuttaweb.views import MasterView
from wuttaweb.forms.schema import PersonRef
from wuttaweb.db import Session


class UserView(MasterView):
    """
    Master view for users.

    Notable URLs provided by this class:

    * ``/users/``
    * ``/users/new``
    * ``/users/XXX``
    * ``/users/XXX/edit``
    * ``/users/XXX/delete``
    """
    model_class = User

    grid_columns = [
        'username',
        'person',
        'active',
    ]

    # TODO: master should handle this, possibly via configure_form()
    def get_query(self, session=None):
        """ """
        model = self.app.model
        query = super().get_query(session=session)
        return query.order_by(model.User.username)

    def configure_grid(self, g):
        """ """
        super().configure_grid(g)

        # never show these
        g.remove('person_uuid',
                 'role_refs',
                 'password')

        # username
        g.set_link('username')

        # person
        g.set_link('person')

    def configure_form(self, f):
        """ """
        super().configure_form(f)

        # never show these
        f.remove('person_uuid',
                 'password',
                 'role_refs')

        # person
        f.set_node('person', PersonRef(self.request, empty_option=True))
        f.set_required('person', False)

        # username
        f.set_validator('username', self.unique_username)

    def unique_username(self, node, value):
        """ """
        model = self.app.model
        session = Session()

        query = session.query(model.User)\
                       .filter(model.User.username == value)

        if self.editing:
            uuid = self.request.matchdict['uuid']
            query = query.filter(model.User.uuid != uuid)

        if query.count():
            node.raise_invalid("Username must be unique")


def defaults(config, **kwargs):
    base = globals()

    UserView = kwargs.get('UserView', base['UserView'])
    UserView.defaults(config)


def includeme(config):
    defaults(config)

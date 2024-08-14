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
Views for people
"""

from wuttjamaican.db.model import Person
from wuttaweb.views import MasterView


class PersonView(MasterView):
    """
    Master view for people.

    Notable URLs provided by this class:

    * ``/people/``
    * ``/people/new``
    * ``/people/XXX``
    * ``/people/XXX/edit``
    * ``/people/XXX/delete``
    """
    model_class = Person
    model_title_plural = "People"
    route_prefix = 'people'

    grid_columns = [
        'full_name',
        'first_name',
        'middle_name',
        'last_name',
    ]

    # TODO: master should handle this, possibly via configure_form()
    def get_query(self, session=None):
        """ """
        model = self.app.model
        query = super().get_query(session=session)
        return query.order_by(model.Person.full_name)

    def configure_grid(self, g):
        """ """
        super().configure_grid(g)

        # full_name
        g.set_link('full_name')

    # TODO: master should handle this?
    def configure_form(self, f):
        """ """
        super().configure_form(f)

        # first_name
        f.set_required('first_name', False)

        # middle_name
        f.set_required('middle_name', False)

        # last_name
        f.set_required('last_name', False)

        # users
        if 'users' in f:
            f.fields.remove('users')


def defaults(config, **kwargs):
    base = globals()

    PersonView = kwargs.get('PersonView', base['PersonView'])
    PersonView.defaults(config)


def includeme(config):
    defaults(config)

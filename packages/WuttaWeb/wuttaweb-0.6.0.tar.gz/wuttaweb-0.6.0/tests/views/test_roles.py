# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

import colander

from wuttaweb.views import roles as mod
from tests.util import WebTestCase


class TestRoleView(WebTestCase):

    def make_view(self):
        return mod.RoleView(self.request)

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.Role)
        self.assertFalse(grid.is_linked('name'))
        view.configure_grid(grid)
        self.assertTrue(grid.is_linked('name'))

    def test_configure_form(self):
        model = self.app.model
        view = self.make_view()
        form = view.make_form(model_class=model.Person)
        self.assertNotIn('name', form.validators)
        view.configure_form(form)
        self.assertIsNotNone(form.validators['name'])

    def test_unique_name(self):
        model = self.app.model
        view = self.make_view()

        role = model.Role(name='Foo')
        self.session.add(role)
        self.session.commit()

        with patch.object(mod, 'Session', return_value=self.session):

            # invalid if same name in data
            node = colander.SchemaNode(colander.String(), name='name')
            self.assertRaises(colander.Invalid, view.unique_name, node, 'Foo')

            # but not if name belongs to current role
            view.editing = True
            self.request.matchdict = {'uuid': role.uuid}
            node = colander.SchemaNode(colander.String(), name='name')
            self.assertIsNone(view.unique_name(node, 'Foo'))

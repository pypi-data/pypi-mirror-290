# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

import colander

from wuttaweb.views import users as mod
from tests.util import WebTestCase


class TestUserView(WebTestCase):

    def make_view(self):
        return mod.UserView(self.request)

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.User)
        self.assertFalse(grid.is_linked('person'))
        view.configure_grid(grid)
        self.assertTrue(grid.is_linked('person'))

    def test_configure_form(self):
        model = self.app.model
        view = self.make_view()
        form = view.make_form(model_class=model.Person)
        self.assertIsNone(form.is_required('person'))
        view.configure_form(form)
        self.assertFalse(form.is_required('person'))

    def test_unique_username(self):
        model = self.app.model
        view = self.make_view()

        user = model.User(username='foo')
        self.session.add(user)
        self.session.commit()

        with patch.object(mod, 'Session', return_value=self.session):

            # invalid if same username in data
            node = colander.SchemaNode(colander.String(), name='username')
            self.assertRaises(colander.Invalid, view.unique_username, node, 'foo')

            # but not if username belongs to current user
            view.editing = True
            self.request.matchdict = {'uuid': user.uuid}
            node = colander.SchemaNode(colander.String(), name='username')
            self.assertIsNone(view.unique_username(node, 'foo'))

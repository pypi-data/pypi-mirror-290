# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

from pyramid.httpexceptions import HTTPNotFound

from wuttaweb.views import people
from tests.util import WebTestCase


class TestPersonView(WebTestCase):

    def make_view(self):
        return people.PersonView(self.request)

    def test_get_query(self):
        view = self.make_view()
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_grid(self):
        model = self.app.model
        view = self.make_view()
        grid = view.make_grid(model_class=model.Setting)
        self.assertEqual(grid.linked_columns, [])
        view.configure_grid(grid)
        self.assertIn('full_name', grid.linked_columns)

    def test_configure_form(self):
        model = self.app.model
        view = self.make_view()
        form = view.make_form(model_class=model.Person)
        form.set_fields(form.get_model_fields())
        self.assertEqual(form.required_fields, {})
        view.configure_form(form)
        self.assertTrue(form.required_fields)
        self.assertFalse(form.required_fields['middle_name'])

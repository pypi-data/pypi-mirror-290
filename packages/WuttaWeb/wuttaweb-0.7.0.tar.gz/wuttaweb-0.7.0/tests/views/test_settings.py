# -*- coding: utf-8; -*-

from unittest.mock import patch

from pyramid.httpexceptions import HTTPNotFound

from wuttaweb.views import settings
from tests.util import WebTestCase


class TestAppInfoView(WebTestCase):

    def setUp(self):
        self.setup_web()
        self.pyramid_config.include('wuttaweb.views.essential')

    def make_view(self):
        return settings.AppInfoView(self.request)

    def test_index(self):
        # sanity/coverage check
        view = self.make_view()
        response = view.index()

    def test_configure_get_simple_settings(self):
        # sanity/coverage check
        view = self.make_view()
        simple = view.configure_get_simple_settings()

    def test_configure_get_context(self):
        # sanity/coverage check
        view = self.make_view()
        context = view.configure_get_context()


class TestSettingView(WebTestCase):

    def make_view(self):
        return settings.SettingView(self.request)

    def test_get_grid_data(self):

        # empty data by default
        view = self.make_view()
        data = view.get_grid_data(session=self.session)
        self.assertEqual(len(data), 0)

        # unless we save some settings
        self.app.save_setting(self.session, 'foo', 'bar')
        self.session.commit()
        data = view.get_grid_data(session=self.session)
        self.assertEqual(len(data), 1)

    def test_configure_form(self):
        view = self.make_view()
        form = view.make_form(fields=view.get_form_fields())
        self.assertNotIn('value', form.required_fields)
        view.configure_form(form)
        self.assertIn('value', form.required_fields)
        self.assertFalse(form.required_fields['value'])

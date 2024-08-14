# -*- coding: utf-8; -*-

import functools
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pyramid import testing
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from wuttjamaican.conf import WuttaConfig
from wuttaweb.views import master
from wuttaweb.subscribers import new_request_set_user
from tests.util import WebTestCase


class TestMasterView(WebTestCase):

    def test_defaults(self):
        with patch.multiple(master.MasterView, create=True,
                            model_name='Widget',
                            viewable=False,
                            editable=False,
                            deletable=False):
            master.MasterView.defaults(self.pyramid_config)

    ##############################
    # class methods
    ##############################

    def test_get_model_class(self):
        
        # no model class by default
        self.assertIsNone(master.MasterView.get_model_class())

        # subclass may specify
        MyModel = MagicMock()
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertIs(master.MasterView.get_model_class(), MyModel)

    def test_get_model_name(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_name)

        # subclass may specify model name
        master.MasterView.model_name = 'Widget'
        self.assertEqual(master.MasterView.get_model_name(), 'Widget')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Blaster')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_model_name(), 'Blaster')

    def test_get_model_name_normalized(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_name_normalized)

        # subclass may specify *normalized* model name
        master.MasterView.model_name_normalized = 'widget'
        self.assertEqual(master.MasterView.get_model_name_normalized(), 'widget')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_name_normalized(), 'blaster')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_model_name_normalized(), 'dinosaur')

    def test_get_model_title(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_title)

        # subclass may specify  model title
        master.MasterView.model_title = 'Wutta Widget'
        self.assertEqual(master.MasterView.get_model_title(), "Wutta Widget")
        del master.MasterView.model_title

        # or it may specify model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_title(), "Blaster")
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_model_title(), "Dinosaur")

    def test_get_model_title_plural(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_title_plural)

        # subclass may specify *plural* model title
        master.MasterView.model_title_plural = 'People'
        self.assertEqual(master.MasterView.get_model_title_plural(), "People")
        del master.MasterView.model_title_plural

        # or it may specify *singular* model title
        master.MasterView.model_title = 'Wutta Widget'
        self.assertEqual(master.MasterView.get_model_title_plural(), "Wutta Widgets")
        del master.MasterView.model_title

        # or it may specify model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_title_plural(), "Blasters")
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_model_title_plural(), "Dinosaurs")

    def test_get_model_key(self):

        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_key)

        # subclass may specify model key
        master.MasterView.model_key = 'uuid'
        self.assertEqual(master.MasterView.get_model_key(), ('uuid',))
        del master.MasterView.model_key

    def test_get_route_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_route_prefix)

        # subclass may specify route prefix
        master.MasterView.route_prefix = 'widgets'
        self.assertEqual(master.MasterView.get_route_prefix(), 'widgets')
        del master.MasterView.route_prefix

        # subclass may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_route_prefix(), 'blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_route_prefix(), 'dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Truck')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_route_prefix(), 'trucks')

    def test_get_url_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_url_prefix)

        # subclass may specify url prefix
        master.MasterView.url_prefix = '/widgets'
        self.assertEqual(master.MasterView.get_url_prefix(), '/widgets')
        del master.MasterView.url_prefix

        # or it may specify route prefix
        master.MasterView.route_prefix = 'trucks'
        self.assertEqual(master.MasterView.get_url_prefix(), '/trucks')
        del master.MasterView.route_prefix

        # or it may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_url_prefix(), '/blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_url_prefix(), '/dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Machine')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_url_prefix(), '/machines')

    def test_get_instance_url_prefix(self):

        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_instance_url_prefix)

        # typical example with url_prefix and simple key
        master.MasterView.url_prefix = '/widgets'
        master.MasterView.model_key = 'uuid'
        self.assertEqual(master.MasterView.get_instance_url_prefix(), '/widgets/{uuid}')
        del master.MasterView.url_prefix
        del master.MasterView.model_key

        # typical example with composite key
        master.MasterView.url_prefix = '/widgets'
        master.MasterView.model_key = ('foo', 'bar')
        self.assertEqual(master.MasterView.get_instance_url_prefix(), '/widgets/{foo}|{bar}')
        del master.MasterView.url_prefix
        del master.MasterView.model_key

    def test_get_template_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_template_prefix)

        # subclass may specify template prefix
        master.MasterView.template_prefix = '/widgets'
        self.assertEqual(master.MasterView.get_template_prefix(), '/widgets')
        del master.MasterView.template_prefix

        # or it may specify url prefix
        master.MasterView.url_prefix = '/trees'
        self.assertEqual(master.MasterView.get_template_prefix(), '/trees')
        del master.MasterView.url_prefix

        # or it may specify route prefix
        master.MasterView.route_prefix = 'trucks'
        self.assertEqual(master.MasterView.get_template_prefix(), '/trucks')
        del master.MasterView.route_prefix

        # or it may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_template_prefix(), '/blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_template_prefix(), '/dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Machine')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_template_prefix(), '/machines')

    def test_get_grid_key(self):

        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_grid_key)

        # subclass may specify grid key
        master.MasterView.grid_key = 'widgets'
        self.assertEqual(master.MasterView.get_grid_key(), 'widgets')
        del master.MasterView.grid_key

        # or it may specify route prefix
        master.MasterView.route_prefix = 'trucks'
        self.assertEqual(master.MasterView.get_grid_key(), 'trucks')
        del master.MasterView.route_prefix

        # or it may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_grid_key(), 'blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_grid_key(), 'dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Machine')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_grid_key(), 'machines')

    def test_get_config_title(self):

        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_config_title)

        # subclass may specify config title
        master.MasterView.config_title = 'Widgets'
        self.assertEqual(master.MasterView.get_config_title(), "Widgets")
        del master.MasterView.config_title

        # subclass may specify *plural* model title
        master.MasterView.model_title_plural = 'People'
        self.assertEqual(master.MasterView.get_config_title(), "People")
        del master.MasterView.model_title_plural

        # or it may specify *singular* model title
        master.MasterView.model_title = 'Wutta Widget'
        self.assertEqual(master.MasterView.get_config_title(), "Wutta Widgets")
        del master.MasterView.model_title

        # or it may specify model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_config_title(), "Blasters")
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        with patch.multiple(master.MasterView, create=True,
                            model_class=MyModel):
            self.assertEqual(master.MasterView.get_config_title(), "Dinosaurs")

    ##############################
    # support methods
    ##############################

    def test_render_to_response(self):

        def widgets(request): return {}
        self.pyramid_config.add_route('widgets', '/widgets/')
        self.pyramid_config.add_view(widgets, route_name='widgets')

        # basic sanity check using /master/index.mako
        # (nb. it skips /widgets/index.mako since that doesn't exist)
        with patch.multiple(master.MasterView, create=True,
                            model_name='Widget',
                            creatable=False):
            view = master.MasterView(self.request)
            response = view.render_to_response('index', {})
            self.assertIsInstance(response, Response)

        # basic sanity check using /appinfo/index.mako
        with patch.multiple(master.MasterView, create=True,
                            model_name='AppInfo',
                            route_prefix='appinfo',
                            url_prefix='/appinfo',
                            creatable=False):
            view = master.MasterView(self.request)
            response = view.render_to_response('index', {})
            self.assertIsInstance(response, Response)

        # bad template name causes error
        master.MasterView.model_name = 'Widget'
        self.assertRaises(IOError, view.render_to_response, 'nonexistent', {})
        del master.MasterView.model_name

    def test_get_index_title(self):
        master.MasterView.model_title_plural = "Wutta Widgets"
        view = master.MasterView(self.request)
        self.assertEqual(view.get_index_title(), "Wutta Widgets")
        del master.MasterView.model_title_plural

    def test_make_model_grid(self):
        model = self.app.model

        # no model class
        with patch.multiple(master.MasterView, create=True,
                            model_name='Widget',
                            model_key='uuid'):
            view = master.MasterView(self.request)
            grid = view.make_model_grid()
            self.assertIsNone(grid.model_class)

        # explicit model class
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            grid = view.make_model_grid(session=self.session)
            self.assertIs(grid.model_class, model.Setting)

    def test_get_grid_data(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo', 'bar')
        self.session.commit()

        # basic logic with Setting model
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            view = master.MasterView(self.request)
            data = view.get_grid_data(session=self.session)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0], {'name': 'foo', 'value': 'bar'})

        # error if model not known
        view = master.MasterView(self.request)
        self.assertFalse(hasattr(master.MasterView, 'model_class'))
        def get_query(session=None):
            session = session or self.session
            return session.query(model.Setting)
        with patch.object(view, 'get_query', new=get_query):
            self.assertRaises(ValueError, view.get_grid_data, session=self.session)

    def test_configure_grid(self):
        model = self.app.model

        # uuid field is pruned
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            view = master.MasterView(self.request)
            grid = view.make_grid(model_class=model.Setting,
                                  columns=['uuid', 'name', 'value'])
            self.assertIn('uuid', grid.columns)
            view.configure_grid(grid)
            self.assertNotIn('uuid', grid.columns)

    def test_get_instance(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo', 'bar')
        self.session.commit()
        self.assertEqual(self.session.query(model.Setting).count(), 1)

        # default not implemented
        view = master.MasterView(self.request)
        self.assertRaises(NotImplementedError, view.get_instance)

        # fetch from DB if model class is known
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            view = master.MasterView(self.request)

            # existing setting is returned
            self.request.matchdict = {'name': 'foo'}
            setting = view.get_instance(session=self.session)
            self.assertIsInstance(setting, model.Setting)
            self.assertEqual(setting.name, 'foo')
            self.assertEqual(setting.value, 'bar')

            # missing setting not found
            self.request.matchdict = {'name': 'blarg'}
            self.assertRaises(HTTPNotFound, view.get_instance, session=self.session)

    def test_make_model_form(self):
        model = self.app.model

        # no model class
        with patch.multiple(master.MasterView, create=True,
                            model_name='Widget',
                            model_key='uuid'):
            view = master.MasterView(self.request)
            form = view.make_model_form()
            self.assertIsNone(form.model_class)

        # explicit model class
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            form = view.make_model_form()
            self.assertIs(form.model_class, model.Setting)

    def test_configure_form(self):
        model = self.app.model

        # uuid field is pruned
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            view = master.MasterView(self.request)
            form = view.make_form(model_class=model.Setting,
                                  fields=['uuid', 'name', 'value'])
            self.assertIn('uuid', form.fields)
            view.configure_form(form)
            self.assertNotIn('uuid', form.fields)

    def test_objectify(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo', 'bar')
        self.session.commit()
        self.assertEqual(self.session.query(model.Setting).count(), 1)

        # no model class
        with patch.multiple(master.MasterView, create=True,
                            model_name='Widget',
                            model_key='uuid'):
            view = master.MasterView(self.request)
            form = view.make_model_form(fields=['name', 'description'])
            form.validated = {'name': 'first'}
            obj = view.objectify(form)
            self.assertIs(obj, form.validated)

        # explicit model class (editing)
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting,
                            editing=True):
            form = view.make_model_form()
            form.validated = {'name': 'foo', 'value': 'blarg'}
            form.model_instance = self.session.query(model.Setting).one()
            obj = view.objectify(form)
            self.assertIsInstance(obj, model.Setting)
            self.assertEqual(obj.name, 'foo')
            self.assertEqual(obj.value, 'blarg')

        # explicit model class (creating)
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting,
                            creating=True):
            form = view.make_model_form()
            form.validated = {'name': 'another', 'value': 'whatever'}
            obj = view.objectify(form)
            self.assertIsInstance(obj, model.Setting)
            self.assertEqual(obj.name, 'another')
            self.assertEqual(obj.value, 'whatever')

    def test_persist(self):
        model = self.app.model
        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting):
            view = master.MasterView(self.request)

            # new instance is persisted
            setting = model.Setting(name='foo', value='bar')
            self.assertEqual(self.session.query(model.Setting).count(), 0)
            view.persist(setting, session=self.session)
            self.session.commit()
            setting = self.session.query(model.Setting).one()
            self.assertEqual(setting.name, 'foo')
            self.assertEqual(setting.value, 'bar')

    ##############################
    # view methods
    ##############################

    def test_index(self):
        
        # sanity/coverage check using /settings/
        master.MasterView.model_name = 'Setting'
        master.MasterView.model_key = 'name'
        master.MasterView.grid_columns = ['name', 'value']
        view = master.MasterView(self.request)
        response = view.index()
        # then again with data, to include view action url
        data = [{'name': 'foo', 'value': 'bar'}]
        with patch.object(view, 'get_grid_data', return_value=data):
            response = view.index()
        del master.MasterView.model_name
        del master.MasterView.model_key
        del master.MasterView.grid_columns

    def test_create(self):
        model = self.app.model

        # sanity/coverage check using /settings/new
        with patch.multiple(master.MasterView, create=True,
                            model_name='Setting',
                            model_key='name',
                            form_fields=['name', 'value']):
            view = master.MasterView(self.request)

            # no setting yet
            self.assertIsNone(self.app.get_setting(self.session, 'foo.bar'))

            # get the form page
            response = view.create()
            self.assertIsInstance(response, Response)
            self.assertEqual(response.status_code, 200)
            # self.assertIn('frazzle', response.text)
            # nb. no error
            self.assertNotIn('Required', response.text)

            def persist(setting):
                self.app.save_setting(self.session, setting['name'], setting['value'])
                self.session.commit()

            # post request to save setting
            self.request.method = 'POST'
            self.request.POST = {
                'name': 'foo.bar',
                'value': 'fraggle',
            }
            with patch.object(view, 'persist', new=persist):
                response = view.create()
            # nb. should get redirect back to view page
            self.assertEqual(response.status_code, 302)
            # setting should now be in DB
            self.assertEqual(self.app.get_setting(self.session, 'foo.bar'), 'fraggle')

            # try another post with invalid data (value is required)
            self.request.method = 'POST'
            self.request.POST = {}
            with patch.object(view, 'persist', new=persist):
                response = view.create()
            # nb. should get a form with errors
            self.assertEqual(response.status_code, 200)
            self.assertIn('Required', response.text)
            # setting did not change in DB
            self.assertEqual(self.app.get_setting(self.session, 'foo.bar'), 'fraggle')

    def test_view(self):

        # sanity/coverage check using /settings/XXX
        setting = {'name': 'foo.bar', 'value': 'baz'}
        self.request.matchdict = {'name': 'foo.bar'}
        with patch.multiple(master.MasterView, create=True,
                            model_name='Setting',
                            model_key='name',
                            grid_columns=['name', 'value'],
                            form_fields=['name', 'value']):
            view = master.MasterView(self.request)
            with patch.object(view, 'get_instance', return_value=setting):
                response = view.view()

    def test_edit(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo.bar', 'frazzle')
        self.session.commit()

        def get_instance():
            setting = self.session.query(model.Setting).get('foo.bar')
            return {
                'name': setting.name,
                'value': setting.value,
            }

        # sanity/coverage check using /settings/XXX/edit
        self.request.matchdict = {'name': 'foo.bar'}
        with patch.multiple(master.MasterView, create=True,
                            model_name='Setting',
                            model_key='name',
                            form_fields=['name', 'value']):
            view = master.MasterView(self.request)
            with patch.object(view, 'get_instance', new=get_instance):

                # get the form page
                response = view.edit()
                self.assertIsInstance(response, Response)
                self.assertEqual(response.status_code, 200)
                self.assertIn('frazzle', response.text)
                # nb. no error
                self.assertNotIn('Required', response.text)

                def persist(setting):
                    self.app.save_setting(self.session, 'foo.bar', setting['value'])
                    self.session.commit()

                # post request to save settings
                self.request.method = 'POST'
                self.request.POST = {
                    'name': 'foo.bar',
                    'value': 'froogle',
                }
                with patch.object(view, 'persist', new=persist):
                    response = view.edit()
                # nb. should get redirect back to view page
                self.assertEqual(response.status_code, 302)
                # setting should be updated in DB
                self.assertEqual(self.app.get_setting(self.session, 'foo.bar'), 'froogle')

                # try another post with invalid data (value is required)
                self.request.method = 'POST'
                self.request.POST = {}
                with patch.object(view, 'persist', new=persist):
                    response = view.edit()
                # nb. should get a form with errors
                self.assertEqual(response.status_code, 200)
                self.assertIn('Required', response.text)
                # setting did not change in DB
                self.assertEqual(self.app.get_setting(self.session, 'foo.bar'), 'froogle')

    def test_delete(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo.bar', 'frazzle')
        self.session.commit()
        self.assertEqual(self.session.query(model.Setting).count(), 1)

        def get_instance():
            setting = self.session.query(model.Setting).get('foo.bar')
            return {
                'name': setting.name,
                'value': setting.value,
            }

        # sanity/coverage check using /settings/XXX/delete
        self.request.matchdict = {'name': 'foo.bar'}
        with patch.multiple(master.MasterView, create=True,
                            model_name='Setting',
                            model_key='name',
                            form_fields=['name', 'value']):
            view = master.MasterView(self.request)
            with patch.object(view, 'get_instance', new=get_instance):

                # get the form page
                response = view.delete()
                self.assertIsInstance(response, Response)
                self.assertEqual(response.status_code, 200)
                self.assertIn('frazzle', response.text)

                def delete_instance(setting):
                    self.app.delete_setting(self.session, setting['name'])

                # post request to save settings
                self.request.method = 'POST'
                self.request.POST = {}
                with patch.object(view, 'delete_instance', new=delete_instance):
                    response = view.delete()
                # nb. should get redirect back to view page
                self.assertEqual(response.status_code, 302)
                # setting should be gone from DB
                self.assertEqual(self.session.query(model.Setting).count(), 0)

    def test_delete_instance(self):
        model = self.app.model
        self.app.save_setting(self.session, 'foo.bar', 'frazzle')
        self.session.commit()
        setting = self.session.query(model.Setting).one()

        with patch.multiple(master.MasterView, create=True,
                            model_class=model.Setting,
                            form_fields=['name', 'value']):
            view = master.MasterView(self.request)
            view.delete_instance(setting)
            self.session.commit()
            self.assertEqual(self.session.query(model.Setting).count(), 0)

    def test_configure(self):
        model = self.app.model

        # mock settings
        settings = [
            {'name': 'wutta.app_title'},
            {'name': 'wutta.foo', 'value': 'bar'},
            {'name': 'wutta.flag', 'type': bool},
            {'name': 'wutta.number', 'type': int, 'default': 42},
            {'name': 'wutta.value1', 'save_if_empty': True},
            {'name': 'wutta.value2', 'save_if_empty': False},
        ]

        view = master.MasterView(self.request)
        with patch.object(self.request, 'current_route_url', return_value='/appinfo/configure'):
            with patch.object(master, 'Session', return_value=self.session):
                with patch.multiple(master.MasterView, create=True,
                                    model_name='AppInfo',
                                    route_prefix='appinfo',
                                    template_prefix='/appinfo',
                                    creatable=False,
                                    configure_get_simple_settings=MagicMock(return_value=settings)):

                    # get the form page
                    response = view.configure()
                    self.assertIsInstance(response, Response)

                    # post request to save settings
                    self.request.method = 'POST'
                    self.request.POST = {
                        'wutta.app_title': 'Wutta',
                        'wutta.foo': 'bar',
                        'wutta.flag': 'true',
                    }
                    response = view.configure()
                    # nb. should get redirect back to configure page
                    self.assertIsInstance(response, HTTPFound)

                    # should now have 5 settings
                    count = self.session.query(model.Setting).count()
                    self.assertEqual(count, 5)
                    get_setting = functools.partial(self.app.get_setting, self.session)
                    self.assertEqual(get_setting('wutta.app_title'), 'Wutta')
                    self.assertEqual(get_setting('wutta.foo'), 'bar')
                    self.assertEqual(get_setting('wutta.flag'), 'true')
                    self.assertEqual(get_setting('wutta.number'), '42')
                    self.assertEqual(get_setting('wutta.value1'), '')
                    self.assertEqual(get_setting('wutta.value2'), None)

                    # post request to remove settings
                    self.request.method = 'POST'
                    self.request.POST = {'remove_settings': '1'}
                    response = view.configure()
                    # nb. should get redirect back to configure page
                    self.assertIsInstance(response, HTTPFound)

                    # should now have 0 settings
                    count = self.session.query(model.Setting).count()
                    self.assertEqual(count, 0)

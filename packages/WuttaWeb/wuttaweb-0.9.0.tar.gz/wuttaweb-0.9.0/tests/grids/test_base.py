# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch

from paginate import Page
from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttaweb.grids import base
from wuttaweb.forms import FieldList
from tests.util import WebTestCase


class TestGrid(WebTestCase):

    def make_grid(self, request=None, **kwargs):
        return base.Grid(request or self.request, **kwargs)

    def test_constructor(self):

        # empty
        grid = self.make_grid()
        self.assertIsNone(grid.key)
        self.assertEqual(grid.columns, [])
        self.assertIsNone(grid.data)

        # now with columns
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertIsInstance(grid.columns, FieldList)
        self.assertEqual(grid.columns, ['foo', 'bar'])

    def test_vue_tagname(self):
        grid = self.make_grid()
        self.assertEqual(grid.vue_tagname, 'wutta-grid')

    def test_vue_component(self):
        grid = self.make_grid()
        self.assertEqual(grid.vue_component, 'WuttaGrid')

    def test_get_columns(self):
        model = self.app.model

        # empty
        grid = self.make_grid()
        self.assertEqual(grid.columns, [])
        self.assertEqual(grid.get_columns(), [])

        # explicit
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertEqual(grid.columns, ['foo', 'bar'])
        self.assertEqual(grid.get_columns(), ['foo', 'bar'])

        # derived from model
        grid = self.make_grid(model_class=model.Setting)
        self.assertEqual(grid.columns, ['name', 'value'])
        self.assertEqual(grid.get_columns(), ['name', 'value'])

    def test_append(self):
        grid = self.make_grid(columns=['one', 'two'])
        self.assertEqual(grid.columns, ['one', 'two'])
        grid.append('one', 'two', 'three')
        self.assertEqual(grid.columns, ['one', 'two', 'three'])

    def test_remove(self):
        grid = self.make_grid(columns=['one', 'two', 'three', 'four'])
        self.assertEqual(grid.columns, ['one', 'two', 'three', 'four'])
        grid.remove('two', 'three')
        self.assertEqual(grid.columns, ['one', 'four'])

    def test_set_label(self):
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertEqual(grid.labels, {})

        # basic
        grid.set_label('foo', "Foo Fighters")
        self.assertEqual(grid.labels['foo'], "Foo Fighters")

        # can replace label
        grid.set_label('foo', "Different")
        self.assertEqual(grid.labels['foo'], "Different")
        self.assertEqual(grid.get_label('foo'), "Different")

    def test_get_label(self):
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertEqual(grid.labels, {})

        # default derived from key
        self.assertEqual(grid.get_label('foo'), "Foo")

        # can override
        grid.set_label('foo', "Different")
        self.assertEqual(grid.get_label('foo'), "Different")

    def test_set_renderer(self):
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertEqual(grid.renderers, {})

        def render1(record, key, value):
            pass

        # basic
        grid.set_renderer('foo', render1)
        self.assertIs(grid.renderers['foo'], render1)

        def render2(record, key, value, extra=None):
            return extra

        # can pass kwargs to get a partial
        grid.set_renderer('foo', render2, extra=42)
        self.assertIsNot(grid.renderers['foo'], render2)
        self.assertEqual(grid.renderers['foo'](None, None, None), 42)

    def test_linked_columns(self):
        grid = self.make_grid(columns=['foo', 'bar'])
        self.assertEqual(grid.linked_columns, [])
        self.assertFalse(grid.is_linked('foo'))

        grid.set_link('foo')
        self.assertEqual(grid.linked_columns, ['foo'])
        self.assertTrue(grid.is_linked('foo'))
        self.assertFalse(grid.is_linked('bar'))

        grid.set_link('bar')
        self.assertEqual(grid.linked_columns, ['foo', 'bar'])
        self.assertTrue(grid.is_linked('foo'))
        self.assertTrue(grid.is_linked('bar'))

        grid.set_link('foo', False)
        self.assertEqual(grid.linked_columns, ['bar'])
        self.assertFalse(grid.is_linked('foo'))
        self.assertTrue(grid.is_linked('bar'))

    def test_get_pagesize_options(self):
        grid = self.make_grid()

        # default
        options = grid.get_pagesize_options()
        self.assertEqual(options, [5, 10, 20, 50, 100, 200])

        # override default
        options = grid.get_pagesize_options(default=[42])
        self.assertEqual(options, [42])

        # from config
        self.config.setdefault('wuttaweb.grids.default_pagesize_options', '1 2 3')
        options = grid.get_pagesize_options()
        self.assertEqual(options, [1, 2, 3])

    def test_get_pagesize(self):
        grid = self.make_grid()

        # default
        size = grid.get_pagesize()
        self.assertEqual(size, 20)

        # override default
        size = grid.get_pagesize(default=42)
        self.assertEqual(size, 42)

        # override default options
        self.config.setdefault('wuttaweb.grids.default_pagesize_options', '10 15 30')
        grid = self.make_grid()
        size = grid.get_pagesize()
        self.assertEqual(size, 10)

        # from config
        self.config.setdefault('wuttaweb.grids.default_pagesize', '15')
        size = grid.get_pagesize()
        self.assertEqual(size, 15)

    ##############################
    # configuration methods
    ##############################

    def test_load_settings(self):
        grid = self.make_grid(key='foo', paginated=True, paginate_on_backend=True,
                              pagesize=20, page=1)

        # settings are loaded, applied, saved
        self.assertEqual(grid.page, 1)
        self.assertNotIn('grid.foo.page', self.request.session)
        self.request.GET = {'pagesize': '10', 'page': '2'}
        grid.load_settings()
        self.assertEqual(grid.page, 2)
        self.assertEqual(self.request.session['grid.foo.page'], 2)

        # can skip the saving step
        self.request.GET = {'pagesize': '10', 'page': '3'}
        grid.load_settings(store=False)
        self.assertEqual(grid.page, 3)
        self.assertEqual(self.request.session['grid.foo.page'], 2)

        # no error for non-paginated grid
        grid = self.make_grid(key='foo', paginated=False)
        grid.load_settings()
        self.assertFalse(grid.paginated)

    def test_request_has_settings(self):
        grid = self.make_grid(key='foo')

        self.assertFalse(grid.request_has_settings())

        with patch.object(self.request, 'GET', new={'pagesize': '20'}):
            self.assertTrue(grid.request_has_settings())

        with patch.object(self.request, 'GET', new={'page': '1'}):
            self.assertTrue(grid.request_has_settings())

    def test_update_page_settings(self):
        grid = self.make_grid(key='foo')

        # settings are updated from session
        settings = {'pagesize': 20, 'page': 1}
        self.request.session['grid.foo.pagesize'] = 10
        self.request.session['grid.foo.page'] = 2
        grid.update_page_settings(settings)
        self.assertEqual(settings['pagesize'], 10)
        self.assertEqual(settings['page'], 2)

        # settings are updated from request
        self.request.GET = {'pagesize': '15', 'page': '4'}
        grid.update_page_settings(settings)
        self.assertEqual(settings['pagesize'], 15)
        self.assertEqual(settings['page'], 4)

    def test_persist_settings(self):
        grid = self.make_grid(key='foo', paginated=True, paginate_on_backend=True)

        # nb. no error if empty settings, but it saves null values
        grid.persist_settings({})
        self.assertIsNone(self.request.session['grid.foo.page'])

        # provided values are saved
        grid.persist_settings({'pagesize': 15, 'page': 3})
        self.assertEqual(self.request.session['grid.foo.page'], 3)

    ##############################
    # data methods
    ##############################

    def test_get_visible_data(self):
        data = [
            {'foo': 1, 'bar': 1},
            {'foo': 2, 'bar': 2},
            {'foo': 3, 'bar': 3},
            {'foo': 4, 'bar': 4},
            {'foo': 5, 'bar': 5},
            {'foo': 6, 'bar': 6},
            {'foo': 7, 'bar': 7},
            {'foo': 8, 'bar': 8},
            {'foo': 9, 'bar': 9},
        ]
        grid = self.make_grid(data=data,
                              columns=['foo', 'bar'],
                              paginated=True, paginate_on_backend=True,
                              pagesize=4, page=2)
        visible = grid.get_visible_data()
        self.assertEqual(len(visible), 4)
        self.assertEqual(visible[0], {'foo': 5, 'bar': 5})

    def test_paginate_data(self):
        grid = self.make_grid()
        pager = grid.paginate_data([])
        self.assertIsInstance(pager, Page)

    ##############################
    # rendering methods
    ##############################

    def test_render_vue_tag(self):
        grid = self.make_grid(columns=['foo', 'bar'])
        html = grid.render_vue_tag()
        self.assertEqual(html, '<wutta-grid></wutta-grid>')

    def test_render_vue_template(self):
        self.pyramid_config.include('pyramid_mako')
        self.pyramid_config.add_subscriber('wuttaweb.subscribers.before_render',
                                           'pyramid.events.BeforeRender')

        grid = self.make_grid(columns=['foo', 'bar'])
        html = grid.render_vue_template()
        self.assertIn('<script type="text/x-template" id="wutta-grid-template">', html)

    def test_get_vue_columns(self):

        # error if no columns are set
        grid = self.make_grid()
        self.assertRaises(ValueError, grid.get_vue_columns)

        # otherwise get back field/label dicts
        grid = self.make_grid(columns=['foo', 'bar'])
        columns = grid.get_vue_columns()
        first = columns[0]
        self.assertEqual(first['field'], 'foo')
        self.assertEqual(first['label'], 'Foo')

    def test_get_vue_data(self):

        # empty if no columns defined
        grid = self.make_grid()
        data = grid.get_vue_data()
        self.assertEqual(data, [])

        # typical data is a list
        mydata = [
            {'foo': 'bar'},
        ]
        grid = self.make_grid(columns=['foo'], data=mydata)
        data = grid.get_vue_data()
        self.assertEqual(data, [{'foo': 'bar'}])

        # if grid has actions, that list may be supplemented
        grid.actions.append(base.GridAction(self.request, 'view', url='/blarg'))
        data = grid.get_vue_data()
        self.assertIsNot(data, mydata)
        self.assertEqual(data, [{'foo': 'bar', '_action_url_view': '/blarg'}])

        # also can override value rendering
        grid.set_renderer('foo', lambda record, key, value: "blah blah")
        data = grid.get_vue_data()
        self.assertEqual(data, [{'foo': 'blah blah', '_action_url_view': '/blarg'}])

    def test_get_vue_pager_stats(self):
        data = [
            {'foo': 1, 'bar': 1},
            {'foo': 2, 'bar': 2},
            {'foo': 3, 'bar': 3},
            {'foo': 4, 'bar': 4},
            {'foo': 5, 'bar': 5},
            {'foo': 6, 'bar': 6},
            {'foo': 7, 'bar': 7},
            {'foo': 8, 'bar': 8},
            {'foo': 9, 'bar': 9},
        ]

        grid = self.make_grid(columns=['foo', 'bar'], pagesize=4, page=2)
        grid.pager = grid.paginate_data(data)
        stats = grid.get_vue_pager_stats()
        self.assertEqual(stats['item_count'], 9)
        self.assertEqual(stats['items_per_page'], 4)
        self.assertEqual(stats['page'], 2)
        self.assertEqual(stats['first_item'], 5)
        self.assertEqual(stats['last_item'], 8)


class TestGridAction(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.request = testing.DummyRequest(wutta_config=self.config, use_oruga=False)

    def make_action(self, key, **kwargs):
        return base.GridAction(self.request, key, **kwargs)

    def test_render_icon(self):

        # icon is derived from key by default
        action = self.make_action('blarg')
        html = action.render_icon()
        self.assertIn('<i class="fas fa-blarg">', html)

        # oruga has different output
        self.request.use_oruga = True
        html = action.render_icon()
        self.assertIn('<o-icon icon="blarg">', html)

    def test_render_label(self):

        # label is derived from key by default
        action = self.make_action('blarg')
        label = action.render_label()
        self.assertEqual(label, "Blarg")

        # otherwise use what caller provides
        action = self.make_action('foo', label="Bar")
        label = action.render_label()
        self.assertEqual(label, "Bar")

    def test_render_icon_and_label(self):
        action = self.make_action('blarg')
        with patch.multiple(action,
                            render_icon=lambda: 'ICON',
                            render_label=lambda: 'LABEL'):
            html = action.render_icon_and_label()
            self.assertEqual('ICON LABEL', html)

    def test_get_url(self):
        obj = {'foo': 'bar'}

        # null by default
        action = self.make_action('blarg')
        url = action.get_url(obj)
        self.assertIsNone(url)

        # or can be "static"
        action = self.make_action('blarg', url='/foo')
        url = action.get_url(obj)
        self.assertEqual(url, '/foo')

        # or can be "dynamic"
        action = self.make_action('blarg', url=lambda o, i: '/yeehaw')
        url = action.get_url(obj)
        self.assertEqual(url, '/yeehaw')

# -*- coding: utf-8; -*-

from unittest.mock import MagicMock

from tailbone.grids import core as mod
from tests.util import WebTestCase


class TestGrid(WebTestCase):

    def setUp(self):
        self.setup_web()
        self.config.setdefault('rattail.web.menus.handler_spec', 'tests.util:NullMenuHandler')

    def make_grid(self, key=None, data=[], **kwargs):
        return mod.Grid(self.request, key=key, data=data, **kwargs)

    def test_basic(self):
        grid = self.make_grid('foo')
        self.assertIsInstance(grid, mod.Grid)

    def test_deprecated_params(self):

        # component
        grid = self.make_grid()
        self.assertEqual(grid.vue_tagname, 'tailbone-grid')
        grid = self.make_grid(component='blarg')
        self.assertEqual(grid.vue_tagname, 'blarg')

        # pageable
        grid = self.make_grid()
        self.assertFalse(grid.paginated)
        grid = self.make_grid(pageable=True)
        self.assertTrue(grid.paginated)

        # default_pagesize
        grid = self.make_grid()
        self.assertEqual(grid.pagesize, 20)
        grid = self.make_grid(default_pagesize=15)
        self.assertEqual(grid.pagesize, 15)

        # default_page
        grid = self.make_grid()
        self.assertEqual(grid.page, 1)
        grid = self.make_grid(default_page=42)
        self.assertEqual(grid.page, 42)

    def test_vue_tagname(self):

        # default
        grid = self.make_grid('foo')
        self.assertEqual(grid.vue_tagname, 'tailbone-grid')

        # can override with param
        grid = self.make_grid('foo', vue_tagname='something-else')
        self.assertEqual(grid.vue_tagname, 'something-else')

        # can still pass old param
        grid = self.make_grid('foo', component='legacy-name')
        self.assertEqual(grid.vue_tagname, 'legacy-name')

    def test_vue_component(self):

        # default
        grid = self.make_grid('foo')
        self.assertEqual(grid.vue_component, 'TailboneGrid')

        # can override with param
        grid = self.make_grid('foo', vue_tagname='something-else')
        self.assertEqual(grid.vue_component, 'SomethingElse')

        # can still pass old param
        grid = self.make_grid('foo', component='legacy-name')
        self.assertEqual(grid.vue_component, 'LegacyName')

    def test_component(self):

        # default
        grid = self.make_grid('foo')
        self.assertEqual(grid.component, 'tailbone-grid')

        # can override with param
        grid = self.make_grid('foo', vue_tagname='something-else')
        self.assertEqual(grid.component, 'something-else')

        # can still pass old param
        grid = self.make_grid('foo', component='legacy-name')
        self.assertEqual(grid.component, 'legacy-name')

    def test_component_studly(self):

        # default
        grid = self.make_grid('foo')
        self.assertEqual(grid.component_studly, 'TailboneGrid')

        # can override with param
        grid = self.make_grid('foo', vue_tagname='something-else')
        self.assertEqual(grid.component_studly, 'SomethingElse')

        # can still pass old param
        grid = self.make_grid('foo', component='legacy-name')
        self.assertEqual(grid.component_studly, 'LegacyName')

    def test_actions(self):

        # default
        grid = self.make_grid('foo')
        self.assertEqual(grid.actions, [])

        # main actions
        grid = self.make_grid('foo', main_actions=['foo'])
        self.assertEqual(grid.actions, ['foo'])

        # more actions
        grid = self.make_grid('foo', main_actions=['foo'], more_actions=['bar'])
        self.assertEqual(grid.actions, ['foo', 'bar'])

    def test_set_label(self):
        model = self.app.model
        grid = self.make_grid(model_class=model.Setting)
        self.assertEqual(grid.labels, {})

        # basic
        grid.set_label('name', "NAME COL")
        self.assertEqual(grid.labels['name'], "NAME COL")

        # can replace label
        grid.set_label('name', "Different")
        self.assertEqual(grid.labels['name'], "Different")
        self.assertEqual(grid.get_label('name'), "Different")

        # can update only column, not filter
        self.assertEqual(grid.labels, {'name': "Different"})
        self.assertIn('name', grid.filters)
        self.assertEqual(grid.filters['name'].label, "Different")
        grid.set_label('name', "COLUMN ONLY", column_only=True)
        self.assertEqual(grid.get_label('name'), "COLUMN ONLY")
        self.assertEqual(grid.filters['name'].label, "Different")

    def test_get_view_click_handler(self):
        model = self.app.model
        grid = self.make_grid(model_class=model.Setting)

        grid.actions.append(
            mod.GridAction(self.request, 'view',
                           click_handler='clickHandler(props.row)'))

        handler = grid.get_view_click_handler()
        self.assertEqual(handler, 'clickHandler(props.row)')

    def test_set_action_urls(self):
        model = self.app.model
        grid = self.make_grid(model_class=model.Setting)

        grid.actions.append(
            mod.GridAction(self.request, 'view', url='/blarg'))

        setting = {'name': 'foo', 'value': 'bar'}
        grid.set_action_urls(setting, setting, 0)
        self.assertEqual(setting['_action_url_view'], '/blarg')

    def test_pageable(self):
        grid = self.make_grid()
        self.assertFalse(grid.paginated)
        grid.pageable = True
        self.assertTrue(grid.paginated)
        grid.paginated = False
        self.assertFalse(grid.pageable)

    def test_get_pagesize_options(self):
        grid = self.make_grid()

        # default
        options = grid.get_pagesize_options()
        self.assertEqual(options, [5, 10, 20, 50, 100, 200])

        # override default
        options = grid.get_pagesize_options(default=[42])
        self.assertEqual(options, [42])

        # from legacy config
        self.config.setdefault('tailbone.grid.pagesize_options', '1 2 3')
        grid = self.make_grid()
        options = grid.get_pagesize_options()
        self.assertEqual(options, [1, 2, 3])

        # from new config
        self.config.setdefault('wuttaweb.grids.default_pagesize_options', '4, 5, 6')
        grid = self.make_grid()
        options = grid.get_pagesize_options()
        self.assertEqual(options, [4, 5, 6])

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

        # from legacy config
        self.config.setdefault('tailbone.grid.default_pagesize', '12')
        grid = self.make_grid()
        size = grid.get_pagesize()
        self.assertEqual(size, 12)

        # from new config
        self.config.setdefault('wuttaweb.grids.default_pagesize', '15')
        grid = self.make_grid()
        size = grid.get_pagesize()
        self.assertEqual(size, 15)

    def test_render_vue_tag(self):
        model = self.app.model

        # standard
        grid = self.make_grid('settings', model_class=model.Setting)
        html = grid.render_vue_tag()
        self.assertIn('<tailbone-grid', html)
        self.assertNotIn('@deleteActionClicked', html)

        # with delete hook
        master = MagicMock(deletable=True, delete_confirm='simple')
        master.has_perm.return_value = True
        grid = self.make_grid('settings', model_class=model.Setting)
        html = grid.render_vue_tag(master=master)
        self.assertIn('<tailbone-grid', html)
        self.assertIn('@deleteActionClicked', html)

    def test_render_vue_template(self):
        # self.pyramid_config.include('tailbone.views.common')
        model = self.app.model

        # sanity check
        grid = self.make_grid('settings', model_class=model.Setting)
        html = grid.render_vue_template(session=self.session)
        self.assertIn('<b-table', html)

    def test_get_vue_columns(self):
        model = self.app.model

        # sanity check
        grid = self.make_grid('settings', model_class=model.Setting)
        columns = grid.get_vue_columns()
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]['field'], 'name')
        self.assertEqual(columns[1]['field'], 'value')

    def test_get_vue_data(self):
        model = self.app.model

        # sanity check
        grid = self.make_grid('settings', model_class=model.Setting)
        data = grid.get_vue_data()
        self.assertEqual(data, [])

        # calling again returns same data
        data2 = grid.get_vue_data()
        self.assertIs(data2, data)


class TestGridAction(WebTestCase):

    def test_constructor(self):

        # null by default
        action = mod.GridAction(self.request, 'view')
        self.assertIsNone(action.target)
        self.assertIsNone(action.click_handler)

        # but can set them
        action = mod.GridAction(self.request, 'view',
                                target='_blank',
                                click_handler='doSomething(props.row)')
        self.assertEqual(action.target, '_blank')
        self.assertEqual(action.click_handler, 'doSomething(props.row)')

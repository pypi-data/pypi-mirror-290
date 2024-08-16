# -*- coding: utf-8; -*-

from unittest.mock import MagicMock

from tailbone.grids import core as mod
from tests.util import WebTestCase


class TestGrid(WebTestCase):

    def setUp(self):
        self.setup_web()
        self.config.setdefault('rattail.web.menus.handler_spec', 'tests.util:NullMenuHandler')

    def make_grid(self, key, data=[], **kwargs):
        kwargs.setdefault('request', self.request)
        return mod.Grid(key, data=data, **kwargs)

    def test_basic(self):
        grid = self.make_grid('foo')
        self.assertIsInstance(grid, mod.Grid)

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

# -*- coding: utf-8; -*-

from unittest.mock import patch

from sqlalchemy import orm

from tailbone.views.wutta import people as mod
from tests.util import WebTestCase


class TestPersonView(WebTestCase):

    def make_view(self):
        return mod.PersonView(self.request)

    def test_includeme(self):
        self.pyramid_config.include('tailbone.views.wutta.people')

    def test_get_query(self):
        view = self.make_view()

        # sanity / coverage check
        query = view.get_query(session=self.session)
        self.assertIsInstance(query, orm.Query)

    def test_configure_form(self):
        model = self.app.model
        barney = model.User(username='barney')
        self.session.add(barney)
        self.session.commit()
        view = self.make_view()

        # customers field remains when viewing
        with patch.object(view, 'viewing', new=True):
            form = view.make_form(model_instance=barney,
                                  fields=view.get_form_fields())
            self.assertIn('customers', form.fields)
            view.configure_form(form)
            self.assertIn('customers', form)

        # customers field removed when editing
        with patch.object(view, 'editing', new=True):
            form = view.make_form(model_instance=barney,
                                  fields=view.get_form_fields())
            self.assertIn('customers', form.fields)
            view.configure_form(form)
            self.assertNotIn('customers', form)

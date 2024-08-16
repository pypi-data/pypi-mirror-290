# -*- coding: utf-8; -*-

from unittest.mock import patch

from tailbone.views import master as mod
from tests.util import WebTestCase


class TestMasterView(WebTestCase):

    def make_view(self):
        return mod.MasterView(self.request)

    def test_make_form_kwargs(self):
        self.pyramid_config.add_route('settings.view', '/settings/{name}')
        model = self.app.model
        setting = model.Setting(name='foo', value='bar')
        self.session.add(setting)
        self.session.commit()
        with patch.multiple(mod.MasterView, create=True,
                            model_class=model.Setting):
            view = self.make_view()

            # sanity / coverage check
            kw = view.make_form_kwargs(model_instance=setting)
            self.assertIsNotNone(kw['action_url'])

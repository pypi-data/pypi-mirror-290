# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Person Views
"""

from rattail.db.model import Person

from wuttaweb.views import people as wutta
from tailbone.views import people as tailbone
from tailbone.db import Session


class PersonView(wutta.PersonView):
    """
    This is the first attempt at blending newer Wutta views with
    legacy Tailbone config.

    So, this is a Wutta-based view but it should be included by a
    Tailbone app configurator.
    """
    model_class = Person
    Session = Session

    # labels = {
    #     'display_name': "Full Name",
    # }

    grid_columns = [
        'display_name',
        'first_name',
        'last_name',
        'phone',
        'email',
        'merge_requested',
    ]

    form_fields = [
        'first_name',
        'middle_name',
        'last_name',
        'display_name',
        'default_phone',
        'default_email',
        # 'address',
        # 'employee',
        'customers',
        # 'members',
        'users',
    ]

    def get_query(self, session=None):
        """ """
        model = self.app.model
        session = session or self.Session()
        return session.query(model.Person)\
                      .order_by(model.Person.display_name)

    def configure_form(self, f):
        """ """
        super().configure_form(f)

        # default_phone
        f.set_required('default_phone', False)

        # default_email
        f.set_required('default_email', False)

        # customers
        if self.creating or self.editing:
            f.remove('customers')


def defaults(config, **kwargs):
    base = globals()

    kwargs.setdefault('PersonView', base['PersonView'])
    tailbone.defaults(config, **kwargs)


def includeme(config):
    defaults(config)

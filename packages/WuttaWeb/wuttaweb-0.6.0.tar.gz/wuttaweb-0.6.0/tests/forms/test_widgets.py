# -*- coding: utf-8; -*-

import colander
import deform
from pyramid import testing

from wuttaweb.forms import widgets
from wuttaweb.forms.schema import PersonRef
from tests.util import WebTestCase

class TestObjectRefWidget(WebTestCase):

    def test_serialize(self):
        model = self.app.model
        person = model.Person(full_name="Betty Boop")
        self.session.add(person)
        self.session.commit()

        # standard (editable)
        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        widget = widgets.ObjectRefWidget(self.request)
        field = deform.Field(node)
        html = widget.serialize(field, person.uuid)
        self.assertIn('<select ', html)

        # readonly
        node = colander.SchemaNode(PersonRef(self.request, session=self.session))
        node.model_instance = person
        widget = widgets.ObjectRefWidget(self.request)
        field = deform.Field(node)
        html = widget.serialize(field, person.uuid, readonly=True)
        self.assertEqual(html, '<span>Betty Boop</span>')

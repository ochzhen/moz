# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from service import *


class MOZDocumentTestCase(TestCase):

    def setUp(self):
        MOZDocument.objects.create(title='Document1', content='Test content 1', document='path/to/doc1')
        MOZDocument.objects.create(title='Document2', content='Test content 2', document='path/to/doc2')
        MOZDocument.objects.create(title='Document3', content='Test content 3', document='path/to/doc3')

    def test_get_all_will_return_all_objects(self):
        self.assertEqual(3, len(get_all_documents_order_by_title()))
        self.assertEqual(3, len(get_all_documents_order_by_title(True)))

    def test_get_number_will_return_number_of_objects(self):
        self.assertEqual(1, len(get_number_of_documents_order_by_title(1)))
        self.assertEqual(2, len(get_number_of_documents_order_by_title(2, True)))

    def test_get_order_by_title_asc(self):
        self.assertEqual('Document1', get_all_documents_order_by_title()[0].title)
        self.assertEqual('Document1', get_number_of_documents_order_by_title(1)[0].title)

    def test_get_order_by_title_desc(self):
        self.assertEqual('Document3', get_all_documents_order_by_title(True)[0].title)
        self.assertEqual('Document3', get_number_of_documents_order_by_title(1, True)[0].title)

    def test_get_by_id(self):
        self.assertEqual('Document1', get_document_by_id(1).title)

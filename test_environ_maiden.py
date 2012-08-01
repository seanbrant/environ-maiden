#!/usr/bin/env python

import unittest

from mock import patch

from environ_maiden import Environment


class EnvironmentTestCase(unittest.TestCase):

    def setUp(self):
        self.environ_patcher = patch('environm.os.environ', dict())
        self.environ = self.environ_patcher.start()

    def tearDown(self):
        self.environ_patcher.stop()

    def test_items_come_from_environ(self):
        self.environ['KEY'] = 'value'
        self.assertEqual(Environment().environ, {'KEY': 'value'})

    def test_repr(self):
        self.assertEqual(repr(Environment()), '<Environment: {}>')

    def test_get_ignores_prefix(self):
        self.environ['KEY'] = 'value'
        self.assertEqual(Environment().get('KEY'), 'value')

    def test_get_adds_prefix(self):
        self.environ['PREFIX_KEY'] = 'value'
        self.assertEqual(Environment(prefix='PREFIX').get('KEY'), 'value')

    def test_bool_true(self):
        for value in [1, '1', 'true', 't', 'True', 'TRUE']:
            self.environ['KEY'] = value
            self.assertTrue(Environment().bool('KEY'), '{0} is not True'.format(value))

    def test_bool_false(self):
        for value in [0, '0', 'false', 'f', 'False', 'FALSE']:
            self.environ['KEY'] = value
            self.assertFalse(Environment().bool('KEY'), '{0} is not False'.format(value))

    def test_bool_invalid(self):
        self.environ['KEY'] = 'not-valid'
        self.assertRaises(ValueError, Environment().bool, 'KEY')

    def test_int_valid(self):
        self.environ['KEY'] = '1'
        self.assertEqual(Environment().int('KEY'), 1)

    def test_int_invalid(self):
        self.environ['KEY'] = 'not-valid'
        self.assertRaises(ValueError, Environment().int, 'KEY')

    def test_list_with_already_a_list(self):
        self.environ['KEY'] = [1, 2]
        self.assertEqual(Environment().list('KEY'), [1, 2])

    def test_list_splits_by_comma(self):
        self.environ['KEY'] = '1,2'
        self.assertEqual(Environment().list('KEY'), ['1', '2'])

    def test_list_trims_white_space(self):
        self.environ['KEY'] = '1, 2'
        self.assertEqual(Environment().list('KEY'), ['1', '2'])

    def test_list_with_corce(self):
        self.environ['KEY'] = '1,2'
        self.assertEqual(Environment().list('KEY', corce=int), [1, 2])

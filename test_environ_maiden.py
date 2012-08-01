#!/usr/bin/env python

import unittest

from mock import patch

from environm import Env


class EnvironmentTestCase(unittest.TestCase):

    def setUp(self):
        self.environ_patcher = patch('environm.os.environ', dict())
        self.environ = self.environ_patcher.start()

    def tearDown(self):
        self.environ_patcher.stop()

    def test_items_come_from_environ(self):
        self.environ['KEY'] = 'value'
        self.assertEqual(Env(), {'KEY': 'value'})

    def test_repr(self):
        self.assertEqual(repr(Env()), '<Env: {}>')

    def test_bool_true(self):
        for value in [1, '1', 'true', 't', 'True', 'TRUE']:
            self.environ['KEY'] = value
            self.assertTrue(Env().bool('KEY'), '{0} is not True'.format(value))

    def test_bool_false(self):
        for value in [0, '0', 'false', 'f', 'False', 'FALSE']:
            self.environ['KEY'] = value
            self.assertFalse(Env().bool('KEY'), '{0} is not False'.format(value))

    def test_bool_invalid(self):
        self.environ['KEY'] = 'not-valid'
        self.assertRaises(ValueError, Env().bool, 'KEY')

    def test_int_valid(self):
        self.environ['KEY'] = '1'
        self.assertEqual(Env().int('KEY'), 1)

    def test_int_invalid(self):
        self.environ['KEY'] = 'not-valid'
        self.assertRaises(ValueError, Env().int, 'KEY')

    def test_list_with_already_a_list(self):
        self.environ['KEY'] = [1, 2]
        self.assertEqual(Env().list('KEY'), [1, 2])

    def test_list_splits_by_comma(self):
        self.environ['KEY'] = '1,2'
        self.assertEqual(Env().list('KEY'), ['1', '2'])

    def test_list_trims_white_space(self):
        self.environ['KEY'] = '1, 2'
        self.assertEqual(Env().list('KEY'), ['1', '2'])

    def test_list_with_corce(self):
        self.environ['KEY'] = '1,2'
        self.assertEqual(Env().list('KEY', corce=int), [1, 2])

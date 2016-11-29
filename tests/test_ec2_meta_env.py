"""Tests the Python3 implementation of ec2_meta_env"""
import argparse
import random
import string
import unittest

import requests

import ec2_meta_env

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class Ec2MetaEnvTestCase(unittest.TestCase):

    def _setup_mock(self, get_func):
        value = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        get_func.return_value.text = value
        return value

    def _get_ns(self, env, **kwargs):
        """Provides some sensible defaults for argparse.Namespace"""
        defaults = {
            'command': 'my-cmd',
            'override': False,
            'strict': False,
            'timeout': 0.2,
        }
        defaults.update(kwargs)
        return argparse.Namespace(env=env, **defaults)


@patch('ec2_meta_env.requests.get')
class GetEnvironUnitTests(Ec2MetaEnvTestCase):

    def test_set_one_var(self, get):
        test_value = self._setup_mock(get)
        ns = self._get_ns(['local-ipv4'])
        env = ec2_meta_env.get_environ({}, ns)
        self.assertEqual(get.call_count, 1)
        self.assertTrue('EC2_LOCAL_IPV4' in env)
        self.assertEqual(env['EC2_LOCAL_IPV4'], test_value)

    def test_set_many_var(self, get):
        test_value = self._setup_mock(get)
        ns = self._get_ns(['local-ipv4', 'local-hostname'])
        env = ec2_meta_env.get_environ({}, ns)
        self.assertEqual(get.call_count, 2)
        self.assertTrue('EC2_LOCAL_IPV4' in env)
        self.assertTrue('EC2_LOCAL_HOSTNAME' in env)
        self.assertEqual(env['EC2_LOCAL_IPV4'], test_value)
        self.assertEqual(env['EC2_LOCAL_HOSTNAME'], test_value)

    def test_override(self, get):
        base_env = {'EC2_LOCAL_IPV4': 'original-data'}
        test_value = self._setup_mock(get)
        ns = self._get_ns(['local-ipv4'], override=True)
        env = ec2_meta_env.get_environ(base_env, ns)
        self.assertEqual(get.call_count, 1)
        self.assertEqual(env['EC2_LOCAL_IPV4'], test_value)

    def test_dont_override(self, get):
        base_env = {'EC2_LOCAL_IPV4': 'original-data'}
        self._setup_mock(get)
        ns = self._get_ns(['local-ipv4'], override=False)
        env = ec2_meta_env.get_environ(base_env, ns)
        self.assertEqual(get.call_count, 1)
        self.assertEqual(env['EC2_LOCAL_IPV4'], 'original-data')

    def test_strict_exception(self, get):
        get.side_effect = requests.exceptions.RequestException()
        self._setup_mock(get)
        ns = self._get_ns(['local-ipv4'], strict=True)
        with self.assertRaises(requests.exceptions.RequestException):
            ec2_meta_env.get_environ({}, ns)
        self.assertEqual(get.call_count, 1)

    def test_unstrict_exception(self, get):
        get.side_effect = requests.exceptions.RequestException()
        self._setup_mock(get)
        ns = self._get_ns(['local-ipv4'], strict=False)
        env = ec2_meta_env.get_environ({}, ns)
        self.assertEqual(get.call_count, 1)
        self.assertFalse('EC2_LOCAL_IPV4' in env)


@patch('ec2_meta_env.requests.get')
@patch('ec2_meta_env.subprocess.Popen')
class MainIntegrationTests(Ec2MetaEnvTestCase):

    def test_basic_usage(self, popen, get):
        test_value = self._setup_mock(get)
        popen.return_value.returncode = 123
        ret_val = ec2_meta_env.main(
            {'MY_VAR': 'some-val'},
            ['-e', 'local-ipv4', 'my-cmd'],
        )
        get.assert_called_once_with(
            'http://169.254.169.254/latest/meta-data/local-ipv4',
            timeout=0.2,
        )
        popen.assert_called_once_with(
            ['my-cmd'],
            env={
                'MY_VAR': 'some-val',
                'EC2_LOCAL_IPV4': test_value,
            },
        )
        self.assertEqual(ret_val, 123)


if __name__ == '__main__':
    unittest.main()

# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p
import mock
import json

# project
from tests.checks.common import AgentCheckTest

MOCK_OK_CONFIG = {
    'init_config': {},
    'instances': [
        {'url': 'http://localhost:7002'}
    ]
}
MOCK_CRITICAL_CONFIG = {
    'init_config': {},
    'instances': [
        {'url': 'http://badurl:7002'}
    ]
}

class MockResponse:
   def __init__(self, json_data, status_code):
       self.json_data = json_data
       self.status_code = status_code

   def json(self):
       return self.json_data

def mock_requests_get(*args, **kwargs):

    if args[0] == 'http://localhost:7002/health':
        return MockResponse({"status": "UP"}, 200)
    else:
        return MockResponse(None, 404)

class TestSpinnaker_clouddriver(AgentCheckTest):
    CHECK_NAME = 'spinnaker_clouddriver'
    SERVICE_CHECK_NAME = 'spinnaker.clouddriver.health'

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_ok_service_check(self, mock_requests):
        self.run_check(MOCK_OK_CONFIG)
        self.print_current_state()
        self.assertServiceCheckOK(self.SERVICE_CHECK_NAME)
        self.coverage_report()

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_critical_service_check(self, mock_requests):
        self.assertRaises(
            Exception,
            lambda: self.run_check(MOCK_CRITICAL_CONFIG)
        )
        self.print_current_state()
        self.assertServiceCheckCritical(self.SERVICE_CHECK_NAME)
        self.coverage_report()

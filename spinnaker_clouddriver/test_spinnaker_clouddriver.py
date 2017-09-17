# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from nose.plugins.attrib import attr

# 3p

# project
from tests.checks.common import AgentCheckTest


instance = {
    'host': 'localhost',
    'port': 26379,
    'password': 'datadog-is-devops-best-friend'
}


# NOTE: Feel free to declare multiple test classes if needed

@attr(requires='spinnaker_clouddriver')
class TestSpinnaker_clouddriver(AgentCheckTest):
    """Basic Test for spinnaker_clouddriver integration."""
    CHECK_NAME = 'spinnaker_clouddriver'

    def test_check(self):
        """
        Testing Spinnaker_clouddriver check.
        """
        self.load_check({}, {})

        # run your actual tests...

        self.assertTrue(True)
        # Raises when COVERAGE=true and coverage < 100%
        self.coverage_report()

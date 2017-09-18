# (C) Datadog, Inc. 2010-2016
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from checks import AgentCheck

class Spinnaker_clouddriverCheck(AgentCheck):
    DEFAULT_TIMEOUT = 5
    SERVICE_CHECK_NAME = 'spinnaker.clouddriver.health'

    def check(self, instance):
        url = instance['url']
        timeout = float(instance.get('timeout', self.DEFAULT_TIMEOUT))

        health = self._get_health(url, timeout)
        if health is not None:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.OK,
                tags=["url:{0}".format(url)],
            )

    def _get_health(self, url, timeout):
        return self._get_json(url + '/health', timeout)

    def _get_json(self, url, timeout):
        try:
            r = requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Timeout when hitting %s" % url,
                tags=["url:{0}".format(url)],
            )
            raise
        except Exception as e:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Error hitting %s. Error: %s" % (url, e.message),
                tags=["url:{0}".format(url)],
            )
            raise

        if r.status_code != 200:
            self.service_check(
                self.SERVICE_CHECK_NAME,
                AgentCheck.CRITICAL,
                message="Got %s when hitting %s" % (r.status_code, url),
                tags=["url:{0}".format(url)]
            )
            raise Exception("Http status code {0} on url {1}".format(r.status_code, url))

        return r.json()

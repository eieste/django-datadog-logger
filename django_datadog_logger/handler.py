import logging
import urllib.parse
import urllib.request
import json


class DatadogHandler(logging.Handler):

    def __init__(self, host, api_key, parameters):
        logging.Handler.__init__(self)
        self.host = host
        self.api_key = api_key
        parameters.update({
            "ddsource": "django-datadog-handler"
        })

        self.parameters = urllib.parse.urlencode(parameters)

    def emit(self, record):
        data = self.format(record).encode("utf8")
        try:
            req = urllib.request.Request("https://{}/v1/input/{}/?{}".format(self.host, self.api_key, self.parameters),
                                         data=data,
                                         headers={'content-type': 'application/json'})
            response = urllib.request.urlopen(req)
        except Exception as e:
            self.handleError(record)

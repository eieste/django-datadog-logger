"""
    Orginal json formatter by:
    https://github.com/marselester/json-log-formatter
    Published under MIT License
    install the Orginal via: pip3 install json-log-formatter
"""


from datetime import datetime
from django.utils import timezone
import json
import logging

BUILTIN_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
}


class DatadogJsonFormatter(logging.Formatter):
    """Datadog JSON log formatter.

    """

    json_lib = json

    def format(self, record):
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value will return None because they modified the
        # argument passed in.
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    def to_json(self, record):
        """Converts record dict to a JSON string.

        Override this method to change the way dict is converted to JSON.

        """
        return self.json_lib.dumps(record)

    def extra_from_record(self, record):
        """Returns `extra` dict you passed to logger.

        The `extra` keyword argument is used to populate the `__dict__` of
        the `LogRecord`.

        """
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in BUILTIN_ATTRS
        }

    def json_record(self, message, extra, record):
        """Prepares a JSON payload which will be logged.

        Override this method to change JSON log format.

        :param message: Log message, e.g., `logger.info(msg='Sign up')`.
        :param extra: Dictionary that was passed as `extra` param
            `logger.info('Sign up', extra={'referral_code': '52d6ce'})`.
        :param record: `LogRecord` we got from `JSONFormatter.format()`.
        :return: Dictionary which will be passed to JSON lib.

        """

        try:
            extra["trace_id"] = record.dd.trace_id
        except Exception:
            pass

        extra['message'] = message
        if 'time' not in extra:
            extra['time'] = timezone.now()

        if str(record.levelname).lower() == "exception":
            extra["status"] = "trace"
        extra["source"] = record.pathname

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        extra = self.recursive_cleanup(extra)
        return extra

    def recursive_cleanup(self, extra):
        result = {}
        
        for key, value in extra.items():
            if type(value) in [dict, list, tuple]:
                result[key] = self.recursive_cleanup(value)
            else:
                try:
                    json.dumps({"a": value})
                except Exception:
                    pass
                else:
                    result[key] = value
        return result


    def mutate_json_record(self, json_record):
        """Override it to convert fields of `json_record` to needed types.

        Default implementation converts `datetime` to string in ISO8601 format.

        """
        for attr_name in json_record:
            attr = json_record[attr_name]
            if isinstance(attr, datetime):
                json_record[attr_name] = attr.isoformat()
        return json_record

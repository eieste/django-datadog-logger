# Django - Datadog Log Handler (via JSON)

This Django Module can you help to send Logs directly to Datadog without a
dd-agent. It uses the Datadog https log API.

Configure your django logging as follow:

```python3
LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
      "datadogjson": {
          "()": "django_datadog_logger.formatter.DatadogJsonFormatter"
      }
  },
  "handlers": {
    "datadog": {
      "class": "django_datadog_logger.handlers.DatadogHandler",
      "host": "http-intake.logs.datadoghq.eu",      # or http-intake.logs.datadoghq.com 
      "api_key": os.environ.get("DD_API_KEY"),      # Your datadog API KEY
      "parameters": {
          "ddtags": "environment:demo",
          "ddservice": "<YourApplicationName>",
            # Add here your additional parameters (Only key value pairs allowed)
      },
      "formatter": "datadogjson"
    },
  },
  "loggers": {
        "": {
            "handlers": ["datadog"],
            "level": "DEBUG"
        },
        "django": {
            "handlers": ["datadog"],
            "level": "WARNING"
        }
    }
}


```



## Miscellaneous
The JSON Formatter originates from the project:
>    https://github.com/marselester/json-log-formatter
>    Published under MIT License
>    install the Orginal via: pip3 install json-log-formatter

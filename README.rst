FM Slack Service
================

|circle| |coveralls|

This application posts the currently playing track into a Slack Channel.

Configuration
-------------

The application takes several configurable options which can also be defined
as environment variables:

* ``--log-level / -l / FM_SLACK_LOG_LEVEL``: Verbosity level of logging
* ``--redis-uri / -r /FM_SLACK_REDIS_URI`` - The Redis server url, e.g: ``Redis://host:port/``
* ``--redis-channel / -c / FM_SLACK_REDIS_CHANNEL`` - The channel to listen for / publish events
* ``--slack-webhook-url / -s / FM_SLACK_SLACK_WEBHOOK_URL`` - The Slack API Webhook
* ``--api-url / -a / FM_SLACK_API_URL`` - The API root endpoint

.. |circle| image:: https://img.shields.io/circleci/project/thisissoon/FM-Slack/master.svg?style=flat
    :target: https://circleci.com/gh/thisissoon/FM-Slack/tree/master

.. |coveralls| image:: https://img.shields.io/coveralls/thisissoon/FM-Slack/master.svg?style=flat
  :target: https://coveralls.io/r/thisissoon/FM-Slack?branch=master

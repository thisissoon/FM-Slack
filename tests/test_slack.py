#!/usr/bin/env python
# encoding: utf-8

"""
tests.test_slack
================

Tests for the Slack integration
"""

import json
import mock
import unittest
import requests

from fmslack.cli import query_api, slack_post


class BaseTestCase(unittest.TestCase):

    def setUp(self):

        # Requests patcher
        requests_patcher = mock.patch(
            'fmslack.cli.requests')
        self.requests = requests_patcher.start()
        self.addCleanup(requests_patcher.stop)

        # Logger patcher
        logger_patcher = mock.patch(
            'fmslack.cli.logger')
        self.logger = logger_patcher.start()
        self.addCleanup(logger_patcher.stop)


class TestQueryApi(BaseTestCase):

    def test_tracks_request(self):

        get = mock.MagicMock(status_code=200, data={'name': 'some name'})
        self.requests.get.return_value = get
        query_api('http://api.thisissoon.fm', 'uri')

        self.requests.get.assert_called_once_with(
            'http://api.thisissoon.fm/tracks/uri',
            verify=False)

    def test_tracks_status_error(self):

        get = mock.MagicMock(status_code=404)
        self.requests.get.return_value = get
        query_api('http://api.thisissoon.fm', 'uri')

        self.logger.error.assert_called_once_with(
            'API returned invalid status code 404')

    def test_tracks_request_error(self):

        self.requests.get.side_effect = requests.exceptions.RequestException()
        self.assertRaises(
            requests.exceptions.RequestException,
            query_api,
            'http://api.thisissoon.fm',
            'spotify_uri')


class TestSlackPost(BaseTestCase):

    track = {
        'name': 'track name',
        'artists': [{'name': 'artist 1'}, {'name': 'artist 2'}],
        'album': 'album name',
        'image': 'http://albumimage.url'
    }

    def test_slack_post(self):
        post = mock.MagicMock(status_code=200)
        self.requests.post.return_value = post

        slack_post(
            'http://slack.com',
            self.track['name'],
            self.track['artists'],
            self.track['album'],
            self.track['image'])

        assert self.requests.post.call_count == 1

    def test_mutliple_artists_concatinated(self):
        post = mock.MagicMock(status_code=200)
        self.requests.post.return_value = post

        slack_post(
            'http://slack.com',
            self.track['name'],
            self.track['artists'],
            self.track['album'],
            self.track['image'])

        text = json.loads(self.requests.post.call_args[1]['data'])['text']
        expected = u'Now playing: *artist 1 & artist 2 - album name: track name*'

        self.requests.post.assert_called_once()
        assert text == expected

    def test_slack_post_status_error(self):

        post = mock.MagicMock(status_code=401)
        self.requests.post.return_value = post

        slack_post(
            'http://slack.com',
            self.track['name'],
            self.track['artists'],
            self.track['album'],
            self.track['image'])

        self.logger.error.assert_called_once_with('Slack returned invalid status code 401')

    def test_slack_post_request_error(self):

        self.requests.post.side_effect = requests.exceptions.RequestException()
        self.assertRaises(
            requests.exceptions.RequestException,
            slack_post,
            'http://slack.com',
            self.track['name'],
            self.track['artists'],
            self.track['album'],
            self.track['image'])

    def test_unicode(self):
        post = mock.MagicMock(status_code=200)
        self.requests.post.return_value = post
        self.track['name'] = u'Track name with some funky chars çö'

        slack_post(
            'http://slack.com',
            self.track['name'],
            self.track['artists'],
            self.track['album'],
            self.track['image'])

        text = json.loads(self.requests.post.call_args[1]['data'])['text']
        expected = u'Now playing: *artist 1 & artist 2 - album name: Track name with some funky chars \xe7\xf6*'

        self.requests.post.assert_called_once()
        assert text == expected

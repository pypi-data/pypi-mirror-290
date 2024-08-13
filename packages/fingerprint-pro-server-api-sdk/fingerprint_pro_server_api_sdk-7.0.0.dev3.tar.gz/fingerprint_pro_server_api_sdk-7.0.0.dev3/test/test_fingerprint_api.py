# coding: utf-8

"""
    Fingerprint Pro Server API

    Fingerprint Pro Server API allows you to get information about visitors and about individual events in a server environment. This API can be used for data exports, decision-making, and data analysis scenarios.  # noqa: E501

    OpenAPI spec version: 3
    Contact: support@fingerprint.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import io
import unittest

import urllib3

from fingerprint_pro_server_api_sdk import (Configuration, TooManyRequestsResponse, ErrorVisits403,
                                            ErrorCommon403Response, ErrorEvent404Response, ErrorVisitor400Response,
                                            ErrorVisitor404Response, ErrorCommon429Response, EventUpdateRequest,
                                            ErrorUpdateEvent400Response, ErrorUpdateEvent409Response)
from fingerprint_pro_server_api_sdk.api.fingerprint_api import FingerprintApi  # noqa: E501
from fingerprint_pro_server_api_sdk.rest import KnownApiException, ApiException
from urllib.parse import urlencode

API_KEY = 'private_key'

VERSION = '7.0.0.dev3'


class MockPoolManager(object):
    def __init__(self, tc):
        self._tc = tc
        self._reqs = []

    def expect_request(self, *args, **kwargs):
        self._reqs.append((args, kwargs))

    @staticmethod
    def get_mock_from_path(path):
        return path.split('/')[-1]

    def request(self, *args, **kwargs):
        self._tc.assertTrue(len(self._reqs) > 0)
        r = self._reqs.pop(0)
        status = 200
        if r[1].get('status') is not None:
            status = r[1].get('status')
            r[1].pop('status')

        if r[1].get('method') != 'GET':
            request_path = r[0][1].split('?')[0]
        else:
            request_path = r[0][1]

        self._tc.maxDiff = None
        self._tc.assertEqual(r[0], args)
        self._tc.assertEqual(r[1], kwargs)

        # TODO Add support for more complex paths?
        mock_file_by_first_argument = MockPoolManager.get_mock_from_path(request_path)

        if mock_file_by_first_argument == 'bad_text_data':
            return urllib3.HTTPResponse(status=200, body='really bad data')
        if mock_file_by_first_argument == 'bad_json_data':
            return urllib3.HTTPResponse(status=200, body='{}')
        if mock_file_by_first_argument == 'empty_event_answer':
            return urllib3.HTTPResponse(status=200, body='{"products": {}}')
        if mock_file_by_first_argument == 'delete_visitor':
            return urllib3.HTTPResponse(status=200, body='OK')
        if mock_file_by_first_argument == 'update_event':
            return urllib3.HTTPResponse(status=200, body='OK')
        try:
            with io.open('./test/mocks/' + mock_file_by_first_argument, 'r', encoding='utf-8') as mock_file:
                answer_mock = mock_file.read()
                mock_file.close()
            headers = {}
            if mock_file_by_first_argument == 'get_visits_429_too_many_requests_error.json':
                headers.update({'Retry-After': '4'})

            return urllib3.HTTPResponse(status=status, body=answer_mock, headers=headers)
        except IOError as e:
            print(e)
            return urllib3.HTTPResponse(status=200, body='{"visitorId": "%s", "visits": []}' % mock_file_by_first_argument)
            pass


class TestFingerprintApi(unittest.TestCase):
    """FingerprintApi unit test stubs"""

    def setUp(self):
        configuration = Configuration(api_key=API_KEY, region="us")
        self.api = FingerprintApi(configuration)  # noqa: E501
        self.integration_info = ('ii', 'fingerprint-pro-server-python-sdk/%s' % VERSION)
        self.request_headers = {
            'Content-Type': 'application/json',
            'Auth-API-Key': 'private_key',
            'Accept': 'application/json',
            'User-Agent': 'Swagger-Codegen/%s/python' % VERSION
        }

    def tearDown(self):
        del self.api
        pass

    @staticmethod
    def get_visitors_path(visitor_id, region='us'):
        domain = {
            "us": "api.fpjs.io",
            "eu": "eu.api.fpjs.io",
            "ap": "ap.api.fpjs.io",
        }.get(region, "api.fpjs.io")
        return 'https://%s/visitors/%s' % (domain, visitor_id)

    @staticmethod
    def get_events_path(request_id, region='us'):
        domain = {
            "us": "api.fpjs.io",
            "eu": "eu.api.fpjs.io",
            "ap": "ap.api.fpjs.io",
        }.get(region, "api.fpjs.io")
        return 'https://%s/events/%s' % (domain, request_id)

    def test_get_visits_correct_data(self):
        """Test checks correct code run result in default scenario"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file1 = 'get_visits_200_limit_1.json'
        mock_file2 = 'get_visits_200_limit_500.json'
        mock_file3 = 'get_visits_200_limit_500.json'
        mock_file4 = 'get_visits_200_limit_500.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file1),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file2),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file3),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file4),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        self.api.get_visits(mock_file1)
        self.api.get_visits(mock_file2)

    def test_get_visits_error_403(self):
        """Test checks correct code run result in case of 403 error for get_visits method"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file = 'get_visits_403_error.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None, status=403)
        with self.assertRaises(KnownApiException) as context:
            self.api.get_visits(mock_file)
        self.assertEqual(context.exception.status, 403)
        structured_error = context.exception.structured_error
        self.assertIsInstance(context.exception.structured_error, ErrorVisits403)

    def test_get_visits_error_429(self):
        """Test checks correct code run result in case of 429 error for get_visits method"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file = 'get_visits_429_too_many_requests_error.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None, status=429)
        with self.assertRaises(KnownApiException) as context:
            self.api.get_visits(mock_file)
        self.assertEqual(context.exception.status, 429)
        self.assertIsInstance(context.exception.structured_error, TooManyRequestsResponse)
        self.assertEqual(context.exception.structured_error.retry_after, 4)

    def test_get_visits_error_429_empty_retry_after(self):
        """Test checks retry after value in exception in case of 429 error for get_visits method"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file = 'get_visits_429_too_many_requests_error_empty_header.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None, status=429)
        with self.assertRaises(KnownApiException) as context:
            self.api.get_visits(mock_file)
        self.assertEqual(context.exception.status, 429)
        self.assertIsInstance(context.exception.structured_error, TooManyRequestsResponse)
        self.assertEqual(context.exception.structured_error.retry_after, 1)

    def test_get_event_correct_data(self):
        """Test checks correct code run result in default scenario"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file1 = 'get_event_200.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file1),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)

        self.api.get_event(mock_file1)

    def test_get_event_errors_200(self):
        """Test checks correct code run result in scenario of arrors in BotD or identification API"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file_botd_fail = 'get_event_200_botd_failed_error.json'
        mock_file_botd_429 = 'get_event_200_botd_too_many_requests_error.json'
        mock_file_identification_fail = 'get_event_200_identification_failed_error.json'
        mock_file_identification_429 = 'get_event_200_identification_too_many_requests_error.json'
        mock_file_all_errors = 'get_event_200_all_errors.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file_botd_fail),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file_botd_429),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET',
                                 TestFingerprintApi.get_events_path(request_id=mock_file_identification_fail),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET',
                                 TestFingerprintApi.get_events_path(request_id=mock_file_identification_429),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file_all_errors),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)

        self.api.get_event(mock_file_botd_fail)
        self.api.get_event(mock_file_botd_429)
        self.api.get_event(mock_file_identification_fail)
        self.api.get_event(mock_file_identification_429)
        self.api.get_event(mock_file_all_errors)

    def test_get_event_error_403(self):
        """Test checks correct code run result in case of 403 error for get_event method"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file = 'get_event_403_error.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None, status=403)
        with self.assertRaises(KnownApiException) as context:
            self.api.get_event(mock_file)
        self.assertEqual(context.exception.status, 403)
        self.assertIsInstance(context.exception.structured_error, ErrorCommon403Response)

    def test_get_event_error_404(self):
        """Test checks correct code run result in case of 404 error for get_event method"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mock_file = 'get_event_404_error.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None, status=404)
        with self.assertRaises(KnownApiException) as context:
            self.api.get_event(mock_file)
        self.assertEqual(context.exception.status, 404)
        self.assertIsInstance(context.exception.structured_error, ErrorEvent404Response)

    def test_get_event_empty_data(self):
        """Test checks correct code running in case of there is no events"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mocked_id = 'empty_event_answer'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mocked_id),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)

        response = self.api.get_event(mocked_id)
        self.assertIsNotNone(response.products)
        for field in response.products.attribute_map.keys():
            value = getattr(response.products, field)
            self.assertIsNone(value, f"Signal '{field}' is not empty")


    def test_get_visits_empty_answer(self):
        """Test checks correct code running in case of there is no visits"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mocked_id = 'empty_answer'
        mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mocked_id),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)
        self.assertEqual(self.api.get_visits(mocked_id).visits, [])

    def test_get_visits_bad_data(self):
        """Test checks exception raising when client receives answer with bad data shape"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        test_cases = [
            ('bad_text_data', 'really bad data'),
            ('bad_json_data', '{}')
        ]
        for (mocked_id, raw_data) in test_cases:
            mock_pool.expect_request('GET', TestFingerprintApi.get_visitors_path(visitor_id=mocked_id),
                                     fields=[self.integration_info], headers=self.request_headers,
                                     preload_content=True, timeout=None)
            with self.assertRaises(ApiException) as context:
                self.api.get_visits(mocked_id)
            self.assertEqual(context.exception.status, 200)
            self.assertIsInstance(context.exception.reason, ValueError)
            self.assertEqual(context.exception.body, raw_data)

    def test_init_with_region(self):
        """Test that link for us region generates correct"""
        regions_list = ["us", "eu", "ap"]
        for region in regions_list:
            configuration = Configuration(api_key=API_KEY, region=region)
            del self.api
            self.api = FingerprintApi(configuration)  # noqa: E501
            mock_pool = MockPoolManager(self)
            self.api.api_client.rest_client.pool_manager = mock_pool
            mocked_id = 'empty_answer'
            mock_pool.expect_request('GET',
                                     TestFingerprintApi.get_visitors_path(visitor_id=mocked_id, region=region),
                                     fields=[self.integration_info], headers=self.request_headers,
                                     preload_content=True, timeout=None)
            self.assertEqual(self.api.get_visits(mocked_id).visits, [])

    def test_delete_visitor_data(self):
        """Test that delete visit method works"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mocked_id = 'delete_visitor'
        mock_pool.expect_request('DELETE',
                                 TestFingerprintApi.get_visitors_path(visitor_id=mocked_id) + '?' + urlencode(
                                     [self.integration_info]),
                                 body='{}', headers=self.request_headers, preload_content=True, timeout=None)
        self.api.delete_visitor_data(mocked_id)

    def test_delete_visitor_data_400_error(self):
        """Test that delete visit method returns 400 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mocks = ['400_error_empty_visitor_id.json', '400_error_incorrect_visitor_id.json']

        for mock_file in mocks:
            mock_pool.expect_request('DELETE',
                                     TestFingerprintApi.get_visitors_path(visitor_id=mock_file) + '?' + urlencode(
                                         [self.integration_info]),
                                     body='{}', headers=self.request_headers, preload_content=True, timeout=None,
                                     status=400)
        for mock_file in mocks:
            with self.assertRaises(KnownApiException) as context:
                self.api.delete_visitor_data(mock_file)
            self.assertEqual(context.exception.status, 400)
            self.assertIsInstance(context.exception.structured_error, ErrorVisitor400Response)

    def test_delete_visitor_data_403_error(self):
        """Test that delete visit method returns 403 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool
        mocks = ['403_error_feature_not_enabled.json',
                 '403_error_token_not_found.json',
                 '403_error_token_required.json',
                 '403_error_wrong_region.json']

        for mock_file in mocks:
            mock_pool.expect_request('DELETE',
                                     TestFingerprintApi.get_visitors_path(visitor_id=mock_file) + '?' + urlencode(
                                         [self.integration_info]),
                                     body='{}', headers=self.request_headers, preload_content=True, timeout=None,
                                     status=403)

        for mock_file in mocks:
            with self.assertRaises(KnownApiException) as context:
                self.api.delete_visitor_data(mock_file)
            self.assertEqual(context.exception.status, 403)
            self.assertIsInstance(context.exception.structured_error, ErrorCommon403Response)

    def test_delete_visitor_data_404_error(self):
        """Test that delete visit method returns 404 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = '404_error_visitor_not_found.json'
        mock_pool.expect_request('DELETE',
                                 TestFingerprintApi.get_visitors_path(visitor_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 body='{}', headers=self.request_headers, preload_content=True, timeout=None,
                                 status=404)

        with self.assertRaises(KnownApiException) as context:
            self.api.delete_visitor_data(mock_file)
        self.assertEqual(context.exception.status, 404)
        self.assertIsInstance(context.exception.structured_error, ErrorVisitor404Response)

    def test_delete_visitor_data_429_error(self):
        """Test that delete visit method returns 429 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = '429_error_too_many_requests.json'
        mock_pool.expect_request('DELETE',
                                 TestFingerprintApi.get_visitors_path(visitor_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 body='{}', headers=self.request_headers, preload_content=True, timeout=None,
                                 status=429)

        with self.assertRaises(KnownApiException) as context:
            self.api.delete_visitor_data(mock_file)
        self.assertEqual(context.exception.status, 429)
        self.assertIsInstance(context.exception.structured_error, ErrorCommon429Response)

    def test_update_event(self):
        """Test that update event method returns 200"""
        test_cases = [
            (EventUpdateRequest(linked_id='qwe'), '{"linkedId": "qwe"}'),
            (EventUpdateRequest(tag={'qwe': 123}), '{"tag": {"qwe": 123}}'),
            (EventUpdateRequest(suspect=False), '{"suspect": false}'),
            (EventUpdateRequest(suspect=True), '{"suspect": true}'),
            (EventUpdateRequest(linked_id='qwe', tag={'qwe': 123}, suspect=False),
             '{"linkedId": "qwe", "tag": {"qwe": 123}, "suspect": false}')
        ]

        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'update_event'

        for (update_body, serialized_body) in test_cases:
            mock_pool.expect_request('PUT',
                                     TestFingerprintApi.get_events_path(request_id=mock_file) + '?' + urlencode(
                                         [self.integration_info]),
                                     headers=self.request_headers, preload_content=True, timeout=None, status=200,
                                     body=serialized_body)

            self.api.update_event(update_body, mock_file)

    def test_update_event_400_error(self):
        """Test that update event method returns 400 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'update_event_400_error.json'
        mock_pool.expect_request('PUT',
                                 TestFingerprintApi.get_events_path(request_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 headers=self.request_headers, preload_content=True, timeout=None, status=400,
                                 body="{}")

        with self.assertRaises(KnownApiException) as context:
            self.api.update_event({}, mock_file)
        self.assertEqual(context.exception.status, 400)
        self.assertIsInstance(context.exception.structured_error, ErrorUpdateEvent400Response)

    def test_update_event_403_error(self):
        """Test that delete visit method returns 403 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'update_event_403_error.json'
        mock_pool.expect_request('PUT',
                                 TestFingerprintApi.get_events_path(request_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 headers=self.request_headers, preload_content=True, timeout=None, status=403,
                                 body="{}")

        with self.assertRaises(KnownApiException) as context:
            self.api.update_event({}, mock_file)
        self.assertEqual(context.exception.status, 403)
        self.assertIsInstance(context.exception.structured_error, ErrorCommon403Response)

    def test_update_event_404_error(self):
        """Test that delete visit method returns 404 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'update_event_404_error.json'
        mock_pool.expect_request('PUT',
                                 TestFingerprintApi.get_events_path(request_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 headers=self.request_headers, preload_content=True, timeout=None, status=404,
                                 body="{}")

        with self.assertRaises(KnownApiException) as context:
            self.api.update_event({}, mock_file)
        self.assertEqual(context.exception.status, 404)
        self.assertIsInstance(context.exception.structured_error, ErrorEvent404Response)

    def test_update_event_409_error(self):
        """Test that delete visit method returns 409 error"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'update_event_409_error.json'
        mock_pool.expect_request('PUT',
                                 TestFingerprintApi.get_events_path(request_id=mock_file) + '?' + urlencode(
                                     [self.integration_info]),
                                 headers=self.request_headers, preload_content=True, timeout=None, status=409,
                                 body="{}")

        with self.assertRaises(KnownApiException) as context:
            self.api.update_event({}, mock_file)
        self.assertEqual(context.exception.status, 409)
        self.assertIsInstance(context.exception.structured_error, ErrorUpdateEvent409Response)

    def test_get_event_wrong_shape(self):
        """Test that get event method returns correct response"""
        mock_pool = MockPoolManager(self)
        self.api.api_client.rest_client.pool_manager = mock_pool

        mock_file = 'get_event_200_wrong_shape.json'
        mock_pool.expect_request('GET', TestFingerprintApi.get_events_path(request_id=mock_file),
                                 fields=[self.integration_info], headers=self.request_headers,
                                 preload_content=True, timeout=None)

        with io.open('./test/mocks/' + mock_file, encoding='utf-8') as raw_file:
            raw_file_data = raw_file.read()
            raw_file.close()

        with self.assertRaises(ApiException) as context:
            self.api.get_event(mock_file)
        self.assertEqual(context.exception.status, 200)
        self.assertIsInstance(context.exception.reason, ValueError)
        self.assertEqual(context.exception.body, raw_file_data)


if __name__ == '__main__':
    unittest.main()

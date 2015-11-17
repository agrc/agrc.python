import unittest
from mock import patch, Mock
import requests
import json
import time
from agrc import ags

responseMock = Mock(spec=requests.Response)
token = 'tokenstring'
expDate = (time.time()*1000)+10000

username = 'hello'
password = 'goodbye'
server = '172.16.17.54'


class AGSAdminTest(unittest.TestCase):
    @patch.object(requests, 'post', return_value=responseMock)
    def setUp(self, mock):
        responseMock.json.return_value = {
            'token': token,
            'expires': expDate
        }
        responseMock.raise_for_status.return_value = None
        self.admin = ags.AGSAdmin(username,
                                  password,
                                  server)

    def tearDown(self):
        self.admin = None
        responseMock.reset_mock()

    def test_mixin_props(self):
        s = self.admin
        assert s.server == server

    def test_requests_token(self):
        assert self.admin.token == token
        assert self.admin.tokenExpireDate == expDate

    @patch.object(requests, 'post', return_value=responseMock)
    def test_getServices_returnsList(self, mock):
        s = self.admin

        servicesJson = json.loads(open('./data/getServices.json', 'r').read())
        responseMock.json.return_value = servicesJson

        services = s.getServices()

        self.assertEqual(len(services), 9)
        self.assertEqual(len(s.services), 9)
        self.assertEqual(s.services[0]['serviceName'], 'DNRLands')

    @patch.object(requests, 'post', return_value=responseMock)
    def test_editService_error_on_bad_prop(self, mock):
        s = self.admin

        serviceJson = json.loads(open('./data/service.json', 'r').read())
        responseMock.json.return_value = serviceJson

        self.assertRaises(Exception, s.editService, 'ServiceName', 'MapServer', 'badPropName', 'value')
        s.editService('ServiceName', 'MapServer', 'clusterName', 'value')

    @patch.object(requests, 'post', return_value=responseMock)
    def test_editService_no_change_needed(self, mock):
        s = self.admin

        serviceJson = json.loads(open('./data/service.json', 'r').read())
        responseMock.json.return_value = serviceJson

        prop = 'clusterName'
        value = 'default'
        returned = s.editService('ServiceName', 'MapServer', prop, value)
        self.assertEquals(returned, s.noChangeMsg.format(prop, value))

    @patch.object(requests, 'post', return_value=responseMock)
    def test_request_mixes_in_additional_data(self, mock):
        url = 'blah'
        self.admin.request(url, {'test': 'value'})

        mock.assert_called_with(url, data={
            'f': 'json',
            'token': self.admin.token,
            'test': 'value'}
        )

    @patch.object(requests, 'post', return_value=responseMock)
    def test_request_gets_new_token_if_needed(self, mock):
        newDate = 1370961193377
        newToken = 'newToken'
        responseMock.json.return_value = {
            'token': newToken,
            'expires': newDate
        }

        self.admin.tokenExpireDate = (time.time()*1000)-10000
        self.admin.request('blah')

        assert self.admin.token == newToken
        assert self.admin.tokenExpireDate == newDate

    def test_checkError(self):
        s = self.admin

        response = {
            'status': 'error',
            'code': 500,
            'messages': ["A JSONObject text must begin with '{' at character 1 of maxInstancesPerNode"]
        }
        self.assertRaises(Exception, s.checkError, response)

if __name__ == '__main__':
    unittest.main()

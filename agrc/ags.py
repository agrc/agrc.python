import requests
import json
from time import time

# urls
baseUrl = r'http://{}:6080/arcgis/admin/'
tokenUrl = r'{}generateToken'.format(baseUrl)
servicesUrl = r'{}services'.format(baseUrl)


class AGSAdmin:
    """
    Provides methods for administering arcgis server
    """
    username = ''
    password = ''
    server = ''
    token = ''
    tokenExpireDate = 0
    payload = None
    services = []
    noChangeMsg = "'{}'' is already set to '{}'. No changes made."

    def __init__(self, username, password, server):
        """
        username: String
        password: String
        server: String
            ip address of the server that you are admining
        """
        self.server = server
        self.username = username
        self.password = password

        self.getToken()

    def getToken(self):
        data = {'username': self.username,
                'password': self.password,
                'client': 'requestip',
                'f': 'json'}
        r = requests.post(tokenUrl.format(self.server), data=data)
        r.raise_for_status()
        r = r.json()
        self.checkError(r)

        self.token = r['token']
        self.tokenExpireDate = r['expires']

    def getServices(self):
        def getServicesForFolder(folder):
            if folder is not None:
                url = servicesUrl.format(self.server) + r'/{}'.format(folder)
            else:
                url = servicesUrl.format(self.server)
            responseJson = self.request(url)
            self.services = self.services + responseJson['services']
            try:
                return responseJson['folders']
            except:
                pass

        for folder in getServicesForFolder(None):
            getServicesForFolder(folder)

        return self.services

    def editService(self, service, type, property, value):
        url = '{}/{}.{}'.format(servicesUrl.format(self.server),
                                service,
                                type)
        serviceJson = self.request(url)

        if property not in serviceJson.keys():
            raise Exception('Property: {} not found!'.format(property))

        if serviceJson[property] == value:
            return self.noChangeMsg.format(property, value)

        serviceJson[property] = value

        return self.request('{}/edit'.format(url), {'service': json.dumps(serviceJson)})

    def getServiceProperty(self, service, type, property):
        url = '{}/{}.{}'.format(servicesUrl.format(self.server),
                                service,
                                type)
        serviceJson = self.request(url)

        if property not in serviceJson.keys():
            raise Exception('Property: {} not found!'.format(property))

        return serviceJson[property]

    def stopService(self, service, type):
        return self._commandService(service, type, 'stop')

    def startService(self, service, type):
        return self._commandService(service, type, 'start')

    def deleteService(self, service, type):
        return self._commandService(service, type, 'delete')

    def getStatus(self, service, type):
        return self._commandService(service, type, 'status')

    def _commandService(self, service, type, command):
        url = '{}/{}.{}/{}'.format(servicesUrl.format(self.server),
                                   service,
                                   type,
                                   command)
        return self.request(url)

    def request(self, url, additionalData={}):
        # check to make sure that token isn't expired
        if self.tokenExpireDate <= time()*1000:
            self.getToken()

        data = dict(additionalData.items() + {'f': 'json', 'token': self.token}.items())
        r = requests.post(url, data=data)
        r.raise_for_status()
        self.checkError(r.json())
        return r.json()

    def checkError(self, jsonResponse):
        if 'status' in jsonResponse.keys() and jsonResponse['status'] == 'error':
            raise Exception('; '.join(jsonResponse['messages']))

    def startAllServices(self):
        if len(self.services) == 0:
            self.getServices()

        for s in self.services:
            serv = s['folderName'] + '//' + s['serviceName']
            print 'starting {}'.format(serv)
            self.startService(serv, s['type'])

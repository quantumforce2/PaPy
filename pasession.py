import requests
import base64

""" 
Modules contain login and session classes 

"""
class PAlogin:
    """
    Initiate a TM1 login

    - Capture user information along with host information
    - Creates a base64 encoded cam token
    - Creates an object that can be passed into PASession class

    Attributes:
        user (str): TM1 user id
        password (str): TM1 password
        CAM_namespace (str): CAM namespace
        admin_host (str): tm1 admin host name
        http_port (int): http port no set up in Tm1s.cfg file
        token (str): base64 encoded token
    """
    def __init__(self, user, password, CAM_namespace, admin_host, http_port, token=None):
        self.user = user
        self.password = password
        self.CAM_namespace = CAM_namespace
        self.admin_host = admin_host
        self.http_port = http_port
        self.token = token

    @classmethod
    def login_using_cam(cls, user, password, cam_namespace, admin_host, http_port):
        cam_token = 'CAMNamespace ' + base64.b64encode(
         str.encode("{}:{}:{}".format(user, password, cam_namespace))).decode("ascii")
        login = cls(user, password, cam_namespace, admin_host, http_port, cam_token)
        return login


class PASession:
    """
    Create a TM1 login session

    - Capture login information
    - Creates a header for tm1 rest api request
    - executes http requests methods

    Attributes:
        login (PAlogin): TM1 login object
    """
    __headers = {
      'Connection': 'keep-alive',
      'User-Agent': 'papy',
      'Content-Type': 'application/json; odata.streaming=true; charset=utf-8',
      'Accept': 'application/json;odata.metadata=none',
      'Authorization': ''
    }
    __admin_host = ''
    __http_port = 0
    __url_base = ''
    __protocol  = "https://"

    def __init__(self, login):
        self.login = login
        self.__headers['Authorization'] = login.token
        self.__admin_host = login.admin_host
        self.__http_port = login.http_port
        self.__url_base = self.__protocol + self.__admin_host + ":" + str(self.__http_port) + "/api/v1/"
        self.sess = requests.session()
        self.verify = False

    def GET(self, url, data = ''):
        url = self.__url_base + url
        response = self.sess.get(url=url, headers=self.__headers, data=data, verify=self.verify)
        return response

    def POST(self, url, data = ''):
        url = self.__url_base + url
        response = self.sess.post(url=url, headers=self.__headers, data=data, verify=self.verify)
        return response

    def PATCH(self, url, data = ''):
        url = self.__url_base + url
        response = self.sess.patch(url=url, headers=self.__headers, data=data, verify=self.verify)
        return response

    def DELETE(self, url, data = ''):
        url = self.__url_base + url
        response = self.sess.delete(url=url, headers=self.__headers, data=data, verify=self.verify)
        return response
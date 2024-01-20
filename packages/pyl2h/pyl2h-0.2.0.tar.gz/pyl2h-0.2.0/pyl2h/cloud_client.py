"""Optional (but helpful) client to communicate with Link2Homes cloud"""

import collections
import base64
from urllib.parse import urlencode, unquote
import requests

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1, MD5
from Crypto.PublicKey import RSA

from .const import LOGIN_URL, DEVICE_LIST_URL, USER_AGENT, ACCEPT_LANGUAGE

headers = {
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Accept-Language": ACCEPT_LANGUAGE,
            "Content-Type": "application/x-www-form-urlencoded"
        }

class CloudClient:
    """Cloud client implementation"""

    def __init__(self) -> None:
        self.session = {}

    def hash_password(self, password):
        """Generate MD5 Hash for user Password"""
        md5 = MD5.new()
        md5.update(password.encode("utf-8"))
        return md5.hexdigest().upper()

    def login(self, username, password):
        """Login to the cloud and cache the session within the client instance"""
        data = {
            "appName": "Link2Home",
            "appType": "2",
            "appVersion": "1.1.1",
            "password": self.hash_password(password),
            "phoneSysVersion": "iOS 17.1.2",
            "phoneType": "iPad13,8",
            "username": username,
        }

        data["sign"] = self.get_sign(data)
        print(f'Request: {data}')

        r = requests.post(LOGIN_URL, params=data, headers=headers, timeout=120)
        body = r.json()
        print(f'Status: {r.status_code}, Body: {body}')

        if body['success'] and "data" in body:
            print("We are logged in!")
            self.session = body["data"]
        else:
            print("Login failed!")
            self.session = None

    def list_devices(self):
        """List devices connected to the user account"""
        if self.session is None:
            return []
        print("Getting registered devices...")
        data = {
            "token": self.session["token"]
        }

        data["sign"] = self.get_sign(data)
        r = requests.get(DEVICE_LIST_URL, params=data, timeout=120)
        body = r.json()

        if not body['success'] or not "data" in body:
            raise ValueError("Did not get a processable device listing from Link2Home Cloud")

        devices = []
        for rec in body['data']:
            dev = {
                'mac': rec['macAddress'],
                'companyCode': rec['companyCode'],
                'deviceType': rec['deviceType'], 
                'authCode': rec['authCode'], 
                'name': rec['deviceName'], 
                'image': rec['imageName'], 
                'orderNumber': rec['orderNumber'], 
                'lastOperation': rec['lastOperation'], 
                'cityId': rec['cityId'], 
                'zoneId': rec['zoneId'], 
                'gmtOffset': rec['gmtOffset'], 
                'longtitude': rec['longtitude'], 
                'latitude': rec['latitude'], 
                'version': rec['version'], 
                'groupId': rec['groupId'], 
                'gColorType': rec['gColorType'], 
                'online': rec['online']
            }

            devices.append(dev)

        return devices

    def get_sign(self, data):
        """Calculate SHA-1 Signature for a given request"""
        sorted_data = collections.OrderedDict(sorted(data.items()))
        query_string = unquote(urlencode(sorted_data)).encode("utf-8")

        query_string = ""
        for key in data:
            query_string = query_string + key + "=" + data[key] + "&"
        query_string = query_string[:-1].encode("utf-8")

        print(f'Query String: {query_string}')

        with open("pyl2h/private_key.pem", encoding="utf-8") as key_file:
            key_data = key_file.read()
            key = RSA.import_key(key_data)
            #key = rsa.PrivateKey.load_pkcs1(key_data)

        hash_value = SHA1.new(query_string)
        signer = pkcs1_15.PKCS115_SigScheme(key)
        signature = signer.sign(hash_value)
        #signature = rsa.sign(query_string, key, 'SHA-1')
        encoded_sig = base64.b64encode(signature).decode('utf-8')
        return encoded_sig
    
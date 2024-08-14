# coding: utf-8
import requests
import json

class Document(object):
    content = None

    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)

    def serialize(self):
        """
        :return: A document serialized in JSON
        :rtype: dict
        """
        return 'data:application/pdf;base64,' + self.content


class Base64Document(Document):
    templateType = "base64"

    def __init__(self, content, **attrs):
        super(Base64Document, self).__init__(**attrs)
        self.content = content

    def serialize(self):
        result = super(Base64Document, self).serialize()
        return result

class ConFirmaClient(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.url = 'https://app.confirma.es'
        self.session = requests.Session()
        self.session.auth = (user, password)

    def create_signature(self, canal, tipo, tipofirma, datos, cabecera):
        """
        :param canal: canal string
        :type canal: string
        :param tipo: string
        :type tipo: tipo de peticion
        :param tipofirma: string
        :type tipofirma: Simple o Multi
        :param datos: Dictionary
        :type datos: Dictionary of optional parameters
        :return: A dictionary with signature information
        :rtype: dict
        """
        url = '/'.join([self.url, 'ws_API.php'])
        data = {
            "canal": canal,
            "tipo": tipo,
            "tipofirma": tipofirma,
            "datos": datos
        }
        data = json.dumps(data)
        return self.session.post(
            url, data=data, headers=cabecera
        ).json()

    def check_signature_status(self, cabecera, encriptado):
        url = '/'.join([self.url, 'ws_API_status.php'])
        data = {
            'encriptado': encriptado,
        }
        data = json.dumps(data)
        return self.session.get(
            url, data=data, headers=cabecera
        ).json()

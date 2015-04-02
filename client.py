import json
import urllib.request
import urllib.parse
import urllib.error


class ServerError(Exception):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = None

class Server:
    def __init__(self, base_url):
        self.base = base_url

    def query(self, url, parameters=None ):
         """Charge l'url demandée. Si aucun paramètre n'est spécifié, une requête
            HTTP GET est envoyée. Si des paramètres sont présents, ils sont encodés
            en JSON, et une requête POST est envoyée.

            La méthode préconisée pour envoyer des paramètres consiste à les stocker
            dans un dictionnaire. Ceci permet de nommer les champs. Par exemple :

            # sans paramètres
            >>> server = Server("http://pac.bouillaguet.info/TP1/")
            >>> response = server.query('client-demo')
            >>> print(response)
            Je n'ai pas reçu de paramètres

            #    avec paramètres
            >>> parameters = {'login': 'toto', 'id': 1337}
            >>> response = server.query('client-demo', parameters)
            >>> print(response)
            Dans les paramètres j'ai trouvé :
            *) ``login'' : ``toto''
            *) ``id'' : ``1337''
            <BLANKLINE>
         """
         url = self.base + url
         try:
            request = urllib.request.Request(url)
            data = None
            if parameters is not None:
                data = json.dumps(parameters).encode()
                request.add_header('Content-type', 'application/json')
            with urllib.request.urlopen(request, data) as connexion:
                result = connexion.read().decode()
                if connexion.info()['Content-Type'] == "application/json":
                    result = json.loads(result)
            return result
         except urllib.error.HTTPError as e:
             raise ServerError(e.code, e.read().decode()) from None


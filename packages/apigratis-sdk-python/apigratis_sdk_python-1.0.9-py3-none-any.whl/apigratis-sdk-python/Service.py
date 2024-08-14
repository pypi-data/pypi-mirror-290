import requests
import json

class Service:
    server = "https://gateway.apibrasil.io/api/v2/"

    def __init__(self):
        pass

    def request(self, service, dados):
        try:
            # Carregar e validar dados
            data = json.loads(dados)

            if 'credentials' not in data:
                return {'error': 'Invalid request, missing credentials.'}
            if 'body' not in data:
                return {'error': 'Invalid request, missing body.'}

            credentials = data['credentials']
            payload = json.dumps(data['body'])
            url = self.server + service  # Ajustado para não adicionar o 'action' diretamente na URL

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + credentials['BearerToken'],
                'DeviceToken': credentials['DeviceToken'],
                'User-Agent': 'APIBRASIL/PYTHON-SDK'
            }

            response = requests.post(url, headers=headers, data=payload, allow_redirects=False, stream=True)

            # Verificar se a resposta é JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'error': 'Failed to parse JSON response'}

        except Exception as e:
            return {'error': str(e)}

    def whatsapp(self, dados):
        return self.request('whatsapp', dados)

    def vehicles(self, dados):
        return self.request('vehicles', dados)

    def correios(self, dados):
        return self.request('correios', dados)

    def cep(self, dados):
        return self.request('cep', dados)

    def cnpj(self, dados):
        return self.request('dados/cnpj', dados)

    def cpf(self, dados):
        return self.request('dados/cpf', dados)

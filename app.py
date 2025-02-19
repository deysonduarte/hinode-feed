from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def feed():
    xml_url = "https://www.hinode.com.br/XMLData/consultores.xml"

    try:
        response = requests.get(xml_url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code == 200:
            return Response(response.content, mimetype='application/xml')
        else:
            return f"Erro ao buscar XML: {response.status_code}", 500
    except Exception as e:
        return f"Erro inesperado: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)




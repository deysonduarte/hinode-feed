from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def feed():
    return Response("<xml><message>O site está funcionando, mas o XML não carregou.</message></xml>", mimetype='application/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)



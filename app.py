from flask import Flask, Response, render_template_string
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

HINODE_XML_URL = "https://www.hinode.com.br/XMLData/consultores.xml"

@app.route('/')
def home():
    products = get_products()
    return render_template_string("""
    <html>
    <head><title>Produtos Hinode</title></head>
    <body>
        <h1>Lista de Produtos</h1>
        <ul>
        {% for product in products %}
            <li>{{ product['title'] }} - R$ {{ product['price'] }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """, products=products)

@app.route('/feed.xml')
def feed():
    products = get_products()
    xml_content = generate_feed_xml(products)
    return Response(xml_content, mimetype='application/xml')

def get_products():
    response = requests.get(HINODE_XML_URL)
    root = ET.fromstring(response.content)
    products = []

    for item in root.findall(".//produto"):
        products.append({
            "id": item.find("id").text if item.find("id") is not None else "",
            "title": item.find("nome").text if item.find("nome") is not None else "",
            "description": item.find("descricao").text if item.find("descricao") is not None else "",
            "price": item.find("preco").text if item.find("preco") is not None else "",
            "availability": "in_stock",
            "image_link": item.find("imagem").text if item.find("imagem") is not None else ""
        })

    return products

def generate_feed_xml(products):
    xml_feed = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
    <channel>
        <title>Feed de Produtos Hinode</title>
        <link>https://seudominio.com</link>
        <description>Lista de produtos da Hinode</description>
    """

    for product in products:
        xml_feed += f"""
        <item>
            <g:id>{product['id']}</g:id>
            <title>{product['title']}</title>
            <description>{product['description']}</description>
            <g:price>{product['price']} BRL</g:price>
            <g:availability>{product['availability']}</g:availability>
            <g:image_link>{product['image_link']}</g:image_link>
        </item>
        """

    xml_feed += "</channel></rss>"
    return xml_feed

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
  adicionando app.py

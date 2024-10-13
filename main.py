from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

# Definir la clase Noticia
class Noticia:
    def __init__(self, titulo, link, img, categoria, descripcion):
        self.titulo = titulo
        self.link = link
        self.img = img
        self.categoria = categoria
        self.descripcion = descripcion

    def to_dict(self):
        return {
            'titulo': self.titulo,
            'link': self.link,
            'img': self.img,
            'categoria': self.categoria,
            'descripcion': self.descripcion
        }

# Crear la instancia de Flask
app = Flask(__name__)

@app.route('/api/noticias', methods=['GET'])
def obtener_noticias():
    URL = 'https://www.abc.com.py/'
    response = requests.get(URL)

    if response.status_code == 200:
        sopa_html = BeautifulSoup(response.text, 'html.parser')
        contenedor_noticias = sopa_html.find_all('div', class_='section-content')

        # Noticias destacadas
        noticias = contenedor_noticias[1].find_all('div', class_='item-article')
        lista_noticias = []

        for item in noticias:
            titulo = item.find('div', class_='article-title').span.text
            link = 'www.abc.com.py' + item.find('a', class_='article-link')['href']
            img = item.find('div', class_='article-photo').img['src'] if item.find('div', class_='article-photo') else ""
            descripcion = item.find('div', class_='article-intro').p.text if item.find('div', class_='article-intro') else ""
            categoria = item.find('div', class_='article-category').span.text if item.find('div', class_='article-category') else ""

            noticia = Noticia(titulo, link, img, categoria, descripcion)
            lista_noticias.append(noticia.to_dict())

        return jsonify(lista_noticias)

    return jsonify({"error": "No se pudieron obtener las noticias"}), 500

if __name__ == '__main__':
    app.run(debug=True)

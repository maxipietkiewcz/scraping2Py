import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Función para crear la carpeta si no existe
def crear_carpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

# Función para validar la extensión de la imagen
def es_extension_valida(url):
    extensiones_validas = ['.png', '.jpg', '.jpeg', '.webp']
    return any(url.lower().endswith(ext) for ext in extensiones_validas)

# Función para descargar una imagen dada su URL y guardarla en la carpeta especificada
def descargar_imagen(url, carpeta):
    try:
        respuesta = requests.get(url, stream=True)
        respuesta.raise_for_status()
        nombre_imagen = os.path.join(carpeta, os.path.basename(urlparse(url).path))
        with open(nombre_imagen, 'wb') as archivo:
            for chunk in respuesta.iter_content(chunk_size=8192):
                archivo.write(chunk)
        print(f"Imagen descargada: {nombre_imagen}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo descargar la imagen {url}: {e}")

# Función para realizar el scraping
def scraper(url, carpeta='imagenes', limite=20):  # Para desactivar el límite, use "limite=None"
    crear_carpeta(carpeta)
    contador = 0
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        imagenes = soup.find_all('img')
        
        for img in imagenes:
            if limite is not None and contador >= limite:
                break
            src = img.get('src')
            if src:
                # Manejar URLs relativas
                src = urljoin(url, src)
                if es_extension_valida(src):
                    descargar_imagen(src, carpeta)
                    contador += 1
                else:
                    print(f"Extensión no válida, se omite: {src}")
            else:
                print("Etiqueta <img> sin atributo src encontrado, se omite")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la página {url}: {e}")

# URL de la página a scrapear
url = 'https://www.shutterstock.com/es/search/argentina-worldcup?PPC_GOO_LA_IG-621714502729=&cr=c&ds_ag=FF%3DDSA-All+Pages_AU%3DVisitors&ds_agid=58700008023276312&ds_cid=71700000100238870&ds_eid=700000001478290&gad_source=1&gclid=CjwKCAjw9cCyBhBzEiwAJTUWNQtUjvpOc3a0Auwn9UaGWajB5qEL1yXFfiz_9wgNohZe6ukdl3zqMhoCObcQAvD_BwE&gclsrc=aw.ds&kw=&utm_campaign=CO%3DLatam_LG%3DES_BU%3DIMG_AD%3DDSA_TS%3Dlggeneric_RG%3DAMER_AB%3DACQ_CH%3DSEM_OG%3DCONV_PB%3DGoogle&utm_medium=cpc&utm_source=GOOGLE'
scraper(url, limite=20)

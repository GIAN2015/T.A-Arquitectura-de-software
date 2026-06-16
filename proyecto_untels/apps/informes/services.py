from docx import Document
import io

def leer_archivo(archivo) -> str:
    contenido = archivo.read()
    doc = Document(io.BytesIO(contenido))
    return extraer_contenido(doc)

def extraer_contenido(doc) -> str:
    parrafos = []
    for para in doc.paragraphs:
        texto = para.text.strip()
        if texto:
            parrafos.append(texto)
    return '\n'.join(parrafos)

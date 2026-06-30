from apps.informes.file_readers import build_file_reader

def leer_archivo(archivo) -> str:
    return build_file_reader(archivo.name).read(archivo)

def extraer_contenido(doc) -> str:
    parrafos = []
    for para in doc.paragraphs:
        texto = para.text.strip()
        if texto:
            parrafos.append(texto)
    return '\n'.join(parrafos)

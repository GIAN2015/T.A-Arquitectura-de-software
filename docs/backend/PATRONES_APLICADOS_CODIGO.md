# Patrones Aplicados en Código

## Template Method

Se aplicó en `backend/apps/informes/file_readers.py`.

- `BaseFileReader.read()` define el flujo común:
  - leer bytes
  - parsear contenido
  - normalizar texto
- `DocxFileReader` implementa la lectura de `.docx`
- `PdfFileReader` implementa la lectura de `.pdf`
- `build_file_reader()` selecciona el lector concreto

Esto permite soportar varios formatos sin duplicar el flujo general.

## State Pattern

Se aplicó en `backend/apps/informes/state.py`.

- cada estado tiene una clase propia
- cada clase define transiciones permitidas
- `Informe.transition_to()` delega la transición al estado actual

Estados cubiertos:

- `enviado`
- `validando`
- `observado`
- `revision_docente`
- `rechazado`
- `aprobado`
- `completado`

Esto evita cambios de estado arbitrarios y deja el flujo más claro.

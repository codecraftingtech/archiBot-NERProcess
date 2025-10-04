# archivBot-NERProcess

NER Process

## API de Reconocimiento de Entidades (NER)

Esta API en Python utiliza FastAPI y spaCy con el modelo `es_core_news_sm`
para extraer entidades nombradas de un texto en español.

### Requisitos

1. Python 3.9 o superior (macOS, Windows o Linux).
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecutar la API

Iniciar el servidor con:

```bash
uvicorn archivBot-NERProcess:app --host 0.0.0.0 --port 8000
```

### Probar con cURL

```bash
curl -X POST "http://localhost:8000/ner" -H "Content-Type: application/json" -d '{"text": "Barack Obama nació en Estados Unidos"}'

curl -X POST "http://localhost:8000/ner" -H "Content-Type: application/json" -d '{"text": "El siguiente año en el 2026 me voy a comprar un AUDI en su modelo camioneta"}'

curl -X POST "http://localhost:8000/ner" -H "Content-Type: application/json" -d '{"text": "El señor Marco Quispe se compromete a pagar los primeros días de febrero el monto de 10,000 soles al contado."}'
```

El comando devolverá un JSON con las entidades reconocidas.
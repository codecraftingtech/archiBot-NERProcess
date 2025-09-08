# -*- coding: utf-8 -*-
"""Aplicación de reconocimiento de entidades nombradas (NER) en español.

Esta API utiliza FastAPI y la librería de procesamiento de lenguaje natural
spaCy con el modelo ``es_core_news_sm`` para identificar entidades en un texto.
Funciona en macOS, Windows y Linux.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal
import spacy
from pathlib import Path

# Cargamos el modelo de spaCy para español una única vez al iniciar la app.
# Esto evita recargarlo en cada petición y mejora el rendimiento.
nlp = spacy.load("es_core_news_sm")
nlp_custom = spacy.load("es_model_date_money_es")


# Creamos la instancia de la aplicación FastAPI.
app = FastAPI(title="API NER en español")


class Texto(BaseModel):
    """Estructura de los datos de entrada.

    Espera un JSON con una clave ``text`` que contenga el texto a analizar.
    """

    text: str

class EntityOut(BaseModel):
    text: str
    label: str
    start: int
    end: int
    model: Literal["base", "custom"]

class NerResponse(BaseModel):
    entities: List[EntityOut]  

def ents_to_dicts(doc, model: Literal["base", "custom"]):
    return [
        {"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char, "model": model}
        for e in doc.ents
    ]      

@app.post("/ner")
def obtener_entidades(data: Texto):
    """Extrae las entidades nombradas del texto recibido.

    Args:
        data (Texto): Objeto con el texto a analizar.

    Returns:
        dict: Diccionario con una lista de entidades encontradas.
    """

    # Procesamos el texto con el modelo de spaCy y con el modelo customizado para obtener las entidades.
    ent_base = nlp(data.text)
    ent_custom = nlp_custom(data.text) # tus nuevas entidades (DATE reforzado, MONEY)

    ents = ents_to_dicts(ent_custom, "custom") + ents_to_dicts(ent_base, "base")

    # Quitar duplicados por (start, end, label)
    seen = set()
    uniq = []
    for d in ents:
        key = (d["start"], d["end"], d["label"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(d)

    # Construimos una lista con la información relevante de cada entidad.
    '''entidades = [
        {
            "text": entidad.text,       # Texto exacto de la entidad
            "label": entidad.label_,    # Tipo de entidad (persona, lugar, etc.)
            "start": entidad.start_char, # Posición inicial en el texto
            "end": entidad.end_char      # Posición final en el texto
        }
        for entidad in documento.ents
    ]'''

    # Orden opcional por posición en el texto
    uniq.sort(key=lambda x: (x["start"], x["end"]))
    return {"entities": uniq}

    # Devolvemos las entidades en formato JSON.
    #return {"entities": all_ents}
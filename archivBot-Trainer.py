import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import random

from train_basico import TRAIN_DATA  # tu dataset grande

# ==========================
# Cargar modelo base
# ==========================
print("Empezar el entrenamiento del modelo...")
print("Cargando modelo base...")
nlp = spacy.load("es_core_news_sm")  # partimos de modelo ya entrenado
ner = nlp.get_pipe("ner")

# Añadir nuevas etiquetas si no existen
for label in ["DATE", "MONEY"]:
    ner.add_label(label)

# ==========================
# Congelar otros pipes para no "destruirlos"
# ==========================
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*unaffected_pipes):  # entrenamos solo el NER
    optimizer = nlp.resume_training()
    
    n_iter = 30
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)
            nlp.update(examples, drop=0.3, losses=losses)
        print(f"Iteración {itn} - pérdidas: {losses}")

# ==========================
# Guardar el nuevo modelo
# ==========================
# ...existing code...
output_dir = Path("model_date_money_es")
nlp.to_disk(output_dir)
print(f"Modelo entrenado guardado en {output_dir.resolve()}")

import shutil
shutil.make_archive(str(output_dir), 'zip', root_dir=output_dir)
print(f"Carpeta del modelo comprimida en {output_dir.resolve()}.zip")
import spacy

# Cargar ambos modelos
#nlp_base = spacy.load("es_core_news_sm")
nlp_custom = spacy.load("model_date_money_es")

text = "El pago del señor Jeason Quispe Paño deberá realizarse el 15 de julio de 2025 por un monto de 10,000.00 soles"

#doc_base = nlp_base(text)     # entidades por defecto (PERSON, ORG, LOC, DATE...)
doc_custom = nlp_custom(text) # tus nuevas entidades (DATE reforzado, MONEY)

# Combinar resultados
all_ents = list(doc_custom.ents)

for ent in all_ents:
    print(ent.text, ent.label_)

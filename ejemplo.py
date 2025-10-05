import spacy

# Cargar ambos modelos
#nlp_base = spacy.load("es_core_news_sm")
nlp_custom = spacy.load("model_date_money_es")

#text = "El pago del señor Juan deberá realizarse el 15 de julio de 2025 por un monto de US$ 25,000.00."
text = "El señor Jeason Quispe se compromete a pagar el 15 de febrero el monto de 15000 soles al contado."

#doc_base = nlp_base(text)     # entidades por defecto (PERSON, ORG, LOC, DATE...)
doc_custom = nlp_custom(text) # tus nuevas entidades (DATE reforzado, MONEY)

# Combinar resultados
#all_ents = list(doc_base.ents) + list(doc_custom.ents)
all_ents = list(doc_custom.ents)

for ent in all_ents:
    print(ent.text, ent.label_)

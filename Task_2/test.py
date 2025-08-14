# stanford_pos_nltk.py
import os
import nltk

# Descargas básicas (una sola vez)
nltk.download('punkt')

# Compatibilidad con diferentes versiones de NLTK
try:
    from nltk.tag import StanfordPOSTagger
except Exception:
    from nltk.tag.stanford import StanfordPOSTagger  # fallback para NLTK antiguos

# 1) Rutas a TUS archivos:
STANFORD_JAR = r"Task_2/stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar"           # o 'stanford-postagger.jar'
STANFORD_MODEL = r"/ruta/a/models/english-left3words-distsim.tagger"
# (en algunos paquetes también tienes 'english-bidirectional-distsim.tagger')

# 2) Construir el tagger
tagger = StanfordPOSTagger(
    model_filename=STANFORD_MODEL,
    path_to_jar=STANFORD_JAR,
    encoding="utf8",                      # importante si hay Unicode
    java_options='-Xmx2g'                 # ajusta memoria si quieres
)

def stanford_pos(text: str):
    """Devuelve lista de oraciones, cada una como [(token, PTB_tag), ...]."""
    sents = nltk.sent_tokenize(text)
    tokenized = [nltk.word_tokenize(s) for s in sents]
    tagged_sents = list(tagger.tag_sents(tokenized))  # una llamada por bloque
    return tagged_sents

if __name__ == "__main__":
    sample = "Time flies like an arrow; fruit flies like a banana. The old man the boats."
    for sent in stanford_pos(sample):
        print(sent)
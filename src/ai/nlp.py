from sentence_transformers import SentenceTransformer
print("loading ai model")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_enbedding(text:str):
    if not text:
        return [0.0]* 384

    vector = model.encode(text)
    return vector.tolist()
    
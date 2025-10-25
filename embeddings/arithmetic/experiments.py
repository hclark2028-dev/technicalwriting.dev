from json import load
from os import environ
from sys import exit

from requests import get
from sentence_transformers import SentenceTransformer
# import numpy



class Doc:

    def __init__(self, topic, domain, url, length, embedding):
        self.topic = topic
        self.domain = domain
        self.url = url
        self.length = length
        self.embedding = embedding


def init_docs(model):
    with open("data.json", "r") as f:
        data = load(f)
    tokenizer = model.tokenizer
    docs = []
    max_length = tokenizer.model_max_length
    for item in data:
        url = item["url"]
        response = get(url)
        text = response.text
        length = len(tokenizer.encode(text))
        topic = item["topic"]
        domain = item["domain"]
        if length > max_length:
            exit(f"[ERROR] Document is too large: {topic}, {domain}")
        embedding = model.encode(text)
        doc = Doc(topic, domain, url, length, embedding)
        docs.append(doc)
    return docs


def run_experiment():

    # def create_query(model):
    #     doc = Doc("Writing tests (Playwright Python)", "https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/writing-tests-python.md", model)
    #     return doc.embedding - model.encode("playwright") + model.encode("rust")
 
    environ["TOKENIZERS_PARALLELISM"] = "false"
    model = SentenceTransformer("google/embeddinggemma-300m")
    # query = create_query(model)
    docs = init_docs(model)
    # for doc in docs:
    #     similarity = model.similarity(query, doc.embedding)
    #     # print(doc.description, similarity)


run_experiment()

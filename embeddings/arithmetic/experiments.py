from json import load
from os import environ
from sys import exit

from requests import get
from sentence_transformers import SentenceTransformer


class Doc:

    def __init__(self, topic, domain, url, length, embedding):
        self.topic = topic
        self.domain = domain
        self.url = url
        self.length = length
        self.embedding = embedding
        self.similarity = None


def init_docs(model, task_types):
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
        prompt = "title: {topic} | text: "
        embedding = model.encode(text, prompt=prompt) if task_types else model.encode(text)
        doc = Doc(topic, domain, url, length, embedding)
        docs.append(doc)
    return docs


def create_domain_query(model, task_types):
    url = "https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx"
    response = get(url)
    text = response.text
    if task_types:
        doc = model.encode(text, prompt_name="Retrieval-query")
        supabase = model.encode("supabase", prompt_name="Retrieval-query")
        angular = model.encode("angular", prompt_name="Retrieval-query")
    else:
        doc = model.encode(text)
        supabase = model.encode("supabase")
        angular = model.encode("angular")
    return doc - supabase + angular


def create_topic_query(model, task_types):
    url = "https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx"
    response = get(url)
    text = response.text
    if task_types:
        doc = model.encode(text, prompt_name="Retrieval-query")
        testing = model.encode("testing", prompt_name="Retrieval-query")
        vectors = model.encode("vectors", prompt_name="Retrieval-query")
    else:
        doc = model.encode(text)
        testing = model.encode("testing")
        vectors = model.encode("vectors")
    return doc - testing + vectors


def run_experiments():
    environ["TOKENIZERS_PARALLELISM"] = "false"
    model = SentenceTransformer("google/embeddinggemma-300m")
    for task_types in [True, False]:
        print(f'[INFO] Running "same topic, different domain" experiment with {"customized" if task_types else "default"} task types')
        docs = init_docs(model, task_types)
        query = create_domain_query(model, task_types)
        for doc in docs:
            similarity = model.similarity(query, doc.embedding).item()
            doc.similarity = similarity
        docs.sort(key=lambda doc: doc.similarity, reverse=True)
        print(f'[INFO] Results:')
        for doc in docs:
            print(f'[INFO] "{doc.topic}" ({doc.domain}) => {doc.similarity}')
        print()
        print(f'[INFO] Running "different topic, same domain" experiment with {"customized" if task_types else "default"} task types')
        docs = init_docs(model, task_types)
        query = create_topic_query(model, task_types)
        for doc in docs:
            similarity = model.similarity(query, doc.embedding).item()
            doc.similarity = similarity
        docs.sort(key=lambda doc: doc.similarity, reverse=True)
        print(f'[INFO] Results:')
        for doc in docs:
            print(f'[INFO] "{doc.topic}" ({doc.domain}) => {doc.similarity}')
        print()
    # DEBUG
    for d in init_docs(model, True):
        print(f"* `{d.topic} <{d.url}`_ ({d.domain})")


if __name__ == "__main__":
    run_experiments()

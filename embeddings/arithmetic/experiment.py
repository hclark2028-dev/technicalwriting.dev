from sentence_transformers import SentenceTransformer
import numpy
import requests

def embed(source):
    response = requests.get(source)
    return model.encode(response.text)
  
 
model = SentenceTransformer("google/embeddinggemma-300m")

query_url = "https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/writing-tests-python.md"
playwright_tests = model.encode(requests.get(query_url).text)
playwright = model.encode("playwright")
rust = model.encode("rust")
query = playwright_tests - playwright + rust

docs_urls = [
    "https://raw.githubusercontent.com/rust-lang/book/refs/heads/main/src/ch11-01-writing-tests.md",
    "https://raw.githubusercontent.com/rust-lang/book/refs/heads/main/src/ch13-01-closures.md",
    "https://raw.githubusercontent.com/rust-lang/book/refs/heads/main/src/ch08-01-vectors.md",
    "https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/library-python.md",
    "https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/accessibility-testing-js.md",
    "https://raw.githubusercontent.com/huggingface/transformers/refs/heads/main/docs/source/en/testing.md",
    "https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx",
    "https://raw.githubusercontent.com/pigweed-project/pigweed/refs/heads/main/pw_unit_test/docs.rst",
]
docs = numpy.array([model.encode(requests.get(docs_url).text) for docs_url in docs_urls])

similarities = model.similarity(query, docs)
print(similarities)

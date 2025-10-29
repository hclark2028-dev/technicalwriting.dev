.. _arithmetic:

===================================================
word2vec-style vector arithmetic on docs embeddings
===================================================

`word2vec`_ popularized the idea of representing words as `vectors`_ where
semantically similar words are positioned close to each other in the `vector
space`_. Nowadays these vectors are usually called `embeddings`_. A neat
consequence of the word2vec architecture: adding and subtracting vectors produces
semantically logical results:

  Using a word offset technique where simple algebraic operations are performed
  on the word vectors, it was shown for example that *vector("King")* -
  vector("Man") + vector("Woman")* results in a vector that is closest to the
  vector representation of the word ``Queen``. — `Efficient Estimations of Word
  Representations in Vector Space`_ (the word2vec paper)

Does word2vec-style vector arithmetic work in technical writing contexts?

-----------
Experiments
-----------

word2vec was published in 2013. Embedding models have come a long way since then. word2vec models could only operate on single words. I.e. a vector always represented a single word. Modern embedding models can operate on any text, so long as the text fits in the model's `context window <https://www.ibm.com/think/topics/context-window>`_. I.e. a vector can now represent a word, paragraph, section, document, set of documents, etc.

The following experiments all follow this basic pattern: 

1. Start with the vector of a full document.

2. Subtract the vector of a single word.

3. Add the vector of a single word.

I still don't really grok how it's possible to semantically represent an entire document as a single vector, let alone how adding and subtracting single-word vectors from full-document vectors works. But that will have to be a blog post for another day.

.. _arithmetic-domain:

Same topic, different domain
============================

Starting with the vector for the full text of `Testing Your Database`_ from
the Supabase docs, if I subtract the vector for the word ``supabase``, and
then add the vector for the word ``angular``, the resultant vector should
be close to the concept of "testing in Angular".

.. _arithmetic-topic:

Different topic, same domain
============================

Starting with the vector for the full text of `Testing Your Database`_ from
the Supabase docs, if I subtract the
vector for the word ``testing``, and then add the vector for the word
``vectors``, the resultant vector should be similar to the concept of
"vectors in Supabase".

----------
Task types
----------

From :ref:`previous research <tasks>` I've learned that task types noticeably
affect Gemini Embedding's outputs. EmbeddingGemma (the model I'll be using in
the experiments) also supports tasks types. I'll run both experiments twice:
once with default task types, and again with customized task types.

------------
Verification
------------

There's no way to directly verify that the resultant vectors are
semantically close to the expected concepts. What I can do instead is generate
vectors from the full texts of various docs, and then compare the resultant
vector against the vectors of these various docs using `cosine similarity`_.
For the :ref:`arithmetic-domain` experiment I expect the resultant vector
to be most similar to `Testing`_ or `Testing Services`_ from the Angular docs.
And for the :ref:`arithmetic-topic` experiment I expect the resultant vector to
be most similar to `Vector Columns`_ from the Supabase docs.

Here's the full list of docs that are used in each experiment. They're all fairly short
because EmbeddingGemma only supports 2048 tokens of input and I didn't feel like dealing
with chunking. Most of the docs revolve around testing.

* `Background Processing Using Web Workers <https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/ecosystem/web-workers.md>`_ (Angular)
* `Refer To Locales By ID <https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/i18n/locale-id.md>`_ (Angular)
* `Testing <https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/overview.md>`_ (Angular)
* `Testing Services <https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/services.md>`_ (Angular)
* `LINESTRING <https://raw.githubusercontent.com/cockroachdb/docs/refs/heads/main/src/current/v25.4/linestring.md>`_ (CockroachDB)
* `Test Your Application Locally <https://raw.githubusercontent.com/cockroachdb/docs/refs/heads/main/src/current/v25.4/local-testing.md>`_ (CockroachDB)
* `analysis_test <https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/analysis_test_doc.md>`_ (Skylib)
* `bzl_library <https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/bzl_library.md>`_ (Skylib)
* `diff_test <https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/diff_test_doc.md>`_ (Skylib)
* `Actionability <https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/actionability.md>`_ (Playwright)
* `JUnit <https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/junit-java.md>`_ (Playwright)
* `Writing Tests`_ (Playwright)
* `Branching <https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/deployment/branching.mdx>`_ (Supabase)
* `Testing Your Database <https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx>`_ (Supabase)
* `Testing Your Edge Functions <https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/functions/unit-test.mdx>`_ (Supabase)
* `Vector Columns <https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/ai/vector-columns.mdx>`_ (Supabase)

-------
Results
-------

In the :ref:`arithmetic-domain` experiment (`Testing
Your Database`_ - ``supabase`` + ``angular``) the resultant vector is most similar to
`Testing`_ and `Testing Services`_ from the Angular docs, as expected, **when
custom task types are enabled**. When using the default task types, the resultant
vector is most similar to `Testing Your Database`_ i.e. the doc that we
started with.

In the :ref:`arithmetic-topic` experiment (`Testing
Your Database`_ - ``testing`` + ``vectors``) the resultant vector is most similar to
`Vector Columns`_, as expected.

These preliminary results suggest that yes, word2vec-style vector arithmetic may indeed
work in technical writing contexts.

--------
Appendix
--------

Source code
===========

``experiments.py``:

.. literalinclude:: experiments.py

``data.json``:

.. literalinclude:: data.json

.. _arithmetic-logs:

Logs
====

.. literalinclude:: logs.txt

.. _word2vec: https://en.wikipedia.org/wiki/Word2vec
.. _vectors: https://en.wikipedia.org/wiki/Vector_(mathematics_and_physics)
.. _vector space: https://en.wikipedia.org/wiki/Vector_space
.. _embeddings: https://en.wikipedia.org/wiki/Embedding_(machine_learning)
.. _Efficient Estimations of Word Representations in Vector Space: https://arxiv.org/pdf/1301.3781
.. _EmbeddingGemma: https://arxiv.org/abs/2509.20354

.. _Writing Tests: https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/writing-tests-python.md
.. _Wikipedia: https://en.wikipedia.org/wiki/Word2vec#Preservation_of_semantic_and_syntactic_relationships
.. _Testing Your Database: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx
.. _cosine similarity: https://p.migdal.pl/blog/2025/01/dont-use-cosine-similarity/
.. _Testing: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/overview.md
.. _Testing Services: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/services.md
.. _Vector Columns: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/ai/vector-columns.mdx

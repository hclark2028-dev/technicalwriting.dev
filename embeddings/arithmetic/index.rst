.. _arithmetic:

===================================================
word2vec-style vector arithmetic on docs embeddings
===================================================

`word2vec`_ popularized the idea of representing words as `vectors`_ where
semantically similar words are positioned close to each other in the `vector
space`_. Nowadays these vectors are usually called `embeddings`_.

A neat consequence of the word2vec approach is that adding and subtracting
vectors produces semantically logical results. From `Efficient Estimations of
Word Representations in Vector Space`_ (the word2vec paper):

  Using a word offset technique where simple algebraic operations are performed
  on the word vectors, it was shown for example that ``vector("King")`` -
  ``vector("Man")`` + ``vector("Woman")`` results in a vector that is closest to the
  vector representation of the word ``Queen``.

Does word2vec-style vector arithmetic work in technical writing contexts?

-----------
Experiments
-----------

word2vec was published in 2013. Embedding models have come a long way since
then. word2vec models could only operate on single words. A vector always
represented a single word. Modern embedding models can operate on arbitrary
text. A vector can now represent a word, paragraph, section, document, set of
documents, etc.

My experiments follow the same basic pattern of ``vector("King")`` -
``vector("Man")`` + ``vector("Woman")``, with one difference. The experiments
start out with a vector representing the full text of a document, not a
single-word vector.

.. _arithmetic-domain:

Same topic, different domain
============================

This is the first experiment. Starting with the vector for the full text of
`Testing Your Database`_ from the Supabase docs, subtract the vector for the
word ``supabase``, and then add the vector for the word ``angular``. The
resultant vector should be semantically close to the concept of "testing in
Angular".

.. _arithmetic-topic:

Different topic, same domain
============================

This is the second experiment. Starting with the vector for the full text of
`Testing Your Database`_ from the Supabase docs, subtract the vector for the
word ``testing``, and then add the vector for the word ``vectors``. The
resultant vector should be semantically close to the concept of "vectors in
Supabase".

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

Here's the full list of docs that I use in the experiments:

* `Background Processing Using Web Workers`_ (Angular)
* `Refer To Locales By ID`_ (Angular)
* `Testing`_ (Angular)
* `Testing Services`_ (Angular)
* `LINESTRING`_ (CockroachDB)
* `Test Your Application Locally`_ (CockroachDB)
* `analysis_test`_ (Skylib)
* `bzl_library`_ (Skylib)
* `diff_test`_ (Skylib)
* `Actionability`_ (Playwright)
* `JUnit`_ (Playwright)
* `Writing Tests`_ (Playwright)
* `Branching`_ (Supabase)
* `Testing Your Database`_ (Supabase)
* `Testing Your Edge Functions`_ (Supabase)
* `Vector Columns`_ (Supabase)

For the :ref:`arithmetic-domain` experiment (`Testing Your Database`_ -
``supabase`` + ``angular``) I expect the resultant vector to be most similar to
`Testing`_ or `Testing Services`_ from the Angular docs. And for the
:ref:`arithmetic-topic` experiment (`Testing Your Database`_ - ``testing`` +
``vectors``) I expect the resultant vector to be most similar to `Vector
Columns`_ from the Supabase docs.

Note that I picked short docs because EmbeddingGemma only supports 2048 tokens of
input and I didn't feel like dealing with chunking. Most of the docs revolve around
testing.

-------
Results
-------

In the :ref:`arithmetic-domain` experiment (`Testing Your Database`_ -
``supabase`` + ``angular``) the resultant vector is most similar to `Testing`_
and `Testing Services`_ from the Angular docs, as expected, **when custom task
types are enabled**:

.. literalinclude:: logs.txt
   :start-at: [INFO] Running "same topic, different domain" experiment with customized task types
   :end-before: [INFO] Running "different topic, same domain" experiment with customized task types

When using the default task types, the resultant vector is most similar to
`Testing Your Database`_ i.e. the doc that the experiment started with:

.. literalinclude:: logs.txt
   :start-at: [INFO] Running "same topic, different domain" experiment with default task types
   :end-before: [INFO] Running "different topic, same domain" experiment with default task types

In the :ref:`arithmetic-topic` experiment (`Testing
Your Database`_ - ``testing`` + ``vectors``) the resultant vector is most similar to
`Vector Columns`_, regardless of whether default or custom task types were used.

Custom task types:

.. literalinclude:: logs.txt
   :start-at: [INFO] Running "different topic, same domain" experiment with customized task types
   :end-before: [INFO] Running "same topic, different domain" experiment with default task types

Default task types:

.. literalinclude:: logs.txt
   :start-at: [INFO] Running "different topic, same domain" experiment with default task types
   :end-at: [INFO] "analysis_test" (Skylib) => 0.15578024089336395

So, yes, it seems like word2vec-style vector arithmetic can work in technical
writing contexts. Make sure to set your :ref:`task types <tasks>` correctly.

----------
Discussion
----------

I still don't really understand how it's possible to semantically represent an
entire document as a single vector, let alone how adding and subtracting
single-word vectors from full-document vectors works.

How do we actually incorporate this technique into technical writing workflows
or documentation experiences? I haven't thought that far. 

--------
Appendix
--------

Source code
===========

``experiments.py``:

.. literalinclude:: experiments.py

``data.json``:

.. literalinclude:: data.json

.. _word2vec: https://en.wikipedia.org/wiki/Word2vec
.. _vectors: https://en.wikipedia.org/wiki/Vector_(mathematics_and_physics)
.. _vector space: https://en.wikipedia.org/wiki/Vector_space
.. _embeddings: https://en.wikipedia.org/wiki/Embedding_(machine_learning)
.. _Efficient Estimations of Word Representations in Vector Space: https://arxiv.org/pdf/1301.3781
.. _EmbeddingGemma: https://arxiv.org/abs/2509.20354
.. _Background Processing Using Web Workers: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/ecosystem/web-workers.md
.. _Refer To Locales By ID: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/i18n/locale-id.md
.. _Testing: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/overview.md
.. _Testing Services: https://raw.githubusercontent.com/angular/angular/refs/heads/main/adev/src/content/guide/testing/services.md
.. _LINESTRING: https://raw.githubusercontent.com/cockroachdb/docs/refs/heads/main/src/current/v25.4/linestring.md
.. _Test Your Application Locally: https://raw.githubusercontent.com/cockroachdb/docs/refs/heads/main/src/current/v25.4/local-testing.md
.. _analysis_test: https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/analysis_test_doc.md
.. _bzl_library: https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/bzl_library.md
.. _diff_test: https://raw.githubusercontent.com/bazelbuild/bazel-skylib/refs/heads/main/docs/diff_test_doc.md
.. _Actionability: https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/actionability.md
.. _JUnit: https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/junit-java.md
.. _Writing Tests: https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/writing-tests-python.md
.. _Branching: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/deployment/branching.mdx
.. _Testing Your Database: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx
.. _Testing Your Edge Functions: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/functions/unit-test.mdx
.. _Vector Columns: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/ai/vector-columns.mdx
.. _Wikipedia: https://en.wikipedia.org/wiki/Word2vec#Preservation_of_semantic_and_syntactic_relationships
.. _Testing Your Database: https://raw.githubusercontent.com/supabase/supabase/refs/heads/master/apps/docs/content/guides/database/testing.mdx
.. _cosine similarity: https://p.migdal.pl/blog/2025/01/dont-use-cosine-similarity/

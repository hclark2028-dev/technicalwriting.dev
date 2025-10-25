.. _arithmetic:

====================================
Vector arithmetic on docs embeddings
====================================

`Efficient Estimations of Word Representations in Vector Space`_ (the
word2vec paper) uses vector arithmetic as evidence that their word embedding
architecture can learn semantic relationships:

  Using a word offset technique where simple algebraic operations are performed
  on the word vectors, it was shown for example that ``vector("King") -
  vector("Man") + vector("Woman")`` results in a vector that is closest to the
  vector representation of the word ``Queen``.

Does this type of vector arithmetic work in a technical writing context?

-----------
Experiments
-----------

Same topic, different technology
================================

Imagine that I'm looking for a doc about writing tests in Rust. I want something
like the `Writing tests`_ guide from the Playwright Python docs. Same topic
(writing tests), different technology (Rust, not Playwright Python).

We should be able to express this query with the following vector arithmetic:

1. Generate an embedding for the full text of `Writing tests`_.

2. Subtract the embedding for the word ``playwright``.

3. Add the embedding for the word ``rust``.

To test whether the vector arithmetic produced a useful result, we need a set of
docs to measure similarity against.

-------
Results
-------

.. _Efficient Estimations of Word Representations in Vector Space: https://arxiv.org/pdf/1301.3781
.. _Writing tests: https://raw.githubusercontent.com/microsoft/playwright/refs/heads/main/docs/src/writing-tests-python.md
.. _Wikipedia: https://en.wikipedia.org/wiki/Word2vec#Preservation_of_semantic_and_syntactic_relationships

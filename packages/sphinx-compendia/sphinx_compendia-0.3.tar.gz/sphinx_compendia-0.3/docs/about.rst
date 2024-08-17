.. _about:

#####
About
#####

.. _rationale:

Why |project| was written?
==========================

Structuring a compendium and tracking cross-references has always been a
challenge for a couple of personal projects, namely cooking recipes and
tabletop role-playing game redaction.  After I wrote a few Sphinx extensions
(Sphinx-Terraform_ and Sphinx-Gherkin_), I had finally enough knowledge
of the Sphinx API to find a solution.

.. _Sphinx-Terraform: https://cblegare.gitlab.io/sphinx-terraform/
.. _Sphinx-Gherkin: https://cblegare.gitlab.io/sphinx-gherkin/


.. _known-issues:

Known issues
============

Cross-references in a domain index is suboptimal
------------------------------------------------

Since domain indices are computed *before* cross-references are resolved
in, we have to rebuild the indices for each document as a post-transform
step.  Solutions are investigated directly in Sphinx.  See the following
issues:

*   https://github.com/sphinx-doc/sphinx/issues/10299
*   https://github.com/sphinx-doc/sphinx/issues/10295

The post-transform is performed by the following class.

.. autoclass:: sphinx_compendia.domain.BackrefsIndexer
    :members: run


.. _license:



Python version support policy
=============================

Sphinx supports at all minor versions of Python released in the past 3 years
from the anticipated release date with a minimum of 3 minor versions of Python.
This policy is derived from `SPEC 0`_, a scientific Python domain standard.

.. _SPEC 0: https://scientific-python.org/specs/spec-0000/

For example, a version of Sphinx released in May 2025 would support Python 3.11,
3.12, and 3.13.

This is a summary table with the current policy:

=========== ======
Date        Python
=========== ======
05 Oct 2023 3.10+
----------- ------
04 Oct 2024 3.11+
----------- ------
24 Oct 2025 3.12+
----------- ------
01 Oct 2026 3.13+
----------- ------
01 Oct 2027 3.14+
=========== ======


License
=======

|project|

Copyright © 2022  Charles Bouchard-Légaré


.. literalinclude:: ../LICENSE
    :language: none

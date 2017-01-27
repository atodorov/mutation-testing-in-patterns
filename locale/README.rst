How To Translate
****************

Thanks to Sphinx, we can easily adding new langauge to translate it.


.. image:: http://www.sphinx-doc.org/en/1.5.1/_images/translation.png


Adding new language
===================

For example, if we want to add japanese::

.. code-block:: bash

    sphinx-intl update -p _build/locale -l ja

Then you will got these directories that contain po files:

    * ./locale/ja/LC_MESSAGES/

You can see that in locale directory already have `zh_TW` directory.

Translating
===========

Translate po file under ./locale/jp/LC_MESSAGES directory. The case of
index.po for mutation testing in patterns:

.. code-block:: bash

    #: ../../README.rst:22
    msgid "Mutation testing tools"
    msgstr "<FILL HERE BY TARGET LANGUAGE>"


Update po files by new pot files
================================

If the documentent is updated, it is necessary to generate update pot files
and to apply differences to translated po files.

.. code-block:: bash

    sphinx-intl update -p _build/locale


Reference
=========

`Sphinx Internationalization <http://www.sphinx-doc.org/en/1.5.1/intl.html>_ `

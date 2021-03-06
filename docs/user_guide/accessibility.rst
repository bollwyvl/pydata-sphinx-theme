.. _accessibility:

*************
Accessibility
*************

Creating and publishing content that does not exclude audiences with limited abilities
of various kinds is challenging, but also important, to achieve and then maintain.

While there is no one-size-fits-all solution to maintaining accessible content, this
theme and documentation site use some techniques to avoid common content shortcomings.

.. Note::

    Issues and pull requests to identify or fix accessibility issues on this theme
    or site are heartily welcomed!


In Configuration
================

Some minor configuration options in a site's ``conf.py`` can impact the
accessibility of content generated by this theme, and Sphinx in general.


Natural Language
----------------

If not using a more robust `internationalization approach <https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>`__ ,
speciying at least the baseline natural language will assistive technology
identify if the content is in a language the reader understands.

.. Hint::

    Specifying a ``language`` will propagate to the top-level `html` tag.

    .. code-block:: python

    language = "en"


Site Map
--------

Site maps, usually served from a file called `sitemap.xml` are a broadly-employed
approach to telling programs like search engines and assistive technologies where
different content appears on a website.

.. Hint::

    For a simple site (no extra languages or versions):

    .. code-block:: python

    html_baseurl = os.environ.get("SPHINX_HTML_BASE_URL", "http://localhost:8080/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"



In Your Source
==============

Specify image titles and captions...

Use effective, unique headers...


In Continuous Integration
=========================

A number of automated tools are available for assessing *glaring* accessibility
issues. This theme makes use of:


Lighthouse
----------

`Lighthouse <https://developers.google.com/web/tools/lighthouse>`__, which provides
automated assessment of basic accessibility issues in addition to search engine
automation, page performance, and other best practices.


.. Hint::

    Specifically, `foo-software/lighthouse-check-action <https://github.com/foo-software/lighthouse-check-action>`__
    is run on selected pages from the generated documentation site.


Pa11y CI
--------

`Pa11y CI <https://github.com/pa11y/pa11y-ci>`__ is a command line tool which can check
a number of accessibility standards. It is most effective when paired with a `sitemap.xml`,
such as can be generated with `sphinx-sitemap <https://github.com/jdillard/sphinx-sitemap>`__,
which

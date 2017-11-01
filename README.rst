Alfredo Library for Python
##########################

    Idiomatic way for Python developers to integrate with Alfredo services.

|build| |coverage| |deploy| |versions|

.. |build| image:: https://travis-ci.org/rstorsauce/alfredo-python-sdk.svg?branch=develop
   :target: https://travis-ci.org/rstorsauce/alfredo-python-sdk
.. |coverage| image:: https://coveralls.io/repos/github/rstorsauce/alfredo-python-sdk/badge.svg?branch=develop
   :target: https://coveralls.io/github/rstorsauce/alfredo-python-sdk?branch=develop
.. |deploy| image:: https://img.shields.io/pypi/v/alfredo-python.svg
   :target: https://pypi.python.org/pypi/alfredo-python
.. |versions| image:: https://img.shields.io/pypi/pyversions/alfredo-python.svg
   :target: https://pypi.python.org/pypi/alfredo-python



.. contents::

.. section-numbering::



Installation
============

On most systems, you can use ``pip`` (recommended):

.. code-block:: bash

   # Make sure we have an up-to-date version of pip and setuptools:
   pip install --upgrade pip setuptools

   pip install alfredo-python

Both Python 2 and 3 are supported.



Command Line Interface Usage
============================

The main command to interact with Alfredo stack is ``alfredo``.

Input is expected to be in YAML format, and also the output is serialized in that way.

You can set ``RUOTE_ROOT`` and/or ``VIRGO_ROOT`` env vars to point the CLI and the SDK to your desired installation of the Alfredo stack.

After that, you can execute ``alfredo`` to get the usage help.

You can also execute ``alfredo -help`` to get an updated list of the options you have, with examples.



Python Software Development Kit
===============================

The main module you need to import to interact with the Alfredo stack is ``alfredo``.

The main functions of the module are the ``ruote`` and ``virgo`` ones, to get the client object to further interact with respective services.

You can use ``alfredo.ruote()`` to get annonymous access to the open endpoints in Ruote. The same applies for ``virgo``.

For instance, you can use the annonymous access to get a token given an email and a password.

Please feel free of using the Python console to get used to the SDK prior to using it in real Python code.

.. code-block:: python

   >>> alfredo.ruote().sso.token_by_email.create(email='alice@example.com', password='*******')

   400 - Bad Request

   non_field_errors:
   - Unable to log in with provided credentials.

   >>> alfredo.ruote().sso.token_by_email.create(email='alice@example.com', password='********')

   200 - OK

   token: b1cff2aab075744ddda6b00805617f561e940107


You can use ``alfredo.ruote(token='b1cff2aab075744ddda6b00805617f561e940107')`` to get an authenticated client against Ruote.

.. code-block:: python

   >>> alfredo.ruote(token='b1bff2aab075744ddda6b00805617f561e940107')

   200 - OK

   AWSclusters: http://api.teamjamon.com/AWSclusters/
   apps: http://api.teamjamon.com/apps/
   clusters: http://api.teamjamon.com/clusters/
   datasets: http://api.teamjamon.com/datasets/
   files: http://api.teamjamon.com/files/
   jobs: http://api.teamjamon.com/jobs/
   queues: http://api.teamjamon.com/queues/
   users: http://api.teamjamon.com/users/
   vdcs: http://api.teamjamon.com/vdcs/


Most of the functions mimic the url structure of the http API, and receives named parameters as input.

Please refer to the Alfredo API documentation for further details.



Development
===========

You can create your fork of the repo before making any change.

Never forget to install the requirements first if you are using an isolated virtualenv: ``pip install -r requirements.txt``

And to include the test requirements if you are planning to pass the tests locally ``pip install -r requirements.txt``

You can run the tests using ``nosetests --with-coverage --cover-package=alfredo --stop``

Currently, the main branch is ``develop`` because the code is still in beta. You can make PRs against ``develop``.


Deployment
==========

If you are trying to use travis as a pypi deployment tool, please note that there is no documented way of using passwords with special characters.

Then you can try

.. code-block:: bash

   echo -n "password" | travis encrypt --org --add deploy.password --repo rstorsauce/alfredo-python-sdk

and be sure that your pypi user is the same than the ``deploy.user`` and that you have permissions to deploy ``alfredo-python``.

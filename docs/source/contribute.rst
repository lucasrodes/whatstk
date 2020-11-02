Contribute
==========

We are really open to your thoughts and feedback!

----

Bug reporting
-------------
Please report any bug that you may find to the `issues <https://github.com/lucasrodes/whatstk/issues>`_ section.

----

Requesting a Feature
--------------------
If you find a new feature could be useful for the community, please try to add it in the
`issues <https://github.com/lucasrodes/whatstk/issues>`_ section with a clear description.

----

Submitting a Pull Request
-------------------------
- Start by forking the `develop <https://github.com/lucasrodes/whatstk/tree/develop>`_ branch.
- Add your code to the project!
- Test your code running script `run-tests.sh <https://github.com/lucasrodes/whatstk/blob/master/run-tests.sh>`_.
This script checks the code style (flake8) and the logic of your code (pytest). Note: Make sure to open and read it. The first time you will need to run steps 1.1, 1.2 and 1.3.

.. code-block:: bash

    sh ./run-tests.sh

This script generates three HTML files which are placed within a created folder `reports`.

- Once your code successfully passed the tests, you can submitt a pull request and wait for its aproval


.. todo::

    Use `tox <https://tox.readthedocs.io/en/latest/>`_

Aproval of pull request
^^^^^^^^^^^^^^^^^^^^^^^

A pull request will be accepted if:

- Adds new functionalities of interest.
- Does not decrease the overall project code `coverage <https://codecov.io/gh/lucasrodes/whatstk>`_. 

Note: You will need to add tests for your code. For this, you can check the current `tests <https://github.com/lucasrodes/whatstk/tree/master/tests>`_.

----

Adding new examples
-------------------
To add new examples, consider editing yourself a ``rst`` file in ``docs/source/`` directory in the repository. For
questions or doubts, join the `gitter group <https://gitter.im/whatstk/>`_.

----

API discussions
---------------
Consider joining the `gitter group <https://gitter.im/whatstk/>`_.

----

Doubts?
-------

Feel free to `contact me <https://lcsrg.me/pages/contact>`_ :)
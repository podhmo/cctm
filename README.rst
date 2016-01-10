cctm
========================================

CCTM = cookie cutter template manager

project templates manager for `cookiecutter <https://github.com/audreyr/cookiecutter>`_

(python3 only)


.. code-block:: bash

  $ cctm init
  $ cctm selfupate
  $ cctm list | grep python
  $ cctm install flyondrag/cookiecutter-python
  $ cctm use flyondrag/cookiecutter-python


.. code-block:: bash

  $ cctm list | grep python
  flyondrag/cookiecutter-python(2) -- Python's package skeleton.
  kragniz/cookiecutter-pypackage-minimal(12) -- A minimal template for python packages
  wdm0006/cookiecutter-pipproject(2) -- A(nother) cookiecutter template for pip-installable python p


.. code-block:: bash

  $ cctm show cookiecutter-python
  {
    "created_at": "2015-09-24T09:05:43Z",
    "name": "flyondrag/cookiecutter-python",
    "description": "Python's package skeleton.",
    "updated_at": "2016-01-03T05:45:15Z",
    "url": "https://github.com/flyondrag/cookiecutter-python",
    "star": 2
  }


.. code-block:: bash

  $ cctm list --installed
  flyondrag/cookiecutter-python


commands
----------------------------------------

- init
- show
- list
- selfupdate
- management fetch
- management merge
- management remove

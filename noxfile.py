#!/usr/bin/env python3
#
#
#

import nox

supported_python_versions = [
                             "3.11.2",]

nox.error_on_external_run=False

@nox.session(python=supported_python_versions,venv_backend='venv')
def flake8(session):
    """ Flake8 PEP 8 quality check """
    session.install("flake8")
    session.install("-r", "requirements.txt")
    # E 501 is long line
    session.run("flake8", "--ignore","E501", "checkbox_empire.py", "app/cbx_section.py", "app/cbx_item.py", "app/cbx_empire.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def safety(session):
    """ Check requirements for vulnerabilities """
    session.install("safety")
    session.install("-r", "requirements.txt")
    # safety check -r requirements.txt
    session.run("safety","check", "-r", "requirements.txt")

@nox.session(python=supported_python_versions,venv_backend='venv')
def bandit(session):
    """ Check for common vulnerabilities """
    session.install("bandit")
    session.install("-r", "requirements.txt")
    # bandit -ll -r  foo.py    ( -ll = medium level and higher, -r recursive)
    session.run("bandit","-ll", "-r", "checkbox_empire.py", "app/cbx_section.py", "app/cbx_item.py", "app/cbx_empire.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def mypy(session):
    """ Envorcing types """
    session.install("mypy")
    session.install("-r", "requirements.txt")
    # Check for wrong types
    # mypy --strict-optional  app/ plugins/base/
    session.run("mypy","--strict-optional", "checkbox_empire.py", "app/cbx_section.py", "app/cbx_item.py", "app/cbx_empire.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def pylint(session):
    """ Linting for common mistakes """
    session.install("pylint")
    session.install("-r", "requirements.txt")
    # pylint --rcfile=pylint.rc  foo.py
    session.run("pylint","--rcfile=pylint.rc", "checkbox_empire.py", "app/cbx_section.py", "app/cbx_item.py", "app/cbx_empire.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def unittest(session):
    """ Running unittests with coverage """
    session.install("coverage")
    session.install("-r", "requirements.txt")
    # python -m unittest discover -s tests
    # coverage run --source=app -m unittest discover -s tests
    session.run("coverage","run", "--source=app", "-m","unittest", "discover", "-s", "tests")
    # to get command line report: "coverage report"
    # to get command html report: "coverage html"

@nox.session(python=supported_python_versions,venv_backend='venv')
def docstr_coverage(session):
    """ Enforcing documentation coverage """
    session.install("docstr_coverage")
    session.install("-r", "requirements.txt")
    # pylint --rcfile=pylint.rc  foo.py
    session.run("docstr-coverage","app", "checkbox_empire.py")

@nox.session(python=supported_python_versions,venv_backend='venv')
def pydocstyle(session):
    """ Enforcing PEP 257 documentation style https://peps.python.org/pep-0257/

    We are using sphinx doc. There is an open PR for sphinx parameters https://github.com/PyCQA/pydocstyle/pull/595
    So we do not have a support for parameter checks yet.
    """
    session.install("pydocstyle")
    session.install("-r", "requirements.txt")
    # pylint --rcfile=pylint.rc  foo.py
    session.run("pydocstyle","app", "checkbox_empire.py")
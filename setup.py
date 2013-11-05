try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "yaly",
    description="Yet Another Lex-Yacc",
    long_description = """
YALY is yet another simple implementation lex and Lex-Yacc
implemented in Python.
It is fit for teaching and learning.
It is compatible with both Python 2 and Python 3.
""",
    license="""GPL v2""",
    version = "0.1.1",
    author = "Leonardo Huang",
    author_email = "leon@njuopen",
    maintainer = "Leonardo Huang",
    maintainer_email = "leon@njuopen",
    url = "https://github.com/leon-huang/yalexer",
    packages = ['yaly'],
    install_requires = ['yare'],
    dependency_links = ['https://github.com/leon-huang/yare/tarball/master#egg=yare-0.4.4'],
    classifiers = [
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
    ]
)

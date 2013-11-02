try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "lexer",
    description="A Simple Lexer",
    long_description = """
LEXER is yet another simple lexer implemented in Python.
It is fit for teaching and learning.
It is compatible with both Python 2 and Python 3.
""",
    license="""GPL v2""",
    version = "0.1.0",
    author = "Leonardo Huang",
    author_email = "leon@njuopen",
    maintainer = "Leonardo Huang",
    maintainer_email = "leon@njuopen",
    url = "https://github.com/leon-huang/lexer",
    packages = ['lexer'],
    install_requires = ['pyre'],
    dependency_links = ['https://github.com/leon-huang/pyre/tarball/master#egg=pyre-0.2.1'],
    classifiers = [
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
    ]
)

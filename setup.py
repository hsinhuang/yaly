try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = "yalexer",
    description="Yet Another Lexer",
    long_description = """
YALEXER is yet another simple lexer implemented in Python.
It is fit for teaching and learning.
It is compatible with both Python 2 and Python 3.
""",
    license="""GPL v2""",
    version = "0.1.0",
    author = "Leonardo Huang",
    author_email = "leon@njuopen",
    maintainer = "Leonardo Huang",
    maintainer_email = "leon@njuopen",
    url = "https://github.com/leon-huang/yalexer",
    packages = ['yalexer'],
    install_requires = ['yare'],
    dependency_links = ['https://github.com/leon-huang/yare/tarball/master#egg=yare-0.4.3'],
    classifiers = [
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
    ]
)

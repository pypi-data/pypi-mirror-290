from setuptools import setup

name = "types-google-cloud-ndb"
description = "Typing stubs for google-cloud-ndb"
long_description = '''
## Typing stubs for google-cloud-ndb

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`google-cloud-ndb`](https://github.com/googleapis/python-ndb) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`google-cloud-ndb`.

This version of `types-google-cloud-ndb` aims to provide accurate annotations
for `google-cloud-ndb==2.3.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/google-cloud-ndb. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`37807d753a0e56a178b4c38f80879a4c90592ef3`](https://github.com/python/typeshed/commit/37807d753a0e56a178b4c38f80879a4c90592ef3) and was tested
with mypy 1.11.1, pyright 1.1.375, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.3.0.20240813",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/google-cloud-ndb.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['google-stubs'],
      package_data={'google-stubs': ['cloud/ndb/__init__.pyi', 'cloud/ndb/_batch.pyi', 'cloud/ndb/_cache.pyi', 'cloud/ndb/_datastore_api.pyi', 'cloud/ndb/_datastore_query.pyi', 'cloud/ndb/_eventloop.pyi', 'cloud/ndb/_options.pyi', 'cloud/ndb/_transaction.pyi', 'cloud/ndb/blobstore.pyi', 'cloud/ndb/client.pyi', 'cloud/ndb/context.pyi', 'cloud/ndb/django_middleware.pyi', 'cloud/ndb/exceptions.pyi', 'cloud/ndb/global_cache.pyi', 'cloud/ndb/key.pyi', 'cloud/ndb/metadata.pyi', 'cloud/ndb/model.pyi', 'cloud/ndb/msgprop.pyi', 'cloud/ndb/polymodel.pyi', 'cloud/ndb/query.pyi', 'cloud/ndb/stats.pyi', 'cloud/ndb/tasklets.pyi', 'cloud/ndb/utils.pyi', 'cloud/ndb/version.pyi', 'METADATA.toml', 'cloud/ndb/py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

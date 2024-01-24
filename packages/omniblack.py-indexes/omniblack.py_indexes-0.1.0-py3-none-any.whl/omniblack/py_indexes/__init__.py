from os import getcwd, rename
from os.path import join
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin
from tempfile import NamedTemporaryFile
from hashlib import file_digest as get_file_digest, algorithms_available
from logging import getLogger, DEBUG
from threading import RLock
from atexit import register

from packaging.specifiers import SpecifierSet
from packaging.version import Version
from requests_cache import CachedSession
from xdg.BaseDirectory import save_cache_path
from public import public
from requests_cache.backends.sqlite import SQLiteCache


#: PYPI's api url.
pypi = 'https://pypi.org/simple/'

#: Test PYPI's api url.
#: This is a seperate instance of PYPI.
#: This instance if for testing distrubtion tools and processes.
#: It should not be relied upon for consistent storage of packages
#: as it maybe reset at any time.
test_pypi = 'https://test.pypi.org/simple/'

mime = 'application/vnd.pypi.simple.v1+json'

log = getLogger(__package__)
log.setLevel(DEBUG)

cache_dir = save_cache_path('omniblack')
cache = SQLiteCache(db_path=join(cache_dir, 'http_cache.sqlite'))
session = CachedSession(backend=cache)
register(session.close)
register(cache.close)
session_lock = RLock()


@public
@dataclass
class Meta:
    """Information about the response itself.

    :ivar api_version: The simple repository api version this object uses.
    :vartype api_version: :type:`packaging.version.Version`
    """
    api_version: Version

    @classmethod
    def from_json_dict(cls, json: dict):
        """
        Convert a dict into a :code:`Meta`.

        Will handle an optional values,
        or values with union types.
        """
        return cls(
            api_version=Version(json['api-version']),
        )


@public
@dataclass
class ProjectBrief:
    """A samll amount of information abouth the project.

    :ivar name: The name of the project.
        Whether or not the name is
        :pep:`normalized <503#normalized-names>`
        is an index implemention detail.

    :vartype name: :type:`str`
    """
    name: str

    @classmethod
    def from_json_dict(cls, json):
        """
        Convert a dict into a :code:`ProjectBrief`.

        Will handle an optional values,
        or values with union types.
        """
        return cls(
            name=json['name'],
        )

    def get(self, index=pypi):
        """
        Retrieve the project associated with this project brief.

        :param index: The index to access.
        :type index: :type:`str`
        """
        return Project.get(self.name, index)


def maybe_specifiers(value):
    if isinstance(value, str):
        return SpecifierSet(value)
    else:
        return value


def maybe_date(value):
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    else:
        return value


@public
@dataclass
class File:
    """A description of a distribution file for the project.

    :ivar dist_info_metadata: An optional key that indicates that metadata
        for this file is available, via the same location as specified in
        :pep:`PEP 658 <658#specification>` :python:`self.url + '.metadata'`
        Where this is present, it :rfc:`MUST <2119#section-1>` be
        either a boolean to indicate
        if the file has an associated metadata file, or a dictionary mapping
        hash names to a hex encoded digest of the metadata’s hash.
    :vartype dist_info_metadata: :type:`bool | dict[str, str]`

    :ivar filename: The filename that is being represented.
    :vartype filename: :type:`str`

    :ivar gpg_sig: An optional key that acts a boolean to indicate if the file
        has an associated GPG signature or not. The URL for the signature file
        follows what is specified in :pep:`PEP 503 <503#specification>`
        :python:`self.url + '.asc'`.
        If this key does not exist, then the signature may or may not exist.
    :vartype gpg_sig: :type:`bool`


    :ivar hashes: A dictionary mapping a hash name to a hex encoded digest
        of the file.
        omniblack.py_indexes will use one of these hashes to validate
        downloaded files.
    :vartype hashes: :type:`dict[str, str]`

    :ivar requires_python:  An optional key that exposes the
        :core-metadata:`Requires-Python <requires-python>` metadata field.
        Where this is present, installer tools :rfc:`SHOULD <2119#section-3>`
        ignore the download when installing to a Python version that doesn’t
        satisfy the requirement.
    :vartype requires_python: :type:`typing.Optional[packaging.specifiers.SpecifierSet]`

    :ivar size: The size of the file in bytes.
    :vartype size: :type:`int`

    :ivar upload_time: The time the file was uploaded to the index.
    :vartype upload_time: :type:`typing.Optional[datetime.datetime]`

    :ivar url: The URL that the file can be fetched from.
    :vartype url: :type:`str`

    :ivar yanked: A boolean to indicate if the file has been yanked,
        or a non empty, but otherwise arbitrary, string to indicate that a file
        has been yanked with a specific reason.
        If the yanked key is present and is a truthy value,
        then it :rfc:`SHOULD <2119#section-1>` be interpreted as indicating
        that the file pointed to by the url field
        has been :pep:`"Yanked" <592#specification>`.
    :vartype yanked: :type:`bool | str`
    """
    dist_info_metadata: bool | dict[str, str]
    filename: str
    gpg_sig: bool
    hashes: dict[str, str]
    requires_python: SpecifierSet | None
    size: int
    upload_time: datetime | None
    url: str
    yanked: bool | str

    @classmethod
    def from_json_dict(cls, json: dict):
        """
        Convert a dict into a :code:`Project`.

        Will handle an optional values,
        or values with union types.
        """
        return cls(
            filename=json['filename'],
            url=json['url'],
            hashes=json['hashes'],
            gpg_sig=json.get('gpg-sig', False),
            requires_python=maybe_specifiers(
                json.get('requires-python', None),
            ),
            yanked=json['yanked'],
            dist_info_metadata=json.get('dist-info-metadata', False),
            size=json['size'],
            upload_time=maybe_date(json['upload-time']),
        )

    def download(self, download_directory=None):
        """
        Download this file.

        The file will be validated using :python:`self.hashes` if possible.

        :param download_directory: The directory to store the file in.
        :type download_directory: :type:`typing.Optional[str]`

        :return: The final path the file was downloaded to.
        """

        if download_directory is None:
            download_directory = getcwd()

        final_path = join(download_directory, self.filename)

        try:
            with ExitStack() as stack:
                file = stack.enter_context(
                    NamedTemporaryFile('wb', dir=download_directory),
                )
                stack.enter_context(session_lock)
                resp = session.get(self.url)
                print(resp.url)

                resp.raise_for_status()
                file.write(resp.content)

                rename(file.name, final_path)
        except FileNotFoundError:
            pass

        for algorithm, digest in self.hashes.items():
            if algorithm not in algorithms_available:
                continue

            with open(final_path, 'rb') as file_obj:
                file_digest = get_file_digest(file_obj, algorithm)

                if file_digest.hexdigest() != digest:
                    raise RuntimeError(
                        f'Digest for {final_path} failed to validate. '
                        'File has not be removed, but should not be used '
                        'without care.',
                    )
                else:
                    log.info(f'{self.filename} validated successfully.')

        return final_path


@public
class ProjectList(tuple[ProjectBrief]):
    """
    All projects hosted on the index.

    :ivar meta: The general response metadata.
    :vartype meta: :type:`Meta`
    """
    meta: Meta

    def __new__(cls, projects, *, meta=None):
        cls.meta = meta
        return super().__new__(cls, projects)

    @classmethod
    def from_json_dict(cls, json):
        """
        Convert a dict into a :code:`ProjectList`.

        Will handle an optional values,
        or values with union types.
        """
        return cls(
            projects=tuple(
                ProjectBrief.from_json_dict(project)
                for project in json['projects']
            ),
            meta=Meta.from_json_dict(json['meta']),
        )

    @classmethod
    def get(cls, index=pypi):
        """
        Retrieve all projects from an index.
        This method should be used rarely, as it can be expensive
        for the index.

        :param index: The index to access.
        :type index: :type:`str`
        """
        with session_lock:
            resp = session.get(index, headers=dict(Accept=mime))
            resp.raise_for_status()
            data = resp.json()
            return cls.from_json_dict(data, index)


# Simple Detail page (/simple/$PROJECT/)
@public
@dataclass
class Project:
    """
    A project hosted on the

    :ivar name: The :pep:`normalized name <503#normalized-names>`
        of the project.
    :vartype name: :type:`str`

    :ivar files: The files associated with the project.
    :vartype files: :type:`tuple[File]`

    :ivar meta: The general response metadata.
    :vartype meta: :type:`Meta`

    :ivar versions: All of the project versions uploaded for this project.
    :vartype versions: :type:`frozenset[Version]`
    """
    name: str  # Normalized Name
    meta: Meta
    files: tuple[File]
    versions: frozenset[Version]

    @classmethod
    def from_json_dict(cls, json: dict):
        """
        Convert a dict into a :code:`Project`.

        Will handle an optional values,
        or values with union types.
        """
        return cls(
            name=json['name'],
            meta=Meta.from_json_dict(json['meta']),
            files=tuple(
                File.from_json_dict(file)
                for file in json['files']
            ),
            versions=tuple(
                Version(ver)
                for ver in json['versions']
            ),
        )

    @classmethod
    def get(cls, project, index=pypi):
        """
        Retrieve a project from an index.

        :param project: The :pep:`normalized name <503#normalized-names>`
            of the project.
        :type project: :type:`str`

        :param index: The index to access.
        :type index: :type:`str`
        """
        url = urljoin(index, project)
        with session_lock:
            resp = session.get(url, headers=dict(Accept=mime))
            resp.raise_for_status()
            return cls.from_json_dict(resp.json())

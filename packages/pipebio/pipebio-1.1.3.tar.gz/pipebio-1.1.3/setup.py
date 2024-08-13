from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "DESCRIPTION.md").read_text()

setup(
    name='pipebio',
    version='1.1.3',
    description='A PipeBio client package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pipebio/python-library',
    author='Chris Peters',
    author_email='chris@pipebio.com',
    license='BSD 3-clause',
    packages=[
        'pipebio',
        'pipebio.models'
    ],
    install_requires=[
        "requests==2.32.2",
        "urllib3==2.2.2",
        'pandas~=2.2.2',
        'setuptools~=67.7.2',
        'biopython~=1.78',
        'python-dotenv~=1.0.1',
        'requests-toolbelt~=1.0.0',
        'openpyxl~=3.1.5',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)

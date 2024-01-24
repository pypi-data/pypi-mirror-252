#!/usr/bin/env python
# This is a python script to build and push the python package to https://pypi.org.

from setuptools import find_packages, setup
import os
import sys
import re
from os.path import exists


def recursive_files(base_dir):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list


def get_file_content(file_name):
    """
    get the file content by file_name
    """
    if not os.path.isfile(file_name):
        print(f"ERROR: invalid file: {file_name}, not exist or not file")
        sys.exit(-1)

    with open(file_name, encoding='utf-8') as f:
        content = f.read()
    return content


def parse_requirements(fname='requirements.txt', with_version=True):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.
    @param fname: path to requirements file
    @param with_version: if True include version specs
    @return: List[str]: list of requirements items
    """

    require_fpath = fname

    def parse_line(line):
        """Parse information from a line in a requirements text file."""
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {'line': line}
            if line.startswith('-e '):
                info['package'] = line.split('#egg=')[1]
            elif '@git+' in line:
                info['package'] = line
            else:
                # Remove versioning from the package
                pat = '(' + '|'.join(['>=', '==', '>']) + ')'
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info['package'] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ';' in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip,
                                                     rest.split(';'))
                        info['platform_deps'] = platform_deps
                    else:
                        version = rest  # NOQA
                    info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            startswith = sys.version.startswith('3.9')
            for info in parse_require_file(require_fpath):
                parts = [info['package']]
                if with_version and 'version' in info:
                    parts.extend(info['version'])
                if not startswith:
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get('platform_deps')
                    if platform_deps is not None:
                        parts.append(';' + platform_deps)
                item = ''.join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages



setup(
    name='sealion-conda',
    version='0.0.1.post1',
    description='',
    long_description=get_file_content("README.md"),
    long_description_content_type='text/markdown',
    author='arkmon',
    author_email='',
    keywords=['sealion-conda', 'sealionconda', "sc"],
    url='https://github.com/opensealion/sealion-conda',
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    license='Apache License 2.0',
    install_requires=parse_requirements('sealionconda/requirements.txt'),
    entry_points={
        'console_scripts': [
            'sc=sealionconda.app:main'
        ]
    },
    ext_modules=[],

)

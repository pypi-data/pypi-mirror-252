import argparse
import json
import logging
import os
import zipfile
from tqdm import tqdm


def collect_conda_env_files(conda_meta: str):
    conda_json_files = os.listdir(conda_meta)
    conda_env_pkgs = []
    for json_file in tqdm(conda_json_files, desc="Seeking conda env files:"):
        # print(json_file)
        if json_file.endswith('.json'):
            full_path = f"{conda_meta}/{json_file}"
            # print(f"fullpath={full_path}")
            with open(full_path, "r") as f:
                data = json.load(f)
                extracted_package_dir = data.get("extracted_package_dir")
                package_tarball_full_path = data.get("package_tarball_full_path")
                if extracted_package_dir:
                    conda_env_pkgs.append(extracted_package_dir)
                if package_tarball_full_path:
                    conda_env_pkgs.append(package_tarball_full_path)
    logger.info(conda_env_pkgs)
    return conda_env_pkgs


def compress_pkgs(zip_file: str, conda_env_pkgs: list):
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for pkg in tqdm(conda_env_pkgs, desc="Compressing files:"):
            if os.path.isfile(pkg) or os.path.isdir(pkg):
                zipf.write(pkg, os.path.basename(pkg))
            else:
                logger.debug(f"Warning: {pkg} is not a file or does not exist. Skipping.")


def uncompress_pkgs(extract_to, zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc="Uncompressing files:"):
            extracted_path = os.path.join(extract_to, member.filename)
            if not os.path.exists(extracted_path):
                zip_ref.extract(member, extract_to)
            else:
                logger.debug(f"Skipping {extracted_path}, it already exists.")
        # zip_ref.extractall(extract_to)


def create_parser():
    parser = argparse.ArgumentParser(description="Sealion Conda Management Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # clone: add params
    _clone_parser = subparsers.add_parser('clone', help='clone a conda environment')
    _clone_parser.add_argument('-b', required=True, help='path to the base conda')
    _clone_parser.add_argument('-e', required=True, help='path to the conda environment to be cloned')
    _clone_parser.add_argument('new_env_name', help='name of the new conda environment')

    # pkg: add params
    _pkg_parser = subparsers.add_parser('pkg', help='package a conda environment into a zip file')
    _pkg_parser.add_argument('-b', required=True, help='path to the base conda')
    _pkg_parser.add_argument('-e', required=True, help='path to the conda environment to be packaged')
    _pkg_parser.add_argument('zip_path', help='path to save the package zip file')

    # create: add params
    _create_parser = subparsers.add_parser('create', help='create a new conda environment from a zip file')
    _create_parser.add_argument('-f', required=True, help='path to the package zip file')
    _create_parser.add_argument('new_env_name', help='name of the new conda environment')

    return parser


def log(name):
    """
    @param name: python file name
    @return: Logger
    """
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(levelname)s:     %(asctime)s - %(module)s-%(funcName)s-line:%(lineno)d - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    _logger.addHandler(ch)
    return _logger


logger = log("util")


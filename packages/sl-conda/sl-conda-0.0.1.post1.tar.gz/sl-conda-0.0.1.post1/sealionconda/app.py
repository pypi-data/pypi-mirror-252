import os
from sealionconda.utils import log, create_parser
import sealionconda.utils as utils

logger = log(__name__)


def clone(conda_base: str, conda_env: str, new_env: str):
    conda_env = f"{conda_base}/envs/{conda_env}"
    conda_meta = f"{conda_env}/conda-meta"

    # collect necessary conda env files from $CONDA-PATH/envs/$conda_env/conda-meta
    conda_env_pkgs = utils.collect_conda_env_files(conda_meta)

    # compress the files from conda_env_pkgs
    zip_file = "pkgs.zip"
    utils.compress_pkgs(zip_file, conda_env_pkgs)

    # uncompress the zip_file
    extract_to = f"{conda_base}/pkgs"
    logger.debug(extract_to)
    utils.uncompress_pkgs(extract_to, zip_file)

    # create the new conda env by --clone
    create_conda_env = f"{conda_base}/bin/conda create -n {new_env} --clone {conda_env}"
    print(create_conda_env)
    os.system(create_conda_env)
    os.system(f"rm -rf ./{zip_file}")


def init_check():
    """
    TODO
    checklist for running sealion-cond
    1. is conda installed?
    :return:
    """
    pass


def check_conda_env(args):
    """
    TODO
    check if conda env is valid
    :param args:
    :return:
    """
    pass


def pkg(conda_base: str, conda_env: str, zip_path: str):
    conda_env = f"{conda_base}/envs/{conda_env}"
    conda_meta = f"{conda_env}/conda-meta"

    # collect necessary conda env files from $CONDA-PATH/envs/$conda_env/conda-meta
    conda_env_pkgs = utils.collect_conda_env_files(conda_meta)

    # compress the files from conda_env_pkgs
    zip_file = zip_path
    utils.compress_pkgs(zip_file, conda_env_pkgs)


# def create(zip_path: str, new_env_name: str):
#     # uncompress the zip_file
#     pkg(conda_base, new_env_name, zip_path)
#
#     # create the new conda env by --clone
#     os.system(f"conda create -n {new_env_name} --clone {conda_env}")


def main():
    parser = create_parser()
    args = parser.parse_args()

    init_check()
    check_conda_env(args)

    if args.command == 'clone':
        logger.info(f"Cloning environment from {args.b}/envs/{args.e} to {args.new_env_name}")
        clone(args.b, args.e, args.new_env_name)
    elif args.command == 'pkg':
        logger.info(f"Packaging environment from {args.b}/envs/{args.e} to {args.zip_path}")
        # TODO 这里添加 'pkg' 的处理逻辑
        pkg(args.b, args.e, args.zip_path)
    elif args.command == 'create':
        logger.info(f"Creating environment from {args.f} with name {args.new_env_name}")
        # TODO 这里添加 'create' 的处理逻辑
        # create(args.f, args.new_env_name)


if __name__ == "__main__":
    main()

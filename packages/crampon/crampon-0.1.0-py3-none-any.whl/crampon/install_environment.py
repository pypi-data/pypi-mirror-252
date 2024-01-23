#!/usr/bin/env python
"""
Single-file python script to install a conda environment given a directory of requirements or freeze files.
Assumes conda is installed.

This is intentionally written in 3.7-compatible python to make it easier to run it anywhere.
"""
import argparse
from importlib.util import module_from_spec, spec_from_file_location
from typing import Any, Optional, Union
from pathlib import Path
import logging
import subprocess
from contextlib import contextmanager
import os


def install_environment_parser():
    """ Returns a new parser with all arguments added for install_environment. """
    parser = argparse.ArgumentParser()
    parser.add_argument('env_dir', type=Path, nargs='?', default=Path.cwd(),
                        help='The environment directory to install.')
    parser.add_argument('--solve', action='store_true',
                        help='Run dependency solving and regenerate the freeze files. Slower.')
    parser.add_argument('--no_local_requirements', action='store_true',
                        help='After installing the conda environment and dependencies, install the py65 package locally.')
    parser.add_argument('--clean', action='store_true',
                        help='Clear the conda cache after installation.')
    parser.add_argument('--no_bump', action='store_true',
                        help='Disable the auto-bump if solving yields changes to the freeze files.')
    return parser


def main():
    """
    Commandline entrypoint to install_environment_dir().
    """
    parser = install_environment_parser()
    args = parser.parse_args()

    install_environment_dir(args.env_dir, args.solve,
                            not args.no_local_requirements, args.clean, not args.no_bump)


def install_environment_dir(env_dir: Path, solve: bool, local_requirements: bool, clean: bool, bump: bool):
    """
    Install or update a conda environment given a directory of requirement files.

    Parameters
    ----------
    env_dir : Path
        The directory containing the files
    solve : bool
        If True, solve the constraints and write new freeze files.
        If False, just use the existing freeze files to save time.
    local_requirements : bool
        If True, after installing the conda environment, install
        the py65 package and its local requirements in dev mode.
    clean : bool
        if True, clear conda's package cache after installation.
    """
    env_dir = env_dir.resolve()
    if not env_dir.exists():
        raise FileNotFoundError(f'No such environment directory: {env_dir}')

    env_name = os.environ.get('ENV_NAME', env_dir.name)
    if env_exists(env_name):
        print('Updating existing.')
        subcommand = 'update'
    else:
        print('Creating from scratch.')
        subcommand = 'create'

    freeze_contents_changed = False
    with cwd(env_dir):
        sh('conda clean --all -y')
        if solve:
            # TODO: use the checked-in versions of the freeze files here
            orig_freeze_file_contents = get_freeze_file_contents(env_dir)

            maybe_generate_constraint_files(env_dir)
            maybe_install_mamba()

            sh(conda_run(
                'base', f'mamba env {subcommand} -n {env_name} --file environment.yml'))
            sh(conda_run(env_name, 'conda list --explicit > conda_requirements.txt'))
            sh(conda_run(env_name, 'pip install pip-tools==6.13.0'))
            sh(conda_run(env_name, 'pip-compile -v --resolver backtracking'))
            sh(conda_run(env_name, 'pip install -r requirements.txt --no-deps'))

            new_freeze_file_contents = get_freeze_file_contents(env_dir)

            freeze_contents_changed = orig_freeze_file_contents != new_freeze_file_contents
        else:
            sh(f'conda {subcommand} -n {env_name} --file conda_requirements.txt')
            sh(conda_run(env_name, 'pip install -r requirements.txt --no-deps'))

        if (env_dir / 'extra_build_steps.sh').exists():
            print('Found extra_build_steps.sh. Executing')
            sh(conda_run(env_name, 'bash extra_build_steps.sh'))

    if local_requirements:
        print('Installing local py65 package and requirements.')
        sh(conda_run(env_name, 'pip install -r requirements_local.txt'),
           cwd=get_repo_root())

    if clean:
        print('Cleaning conda and pip package caches.')
        sh('conda clean -afy')
        sh('pip cache purge')

    print(f'Completed installation of {env_name}.')

    if bump and freeze_contents_changed and env_dir != get_repo_root():
        bump_result = sh(f'bump {env_dir}', check=False, capture_output=True)
        if bump_result.returncode == 0:
            print(
                f'Solving yielded changes to the freeze files. Bumped {env_dir} accordingly.')


def env_exists(env_name):
    """
    Check if a conda environment with name env_name is installed on the current system.
    """
    _env_exists_result = sh(
        f'conda env list | grep "^{env_name}\\s"', check=False)
    return _env_exists_result.returncode == 0


@contextmanager
def cwd(target_dir: Union[str, Path]):
    """
    Context manager that will temporarily change the working directory to dir.
    When exiting the context manager, you will return to the old working directory.
    """
    old_cwd = os.getcwd()
    try:
        os.chdir(target_dir)
        yield
    finally:
        os.chdir(old_cwd)


def get_freeze_file_contents(env_dir: Path) -> dict:
    """
    Read freeze files from an environment directory and return their contents in a dict.

    Used for checking whether to bump after solving new dependencies.
    """
    result: dict = {}
    for key, file_name in [('conda', 'conda_requirements.txt'), ('pip', 'requirements.txt')]:
        freeze_path = env_dir / file_name
        if freeze_path.exists():
            with open(freeze_path) as f:
                result[key] = f.read()
        else:
            result[key] = None
    return result


def maybe_generate_constraint_files(env_dir: Path):
    """
    Try to generate the constraint files (environment.yml and requirements.in) using a
    file build.py with code to do so.

    If the file doesn't exist,
    """
    try:
        build_class = _get_build_class(env_dir)
    except FileNotFoundError:
        print(f'{env_dir / "build.py"} not found. Cannot regenerate constraint files.')
    else:
        build_obj = build_class()
        if hasattr(build_obj, 'PREPARE_CONSTRAINT_FILES'):
            print('Generating constraint files environment.yml and requirements.in.')
            build_obj.PREPARE_CONSTRAINT_FILES(env_dir)
        else:
            print(f'{env_dir / "build.py"} does not implement PREPARE_CONSTRAINT_FILES(). '
                  'Cannot regenerate constraint files.')

            if not (env_dir / 'environment.yml').exists() or not (env_dir / 'requirements.in').exists():
                raise FileNotFoundError(
                    f'Missing constraint files environment.yml or requirements.in in {env_dir}.')
            print('Using existing constraint files.')


def _get_build_class(env_dir: Path):
    # Check for a `build.py`.
    if (env_dir / 'build.py').exists():
        logging.info('Found %s custom build script. Loading.',
                     env_dir / "build.py")
        return _dynamic_load_module_entrypoint(env_dir / 'build.py')
    raise FileNotFoundError(f'Expected {env_dir / "build.py"} to exist.')


def _dynamic_load_module_entrypoint(path: Path):
    module_name = path.stem
    spec = spec_from_file_location(module_name, path)  # type: Any
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return getattr(module, 'BUILD')
    except AttributeError as err:
        raise AttributeError(
            f'Expected {path} to have an attribute BUILD. No such attribute.') from err


def maybe_install_mamba():
    """
    Check if mamba is currently installed. Install it in the base environment if not.
    """
    result = sh('command -v mamba &> /dev/null', capture_output=True)
    if not result.stdout:  # not installed, download it
        print('No mamba found; Installing in the base conda environment. This can take some time.')
        sh('conda install -c conda-forge -n base mamba --yes')

# pylint: disable=redefined-outer-name


def sh(*command: str, check: bool = True, cwd: Optional[Union[str, Path]] = None, capture_output: bool = False):
    """
    Convenience wrapper around subprocess.run to shorten the code.
    """
    cmd = ' '.join(command)

    logging.info('Shell command: %s', cmd)
    return subprocess.run(cmd, shell=True, check=check, cwd=cwd, capture_output=capture_output)


def conda_run(env_name: str, cmd: str) -> str:
    """
    Take a shell command string and prepend it in a `conda run` invocation, so it will be
    executed in a particular environment. Does not actually run the command.

    Used to reduce boilerplate.
    """
    return f'conda run -n {env_name} --no-capture-output {cmd}'


def get_repo_root() -> Path:
    """
    Return the path to the repo root.
    """
    return Path(os.environ['PY65_REPO_ROOT']).resolve()


if __name__ == '__main__':
    main()

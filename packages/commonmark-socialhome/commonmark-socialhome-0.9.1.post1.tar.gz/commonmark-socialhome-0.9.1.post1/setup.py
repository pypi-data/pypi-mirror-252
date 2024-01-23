from setuptools import setup, find_packages, Command
import io
from os import path


class Test(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([
            sys.executable, 'commonmark/tests/run_spec_tests.py'])
        raise SystemExit(errno)


tests_require = [
    'flake8',
    'hypothesis',
]


this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'cmark = commonmark.cmark:main',
        ]
    },
    cmdclass={'test': Test},
    tests_require=tests_require,
)

import re
import sys
from pathlib import Path

from setuptools import setup


NAME = 'camera-calculator'
AUTHOR = 'taras.lishchenko'
EMAIL = 'taras.lishchenko@gmail.com'
URL = 'https://github.com/jackersson/camera-calculator'
DESCRIPTION = (
    'Camera-Calculator based on VidiLabs APP'
    'https://www.youtube.com/watch?v=rlod2XloxCQ&feature=youtu.be&t=23 ')


# ------------------------------------------------

def read(file):
    return Path(file).read_text('utf-8').strip()


try:
    version = re.findall(
        r"^__version__ = '([^']+)'\r?$",
        read(Path(__file__).parent / 'camera' / '__init__.py'), re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


setup_requires = []
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')


install_requires = [
    r for r in read('requirements.txt').split('\n') if r]


setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description='\n\n'.join((read('README.md'), read('CHANGES.md'))),
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='Apache 2',
    packages=['camera'],
    include_package_data=True,
    setup_requires=setup_requires,
    tests_require=['pytest'],
    test_suite="tests",
    python_requires='>=3.5',
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
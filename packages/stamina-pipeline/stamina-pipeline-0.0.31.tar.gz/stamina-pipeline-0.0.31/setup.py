from setuptools import find_packages, setup
from app.stamina.src.core.constants import STM_VERSION, STM_PACKAGE_NAME

with open('app/Readme.md', 'r') as f:
    long_description = f.read()

setup(
    name=STM_PACKAGE_NAME,
    version=STM_VERSION,
    description='A pipeline tool for VFX artists.',
    package_dir={'':'app'},
    packages=find_packages(where='app'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/costagliola-quentin/stamina',
    author='QuentinCostagliola',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=['userpaths', 'PySide2'],
    extra_require={
        'dev': ['twine>=4.0.2']
    },
    python_requires='>=3.7'
)
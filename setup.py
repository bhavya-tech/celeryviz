from setuptools import setup, find_packages

def get_requirements():
    return open('./requirements.txt').read().splitlines()

classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

setup(
    name='celeryviz',
    description= "A gui based celery flower",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version='0.0.0a',
    classifiers=classifiers,
    author = "Bhavya",
    packages=find_packages(),
    package_dir={'celeryviz': 'celeryviz'},
    package_data={'celeryviz': ['static/*']},
    install_requires=get_requirements(),
    entry_points={
        'celery.commands': [
            'celeryviz = celeryviz.command:celeryviz',
        ],
    },
)
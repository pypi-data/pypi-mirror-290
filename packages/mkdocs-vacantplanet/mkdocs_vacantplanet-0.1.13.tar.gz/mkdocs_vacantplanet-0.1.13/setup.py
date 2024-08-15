from setuptools import find_packages, setup

VERSION = '0.1.13'

with open('README.md', 'rt', encoding='utf8') as f:
    README = f.read()

setup(
    name='mkdocs-vacantplanet',
    version=VERSION,
    url='https://github.com/vacantplanet/mkdocs-theme',
    license='MIT',
    description='Default mkdocs theme for VacantPlanet projects',
    long_description=README,
    long_description_content_type='text/markdown',
    author='ebene fünf GmbH',
    author_email='vacantplanet@ebenefuenf.de',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mkdocs>=1.3',
        'mkdocs-macros-plugin>=0.7',
        'pymdown-extensions>=10.3',
    ],
    entry_points={
        'mkdocs.themes': [
            'vacantplanet = theme',
        ]
    },
    zip_safe=False,
)

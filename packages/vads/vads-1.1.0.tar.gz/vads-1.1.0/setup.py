from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='vads',
    version='1.1.0',
    license='MIT License',
    author='Rafael Reis Barreto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rafinhareis17@gmail.com',
    keywords='nanosurf',
    description=u'Visualizacao de dados arpes Sirius',
    packages=['vads'],
    install_requires=['numpy','scipy','matplotlib','ipywidgets'],)
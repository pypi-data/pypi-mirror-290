# Criando
from setuptools import setup, find_packages

setup(
    name='tomtom',  # Nome como aparecerá no pip
    version='1.1.2',             # Versão atual
    packages=find_packages(),    # Encontra automaticamente os pacotes de código
    install_requires=[           # Lista de dependências (outros pacotes necessários)
        'numpy', 
        'scipy', 
        'matplotlib',
        'pandas',
        'scikit-learn', 
        'statsmodels', 
        'librosa',
        'soundfile',
        'IPython',
        'plotly',
        'seaborn',
        'notebook',
        'jupyter'
    ],
    author='Carlos Eduardo Leal de Castro',
    author_email='lealdecastro@gmail.com',
    description='Funções para tese de doutorado. Em breve mais.',
    long_description=open('README.md').read(),  # Lê a descrição do README (se existir)
    long_description_content_type='text/markdown',
    url='https://github.com/carloselcastro/tomtom.git',  # Link para o repositório
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
],
)

from setuptools import setup, find_packages

setup(
    name='pathobs',
    version='0.1.7',
    description='Pacote para criar e analisar cenários geométricos.',
    author='Marcelo Torres',
    author_email='marcelotores21@gmail.com',
    url='https://github.com/marcelotores',
    packages=find_packages(),  # Isso inclui automaticamente todos os pacotes/subpacotes
    install_requires=[
        'shapely',
        'matplotlib',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

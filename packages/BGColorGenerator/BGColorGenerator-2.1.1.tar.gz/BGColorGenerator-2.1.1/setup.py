from setuptools import setup, find_packages

setup(
    name='BGColorGenerator',  
    version='2.1.1',
    packages=['BGColorGenerator', 'BGColorGenerator.utils'],  # Encuentra automáticamente todos los paquetes
    include_package_data=True,
    install_requires=[
        'tensorflow>=2.0.0',
        'matplotlib',
        'pandas',
        'numpy'
    ],
    package_data={
        'BGColorGenerator': ['**/*'],
    },
    description='A package for predicting the background color based on text color using a trained neural network.',
    long_description=open('README_updated.md').read(),
    long_description_content_type='text/markdown',
    author='Joaquín Francisco Solórzano Corea',
    author_email='joaquinscorea@gmail.com',
    url='https://github.com/joaquinsc999/BGColorGenerator',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

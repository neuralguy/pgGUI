from setuptools import setup, find_packages

setup(
    name='pgUltGUI',
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'pygame-ce',
        'numpy'
    ],
    author='NeuralGuy',
    author_email='neuralguyy@gmail.com',
    description='Lightweight library for easy creation and use of GUI elements in pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/neuralguy/pgGUI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

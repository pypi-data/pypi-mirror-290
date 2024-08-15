from setuptools import setup, find_packages

setup(
    name='sw_extrapolation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    description='A package to extrapolate forward rates using the Smith-Wilson method.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sw_extrapolation',
    author='Kilian de Ridder',
    author_email='your.email@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

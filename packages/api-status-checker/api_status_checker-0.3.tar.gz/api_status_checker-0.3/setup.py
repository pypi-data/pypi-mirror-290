from setuptools import setup, find_packages

with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='api_status_checker',
    version='0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'api-status-checker=api_status_checker.__main__:main',
        ],
    },
    author='Diego Saavedra',
    author_email='dsaavedra88@gmail.com',
    description='Un paquete para verificar el estado de una API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/statick88/api_status_checker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    options={
        'egg_info': {
            'egg_base': 'src'
        }
    },
    python_requires='>=3.12',
)
from setuptools import setup, find_packages

from viceroy import __version__

setup(
    name='viceroy',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/ojii/viceory',
    license='BSD',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    description='',
    install_requires=[
        'selenium!=2.49.0',
        'slimit',
    ],
    tests_require=[
        'Django',
        'flask-testing',
        'flask',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

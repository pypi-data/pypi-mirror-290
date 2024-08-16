from pydoc import plain

from setuptools import setup, find_packages

__VERSION__ = '0.0.1'


requirements = [
    'mouse==0.7.1'
]

build_requirements = requirements + ['build', 'twine']

test_requirements = requirements + []

dev_requirements = test_requirements + []

setup(
    name='sat_mouse_mover',
    version=__VERSION__,
    description="This script will move the mouse for you",
    long_description="""
        MS Teams changes your online status after certain minutes, which is kinda annoying. 
        This script will move the mouse for you, when you are not at the desk, 
        this script will move the mouse for you, to keep you online in Teams or some other Messengers. ;-)
    """,
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'build': build_requirements,
        'test': test_requirements,
        'dev': dev_requirements,
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'sat_mouse_mover = main:start',
        ],
    },
)

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'message_on_change'
LONG_DESCRIPTION = 'A programm, that notifie the user when the contents of an url are changed.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    entry_points={
        'console_scripts': [
            'message_on_change = cli',
        ],
    },

    name="message_on_change",
    version=VERSION,
    author="Rūdolfs Driķis",
    author_email="drikisr@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'playsound'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'message_on_change'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)
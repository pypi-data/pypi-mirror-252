from setuptools import setup

setup(
    name='bluidmason',
    version='0.0.1',
    author="Abhishek Chaudhary",
    author_email="abhishek20144047@gmail.com",
    license='MIT',
    description="A command-line tool for generating scaffolding projects with different configurations. ",
    long_description="BuildMason is a command-line tool for generating Flask projects with different configurations. It currently supports creating a basic Flask project, a Flask REST API project, and a Flask project with Blueprints.",
    keywords='cli abhishek chaudhary flask project development software blueprint',
    url='https://github.com/Worm4047/BuildMason',
    py_modules=['buildmason'],
    install_requires=['Click', 'cookiecutter', ],
    entry_points={
        'console_scripts': [
            'buildmason = buildmason.app:cli'
        ]
    },
)
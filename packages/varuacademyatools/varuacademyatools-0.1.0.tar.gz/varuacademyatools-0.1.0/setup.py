from setuptools import setup, find_packages

setup(
    name='varuacademyatools',
    version='0.1.0',
    author='Vaaru Academy',
    author_email='vaaruacademy@gmail.com',
    description='This is a package created to includes tools used by Students of Vaaru Academy',
    packages=find_packages(),
    py_modules=['vacalc','vawelcome'],
    license="MIT",
)
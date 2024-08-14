from setuptools import setup, find_packages

setup(name='hnt_sap_notify_library',
    version='0.0.1',
    license='MIT License',
    author='Pepe',
    keywords='notity',
    description=u'Lib to access sap gui to run transactions',
    packages=find_packages(),
    package_data={'hnt_sap_notify': ['common/*', 'notity/*']},
    install_requires=[
    'python-dotenv',
    'robotframework-sapguilibrary',
    ])
from setuptools import setup


setup(
    name='salure_helpers_ftp',
    version='2.2.0',
    description='FTP wrapper from Salure',
    long_description='FTP wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.ftp"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'requests>=2,<=3',
        'paramiko>=2,<=4',
        'pysftp>0.2,<1'
    ],
    zip_safe=False,
)
from setuptools import setup
release_version = '1.0.1'

setup(
    name='perfecto-py3-ps',
    packages=['perfecto','perfecto/client', 'perfecto/Exceptions', 'perfecto/model', 'perfecto/test'],  # this must be the same as the name above
    package_data = {'': ['*.txt']},
	version=release_version,
    License='OSI Approved :: Apache Software License Classifier',
    Description='Perfecto PS customized Reporting SDK for Python\nPerfecto Reporting is a multiple execution digital report',
    author='Perfecto',
    author_email='perfecto@perfectomobile.com',
    url='https://github.com/PerfectoMobileSA/reporting-python3-sdk-ps.git',  # use the URL to the GitHub repo
    download_url='https://github.com/PerfectoMobileSA/reporting-python3-sdk-ps.git',
    keywords=['Perfecto', 'PerfectoMobile', 'Reporting', 'Selenium', 'Appium', 'Automation testing'],
    classifiers=[ 'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent']
)
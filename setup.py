from ez_setup import use_setuptools
use_setuptools()

from datetime import datetime

#from distutils.core import setup
from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt')

now = datetime.now()
isof = now.isoformat()
# 2014-01-12T15:25:00.123
# 12345678901234567890123
dt = isof[5:7]+isof[8:10]
tm = isof[11:13]+isof[14:16]
dttm = dt+'-'+tm
VERSION = '9.9.9'
with open('VERSION') as V:
    FILEVERS = V.read()
    FVERS = FILEVERS[:5]
    VERSION = VERSION if (FILEVERS > VERSION) else FVERS 

VERSION = VERSION+'-'+dttm
LIT_LICENSE = 'LIT_LICENSE'
with open('LIT_LICENSE') as LL:
    LLIC = LL.read()
    if len(LLIC) > 20: LIT_LICENSE = LLIC
    print 'LIT_LICENSE:'+ LIT_LICENSE

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

# print 'start ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
# print reqs
# print 'end ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'

setup(
    name='shelder',
    version=VERSION,
    packages=['shelder'],

    package_dir={'': 'src'},
    data_files = [
        ('shelder', ['LIT_LICENSE', 'requirements.txt', 'ez_setup.py']),
    ],
    author='Jon Crowell',
    author_email='dev@literatelabs.com',
    url='shelder.literatelabs.com',
    description='Selenium Shell Spider',
    license=LIT_LICENSE,
    platforms=[],
    install_requires = reqs,
    long_description="""
        Shelder is a library to enable Scrapy to be used with Selenium.  It
        provides a command-line shell for configuring, exploring, and driving
        live crawlers from within their Selenium browser context.
        """
    )





# http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool

# from pip.req import parse_requirements did not work for me and
# I think it's for the blank lines in my requirements.txt, but
# this function does work

# def parse_requirements(requirements):
#     with open(requirements) as f:
#         return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

# reqs = parse_requirements(<requirements_path>)

# setup(
#     ...
#     install_requires=reqs,
#     ...
# )

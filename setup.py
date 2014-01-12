#from distutils.core import setup
from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('./requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

print 'start ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
print reqs
print 'end ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'

setup(
    name='shelder',
    version='0.1.9',
    packages=['shelder'],
    package_dir={'shelder': 'shelder'},
    package_data={'shelder': ['LIT_LICENSE']},
    author='Jon Crowell',
    author_email='dev@literatelabs.com',
    url='literatelabs.com',
    description='Selenium Shell Spider',
    license='LIT_LICENSE',
    platforms=[],
    install_requires = reqs
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

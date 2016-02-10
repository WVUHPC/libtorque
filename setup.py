
from setuptools import setup, find_packages

setup(
    name = 'libtorque',
    version = '1.2.1',

    description = 'Class for creating efficient qsub torque submitfilters',
    author = 'Nathan Gregg, M Carlise'
    author_email = 'negregg@mail.wvu.edu, mcarlise@mail.wvu.edu',
    license = 'GPLv3+',

    classifiers = [ 'Development Status :: 3 - Alpha',
                    '''License :: OSI Approved ::
                    GNU General Public License v3 or later (GPLv3+)''',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    ], # classifiers

    keywords = 'qsub, torque, moab',
    packages = find_packages (),

    test_suite = 'nose2.collector.collector',

) # setup ()

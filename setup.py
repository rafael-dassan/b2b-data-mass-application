import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='b2b-data-mass-application',
     version='0.1',
     author="BEES Force Team",
     description="BEES Data mass cloning from PRD to QAI or UAT",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://ab-inbev.visualstudio.com/GHQ_B2B_Delta/_git/b2b-data-mass-application",
     packages=setuptools.find_packages(),
     package_data={'data_mass': ['data/*.json',
                                 'mass_populator/country/data/*.csv'
                                 'mass_populator/country/data/ar/*.csv',
                                 'mass_populator/country/data/br/*.csv',
                                 'mass_populator/country/data/ca/*.csv',
                                 'mass_populator/country/data/co/*.csv',
                                 'mass_populator/country/data/do/*.csv',
                                 'mass_populator/country/data/ec/*.csv',
                                 'mass_populator/country/data/mx/*.csv',
                                 'mass_populator/country/data/pa/*.csv',
                                 'mass_populator/country/data/pe/*.csv',
                                 'mass_populator/country/data/py/*.csv',
                                 'mass_populator/country/data/ar/*.csv']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
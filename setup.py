import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='b2b-data-mass-application',
     version='0.1',
     scripts=[],
     packages=['data-mass'],
     package_dir={'data-mass': 'data-mass'},
     author="BEES Force Team",
     author_email="",
     description="BEES Data mass cloning from PRD to QAI or UAT",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://ab-inbev.visualstudio.com/GHQ_B2B_Delta/_git/b2b-data-mass-application",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
# from setuptools import setup, find_packages

# setup(
#     author="practice1",
#     description="for pactice",
#     name="packtest1", # this is the name of the package when using "pip install packtest1". when importing, "import test_pack" (the actual directory names). (refer to for_test_of_deployment)
#     packages=find_packages(['test_pack', 'test_pack.*']),
#     version="0.0.1",
#     #data_files=[('', ['LICENSE', 'README.md'])],
#     #include_package_data=True,
#     install_requires = ['numpy >=1.10', 'pandas'] # this better cover as many versions as possible (different from requirements.txt, which is "exact" version of installation via "pip freeze > requirements.txt", then install via "pip install -r requirements.txt")
# )



from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.md') as history_file:
#     history = history_file.read()

setup(
    author="All credit to you",
    author_email='you@chapter4.com',
    description="A package for converting between imperial unit lengths and weights.",
    name='packtest1',
    packages=find_packages(include=['test_pack', 'test_pack.*']),
    version='0.0.1',
    install_requires=['numpy>=1.10', 'pandas'],
    #python_requires="==3.6.*",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='test pack',    
    #zip_safe=False,
)

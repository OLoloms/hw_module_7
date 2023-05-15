from setuptools import setup, find_namespace_packages

setup(
    name='Clean Folder',
    version='0.0.1',
    description='Folder sorter by Python',
    url='http://github.com/dummy_user/useful',
    author='Sergij Tsapkov',
    author_email='prostotsapkov@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["cleanfolder=clean_folder.clean:clean"]}
)
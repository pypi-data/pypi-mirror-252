from setuptools import find_packages, setup
setup(
    name='mt5linux-tc',
    packages=find_packages(include=['mt5linux-tc']),
    version='0.2.1',
    description='MetaTrader5 for linux users',
    long_description=open('README.md','r').read(),
    long_description_content_type='text/markdown',
    author='Lucas Prett Campagna',
    license='MIT',
    url = 'https://github.com/Traders-Connect/mt5linux-tc',
    install_requires=open('requirements.txt','r').read().split('\n'),
    setup_requires=[],
    tests_require=[],
    test_suite='tests',
)

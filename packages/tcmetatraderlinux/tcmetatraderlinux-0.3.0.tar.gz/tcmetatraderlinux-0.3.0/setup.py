from setuptools import find_packages, setup
setup(
    name='tcmetatraderlinux',
    packages=find_packages(include=['tcmetatraderlinux']),
    version='0.3.0',
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

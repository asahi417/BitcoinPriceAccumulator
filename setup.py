from setuptools import setup, find_packages

FULL_VERSION = '0.0.0'

with open('README.md') as f:
    readme = f.read()

setup(
    name='btc_price',
    version=FULL_VERSION,
    description='BTC price accumulator',
    long_description=readme,
    author='Asahi Ushio',
    author_email='asahi1992ushio@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'sqlalchemy',
        'pandas',
        'numpy',
        'psycopg2',
        'psycopg2-binary',
        # 'matplotlib',
        'toml',
        'slackweb',
        'pytz'
    ],
    # dependency_links=[
    #     'git+https://github.com/matplotlib/mpl_finance.git'
    #     # 'git+https://github.com/yagays/pybitflyer.git'
    # ]
)
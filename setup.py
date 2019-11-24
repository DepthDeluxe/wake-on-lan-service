from setuptools import setup, find_packages

test_dependencies = [
    'pytest >= 5.3.0'
]

setup(
    name='wol-service',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'flask >= 1.1.1',
        'flask-sqlalchemy >= 2.4.1',
        'get-mac >= 0.8.1',
        'sqlalchemy >= 1.3.11',
        'wakeonlan >= 1.1.6'
   ],
   tests_require=test_dependencies,
   extras_require={
       'test': test_dependencies
   }
)
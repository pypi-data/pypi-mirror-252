from setuptools import setup

setup(name='awslambdatools',
      version="0.0.1",
      description='Package for dealing with lambdas running on Python',
      author='Edward Velo',
      author_email='vattico@gmail.com',
      packages=['awslambdatools'],
      install_requires=['boto3','botocore','logging',
                        'dateutil','jmespath','s3transfer','urllib'],
      python_requires='>=3.6')
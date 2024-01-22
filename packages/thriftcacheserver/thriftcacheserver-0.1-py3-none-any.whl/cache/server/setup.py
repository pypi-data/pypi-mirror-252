from setuptools import setup

setup(name='thriftcacheserver',
      version='0.1',
      description='A cache server using thrift',
      url='https://github.com/codophobia/key-value-cache-thrift-python',
      author='Shivam Mitra',
      author_email='shivamm389@gmail.com',
      license='APACHE',
      packages=['server'],
      install_requires=[
          'thrift',
      ],
      zip_safe=False)
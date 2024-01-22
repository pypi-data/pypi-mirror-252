from setuptools import setup, find_packages

setup(name='thriftcacheserver',
      version='0.1',
      description='A cache server using thrift',
      url='https://github.com/codophobia/key-value-cache-thrift-python',
      entry_points={
        'console_scripts': [
            'thriftcacheserver = cache.__main__:main',
        ]
      },
      author='Shivam Mitra',
      author_email='shivamm389@gmail.com',
      license='APACHE',
      packages=find_packages(),
      install_requires=[
          'thrift',
      ],
      zip_safe=False)
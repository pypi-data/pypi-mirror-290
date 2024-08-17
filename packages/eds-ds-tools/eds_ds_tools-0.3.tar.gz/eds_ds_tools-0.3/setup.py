from setuptools import setup

setup(name='eds_ds_tools',
      version='0.3',
      description='tools for data science',
      packages=['eds_ds_tools'],
      author_email='wenleicao@gmail.com',
      zip_safe=False,
      install_requires=[      
      'boto3', 'botocore', 'numpy', 'pandas', 'pytz', 'requests', 'fastparquet', 'psycopg2', 'pymssql', 'sqlalchemy', 'teradata'
      ]
      )

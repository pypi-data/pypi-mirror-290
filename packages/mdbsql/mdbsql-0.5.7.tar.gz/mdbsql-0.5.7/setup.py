from distutils.core import setup
# import setuptools

packages = ['mdbsql']
setup(name='mdbsql',
      version='0.5.7',
      author='xigua, ',
      author_email="2587125111@qq.com",
      url='https://pypi.org/project/mdbsql',
      long_description='''
      世界上最庄严的问题：我能做什么好事？
      ''',
      packages=packages,
      package_dir={'requests': 'requests'},
      license="MIT",
      python_requires='>=3.6',
      )

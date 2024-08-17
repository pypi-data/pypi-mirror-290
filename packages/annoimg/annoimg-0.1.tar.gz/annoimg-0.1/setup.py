from setuptools import setup

setup(name='annoimg',
      version='0.1',
      description='Semi-auto annotation images using SAM2',
      packages=['annoimg'],
      author_email='aleksandr.bakhshiev@compvisionsys.com',
      zip_safe=False,
      entry_points = {
              'console_scripts': [
                  'command-name = package.label:__main__',
              ],
          })
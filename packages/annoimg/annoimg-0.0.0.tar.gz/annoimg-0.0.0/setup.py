from pathlib import Path
from setuptools import setup


def get_install_requires() -> list[str]:
    file_name = Path(__file__).parent / 'requirements.txt'
    targets = []
    if file_name.exists():
        with open(file_name, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(name='annoimg',
      version='0.0.0',
      description='Semi-auto annotation images using SAM2',
      install_requires=get_install_requires(),
      packages=['annoimg'],
      author_email='aleksandr.bakhshiev@compvisionsys.com',
      zip_safe=False,
      scripts=['bin/annoimg-annotate', 'bin/annoimg-label', 'bin/annoimg-convert-cvat'],
      package_data={'': ['cvat1.1_template.xml']},
      include_package_data=True)


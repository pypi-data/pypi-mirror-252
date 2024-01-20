from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='AioKeksik',
      version='1.2',
      url='https://github.com/Obnovlator3000/AioKeksik',
      license='MIT',
      description='Неофициальная асинхронная библиотека для работы с API https://keksik.io',
      packages=['AioKeksik'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Obnovlator3000',
      install_requires=['aiohttp', 'ujson'],
      author_email='obnovlator3000@lisi4ka.ru',
      zip_safe=False)
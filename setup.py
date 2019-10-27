import setuptools

setuptools.setup(name='sheenroo_algs',
                 version='1.0',
                 description='Ein Python-Modul für verschiedene Algorithmen',
                 url='https://github.com/xinru1414/sheenroo_algs',
                 author='SheenRoo die chinesische Prinzessin',
                 author_email='xinru1414@gmail.com',
                 tests_require=['pytest'],
                 setup_requires=['pytest-runner'],
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

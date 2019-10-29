import setuptools


extras_require={'allennlp': ['allennlp']}

test_require = ['pytest']

for extras in extras_require.values():
    test_require.extend(extras)



setuptools.setup(name='sheenroo_algs',
                 version='1.0',
                 description='Ein Python-Modul für verschiedene Algorithmen',
                 url='https://github.com/xinru1414/sheenroo_algs',
                 author='SheenRoo die chinesische Prinzessin',
                 author_email='xinru1414@gmail.com',
                 tests_require=test_require,
                 setup_requires=['pytest-runner'],
                 extras_require=extras_require,
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

from setuptools import find_packages, setup

setup(
    name='tinymessages',
    version='0.1.0',
    author='Michael Lamertz',
    author_email='michael.lamertz@gmail.com',
    url='https://github.com/dickerdackel/tinymessages',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ ],
    entry_points={
        'console_scripts': [
            'broker-demo = tinymessages.broker_demo:main',
            'relay-demo = tinymessages.relay_demo:main',
        ],
    },
)

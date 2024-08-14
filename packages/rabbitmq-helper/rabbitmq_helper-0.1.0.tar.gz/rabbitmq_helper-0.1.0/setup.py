from setuptools import setup, find_packages

setup(
    name='rabbitmq_helper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pika'],
    author='Barretão',
    author_email='pedroautomacao@hotmail.com',
    description='Uma biblioteca para facilitar as configurações de RabbitMQ',
    long_description=open('README').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/frexco-digital/rabbitmq_helper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
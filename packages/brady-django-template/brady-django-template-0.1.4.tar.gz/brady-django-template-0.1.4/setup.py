from setuptools import setup, find_packages

setup(
    name='brady-django-template',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True, 
    package_data={
        'brady_django_template': ['project-template/**/*'], 
    },
    install_requires=[
        'Django',
    ],
    entry_points={
        'console_scripts': [
            'brady-django-template=brady_django_template.main:create_django_project',
        ],
    },
    description='A tool to create Django projects with a custom template.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KyawKoKoTun/brady-django-template',
    author='Kyaw Ko Ko Tun',
    author_email='kyawkokotunmm475157@gmail.com',
    license='MIT',
)

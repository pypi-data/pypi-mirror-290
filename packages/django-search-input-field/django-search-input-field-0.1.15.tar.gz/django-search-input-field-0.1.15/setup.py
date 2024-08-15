from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for the long description
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='django-search-input-field',
    version='0.1.15',
    license='MIT',
    author="Mina Atef",
    author_email='mina.atef0@gmail.com',
    packages=find_packages(include=['django_search_input_field', 'django_search_input_field.*']),
    include_package_data=True,
    package_data={'django_search_input_field': ['templates/*']},
    url='https://github.com/MinaAtef1/django-search-input-form',
    description='A Django app providing a search input field.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'djangorestframework',
        # Add any package dependencies here
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
    ],
    keywords='django search input field',
    python_requires='>=3.6',
)

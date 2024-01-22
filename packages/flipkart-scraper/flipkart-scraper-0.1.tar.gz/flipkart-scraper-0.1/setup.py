from setuptools import setup, find_packages

setup(
    name='flipkart-scraper',
    version='0.1',
    author='Mutyala Durga Venu Kumar',
    author_email='thevk22@gmail.com',
    description='A Flipkart scraper for extracting product information',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mdvenukumar/flipkart-scraper',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='flipkart scraper web scraping',
    project_urls={
        'Source': 'https://github.com/mdvenukumar/flipkart-scraper',
        'Bug Reports': 'https://github.com/mdvenukumar/flipkart-scraper/issues',
    },
)

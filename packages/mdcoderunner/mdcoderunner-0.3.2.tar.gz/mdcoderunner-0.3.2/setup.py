from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

long_description = long_description.replace('assets/imgs/demo1.png',"https://github.com/SivaSankarS365/Markdown-code-runner/raw/main/assets/imgs/demo1.png")
long_description = long_description.replace('assets/imgs/demo2.png',"https://github.com/SivaSankarS365/Markdown-code-runner/raw/main/assets/imgs/demo2.png")
long_description = long_description.replace('assets/imgs/timeit.jpeg',"https://github.com/SivaSankarS365/Markdown-code-runner/raw/main/assets/imgs/timeit.jpeg")

setup(
    name='mdcoderunner',
    version='0.3.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jinja2==3.1.3',
    ],
    entry_points={
        'console_scripts': ['mdcoderunner=mdcoderunner.api:main'],
    },
    author='Siva Sankar Sajeev',
    author_email='sivasankars365@gmail.com',
    description='A tool for running code blocks in Markdown files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SivaSankarS365/Markdown-code-runner',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
from setuptools import setup, find_packages

setup(
    name='salaar',
    version='1.1.1.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # If your package includes any command-line scripts, list them here
        ],
    },
    author='jagilam kumar chandra',
    author_email='jagilamkumar@gmail.com',
    description='this is the library to know salaar movie khannsaar relations and vote-count of the particular persons use names as "dhaara", "devaratha_raisaar", "shiva_mannar", "raja_mannar", "varadha_raj_mannar" baachi", "rudra", "radha_rama", "om", "narang", "vishnu", baarava"      and   use tribe names as shouryaanga, mannar, ghaniyar if you want get the vote count first specify tribe and second argument as a name of the person',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

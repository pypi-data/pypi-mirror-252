from setuptools import setup, find_packages

setup(
    name='salaar',
    version='1',  # Update with your version number
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add any console scripts here if needed
        ],
    },
    author='jagilam kumar chandra',
    author_email='jagilamkumar@gmail.com',
    description='this is the library to know salaar movie khannsaar relations and vote-count of the particular persons use names as "dhaara", "devaratha_raisaar", "shiva_mannar", "raja_mannar", "varadha_raj_mannar" baachi", "rudra", "radha_rama", "om", "narang", "vishnu", baarava"      and   use tribe names as shouryaanga, mannar, ghaniyar if you want get the vote count first specify tribe and second argument as a name of the person',
    url='',
)

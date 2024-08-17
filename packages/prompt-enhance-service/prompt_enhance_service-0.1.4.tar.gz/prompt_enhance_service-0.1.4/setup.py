from setuptools import setup, find_packages

setup(
    name='prompt_enhance_service',
    version='0.1.4',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jinka Sai Jagadeesh',
    author_email='saijagadeesh.jinka@gavstech.com',
    license='GAVS Proprietary License',  # Or another license
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'google-cloud-firestore'
        # List of dependencies e.g. 'numpy', 'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Specify your minimum Python version
)

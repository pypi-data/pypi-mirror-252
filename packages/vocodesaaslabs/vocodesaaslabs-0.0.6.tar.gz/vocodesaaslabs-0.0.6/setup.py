from setuptools import setup, find_packages

def parse_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if not line.startswith('#')]

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vocodesaaslabs',
  version='0.0.6',
  description='SaaS Labs version of Vocode',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ajeya Krishna',
  author_email='ajeya@saaslabs.co',
  license='MIT', 
  classifiers=classifiers,
  keywords='voice', 
  packages=find_packages(),
  install_requires=parse_requirements('req.txt'), 
)
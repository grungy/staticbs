from setuptools import setup

setup(name='staticbs',
      version='0.11',
      description='A simple 3D electro-magnetostatic biot-savart solving simulator',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
      ],
      url='https://github.com/grungy/staticbs',
      author='Josh Marks and Andrea Waite',
      author_email='jmarks@udel.edu',
      license='MIT',
      packages=['staticbs'],
      install_requires=['numpy', 'scipy'],
      zip_safe=False)

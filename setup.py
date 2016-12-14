from setuptools import setup

setup(name='staticbs',
      version='0.1',
      description='A simple 3D electro-magnetostatic biot-savart solving simulator',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: electromagnetics :: magnetics :: biot-savart :: magnetic field :: simulator',
      ],
      url='https://github.com/grungy/staticbs',
      author='Josh Marks and Andrea Waite',
      author_email='jmarks@udel.edu',
      license='MIT',
      packages=['staticbs'],
      install_requires=['numpy', 'scipy'],
      zip_safe=False)

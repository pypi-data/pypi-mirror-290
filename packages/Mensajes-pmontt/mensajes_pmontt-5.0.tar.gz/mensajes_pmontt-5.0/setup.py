from setuptools import setup, find_packages

setup(
    name='Mensajes-pmontt',
    version='5.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pedro Montt Pacheco',
    author_email='p-montt@hotmail.com',
    url='https://www.hektor.dev',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() 
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Environment :: Console :: Framebuffer',
        'Environment :: Console :: Newt',
        'Environment :: Console :: svgalib'
    ]



)
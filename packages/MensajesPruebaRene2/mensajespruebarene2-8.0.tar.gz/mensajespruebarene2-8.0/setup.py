from setuptools import setup, find_packages

setup(
    name='MensajesPruebaRene2',
    version='8.0',
    description='Un paquete para mandar saludos y despedidas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rene Hernandez',
    author_email='renescanner97@gmail.com',
    url='https://www.renehdez.com',
    license_files=['LICENSE'],
    packages= find_packages(),
    scripts=['test.py'],
    install_requires=[paquete.strip() for paquete in open ("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)
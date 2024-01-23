from setuptools import setup, find_packages

setup(
    name='HueEngineTESTS',
    version='0.0.4',
    description='A Py-Game Engine',
    url='https://github.com/TheDotBat/Hue',
    author='Setoichi',
    author_email='setoichi.dev@gmail.com',
    license='Apache-2.0',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'pygame-ce',
        'pyautogui',
        'pygame-gui',
        'screeninfo',
        'pygetwindow'
    ],
    classifiers=[
        'Development Status :: 4 - Beta'
    ],
    entry_points={
        'console_scripts': [
            'Hue=Hue.scripts.main:main',
        ]
    },
)


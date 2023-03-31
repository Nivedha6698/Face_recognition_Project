from setuptools import setup

setup(
    name='Face-recognition',
    version='1.0',
    description='This Project has Two endpoint to capture faces and interact with Database',
    author='Nivedha',
    author_email='nivedha6698@gmail.com',
    url='https://github.com/Nivedha6698',
    install_requires=[
        'Flask',
        'opencv-python',
        'face-recognition',
        'dlib-19.22.99-cp38-cp38-win_amd64.whl'
        'pyodbc',
        'numpy',
        'sqlite3'
    ]
)

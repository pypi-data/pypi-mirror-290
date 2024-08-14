from distutils.core import setup

setup(
    name='euclidean_hausdorff',
    version='1.0.2',
    author='Vladyslav Oles',
    author_email='vlad.oles@proton.me',
    packages=['euclidean_hausdorff'],
    url='http://pypi.python.org/pypi/euclidean-hausdorff/',
    description='Approximating the Euclidean Hausdorff Distance',
    long_description=open('README.MD').read(),
    install_requires=[
        "scipy >= 1.12.0",
        "sortedcontainers >= 2.4.0",
        "tqdm >= 4.66.4",
        "numpy >= 1.26.4",
    ],
)
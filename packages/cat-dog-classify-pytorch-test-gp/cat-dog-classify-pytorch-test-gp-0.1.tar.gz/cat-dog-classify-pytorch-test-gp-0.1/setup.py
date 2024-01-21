from setuptools import setup, find_packages

setup(
   name='cat-dog-classify-pytorch-test-gp',
   version='0.1',
   description='Deep Learning Model to classify Cats and Dogs usinbg PyTorch',
   url='https://github.com/gayatriprasad/modelAsPackage',
   author='Sai Gayatri Prasad Peri',
   author_email='gayatriprasad11@gmail.com',
   license='MIT',
   packages=find_packages(),   
   install_requires=['numpy', 'torch', 'torchvision', 'torchaudio', 'pandas', 'matplotlib'],
)

from setuptools import setup, find_packages

setup(
    name='semantic_kitti_api',
    version='0.1',
    package_dir={"": "semantic-kitti-api"},
    packages=find_packages(where="semantic-kitti-api"),
    long_description="Instalacao para o uso do semantic-kitti-api",
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=[
        'numpy>=1.24.0',
        'matplotlib>=2.2.3',
        'vispy>=0.5.3',
        'torch>=1.1.0',
        'PyYAML>=5.1.1',
        'imgui[glfw]>=1.0.0',
        'glfw>=1.8.3',
        'PyOpenGL>=3.1.0',
        'pyqt5>=5.8.1.1',
    ],
    python_requires=">=3.10",
)

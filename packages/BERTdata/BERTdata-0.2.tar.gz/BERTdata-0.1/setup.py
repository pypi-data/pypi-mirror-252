from setuptools import setup, find_packages
packages = find_packages()
print(packages)
setup(
    name='BERTdata',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # 您的包的依赖项
    ],
    include_package_data=True
)

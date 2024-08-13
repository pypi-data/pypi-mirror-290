from setuptools import setup

setup(
    name='scrapy-ja3',
    version='0.1.0',
    description='Scrapy download handler for JA3 fingerprinting',
    author='ChenWei Zhao',
    author_email='chenwei.zhaozhao@gmail.com',
    license='MIT',
    packages=['scrapy_ja3'],
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'Scrapy>=2.6.0',
    ]
)

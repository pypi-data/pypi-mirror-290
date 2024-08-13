import io

from setuptools import setup


def read_file(filename):
    with open(filename) as fp:
        return fp.read().strip()


def read_rst(filename):
    # Ignore unsupported directives by pypi.
    content = read_file(filename)
    return "".join(
        line for line in io.StringIO(content) if not line.startswith(".. comment::")
    )


setup(
    name='scrapy-ja3',
    version='0.1.1',
    description='Scrapy download handler for JA3 fingerprinting',
    long_description=read_rst("README.rst") + "\n\n" + read_rst("HISTORY.rst"),
    author='ChenWei Zhao',
    author_email='chenwei.zhaozhao@gmail.com',
    license='MIT',
    packages=['scrapy_ja3'],
    keywords="scrapy-ja3",
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'Scrapy>=2.6.0',
    ]
)

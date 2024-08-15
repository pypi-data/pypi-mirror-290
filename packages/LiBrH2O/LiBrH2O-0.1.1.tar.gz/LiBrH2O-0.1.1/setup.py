from setuptools import setup

setup(
    name='LiBrH2O',
    version='0.1.1',
    py_modules=['LiBrH2O'],
    author='Rishi_Shi',
    author_email='syq.zju@gmail.com',
    url='https://github.com/syq-tju',
    description='A python library of LiBrH2O properties',

    zip_safe=False,
    # 指定安装目录，确保与 Python 3.12 解释器路径匹配
    options={
        'build': {'build_lib': 'build/lib'},
        'install': {'install_lib': 'c:\\python312\\Lib\\site-packages'}
    }  # 这里将逗号改为冒号
)

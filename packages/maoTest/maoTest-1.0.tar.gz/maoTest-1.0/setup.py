from setuptools import setup

setup(
    name='maoTest',# 需要打包的名字,即本模块要发布的名字
    version='1.0',#版本
    description='A module for test', # 简要描述
    py_modules=['myTest'],   #  需要打包的模块
    author='Mao Haotian', # 作者名
    author_email='404748294@qq.com',   # 作者邮件
    # requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
    license='MIT'
)
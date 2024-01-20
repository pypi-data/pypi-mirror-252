from setuptools import setup, find_packages

# 读取requirements.txt文件内容，并且跳过以"--"开头的行
with open('requirements.txt') as f:
    requirements = []
    for line in f:
        # 忽略以--开头的行
        if line.strip().startswith('--'):
            continue
        # 添加到requirements中
        requirements.append(line.strip())

setup(
    name='fair-GPD',  # 你的包名，需要在PyPI上唯一
    version='0.0.1',  # 当前包版本
    author='junximu',  # 你的名字或你的组织/团队的名字
    author_email='mujunxi@126.com',  # 你的电子邮件地址
    description='Graphormer Based Protein Sequence Design Package: GPD',  # 简短描述
    long_description=open('README.md').read(),  # 从README.md读取长描述
    long_description_content_type='text/markdown',  # 长描述内容的类型
    url='https://github.com/decodermu/GPD',  # 项目URL
    packages=find_packages(),  # 自动找到项目中的所有包
    install_requires=requirements,  # 依赖列表
    dependency_links=[
        'https://download.pytorch.org/whl/cu113'
        # 其他的依赖链接
    ],
    classifiers=[  # 包的分类索引信息
        'Development Status :: 3 - Alpha',  # 开发的状态，通常是'Alpha', 'Beta'或'Stable'
        'Intended Audience :: Developers',  # 目标用户
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # 许可证类型
        'Programming Language :: Python :: 3',  # 编程语言版本
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',  # 支持的Python版本
    include_package_data=True,  # 是否包含数据文件
    license='MIT',  # 许可证
    keywords='GPD',  # 包搜索关键词或标签
    # 其他参数...
)

# 注意：你需要替换your_package_name、your_script、Your Name、your.email@example.com等
# 为你项目的实际信息。


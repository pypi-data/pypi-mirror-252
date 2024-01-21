
# nonebot-plugin-aibot

_✨ NoneBot 插件简单描述 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/teressssa/nonebot-plugin-aibot.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-aibot">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-aibot.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="python">

</div>

## 📖 介绍

这里是插件的详细介绍部分

## 💿 安装



使用包管理器安装，代理源上可能没有此包，需要取消代理

```
pip config unset global.index-url
```

在虚拟环境中安装包


    source .venv/Scripts/activate
    pip install nonebot-plugin-aibot
    pip install --pre --upgrade bigdl-llm[all]
    pip install --upgrade transformers
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = [".venv/lib/nonebot-plugin-aibot/plugins"]




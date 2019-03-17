# VLC Theme ZH

这是一个简单的 Python 脚本，将 VLC 皮肤文件中的字体替换为自定义字体，主要用于添加中文字体支持。例如，对于 example.vlt 将生成 example_zh.vlt

## 用法

```shell
python vlt_zh.py [vlt 文件所在目录] [字体文件路径]
```

## 说明

vlt 文件为 tgz 或 zip 格式的压缩包，包含一个 theme.xml 索引文件和字体图片等资源文件。只需将字体文件放入文件夹内，替换 theme.xml 中的字体文件路径，重新打包即可。

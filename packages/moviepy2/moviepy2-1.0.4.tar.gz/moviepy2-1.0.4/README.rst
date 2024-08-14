#MoviePy2

本项目为 [moviepy的下游分支](https://github.com/Zulko/moviepy)

增加了对torch的支持，性能在不同的显卡提升30%～90%区间

## 性能测试如下

torch2.1.2+cu121环境下

在RTx3080显卡：示例demo从252s提升到75s，提升70%

在Rtx4080显卡：示例demo从252s提升到49s，提升83%
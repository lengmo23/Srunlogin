# Srunlogin

深澜认证登录，ZJU一键登录脚本，基于 @[谁的BUG最难改](https://blog.csdn.net/hackermengzhi "谁的BUG最难改") 脚本参照修改

References：https://blog.csdn.net/hackermengzhi/article/details/130499424



使用方法

```
python3 autologin.py
```

可配合crontab执行检测掉线

```
IP="10.10.98.98"

# 要执行的 Python 脚本路径
PYTHON_SCRIPT="/root/autologin.py"

# Ping 测试
if ! ping -c 1 $IP > /dev/null 2>&1; then
    echo "IP $IP 不通，使用autologin.py脚本..."
    /usr/bin/python3 $PYTHON_SCRIPT
else
    echo "IP $IP 可以ping通！"
fi

```



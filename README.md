# Srunlogin

深澜认证登录，ZJU一键登录脚本，基于 @[谁的BUG最难改](https://blog.csdn.net/hackermengzhi "谁的BUG最难改") 脚本参照修改

References：https://blog.csdn.net/hackermengzhi/article/details/130499424

2024.7月宿舍寝室网络结构升级，传统L2TP拨号上网还是可以使用，保证上网不中断，但是不认证的情况内网不互通、IPV6不通。因为认证系统会占用WIFI认证一个格位，多设备容易挤掉有线网的认证登录，如果使用OPENWRT,需要定期保活。可以配合crontab脚本，保证路由器不断网。

使用方法

```
python3 autologin.py
```
line12\line13\line306需要修改

可配合crontab执行autologin.sh检测掉线

```
IP="10.10.98.98"
PYTHON_SCRIPT="/root/autologin.py"

if ! ping -c 1 $IP > /dev/null 2>&1; then
    echo "IP $IP 不通，使用autologin.py脚本..."
    /usr/bin/python3 $PYTHON_SCRIPT
else
    echo "IP $IP 可以ping通！"
fi

```


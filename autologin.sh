IP="10.10.98.98"
PYTHON_SCRIPT="/root/autologin.py"

if ! ping -c 1 $IP > /dev/null 2>&1; then
    echo "IP $IP 不通，使用autologin.py脚本..."
    /usr/bin/python3 $PYTHON_SCRIPT
else
    echo "IP $IP 可以ping通！"
fi


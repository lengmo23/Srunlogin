#coding=utf-8
import ctypes
import hashlib
import json
import math
import random
import socket
import time
import requests

local_ip='private ip' #内网IP
username = 'id' #学号
password = 'passwd' #密码
init_url="https://net.zju.edu.cn"

class MD5(object):

    '''MD5加密//根据js'''
    def a(self, n):
        r = ''
        e = 32 * len(n)
        for i in range(0,e,8):
            r += chr((n[i >> 5] >> i % 32 & 0xffffffff >> i % 32) & 255)
        return r

    def d(self, n):
        r = [0 for _ in range(len(n) >> 2)]
        e = 8 * len(n)
        for i in range(0,e,8):
            if i >> 5 == len(r):
                r.append(0)
            r[i >> 5] |= ctypes.c_int32((255 & ord(n[i // 8])) << i % 32).value
        return r

    def t(self, n, t):
        r = (65535 & n) + (65535 & t)
        a = ctypes.c_int32(n >> 16).value
        b = ctypes.c_int32(t >> 16).value
        c = ctypes.c_int32(r >> 16).value
        d = ctypes.c_int32(a + b + c << 16).value
        return d | 65535 & r

    def r(self, n, t):
        return ctypes.c_int32(n << t).value | (n >> 32 - t & 0xffffffff >> 32 - t)

    def e(self, n, e, o, u, c, f):
        return self.t(self.r(self.t(self.t(e, n), self.t(u, f)), c), o)

    def o(self, n, t, r, o, u, c, f):
        return self.e(t & r | ~t & o, n, t, u, c, f)

    def u(self, n, t, r, o, u, c, f):
        return self.e(t & o | r & ~o, n, t, u, c, f)

    def c(self, n, t, r, o, u, c, f):
        return self.e(t ^ r ^ o, n, t, u, c, f)

    def f(self, n, t, r, o, u, c, f):
        return self.e(r ^ (t | ~o), n, t, u, c, f)

    def i(self, n, r):
        x = 14 + (r + 64 >> 9 << 4) + 1
        n.extend([0 for _ in range(x - len(n))])
        n[-1] = r
        n[r >> 5] |= ctypes.c_int32(128 << r % 32).value
        l = 1732584193
        g = -271733879
        v = -1732584194
        m = 271733878
        for j in range(0,len(n),16):
            if j + 15 >= len(n):
                x = j + 15 - len(n) + 1
                for _ in range(x):
                    n.append(0)
            i = l
            a = g
            d = v
            h = m
            l = self.o(l, g, v, m, n[j], 7, -680876936)
            m = self.o(m, l, g, v, n[j + 1], 12, -389564586)
            v = self.o(v, m, l, g, n[j + 2], 17, 606105819)
            g = self.o(g, v, m, l, n[j + 3], 22, -1044525330)
            l = self.o(l, g, v, m, n[j + 4], 7, -176418897)
            m = self.o(m, l, g, v, n[j + 5], 12, 1200080426)
            v = self.o(v, m, l, g, n[j + 6], 17, -1473231341)
            g = self.o(g, v, m, l, n[j + 7], 22, -45705983)
            l = self.o(l, g, v, m, n[j + 8], 7, 1770035416)
            m = self.o(m, l, g, v, n[j + 9], 12, -1958414417)
            v = self.o(v, m, l, g, n[j + 10], 17, -42063)
            g = self.o(g, v, m, l, n[j + 11], 22, -1990404162)
            l = self.o(l, g, v, m, n[j + 12], 7, 1804603682)
            m = self.o(m, l, g, v, n[j + 13], 12, -40341101)
            v = self.o(v, m, l, g, n[j + 14], 17, -1502002290)
            g = self.o(g, v, m, l, n[j + 15], 22, 1236535329)
            l = self.u(l, g, v, m, n[j + 1], 5, -165796510)
            m = self.u(m, l, g, v, n[j + 6], 9, -1069501632)
            v = self.u(v, m, l, g, n[j + 11], 14, 643717713)
            g = self.u(g, v, m, l, n[j], 20, -373897302)
            l = self.u(l, g, v, m, n[j + 5], 5, -701558691)
            m = self.u(m, l, g, v, n[j + 10], 9, 38016083)
            v = self.u(v, m, l, g, n[j + 15], 14, -660478335)
            g = self.u(g, v, m, l, n[j + 4], 20, -405537848)
            l = self.u(l, g, v, m, n[j + 9], 5, 568446438)
            m = self.u(m, l, g, v, n[j + 14], 9, -1019803690)
            v = self.u(v, m, l, g, n[j + 3], 14, -187363961)
            g = self.u(g, v, m, l, n[j + 8], 20, 1163531501)
            l = self.u(l, g, v, m, n[j + 13], 5, -1444681467)
            m = self.u(m, l, g, v, n[j + 2], 9, -51403784)
            v = self.u(v, m, l, g, n[j + 7], 14, 1735328473)
            g = self.u(g, v, m, l, n[j + 12], 20, -1926607734)
            l = self.c(l, g, v, m, n[j + 5], 4, -378558)
            m = self.c(m, l, g, v, n[j + 8], 11, -2022574463)
            v = self.c(v, m, l, g, n[j + 11], 16, 1839030562)
            g = self.c(g, v, m, l, n[j + 14], 23, -35309556)
            l = self.c(l, g, v, m, n[j + 1], 4, -1530992060)
            m = self.c(m, l, g, v, n[j + 4], 11, 1272893353)
            v = self.c(v, m, l, g, n[j + 7], 16, -155497632)
            g = self.c(g, v, m, l, n[j + 10], 23, -1094730640)
            l = self.c(l, g, v, m, n[j + 13], 4, 681279174)
            m = self.c(m, l, g, v, n[j], 11, -358537222)
            v = self.c(v, m, l, g, n[j + 3], 16, -722521979)
            g = self.c(g, v, m, l, n[j + 6], 23, 76029189)
            l = self.c(l, g, v, m, n[j + 9], 4, -640364487)
            m = self.c(m, l, g, v, n[j + 12], 11, -421815835)
            v = self.c(v, m, l, g, n[j + 15], 16, 530742520)
            g = self.c(g, v, m, l, n[j + 2], 23, -995338651)
            l = self.f(l, g, v, m, n[j], 6, -198630844)
            m = self.f(m, l, g, v, n[j + 7], 10, 1126891415)
            v = self.f(v, m, l, g, n[j + 14], 15, -1416354905)
            g = self.f(g, v, m, l, n[j + 5], 21, -57434055)
            l = self.f(l, g, v, m, n[j + 12], 6, 1700485571)
            m = self.f(m, l, g, v, n[j + 3], 10, -1894986606)
            v = self.f(v, m, l, g, n[j + 10], 15, -1051523)
            g = self.f(g, v, m, l, n[j + 1], 21, -2054922799)
            l = self.f(l, g, v, m, n[j + 8], 6, 1873313359)
            m = self.f(m, l, g, v, n[j + 15], 10, -30611744)
            v = self.f(v, m, l, g, n[j + 6], 15, -1560198380)
            g = self.f(g, v, m, l, n[j + 13], 21, 1309151649)
            l = self.f(l, g, v, m, n[j + 4], 6, -145523070)
            m = self.f(m, l, g, v, n[j + 11], 10, -1120210379)
            v = self.f(v, m, l, g, n[j + 2], 15, 718787259)
            g = self.f(g, v, m, l, n[j + 9], 21, -343485551)
            l = self.t(l, i)
            g = self.t(g, a)
            v = self.t(v, d)
            m = self.t(m, h)
        return [l, g, v, m]

    def l(self, n, t):
        o = self.d(n)
        u = [0 for _ in range(16)]
        c = [0 for _ in range(16)]
        if len(o) > 16:
            o = self.i(o, 8 * len(n))
        for j in range(16):
            u[j] = 909522486 ^ o[j]
            c[j] = 1549556828 ^ o[j]
        u.extend(self.d(t))
        e = self.i(u, 512 + 8 * len(t))
        c.extend(e)
        r = self.a(self.i(c, 640))
        return r

    def s(self, n, t):
        return self.l(n, t)

    def g(self, n):
        d = list('0123456789abcdef')
        e = []
        for c in list(n):
            c = ord(c)
            e.append(d[c >> 4 & 15])
            e.append(d[15 & c])
            r = ''.join(e)
        return r

    def C(self, n, t):
        return self.g(self.s(n, t))

    def __call__(self, password, token):
        return self.C(token, password)
class BASE64:
    #js:atob() base64加密
    def __init__(self):
        self.base64Alpha = 'LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA'

    def encode(self, s):
        r = []
        x = len(s) % 3
        if x:
            s = s + '\0'*(3 - x)
        for i in range(0,len(s),3):
            d = s[i:i+3]
            a = ord(d[0]) << 16 | ord(d[1]) << 8 | ord(d[2])
            r.append(self.base64Alpha[a>>18])
            r.append(self.base64Alpha[a>>12 & 63])
            r.append(self.base64Alpha[a>>6 & 63])
            r.append(self.base64Alpha[a & 63])
        if x == 1:
            r[-1] = '='
            r[-2] = '='
        if x == 2:
            r[-1] = '='
        return ''.join(r)
def getTime():
    #取时间 等同于js里面的 Date.toValue()
    t = time.time()
    return int(round(t * 1000))
callback = 'jQuery{0}_{1}'.format(random.getrandbits(100), getTime())
def get_challenge():
    #登录认证第一步
    url = 'https://net.zju.edu.cn/cgi-bin/get_challenge'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
    }
    #callback = 'jQuery{0}_{1}'.format(random.getrandbits(100), getTime())
    params = {'callback':callback,
              'username':username,
              'ip':local_ip,
              '_':getTime()}
    r = requests.get(url, params=params, headers=headers)
    #print(r.url)
    # print(r.text)
    data = r.text[len(callback)+1:-1]
    token = json.loads(data)['challenge']
    return token
def statusTest():
    #ping 百度来测试网络是否连通
    import subprocess
    ret = subprocess.run("ping www.baidu.com -n 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s1 = str(ret.stdout, encoding='gbk')
    return True if "0% 丢失" in s1 else False
def encode_userinfo(userinfo, token):
    #对用户信息进行SRBX1
    userinfo = json.dumps(userinfo).replace(' ','')
    if len(userinfo) == 0:
        return ''
    sc = len(userinfo)
    if sc % 4:
        userinfo += '\0' * (4-(sc%4))
    sv = []
    for i in range(0, sc, 4):
        while i >> 2 >= len(sv):
            sv.append(0)
        sv[i >> 2] = ord(userinfo[i]) | ctypes.c_int32(ord(userinfo[i+1]) << 8).value | \
                     ctypes.c_int32(ord(userinfo[i+2]) << 16).value | ctypes.c_int32(ord(userinfo[i+3]) << 24).value
    sv.append(sc)
    v = sv[:]
    sc = len(token)
    sv = []
    for i in range(0, sc, 4):
        while i >> 2 >= len(sv):
            sv.append(0)
        sv[i >> 2] = ord(token[i]) | ctypes.c_int32(ord(token[i+1]) << 8).value | \
                     ctypes.c_int32(ord(token[i+2]) << 16).value | ctypes.c_int32(ord(token[i+3]) << 24).value
    k = sv[:]
    while len(k) < 4:
        k.append(0)
    n = len(v) - 1
    z = v[n]
    y = v[0]
    c = ctypes.c_int32(0x86014019 | 0x183639A0).value
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    m = None
    e = None
    while q > 0:
        d = d + c & (0x8CE0D9BF | 0x731F2640)
        d = ctypes.c_int32(d).value
        e = (d >> 2 & 0xFFFFFFFF >> 2) & 3
        for p in range(n):
            y = v[p + 1]
            m = (z >> 5 & 0xFFFFFFFF >> 5) ^ ctypes.c_int32(y << 2).value
            m += (y >> 3 & 0xFFFFFFFF >> 3) ^ ctypes.c_int32(z << 4).value ^ (d ^ y)
            m += k[p & 3 ^ e] ^ z
            v[p] = ctypes.c_int32(v[p] + m & (0xEFB8D130 | 0x10472ECF)).value
            z = v[p]
        y = v[0]
        m = (z >> 5 & 0xFFFFFFFF >> 5) ^ ctypes.c_int32(y << 2).value
        m += (y >> 3 & 0xFFFFFFFF >> 3) ^ ctypes.c_int32(z << 4).value ^ (d ^ y)
        m += k[(p + 1) & 3 ^ e] ^ z
        v[n] =ctypes.c_int32(v[n] + m & (0xBB390742 | 0x44C6F8BD)).value
        z = v[n]
        q -= 1
    lv = v[:]
    ld = len(lv)
    lc = ctypes.c_int32(ld - 1 << 2).value
    for i in range(ld):
        lv[i] = ''.join([chr(lv[i] & 0xff), chr((lv[i] >> 8 & 0xFFFFFFFF >> 8) & 0xff),
                        chr((lv[i] >> 16 & 0xFFFFFFFF >> 16) & 0xff),
                        chr((lv[i] >> 24 & 0xFFFFFFFF >> 24) & 0xff)])
    l = ''.join(lv)
    base64 = BASE64()
    return r'{SRBX1}' + base64.encode(l)

def srun_portal(username,password):
    #登录认证第二部
    url = 'https://net.zju.edu.cn/cgi-bin/srun_portal'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
    }
    #callback = 'jQuery{0}_{1}'.format(random.getrandbits(100),getTime())
    md5 = MD5()
    token= get_challenge()
    hmd5 = md5(password, token)
    acid = '3' #acid，取决于宿舍环境认证网页的ID，根据实际修改
    n = '200'
    type = '1'
    srun_ver = 'SRunCGIAuthIntfSvr V1.18 B20210926'
    userinfo = {'username':username,
                'password':password,
                'ip':local_ip,
                'acid':acid,
                'srun_ver': srun_ver
                }
    info = encode_userinfo(userinfo, token)
    chkstr = token+username+token+hmd5+token+acid+token+local_ip+token+n+token+type+token+info
    sha1 = hashlib.sha1()
    sha1.update(chkstr.encode())
    chksum = sha1.hexdigest()
    params = {'callback':callback,
              'action':'login',
              'username':username,
              'password':r'{MD5}' + hmd5,
              'os':'Windows10',
              'name':'Windows',
              'double_stack':0,
              'chksum':chksum,
              'info':info,
              'ac_id':acid,
              'ip':local_ip,
              'n':n,
              'type':type,
              '_':getTime()}
    r = requests.get(url, params=params, headers=headers)
    # print(r.text)
    if 'Login is successful' in r.text:
        print('登录认证成功！')
    elif 'ip_already_online' in r.text:
        print("您已在线！")
    elif statusTest()==True:
        print("您虽然不在线但是有网")
    else:
        print('登陆失败，请检查acid或者密码是否正确')
def main():
    print('登录用户名：{}'.format(username))
    print('内网IPV4地址：{}'.format(local_ip))
    srun_portal(username,password)

if __name__ == '__main__':
    main()


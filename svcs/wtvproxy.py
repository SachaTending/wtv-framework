from wtvframework import Service

svc = Service("wtv-proxy") # compatiblity layer for wtv-proxy

svcs = [svc]

@svc.addhandl("preregister")
def preregister_proxy(data):
    return f"""200 OK
Connection: Keep-Alive
wtv-initial-key: BCK9Zzas8So=
Content-Type: text/html
wtv-client-time-zone: GMT -0000
wtv-client-time-dst-rule: GMT
wtv-client-date: Fri, 28 Apr 2023 19:12:37 GMT
Content-length: 0
wtv-visit: wtv-head-waiter:/ValidateLogin
wtv-service: reset
wtv-home: wtv-home:/home
{__builtins__.wtv_svcs_add(connect_host="10.0.0.1")}
"""

@svc.addhandl("supports")
def is_capable(data): return "yes"
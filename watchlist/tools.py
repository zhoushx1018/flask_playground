from flask import request


def GetRealIP(request):
    realIP = ""
    try:
        headerIP = request.headers['X-Forwarded-For']
        if len(headerIP) > 1:
            realIP = headerIP.split(",")[0]
    except:
        try:
            realIP = request.remote_addr
        except:
            realIP = "0.0.0.0"
    return realIP
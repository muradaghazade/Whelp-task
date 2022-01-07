from ipdata import ipdata
from requests import get
from pprint import pprint

# print(socket.gethostbyname(socket.gethostname()))

# from IPy import IP


# def extract_ip():
#     st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:       
#         st.connect(('10.255.255.255', 1))
#         IP = st.getsockname()[0]
#     except Exception:
#         IP = '127.0.0.1'
#     finally:
#         st.close()
#     return IP

# ipp = extract_ip()
# print(ipp)

# ip = IP(ipp)
# print(ip.iptype())

ip = get('https://api.ipify.org').content.decode('utf8')
print(ip)

ipdata = ipdata.IPData('711208fb9c48844a077f6d18e818d20db5954d83280f3be03f2c9cdf')
response = ipdata.lookup(ip)
pprint(response)



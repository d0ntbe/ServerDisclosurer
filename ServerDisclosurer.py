import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def founder_server_version(head,text,location):

    servers_list = ["Apache", "apache", "Nginx", "nginx", "CheryPy", "PHP", "IIS", "LiteSpeed", "OpenGSE", "httpd"]

    ################# in head ###############

    s = 0
    while s != len(servers_list):
        pos = head.find(servers_list[s])
        if pos != -1:
            pos2 = head[pos:].find("\n")
            print("* " + servers_list[s] + " server has founded --> " + head[pos:pos + pos2] + " " + location + " in Header")
            with open('rez.log', 'a') as f:
                f.write("* " + servers_list[s] + " server has founded --> " + head[pos:pos + pos2] + " " + location + " in Header")
                f.close()
        s = s + 1

    ################# in text ###############

    s = 0
    while s != len(servers_list):
        pos = text.find(servers_list[s])
        if pos != -1:
            pos2 = pos + len(servers_list[s])
            print("* " + servers_list[s] + " server has founded --> " + text[pos:pos2] + " " + location + " in Data")
            with open('rez.log', 'a') as f:
                f.write("* " + servers_list[s] + " server has founded --> " + text[pos:pos2] + " " + location + " in Data")
                f.close()
        s = s + 1


def location_boom(a):
    print(a)

############## CFG ####################

try:
    input = sys.argv[1]
except:
    print('\n\nFormat error! USAGE: ServerDisclosure.py https://thetargetplace.com 443\n')
    exit()
    
if input.find("https:") != -1:
    proto = 'https://'
if input.find("http:") != -1:
    proto = 'http://'

server = input.strip(proto)


port = ''
location = '/'

cases_location = ["1", "2", "etc/nginx", "nginx.conf", "common.txt", "api../", "v1/../",
                  "apiv1", "api/v1", "%0a", "%0d%0a", "%0d%0a/", "%0d%0a/..",
                  "%0d%0a/../", "%0d%0a/robots.txt", "$", "$/", "$nginx_version",
                  "$1", "?", "?/", "www.", "%20/", "../../../", "index.php",
                  "index.html", "xmlrpc.php", "bitrix/admin", "%3A%2F%2Fwww.google.com%2Fi",
                  "main",".js",".css"]

cases_server=[]

t = server.count(".")
tmp = server

while t != 0:

    cases_server.append(tmp)
    tmp = tmp[tmp.find(".")+1:]
    t = t - 1


############ START ############################

with open('rez.log', 'w') as f:
    f.write('')
    f.close()

try:

    req = requests.get(proto + server + location + port, verify=False)
    req.close()
    print("Connection establishment! <---")
except:

    print("No connecting with " + proto + server + location + port)

############ Location #############

n = 0
m = 0

while m != len(cases_server):

    while n != len(cases_location):

        #print("Checking " + proto + cases_server[m] + location + cases_location[n] + port)
        try:
            req = requests.get(proto + cases_server[m] + location + cases_location[n] + port, verify=False, timeout=5)
            #print("Status - " + str(req.status_code) + " size - " + str(len(req.text)))
            response_save = proto + cases_server[m] + location + cases_location[n] + port + " --> " + " size " + str(len(req.text)) + " " + "status " + str(req.status_code) + "\n"
            with open('rez.log', 'a') as f:
                f.write(" " +response_save)
                f.close()

            founder_server_version(str(req.headers),str(req.text), str(proto + cases_server[m] + location + cases_location[n] + port))
            req.close()
            n = n + 1

        except:

            print("No connection with " + proto + cases_server[m] + location + cases_location[n] + port)
            n = n + 1

    n = 0
    m = m + 1

print("\nTHX for using. With love from Russia. ZL.)")

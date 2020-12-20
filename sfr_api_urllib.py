# urllib version

import re
import urllib, http.cookiejar

class sfr_client:

    def __init__(self,login=None,password=None,cookie_file=None):
        
        self.browser_session = urllib
        self.cookie = http.cookiejar.MozillaCookieJar()
        cookie_handler = self.browser_session.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        cookie_handler.addheaders = [('User-agent', 'Mozilla/5.0')]
        self.browser_session.request.install_opener(cookie_handler)
        cookie_loaded = False

        # Charge le cookie ici
        if cookie_file != None:
            self.cookie.filename = cookie_file
            try:
                self.cookie.load(self.cookie.filename)
            except:
                pass
        else:
            self.cookie.filename = "default.cookie"

        if cookie_loaded is False:
            if login == None or password == None:    
                raise Exception("Wrong login/password or cookie file")
            else:
                data={"methode":"passwd","login": login, "password": password}
                reponse = self.make_post("http://192.168.1.1/login",data=data)

                if reponse != 200:
                    raise Exception("Impossible to login")       

    # Sert à garder les cookies dans un fichier pour éviter les reconnexion inutiles
    def cookie_save(self,filename=None):
        if type(filename) == str:
            self.cookie.filename = filename
        self.cookie.save(ignore_discard=True, ignore_expires=True)
    
    # Ouvre des ports
    def open_nat(self,rulename,ip_adress,external_port,destination_port=None,nat_type="tcp",port_range="false"):
        # si l'user n'as rien mis, le port de destination sera le même que le port externe
        if destination_port == None:
            destination_port = external_port
        
        # Verifie si l'user n'a pas rentré une plage de port
        if "-" in str(external_port):
            first_port = external_port.split("-")[0]
            second_port = external_port.split("-")[1]
            port_range = "true"

            # Met le plus petit en premier
            if int(first_port) > int(second_port):
                witness = second_port
                second_port = first_port
                first_port = witness
            # Retire la plage, car la meme valeur
            elif int(first_port) == int(second_port):
                external_port = first_port
                port_range = "false"
        else:
            # Si ce n'est pas une plage
            first_port = ""
            second_port = ""
        
        # Le payload nécessaire pour une requête
        post_data = {
            'nat_rulename':str(rulename),
            'nat_proto':str(nat_type),
            'nat_range':str(port_range),
            'nat_extport':str(external_port),
            'nat_extrange_p0':str(first_port),
            'nat_extrange_p1':str(second_port),
            'nat_dstip_p0':'192',
            'nat_dstip_p1':'168',
            'nat_dstip_p2':'1',
            'nat_dstip_p3':str(ip_adress),
            'nat_dstport':str(destination_port),
            'nat_dstrange_p0':str(first_port),
            'nat_dstrange_p1':str(second_port),
            'nat_active':'on',
            'action_add':''
        }

        print(self.make_post("http://192.168.1.1/network/nat",post_data))

    def make_post(self,url,data):
        # Tout les post passent par ici, c'est plus controlable
        if type(data) == dict:
            data = self.browser_session.parse.urlencode(data).encode('UTF-8')
        else:
            data = None

        req = self.browser_session.request.Request(url, data)

        try:
            resp = self.browser_session.request.urlopen(req)
        except urllib.error.HTTPError  as e:
                return e

        return resp.getcode()

    def make_get(self,url):
        request = self.browser_session.request.Request(url)

        try:
            response = self.browser_session.request.urlopen(request)
        except urllib.error.HTTPError  as e:
                return e

        return response
    
    def reboot_modem(self):
        self.make_post("http://192.168.1.1/reboot",data={'submit':""})

    def get_nat(self):
        req = self.make_get("http://192.168.1.1/network/nat").read().decode()
        name = False
        protocole = False
        proto = ""
        nat_list = []
        
        # Va chercher les informations, ma méthode est chaotique mais elle marche
        for i in req.splitlines():
            if '<span class="col_number">' in i:
                nat_id = i.split('<span class="col_number">')[1].split('</span>')[0]

            if name is True:
                rulename = i.replace("\t","")
                name = False

            if protocole is True:
                proto = i.replace("\t","")
                protocole = False

            if 'td data-title="Protocole"' in i:
                protocole = True
            
            if '<td data-title="Nom" class="desactivated">' in i:
                status = "inactif"
                name = True
            elif '<td data-title="Nom" >' in i:
                status = "actif"
                name = True

            if '<td data-title="Ports externes"' in i and '</td>' in i:
                ext_port = i.split('>')[1].split("<")[0]
            
            if '<td data-title="IP de destination"' in i and '</td>' in i:
                dest_ip = i.split('>')[1].split("<")[0]
            
            if '<td data-title="Ports de destination"' in i and '</td>' in i:
                dest_port = i.split('>')[1].split("<")[0]
                nat_list.append({"id":nat_id,"rulename":rulename,"protocole":proto,"status":status,"external_port":ext_port,"ip_adress":dest_ip,"destination_port":dest_port})
        
        # Return une list contenant toutes les informations nécessaires pour chaque port ouvert
        return nat_list
    
    def nat_status(self,nat_id,status):
        if status == "disable":
            post_data = {"action_disable."+str(nat_id):"Désactiver"}
        
        # marche pas encore
        # elif status == "remove":
        #     post_data = {"action_remove."+str(nat_id):""}

        elif status == "enable":
            post_data = {"action_enable."+str(nat_id):"Activer"}

        self.make_post("http://192.168.1.1/network/nat",post_data)
import requests
import pickle
import re

class sfr_client:

    def __init__(self,login="#",password="#",cookies_file="#"):

        self.session = requests.session()
        cookie_loaded = False

        # Charge le cookie ici
        if cookies_file != "#":
            try:
                with open(cookies_file, 'rb') as f:
                    self.session.cookies.update(pickle.load(f))
                cookie_loaded = True
            except FileNotFoundError:
                pass

        if cookie_loaded is False:
            if login == "#" or password == "#":    
                raise Exception("Wrong login/password or cookie file")
            else:
                data={"methode":"passwd","login": login, "password": password}
                reponse = self.make_post("http://192.168.1.1/login",data=data)

                if reponse != 200:
                    raise Exception("Impossible to login")       

    # Sert à garder les cookies dans un fichier pour éviter les reconnexion inutiles
    def save_session(self,filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)
    
    # Ouvre des ports
    def open_nat(self,rulename,ip_adress,external_port,destination_port="#",nat_type="tcp",port_range="false"):
        if destination_port == "#":
            destination_port = external_port
        
        if "-" in str(external_port):
            first_port = external_port.split("-")[0]
            second_port = external_port.split("-")[1]
            port_range = "true"

            if int(first_port) > int(second_port):
                witness = second_port
                second_port = first_port
                first_port = witness
            elif int(first_port) == int(second_port):
                external_port = first_port
                port_range = "false"
        else:
            first_port = ""
            second_port = ""
        
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
        
        self.make_post("http://192.168.1.1/network/nat",post_data)

    def make_post(self,url,data,headers="#"):
        request = self.session.post(url,data)
        return request.status_code
    
    def reboot_modem(self):
        self.make_post("http://192.168.1.1/reboot",data={'submit':""})

    def get_nat(self):
        req = self.session.get("http://192.168.1.1/network/nat")
        name = False
        protocole = False
        proto = ""
        nat_list = []
        
        for i in req.text.splitlines():
            if '<span class="col_number">' in i:
                nat_id = i.split('<span class="col_number">')[1].split('</span>')[0]

            if name is True:
                rulename = i
                name = False

            if protocole is True:
                proto = i
                name = False
            
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
        
        return nat_list
                


api = sfr_client(login="admin",password="password")
api.open_nat("minecraft","27","26666")
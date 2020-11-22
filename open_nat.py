from sfr_api import sfr_client

api = sfr_client(login="admin",password="password")
api.open_nat(rulename="test",ip_adress="27",external_port="6000")

api.nat_status(1,"disable")

a = api.get_nat()
for i in a:
    print(i["id"],i["rulename"],i["protocole"],i["status"],i["external_port"],i["ip_adress"],i["destination_port"])
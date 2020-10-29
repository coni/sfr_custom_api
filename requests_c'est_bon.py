import requests,sys

""" Connexion """
html_file = open("main.html","w")
sess = requests.session()
sess.post("http://192.168.1.1/login", data={"methode":"passwd","login": sys.argv[1], "password": sys.argv[2]})

""" ouvrir un port dans le nat """
# nat_data = {'nat_rulename':'port_boum','nat_proto':'tcp','nat_range':'false','nat_extport':'19777','nat_extrange_p0':'','nat_extrange_p1':'','nat_dstip_p0':'192','nat_dstip_p1':'168','nat_dstip_p2':'1','nat_dstip_p3':'27','nat_dstport':'19777','nat_dstrange_p0':'','nat_dstrange_p1':'','nat_active':'on','action_add':''}
# sess.post("http://192.168.1.1/network/nat",data=nat_data)

""" reboot """
reboot_data = {'submit':""}
sess.post("http://192.168.1.1/reboot",data=reboot_data)
sample = input("requete : ")
dict_ = "{"

for i in range(len(sample.split("&"))):
    if i == len(sample.split("&"))-1:
        dict_ += "'"+sample.split("&")[i].split("=")[0]+"':'"+sample.split("&")[i].split("=")[1]+("'}")
    else:
        dict_ += "'"+sample.split("&")[i].split("=")[0]+"':'"+sample.split("&")[i].split("=")[1]+("',")

print(dict_)
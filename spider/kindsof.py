
def kindsof(diction):
    import pymongo
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.city
    citys=db.citys
    fp_dm = diction['fp_dm'][1:5]+"00"
    city=citys.find_one({"dm":fp_dm})
    if city==None:
        return None
    else:
        diction['fp_zl']=city['dq']+"增值税电子普通发票"
    diction['kp_rq']=diction['kp_rq'][:4]+"年"+diction['kp_rq'][4:6]+"月"+diction['kp_rq'][-2:]+"日"
    diction['kp_je']=diction['kp_je']+"¥"
    return diction
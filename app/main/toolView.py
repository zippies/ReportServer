# -*- coding:utf-8 -*-
from flask import render_template,request,jsonify
from . import url
import json
import traceback

def parseNode(data,nlist):
    dictValues = []
    for v in data.values():
        if type(v) == dict:
            dictValues.append(v)
        elif type(v) == list:
            for d in v:
                if type(d) == dict:
                    parseNode(d,nlist)

    if dictValues:
        nlist.extend(data.keys())
        for d in dictValues:
            parseNode(d,nlist)
    else:
        nlist.extend(data.keys())        

@url.route("/tool/parseNodes",methods=['GET','POST'])
def parseNodes():
    info = {"result":True,"errorMsg":None,"data":None}
    if request.method == "GET":
        return render_template("parseNodes.html")
    else:
        obj = request.json
        nlist = []
        try:
            parseNode(obj,nlist)
            info["data"] = list(set(nlist))
        except Exception as e:
            info["result"] = False
            info["errorMsg"] = str(e)
        finally:
            return jsonify(info)



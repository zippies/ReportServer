# -*- coding:utf-8 -*-
from flask import render_template,request,jsonify
from ..models import db,Report
from . import url
import json
import traceback

@url.route("/<project>/generatereport",methods=['POST'])
def generateReport(project):
    info = {"result":True,"errorMsg":None}
    try:
        content = json.loads(request.form.get("result"))
        buildid = content.get("buildid",None)
        if buildid:
            report = Report(type=1,project=project,content=content,reportid=buildid)
        else:
            report = Report(type=0,project=project,content=content)
            count = Report.query.filter_by(project=project).all()
            report.reportid = len(count)+1 if count else 1
        db.session.add(report)
        db.session.commit()
        info["reportid"] = report.reportid
    except Exception as e:
        info["result"] = False
        info["errorMsg"] = str(e)+traceback.format_exc()
    finally:
        return jsonify(info)

@url.route("/<project>/report/<id>")
def offlineReport(project,id):
    if id == "latest":
        report = Report.query.filter_by(type=0).filter_by(project=project).order_by("id desc").first()
    else:
        report = Report.query.filter_by(type=0).filter_by(project=project).filter_by(reportid=id).first()
    if report:
        return render_template("report.html",result=report.content,time=report.createdtime.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return "报告不存在或已被删除"

@url.route("/<project>/<reportid>")
def onlineReport(project,reportid):
    report = Report.query.filter_by(type=1).filter_by(project=project).filter_by(reportid=reportid).first()
    if report:
        return render_template("report.html",result=report.content,time=report.createdtime.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return "报告不存在或已被删除"


@url.route("/<project>/report/clear")
def clearReport(project):
    reports = Report.query.filter_by(project=project).filter_by(type=0).all()
    if reports:
        for report in reports:
            db.session.delete(report)
        db.session.commit()
        return "清除成功"
    else:
        return "不允许清除"


@url.route("/<project>/report/clear/force")
def forceClearReport(project):
    reports = Report.query.filter_by(project=project).all()
    for report in reports:
        db.session.delete(report)
    db.session.commit()
    return "清除成功"




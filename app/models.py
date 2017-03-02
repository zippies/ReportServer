# -*- coding: utf-8 -*-
from datetime import datetime
from . import db


class Report(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    project = db.Column(db.String(64))
    reportid = db.Column(db.Integer)
    content = db.Column(db.PickleType)
    type = db.Column(db.Integer)
    createdtime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,type,project,content,reportid=None):
        self.type = type #0:debug  1:jenkins
        self.project = project
        self.content = content
        self.reportid = reportid

    def __repr__(self):
        return "%s_Report:%s" %(self.project,self.createdtime)


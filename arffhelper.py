"""
Author: Shay Maor
Description: ArffHelper library

Examples:
SQL - Set up using Flask: (Recommended - sqlite3 easy to get into)
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
	db = SQLAlchemy(app) # set up database
	
	sqlA = SQLAttacher(db) 
	sqlA.setQuery("select * from table;")	# set query for SQLAttacher

	attribute1 = Attribute("column1")
	attribute2 = Attribute("column2")
	attribute3 = Attribute("column3")

	choices = sqlA.getUnique(-1) #allows you to get a list of all the unique options for easy nominal choice addition
	attribute3.addChoices(choices)

	attributes = [attribute1, attribute2, attribute3]

	column = 0
	for attribute in attributes: # add all attributes and their mapping to the sql columns they're in
		sqlA.addAttribute(attribute, column)
		column+=1

	arffdoc = ArffDoc("test") # initialize with relation name
	arffdoc.setAttacher(sqlA) # Attach the SQLAttacher to the ArffDoc instance
	arffdoc.export("test.arff") # export the arff document
	

CSV - Set up using CSV File:
	csvAttach = CSVAttacher(filepath, headers=True) # Create CSV attacher and indicate if there are headers

	attribute1 = Attribute("column1")
	attribute2 = Attribute("column2")
	attribute3 = Attribute("column3")
	
	choices = csvAttach.getUnique(-1) #allows you to get a list of all the unique options for easy nominal choice addition
	attribute3.addChoices(choices)

	attributes = [attribute1, attribute2, attribute3]
	
	column = 0
	for attribute in attributes: # iterate upon all attributes and map to resulting row 
		sqlA.addAttribute(attribute, column)
		column+=1

	arffdoc = ArffDoc("test") # initialize with relation name
	arffdoc.setAttacher(csvAttach) # connect the attacher to the ArffDoc instance
	arffdoc.export("testcsv.arff")	# export the arff document

Manual - Set up using scripting:
	a1 = Attribute("column1")
	a2 = Attribute("column2")
	a3 = Attribute("column3")
	a3.addChoices(["choice1","choice2","choice3"])
	arffdoc = ArffDoc("sample")
	arffdoc.addAttribute(a1)
	arffdoc.addAttribute(a2)
	arffdoc.addAttribute(a3)
	arffdoc.addData(a1, [4,3,2,1])
	arffdoc.addData(a2, [1,2,3,4])
	arffdoc.addData(a3, ["choice1", "choice2", "choice1", "choice2"])
	print(arffdoc.toString())
	arffdoc.export("test.arff")
"""

from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from flask_sqlalchemy import SQLAlchemy

import os
import csv

class Attribute:
	def __init__(self, name, choices=None):
		self.name = name
		if choices:
			self.dataType = "NOMINAL"
			self.choices = choices
		else:
			self.dataType = "NUMERIC"
			self.choices = []
	def addChoice(self, choice):
		if self.dataType == "NUMERIC":
			self.dataType = "NOMINAL"
		self.choices.append(choice)
	def addChoices(self, choices):
		if self.dataType == "NUMERIC":
			self.dataType = "NOMINAL"
		self.choices += choices

	def __repr__(self):
		if self.dataType == "NUMERIC":
			return "@ATTRIBUTE %s\tNUMERIC" % (self.name)
		elif self.dataType == "NOMINAL":
			return "@ATTRIBUTE %s\t{%s}" % (self.name, ",".join(self.choices))

	def __str__(self):
		return self.__repr__()

class ArffDoc:
	def __init__(self, name):
		self.name = name
		self.attrdict = {}
		self.attributes = []
		self.datalength = 0
	def addAttribute(self, attribute):
		self.attributes.append(attribute)
	def addData(self, attributeInstance, data):
		assert(isinstance(attributeInstance, Attribute))
		if self.datalength == 0:
			self.datalength = len(data)
		else:
			assert(len(data)==self.datalength)
		for attribute in self.attributes:
			if attribute == attributeInstance:
				self.attrdict[attribute.name] = data
				break

	def setAttacher(self, attacher):
		attributes = attacher.getAttributes()
		for attribute in attributes:
			self.addAttribute(attribute)
			data = attacher.getData(attribute)
			self.addData(attribute, data)
	
	def setCSVAttacher(self, csvattacher):
		self.setAttacher(csvattacher)

	def setSQLAttacher(self, sqlattacher):
		self.setAttacher(sqlattacher)

	def toString(self):
		headers = "@RELATION %s\n" % (self.name)
		headers += "\n".join([str(attribute) for attribute in self.attributes])
		
		data = "@DATA\n"
	
		for row in range(self.datalength):
			rowvalues = [str(self.attrdict[attribute.name][row]) for attribute in self.attributes]
			currow = ",".join(rowvalues)
			data += currow + "\n"
		towrite = headers + "\n\n" + data
		return towrite 

	def export(self, filename):
		filecontents = self.toString()
		filepath = os.path.join(os.path.curdir, filename)
		with open(filepath, 'w') as arfffile:
			arfffile.write(filecontents)
			arfffile.close()

class Attacher:
	def __init__(self):
		self.attrdict = {}
		self.attributes = []
		self.columns = 0
		self.results = []
	def addAttribute(self, attribute, resultcolumn):
		self.attributes.append(attribute)
		self._attachAttribute(attribute, resultcolumn)

	def _attachAttribute(self, attribute, resultcolumn):
		self.attrdict[attribute.name] = [result[resultcolumn] for result in self.results]

	def getData(self, attribute):
		return self.attrdict[attribute.name]

	def getAttributes(self):
		return self.attributes

	def getUnique(self, resultcolumn):
		data = [result[resultcolumn] for result in self.results]
		unique = []		
		for dp in data:
			if dp not in unique:			
				unique.append(dp)
		return unique
	
	def overrideColumn(self, attribute, data):
		assert(len(data) == len(self.attrdict[attribute.name]))
		self.attrdict[attribute.name] = data


class CSVAttacher(Attacher):
	def __init__(self, filepath, headers=False):
		self.csv = filepath		
		self.attributes = []
		self.attrdict = {}
		self.results = []	
		self.read(filepath, headers)
	
	def read(self, filepath, headers):
		start = 1 if headers else 0
		with open(filepath, 'r') as csvfile:
			count = 0
			spamreader = csv.reader(csvfile, delimiter=';', quotechar=None)
			for row in spamreader:
				if count >= start:
					self.results.append(row)
				count+=1

class SQLAttacher(Attacher):
	def __init__(self, db):
		assert(isinstance(db, SQLAlchemy))
		self.db = db
		self.results = []
		self.columns = 0
		self.attributes = []
		self.attrdict = {}

	def attachQuery(self, sqlString):
		if isinstance(sqlString, TextClause):
			sql = sqlString
		else:
			sql = text(sqlString)
		result = self.db.engine.execute(sql)
		for row in result:
			self.results.append(row)


if __name__ == "__main__":
	a1 = Attribute("column1")
	a2 = Attribute("column2")
	a3 = Attribute("column3")
	a3.addChoices(["choice1","choice2","choice3"])
	arffdoc = ArffDoc("sample")
	arffdoc.addAttribute(a1)
	arffdoc.addAttribute(a2)
	arffdoc.addAttribute(a3)
	arffdoc.addData(a1, [4,3,2,1])
	arffdoc.addData(a2, [1,2,3,4])
	arffdoc.addData(a3, ["choice1", "choice2", "choice1", "choice2"])
	print(arffdoc.toString())
	arffdoc.export("test.arff")

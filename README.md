# MachineLearn
Helper Libraries for Machine Learning Applications

arffhelper.py
Examples:

SQL - Set up using Flask: (Recommended - sqlite3 easy to get into)

```python
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
```
	
CSV - Set up using CSV File:

```python
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
```


Manual - Set up using scripting:

```python
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

```

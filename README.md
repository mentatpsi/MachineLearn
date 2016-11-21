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
a1 = Attribute("sepallength")
	a2 = Attribute("sepalwidth")
	a3 = Attribute("petallength")
	a4 = Attribute("petalwidth")
	a5 = Attribute("class")
	a5.addChoices(["Iris-setosa","Iris-versicolor","Iris-virginica"])
	arffdoc = ArffDoc("iris")
	arffdoc.addAttribute(a1)
	arffdoc.addAttribute(a2)
	arffdoc.addAttribute(a3)
	arffdoc.addAttribute(a4)
	arffdoc.addAttribute(a5)
	arffdoc.addData(a1, [5.1, 4.9, 4.7, 4.6, 5.0, 5.4, 4.6, 5.0, 4.4, 4.9])
	arffdoc.addData(a2, [3.5, 3.0, 3.2, 3.1, 3.6, 3.9, 3.4, 3.4, 2.9, 3.1])
	arffdoc.addData(a3, [1.4, 1.4, 1.3, 1.5, 1.4, 1.7, 1.4, 1.5, 1.4, 1.5])	
	arffdoc.addData(a4, [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1])
	arffdoc.addData(a5, ["Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa", "Iris-setosa"])
	
	print(arffdoc.toString())
	arffdoc.export("test.arff")

```

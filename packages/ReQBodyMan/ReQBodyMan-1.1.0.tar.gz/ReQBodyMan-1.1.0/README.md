# ReQBodyMan

![BrainyTechLogo](https://brainytech.net/wp-content/uploads/2023/11/brainy-tech-site.png)

## Project Description

ReQBodyMan is a package that you can use to manage the validations of body data coming with Request more effectively.

## Installation

### 1 Install to Package

For Windows

```
pip install ReQBodyMan
```

For Linux/MacOs

```
pip3 install ReQBodyMan
``` 

### 2 Dependencies Package

`flask`

## Usege

### 1 Import the package

```py
from ReQBodyMan.ReQBodyMan import ReQBodyMan
```

### 2 Get Form Data

If the data comes from the request with a form, you can get the data as follows.

```py

Data : string, int, float, boolean, list, dict,  
Parameters : contextName, variableType, booleanType=NoneRequired
booleanType default = "int"
Return: data

data = self.ReQBodyMans.form("data_name", "str")
data = self.ReQBodyMans.form("data_name", "int")
data = self.ReQBodyMans.form("data_name", "float")
data = self.ReQBodyMans.form("data_name", "bool", booleanType="bool")
data = self.ReQBodyMans.form("data_name", "bool", booleanType="int" )
data = self.ReQBodyMans.form("data_name", "list")
data = self.ReQBodyMans.form("data_name", "dict")
```

If Variable Type is sent outside the specified format, return None.

### 3 Get Json Data

```py

Data : string, int, float, boolean, list, dict,  
Parameters : contextName, variableType, booleanType=NoneRequired
booleanType default = "int"
Return : Data

data = self.ReQBodyMans.json("data_name", "str")
data = self.ReQBodyMans.json("data_name", "int")
data = self.ReQBodyMans.json("data_name", "float")
data = self.ReQBodyMans.json("data_name", "bool", booleanType="bool")
data = self.ReQBodyMans.json("data_name", "bool", booleanType="int")
data = self.ReQBodyMans.json("data_name", "list")
data = self.ReQBodyMans.json("data_name", "dict")
```

If Variable Type is sent outside the specified format, return None.

### 4 Get File

```py
Data : file
Parameters : fileName
Return: file

file = self.ReQBodyMans.file("fileName")
```
If FileName is not in request.file, the value "The {fileName} is not in request.files" is returned.

### 5 Get Params

```py
Data : string, int, float, boolean, list,  
Parameters : variableName, variableType, booleanType=NoneRequired
booleanType default = "int"
Return : data

data = self.ReQBodyMans.params("data_name", "str")
data = self.ReQBodyMans.params("data_name", "int")
data = self.ReQBodyMans.params("data_name", "float")
data = self.ReQBodyMans.params("data_name", "bool", booleanType="bool")
data = self.ReQBodyMans.params("data_name", "bool", booleanType="int")
data = self.ReQBodyMans.params("data_name", "list")
```

If Variable Type is sent outside the specified format, return None.

# Release Note

## v.1.1.0

1. Added dict property to Params.
2. Added dict property to Json
3. The return value for bool type has been added to return int or bool type according to the value to be given with booleanType.
4. Code refactor.

## v.1.0.1

1. ReadMe file updated

## v.1.0.0

1. Project published.


**ReQBodyMan is a BrainyTech Product.**

**Developer : Murat Bilginer**
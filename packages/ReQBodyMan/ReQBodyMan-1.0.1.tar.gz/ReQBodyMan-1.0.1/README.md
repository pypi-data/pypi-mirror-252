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

**Note: Boolean values have a return value of 1 if True and a return value of 0 if False.**

### 2 Get Form Data

If the data comes from the request with a form, you can get the data as follows.

```py
Data : string, int, float, boolean, list, dict,  
Parameters : contextName, variableType
Return: data

data = self.ReQBodyMans.form("data_name", "str")
data = self.ReQBodyMans.form("data_name", "int")
data = self.ReQBodyMans.form("data_name", "float")
data = self.ReQBodyMans.form("data_name", "bool")
data = self.ReQBodyMans.form("data_name", "list")
data = self.ReQBodyMans.form("data_name", "dict")
```

If Variable Type is sent outside the specified format, data is received according to the str format.

### 3 Get Json Data

```py
Data : string, int, float, boolean, list, dict,  
Parameters : contextName, variableType
Return : Data

data = self.ReQBodyMans.json("data_name", "str")
data = self.ReQBodyMans.json("data_name", "int")
data = self.ReQBodyMans.json("data_name", "float")
data = self.ReQBodyMans.json("data_name", "bool")
data = self.ReQBodyMans.json("data_name", "list")
data = self.ReQBodyMans.json("data_name", "dict")
```

If Variable Type is sent outside the specified format, data is received according to the str format.

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
Parameters : variableName, variableType
Return : data

data = self.ReQBodyMans.params("data_name", "str")
data = self.ReQBodyMans.params("data_name", "int")
data = self.ReQBodyMans.params("data_name", "float")
data = self.ReQBodyMans.params("data_name", "bool")
data = self.ReQBodyMans.params("data_name", "list")
```

If variablename is sent outside the specified format,

variableType : str return : ""
variableType : int return : 0
variableType : float return : 0.0
variableType : bool return : 0
variableType : list return : []




# Release Note

## v.1.0.1

1. ReadMe file updated

## v.1.0.0

1. Project published.


**ReQBodyMan is a BrainyTech Product.**

**Developer : Murat Bilginer**
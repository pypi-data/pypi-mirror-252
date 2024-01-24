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

## Usage

### 1 Import The Package

```py
from ReQBodyMan.ReQBodyMan import ReQBodyMan
```
### 2 ReQBodyMan Create Object

```py
ReQBodyMans = ReQBodyMan()
```

### 3 Get Form Data

If the data comes from the request with a form, you can get the data as follows.

```py

GetData : 
    string, 
    int, 
    float, 
    boolean, 
    list, 
    dict,

Parameters:
    variableName : str, 
    variableType : str, 
    booleanType  : str  > default = "int" NoneRequired

Return: 
    data : str, int, float, bool, list, dict, None

data = ReQBodyMans.form(variableName, variableType, booleanType="int")

data = ReQBodyMans.form("variableName", "str")
data = ReQBodyMans.form("variableName", "int")
data = ReQBodyMans.form("variableName", "float")
data = ReQBodyMans.form("variableName", "bool", booleanType="bool")
data = ReQBodyMans.form("variableName", "bool", booleanType="int" )
data = ReQBodyMans.form("variableName", "list")
data = ReQBodyMans.form("variableName", "dict")
```

If Variable Type is sent outside the specified format, return None.

### 4 Get Json Data

```py

GetData: 
    string, 
    int, 
    float, 
    boolean, 
    list, 
    dict,

Parameters: 
    variableName : str, 
    variableType : str, 
    booleanType  : str  > default = "int" NoneRequired

Return:
    data : str, int, float, bool, list, dict, None

data = ReQBodyMans.json(variableName, variableType, booleanType="int")

data = ReQBodyMans.json("variableName", "str")
data = ReQBodyMans.json("variableName", "int")
data = ReQBodyMans.json("variableName", "float")
data = ReQBodyMans.json("variableName", "bool", booleanType="bool")
data = ReQBodyMans.json("variableName", "bool", booleanType="int")
data = ReQBodyMans.json("variableName", "list")
data = ReQBodyMans.json("variableName", "dict")
```

If Variable Type is sent outside the specified format, return None.

### 5 Get File

```py

GetData: 
    file
    files

Return: 
    data: file or files, None

data = ReQBodyMans.file()

```

### 6 Get SpecificFile

```py

GetData: 
    file

Parameters: 
    fileName : str

Return:
    data: file, None

data = ReQBodyMans.specificFile(fileName)

```
If FileName is not in request.file, the value None is returned.

### 7 Get Params

```py
Data : 
    string
    int
    float
    boolean
    list
    dict

Parameters: 
    variableName : str, 
    variableType : str, 
    booleanType  : str  > default = "int" NoneRequired

Return:
    data : str, int, float, bool, list, dict, None

data = ReQBodyMans.params(variableName, variableType, booleanType="int")

data = ReQBodyMans.params("variableName", "str")
data = ReQBodyMans.params("variableName", "int")
data = ReQBodyMans.params("variableName", "float")
data = ReQBodyMans.params("variableName", "bool", booleanType="bool")
data = ReQBodyMans.params("variableName", "bool", booleanType="int")
data = ReQBodyMans.params("variableName", "list")
data = ReQBodyMans.params("variableName", "dict")
```

### 8 GetAllData Function

```py
Data: 
    string
    int
    float
    boolean
    list
    file

Parameters: 
    bodyJson: dict

variableName: Variable name in body data 

bodyType:  
    form
    json
    params
    file

booleanType:
    int, 
    bool

Return: 
    data: dict or None

data = ReQBodyMans.getAllData(bodyJson)

bodyJson = {

    "variableName" : ["bodyType", "variableType", "booleanType"]
}

# BodyType Json

bodyJson = {
    
    "password"  : ["json", "str"],
    "email"     : ["json", "str"]
}

# Boolean Type Usage 

bodyJson = {
    
    "password"  : ["json", "str"],
    "email"     : ["json", "str"],
    "status"    : ["json", "bool", "int"]
    "status2"   : ["json", "bool", "bool"]
}

# BodyType Form

bodyJson = {
    
    "password"  : ["form", "str"],
    "email"     : ["form", "str"],
    "status"    : ["form", "bool", "int"]
    "status2"   : ["form", "bool", "bool"]
    "fileName"  : ["file"] 
}

# BodyForm Params

bodyJson = {
    
    "password"  : ["params", "str"],
    "email"     : ["params", "str"],
    "status"    : ["params", "bool", "int"]
    "status2"   : ["params", "bool", "bool"] 
}

data = ReQBodyMans.getAllData(bodyJson)

Return data content 

{
    "email" : "test@test.com",
    "password":"test2",
    "status" : "1" or "0",
    "status2" : True or False,
    "fileName" : file
}

```

### 9 GetAllDataHero Function

```py
Data : 
    string
    int
    float
    boolean
    list
    file
    files

Parameters: 
    bodyJson:dict

type: 
    form
    json
    params

variableName: 
    Variable name in body data

variableType:
    string
    int
    float
    boolean
    list
    file
    files

booleanType: 
    int 
    bool

Return: 
    data:dict, None

data = ReQBodyMans.getAllDataHero(bodyJson)

bodyJson = {

    "type"=type, # required Key
    "variableName" : ["variableType", "booleanType"]
}

# BodyType Json

bodyJson = {
    
    "type":"json",
    "password"  : ["str"],
    "email"     : ["str"]
}

# Boolean Type Usage 

bodyJson = {
    
    "type":"json",
    "password"  : ["str"],
    "email"     : ["str"],
    "status"    : ["bool", "int"]
    "status2"   : ["bool", "bool"]
}

# BodyType Form

bodyJson = {
    
    "type":"form",
    "password"  : ["str"],
    "email"     : ["str"],
    "status"    : ["bool", "int"]
    "status2"   : ["bool", "bool"]
    "fileName"  : ["file"] # get all file in request.files
    "fileName2" : ["files"] # Fetches only the file named file from request.files
}

# BodyType Params

bodyJson = {

    "type":"params",
    "password"  : ["str"],
    "email"     : ["str"],
    "status"    : ["bool", "int"]
    "status2"   : ["bool", "bool"] 
}

data = ReQBodyMans.getAllDataHero(bodyJson)

Return data content 

{
    "email" : "test@test.com",
    "password":"test2",
    "status" : "1" or "0",
    "status2" : True or False,
    "fileName" : files,
    "fileName2" : file
}

```

If Variable Type is sent outside the specified format, return None.

# Release Note

## v.1.4.0

1. Major BugFix 
   - file and specificFile Function
  
2. ReadMe Updated 
   - Instructions for use have been updated.

## v.1.3.0

1. getAllDataHero Function Added 
    - Allows you to send all data at once more easily than v1 and receive data as a dictionary
  
2. specificFile Function Added
    - The feature of getting what we want from more than 1 file sent in the request.files has been added.

3. file Function Updated
    - File function has been updated to receive all incoming files in request.files.
    - file function name updated to files

## v.1.2.2

1. ReadMe file updated

## v.1.2.1

1. ReadMe file updated

## v1.2.0

1. getAllData Function Added 
      - Allows you to send all the data at once and receive the data as a dictionary

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
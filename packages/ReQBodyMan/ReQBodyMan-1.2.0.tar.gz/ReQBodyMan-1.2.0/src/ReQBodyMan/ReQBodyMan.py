# region Import Packages

from flask import request
import json
import ast

# endregion

class ReQBodyMan():

    # region Form

    def form(self, contentText, variableType, booleanType="int"):

        self.__formContent = request.form

        if contentText in self.__formContent:

            if variableType == "str":
                    
                if self.__formContent[contentText]:
                    return str(self.__formContent[contentText]).strip()
                else:
                    return ""

            elif variableType == "int":
                if self.__formContent[contentText]:
                    return int(self.__formContent[contentText])
                else:
                    return None

            elif variableType == "float":

                if self.__formContent[contentText]:
                    return float(self.__formContent[contentText])
                else:
                    return None
            
            elif variableType == "bool":

                if booleanType == "int":
                    
                    if self.__formContent[contentText]:
                        
                        return 1 if self.__formContent[contentText] == True else 0
                    
                    else:
                        return 0
                    
                elif booleanType == "bool":

                    if self.__formContent[contentText]:
                        
                        return True if self.__formContent[contentText] == True else False
                    
                    else:
                        return False
            
            elif variableType == "list":
                    
                if self.__formContent[contentText]:
                    return ast.literal_eval(self.__formContent[contentText]) 
                else:
                    return []

            elif variableType == "dict":
                    
                if self.__formContent[contentText]:

                    return json.loads(self.__formContent[contentText])

                else:
                    return None

            else:
                
                if self.__formContent[contentText]:
                    return self.__formContent[contentText]
                else:
                    return None
                 
        else:
            return None
        
    # endregion

    # region Json

    def json(self, contentText, variableType, booleanType="int"):

        self.__jsonContent = request.get_json()

        if contentText in self.__jsonContent:

            if variableType == "str":

                if self.__jsonContent[contentText]:
                    return str(self.__jsonContent[contentText]).strip()
                else:
                    return None

            elif variableType == "int":

                if self.__jsonContent[contentText]:
                    return int(self.__jsonContent[contentText])
                else:
                    return None

            elif variableType == "float":
                    
                if self.__jsonContent[contentText]:
                    return float(self.__jsonContent[contentText])
                else:
                    return None

            elif variableType == "bool":

                if booleanType == "int":
                    
                    if self.__jsonContent[contentText]:
                        
                        return 1 if self.__jsonContent[contentText] == True else 0
                    
                    else:
                        return None
                    
                elif booleanType == "bool":

                    if self.__jsonContent[contentText]:
                        
                        return True if self.__jsonContent[contentText] == True else False
                    
                    else:
                        return None

            elif variableType == "list":
                    
                if self.__jsonContent[contentText]:
                    return self.__jsonContent[contentText]
                else:
                    return None

            elif variableType == "dict":

                if self.__jsonContent[contentText]:

                    return json.loads(self.__jsonContent[contentText])
                
                else:
                    return None

            else:

                if self.__jsonContent[contentText]:
                    return self.__jsonContent[contentText]
                else:
                    return None

        else:

            return None

    # endregion
        
    # region File

    def file(self, fileName):

        if fileName in request.files:
            file = request.files[fileName]
            return file
        else:
            return f"The {fileName} is not in request.files"

    # endregion

    # region Params

    def params(self, variable, variableType, booleanType="int"):

        if str(variable) in request.args:

            if variableType == "str":
                return str(request.args.get(variable)).strip()

            elif variableType == "int":
                return int(request.args.get(variable))

            elif variableType == "float":
                return float(request.args.get(variable))
            
            elif variableType == "bool":

                if booleanType == "int":
                    return 1 if request.args.get(variable) == True else 0
                elif booleanType == "bool":
                    return True if request.args.get(variable) == True else False
            
            elif variableType == "list":
                return ast.literal_eval(request.args.get(variable))
            
            elif variableType == "dict":
                return json.loads(request.args.get(variable))
                    
        else:
            return None

    # endregion

    # region Get All Data
        
    def getAllData(self, bodyJson):

        responseData = {}

        for variableName, bodyList in bodyJson.items():

            if bodyList[0] == "form":

                if len(bodyList) == 3:
                    data = self.form(variableName, bodyList[1], booleanType=bodyList[2])
                
                else:
                    data = self.form(variableName, bodyList[1])

                responseData[variableName] = data
                
            elif bodyList[0] == "json":

                if len(bodyList) == 3:
                    data = self.json(variableName, bodyList[1], booleanType=bodyList[2])
                
                else:
                    data = self.json(variableName, bodyList[1])

                responseData[variableName] = data
                
            elif bodyList[0] == "params":

                if len(bodyList) == 3:
                    data = self.params(variableName, bodyList[1], booleanType=bodyList[2])
                
                else:
                    data = self.params(variableName, bodyList[1])

                responseData[variableName] = data
            
            elif bodyList[0] == "file":
                data = self.file()
                responseData[variableName] = data
            
            else:
                return {"error" : "Body type is not valid"}
           
        return responseData
    
    # endregion
    
# endregion
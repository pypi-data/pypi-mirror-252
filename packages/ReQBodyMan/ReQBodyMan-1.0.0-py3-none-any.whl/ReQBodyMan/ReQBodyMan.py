# region Import Packages

from flask import request
import json
import ast

# endregion

# region RequestContent Class

class ReQBodyMan():

    # region Init

    def __init__(self):
        pass

    # endregion

    # region Logix

    # region Form

    def form(self, contentText, variableType):

        # region Get Form Content

        self.__formContent = request.form

        # endregion

        # region Such A ContentText

        if contentText in self.__formContent:

            # region Int

            if variableType == "int":
                if self.__formContent[contentText]:
                    return int(self.__formContent[contentText])
                else:
                    return None

            # endregion

            # region Float

            elif variableType == "float":

                if self.__formContent[contentText]:
                    return float(self.__formContent[contentText])
                else:
                    return None
            
            # endregion

            # region Str

            elif variableType == "str":
                    
                if self.__formContent[contentText]:
                    return str(self.__formContent[contentText]).strip()
                else:
                    return ""

            # endregion
                
            # region List

            elif variableType == "list":
                    
                if self.__formContent[contentText]:
                    return ast.literal_eval(self.__formContent[contentText]) 
                else:
                    return []
            
            # endregion
                
            # region Dict

            elif variableType == "dict":
                    
                if self.__formContent[contentText]:

                    strDict = self.__formContent[contentText]
                    jsonDict = json.loads(strDict)
                    
                    return jsonDict
                else:
                    return []
            
            # endregion

            # region Any

            else:
                
                if self.__formContent[contentText]:
                    return self.__formContent[contentText]
                else:
                    return None
            
            # endregion

        # endregion

        # region Not Such A ContentText

        else:
            return None
        
        # endregion

    # endregion

    # region Json

    def json(self, contentText, variableType):

        self.__jsonContent = request.get_json()

        # region Such A ContentText

        if contentText in self.__jsonContent:

            # region Int

            if variableType == "int":

                if self.__jsonContent[contentText]:
                    return int(self.__jsonContent[contentText])
                else:
                    return None
            
            # endregion

            # region Float

            elif variableType == "float":
                    
                if self.__jsonContent[contentText]:
                    return float(self.__jsonContent[contentText])
                else:
                    return 0
                    
            # endregion
            
            # region Str

            elif variableType == "str":

                if self.__jsonContent[contentText]:
                    return str(self.__jsonContent[contentText]).strip()
                else:
                    return ""
            
            # endregion

            # region Bool

            elif variableType == "bool":
                    
                if self.__jsonContent[contentText]:
                    return 1 if self.__jsonContent[contentText] == True else 0
                else:
                    return 0

            # endregion

            # region List

            elif variableType == "list":
                    
                if self.__jsonContent[contentText]:
                    return self.__jsonContent[contentText]
                else:
                    return []
            
            # endregion
            
            # region Dict

            elif variableType == "dict":
                    
                if self.__jsonContent[contentText]:
                    return self.__jsonContent[contentText]
                else:
                    return {}
                
            # endregion

            # region Any

            else:

                if self.__jsonContent[contentText]:
                    return self.__jsonContent[contentText]
                else:
                    return None
            
            # endregion

        # endregion

        # region Not Such A ContentText

        else:

            if variableType == "int" or variableType == "float":

                return None
            
            elif variableType == "str":
                    
                return ""
            
            elif variableType == "bool":

                return 0
            
            elif variableType == "list":

                return []
            
            elif variableType == "dict":

                return {}
            
            else:

                return None
        
        # endregion

    # endregion

    # region File

    def file(self, fileName):

        if fileName in request.files:
            file = request.files[fileName]
            return file
        else:
            file = None
            return f"The {fileName} is not in request.files"

    # endregion

    # region Params

    def params(self, variable, variableType):

        if str(variable) in request.args:

            if variableType == "str":
                return str(request.args.get(variable)).strip()

            elif variableType == "int":
                return int(request.args.get(variable))

            elif variableType == "float":

                return float(request.args.get(variable))
            
            elif variableType == "bool":

                return 1 if request.args.get(variable) == True else 0
            
            elif variableType == "list":

                return ast.literal_eval(request.args.get(variable))
            
        else:
            if variableType == "str":
                return ""
            elif variableType == "int":
                return 0
            elif variableType == "float":
                return 0.0
            elif variableType == "bool":
                return 0
            elif variableType == "list":
                return []
            elif variableType == "dict":
                return {}
        
    # endregion

    # endregion

# endregion
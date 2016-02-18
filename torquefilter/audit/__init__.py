
import os, tempfile
import json

class jobauditer:
    
    def __init__ ( self, currentjob ):
        
        self.commands   =   currentjob.comm
        self.attributes =   currentjob.attr

        self.jsonData   =   { }
        self.fileName   =   None

        self.decodePython = json.JSONEncoder ()

    def _checkTable ( self, tableName ):
        """ Make sure tableName exists in jsonData """

        if ( not tableName in self.jsonData ):
            self.jsonData [tableName] = []

    def _checkArgs ( self, cmd, args ):
        """ Each member of args[] needs to be present in cmd[] """

        for argument in args:
            if ( not argument in cmd ):
                return False

        return True

    def _listToDict ( self, arry ):
        """ Convert arry list to dict assuming '-' character indicates key """

        rtnDict = { }

        endIdx = len ( arry ) - 1

        for index, value  in enumerate ( arry ):
            if ( index < endIdx ):
                if value.startswith ( '-' ):
                    nxtValue = arry [ index+1 ]
                    if nxtValue.startswith ( '-' ):
                        rtnDict [value] = True
                    else:
                        rtnDict [value] = nxtValue
            else:
                if value.startswith ( '-' ):
                    rtnDict [value] = True

        return rtnDict

    def _captureArgs ( self, cmd, args ):
        """ Create dict for each arg present in cmd """

        refDict = self._listToDict ( cmd )
        rtnDict = {}

        for argument in args:
            if ( argument in refDict ):
                rtnDict [argument] = refDict [argument]

        return rtnDict
        
    def _writeTable ( self, tableName, valueList ):
        """ Insert valueList into correct table in jsonData """

        self.jsonData [tableName].append ( valueList )

    def init ( self, nameProvided = None ):
        """ Set instance fileName for output """

        if ( nameProvided ):
            if ( os.path.exists ( nameProvided ) ):
                if ( os.path.isdir ( nameProvided ) ):
                    openfd = tempfile.NamedTemporaryFile ( mode='w', \
                            dir = nameProvided, delete = False )
                    self.fileName = openfd.name
                    openfd.close ()
                else:
                    self.fileName = nameProvided
        else:
            openfd = tempfile.NamedTemporaryFile ( mode = 'w', \
                        delete = False )
            self.fileName = openfd.name
            openfd.close ()


    def command ( self, cmdName, args = None ):
        """ Check presence of given command """

        for cmd in self.commands:
            if cmdName in cmd [0]:
                self._checkTable ( 'Commands' )

                if ( args ):
                    if ( self._checkArgs ( cmd, args ) ):
                        self._writeTable ( 'Commands', cmd )
                else:
                    self._writeTable ( 'Commands', cmd )


    def commandArgs ( self, cmdName, args, tableName = False ):
        """ Capture cmdName argument values or presence """

        for cmd in self.commands:
            if cmdName in cmd [0]:
                if ( tableName ):
                    self._checkTable ( tableName )
                else:
                    self._checkTable ( cmdName )
                    tableName = cmdName

                newDict = self._captureArgs ( cmd, args )

                self._writeTable ( tableName, newDict )


    def commandSlice ( self, cmdName, args = None , start = 1, end = None , tableName = False ):
        """ Capture a slice of the command matching cmdName and args """

        for cmd in self.commands:
            if cmdName in cmd [0]:

                if ( tableName ):
                    self._checkTable ( tableName )
                else:
                    self._checkTable ( cmdName )
                    tableName = cmdName

                if ( args ):
                    if ( self._checkArgs ( cmd, args ) ):
                        if ( not end ):
                            end = len ( cmd )
                            
                        self._writeTable ( tableName, cmd [start:end] )
                else:
                    if ( not end ):
                        end = len ( cmd )
                    
                    self._writeTable ( tableName, cmd [start:end] )

    
    def attr ( self, attrName, tableName = False ):
        """ Capture attributes value """

        if ( attrName in self.attributes ):
            self.jsonData [attrName] = self.attributes [attrName]

    def runaudit ( self ):
        """ Commit jsonData to a json file """

        outputfile = open ( self.fileName, mode='w' )
        json.dump ( self.decodePython.encode ( self.jsonData ), outputfile )

        outputfile.close ()

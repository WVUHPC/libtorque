
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
        """ 
        Set output filename/path depending on *nameProvided*.  If *None* audit
        class output would be set according python module tempfile.  If a
        directory is given, a tmpfile will be created and placed in that
        directory.  If a full filename is given, output is directed to given
        filename. 
        """

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
        """ 
        Check presence of *cmdName*.  If *args* (list of strings) are supplied,
        then given arguments must be present within command name in order to be
        recorded as a presence.  This method will only count the number of
        submitted jobs that have *cmdName* present.  If you want to capture
        specific details of command-line arguments use *commandArgs* or
        *commandSlice* method instead.

        For instance, if *cmdName* = 'mpirun' and *args* = ['-np'], the full
        command 'mpirun -host localhost sample.exe' will not be counted since
        the '-np' argument is not present.
        """

        for cmd in self.commands:
            if cmdName in cmd [0]:
                self._checkTable ( 'Commands' )

                if ( args ):
                    if ( self._checkArgs ( cmd, args ) ):
                        self._writeTable ( 'Commands', cmd )
                else:
                    self._writeTable ( 'Commands', cmd )


    def commandArgs ( self, cmdName, args, tableName = False ):
        """ 
        Capture the values of *args* (list of strings) when the *cmdName* 
        (string)  command is used in a job submission.  The output of this
        command will be placed in a entry *tableName*.

        For instance, if *cmdName* = 'mpirun' and *args* = ['-np'], the full
        command 'mpirun -np 15 -host localhost sample.exe' will record the
        argument value: '-np : 15'.  Multiple arguments can be supplied.  If
        given arguments are not all present, arguments that are present will be
        recorded.
        """

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
        """ 
        Capture a slice of a command when *cmdName* (string ) is used in a job
        submission.  What commands are audited is controlled by *cmdName* and
        *args* (list of strings).  Similiar to other command methods within the
        audit class.  If all the specified *args* are not present, the command
        slice is not captured.  The output of this command will be placed in a
        entry *tableName*.  The *start* and *end* parameters control what values
        are captured along the command line.

        For instance, if *cmdName* = 'mpirun', *args* = ['-np'], and *start* =
        2, and the full command 'mpirun -np 12 -host localhost sample.exe
        -output output.txt' The values '12', '-host', 'localhost', 'sample.exe',
        '-output' and 'output.txt' will all be recorded.  This is useful
        whenever you have a command that acts on a variable number of arguments,
        and you want to capture the range of arguments given.
        """

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
        """ 
        Capture *attrName* value in an entry *tableName*. 
        """

        if ( attrName in self.attributes ):
            self.jsonData [attrName] = self.attributes [attrName]

    def runaudit ( self ):
        """ 
        Write JSON output to outpufile.  This method should be run after all
        audit rules are setup.  This prevents numerous writes and data races
        among multiple file streams.
        """

        outputfile = open ( self.fileName, mode='w' )
        json.dump ( self.decodePython.encode ( self.jsonData ), outputfile )

        outputfile.close ()


class systeminfo:
    """ Structure for holding global system information """

    commandsToCheck     =   None
    queuesToCheck       =   None
    maxMem              =   54

    def addComm ( self, commands ):
        
        for comm in commands:
            self.commandsToCheck.append ( comm )

    def addQueue ( self, queues ):

        for name in queues:
            self.queuesToCheck.append ( name )


#!/bin/env python
# libtorque consense_audit.py
# Condenses tmp output files from torque_submitfilter into sqlite3 tables

import sqlite3
import time, os


def rtn_epoch ():
    """ Return a unique name with epoch stamp """

    epoch = time.time ()

    return epoch

def hashadd ( gbl_hash, file_hash ):
    """ Add file_hash values to gbl_hash values.  Summing any identical keys.
    """
    if ( not file_hash ):
        return gbl_hash

    for key in file_hash.keys ():
        if key in gbl_hash:
            gbl_hash [ key ] = gbl_hash [ key ] + file_hash [ key ]
        else:
            gbl_hash [ key ] = file_hash [ key ]

    return gbl_hash

def hash_from_file ( fname ):
    """ Extract hash from torque_submitfiler temp file """

    hash = { }

    try:
        fn = open ( fname, 'r' )
    except IOError:
        return False

    for line in fn:
        key = line.strip ('\n')
        if key in hash:
            hash [ key ] = hash [ key ] + 1
        else:
            hash [ key ] = 1

    return hash

def create_table ( fn ):
    """ Create necessary module table given a filename """

    if ( os.path.isfile ( fn ) ):
        return True

    conn = sqlite3.connect ( fn )
    c = conn.cursor ()

    c.execute ( '''CREATE TABLE modules
                    (module text, loads integer, epoch real)''' )
    c.execute ( '''CREATE TABLE ledger
                    (epoch real, filenum integer, modload integer)''')

    conn.commit ()
    conn.close ()

    return True



def ins_hash_sqlite ( fn, hash, epoch):
    """ Given a dict structure (hash) insert values into sqlite3 table (fn) """

    values = [ ]
    ledger = True

    # Filename must exist
    if ( not os.path.isfile ( fn ) ):
        return False

    conn = sqlite3.connect ( fn )
    c = conn.cursor ()

    # Insert number of files, and number of loads
    values.append ( epoch )
    if 'filenum' in hash:
        values.append ( hash ['filenum'] )
        del hash ['filenum']
    else:
        ledger = False

    if 'loadnum' in hash:
        values.append ( hash ['loadnum'] )
        del hash ['loadnum']
    else:
        ledger = False
   
    if ( ledger ):
        c.execute ( 'INSERT INTO ledger VALUES (?,?,?)', values )

    # Clear values list for re-use with second excutemany statment below
    del values [:]

    # Switch hash to array of arrays
    for key in hash.keys ():
        values.append ( [ key, hash [ key ], epoch ] )

    c.executemany ( 'INSERT INTO modules VALUES (?,?,?)', values )

    conn.commit ()
    conn.close ()

def main ():
    """ Condense all temp module load audit files from torque submitfilter into
    a single sqlite3 table """

    # Total dictionary
    gbl_hash = { }

    # file list
    filedel = [ ]

    # Hardcode directories into CLI API put into place
    indir = "/shared/moduleaudit"
    outdir = "/shared/audit_report"
    outfile = "moduleloads.sql"

    # Add each file to total dictionary
    filenum = 0
    modload = 0
    for fname in os.listdir ( indir ):
        filenum += 1
        file_hash = { }
        fullpath = indir + "/" + fname
        
        file_hash = hash_from_file ( fullpath )

        if ( file_hash == False ):
            continue

        if ( len ( file_hash ) > 0):
            modload += 1
            gbl_hash = hashadd ( gbl_hash, file_hash )

        filedel.append ( fullpath )

    # Put gbl_hash in sqlite db, delete files
    gbl_hash ['filenum'] = filenum
    gbl_hash ['loadnum'] = modload
    dbfile = outdir + "/" + outfile
    create_table ( dbfile )
    ins_hash_sqlite ( dbfile, gbl_hash, rtn_epoch () )

    # Delete files - but for now just exit
    for fname in filedel:
        os.unlink ( fname )
    
if __name__ == '__main__':
    main ()

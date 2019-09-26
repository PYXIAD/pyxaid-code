#!/usr/bin/env python3
# Convert python driver parameters to a C++ input file for the MPI version of Pyxaid.
# I'm not sure everyone uses the same format we do, so this makes the best attempt.
# Dave Turner - Kansas State University - April 2018

# USAGE: py2inputfile.py [python_script_name] [c_input_filename]

import sys
import re

python_script = sys.argv[1]
input_filename = sys.argv[2]

fo = open( input_filename, "w" )
fo.write( "# NOTE:  You may need to delete some junk python lines in this file\n")
fo.write( "# NOTE:  If you define a base directory for Ham and Hprime, include a 'basedir =' line first\n")

fi = open( python_script, "r" )

for lcount, line in enumerate( fi ):

   line = re.sub( r'#.*$', "", line)   # Remove comments
   line = re.sub( r'\n', "", line)     # Remove new line

   if( "states" in line and re.search( r'\[\ *\]', line) ) :
      fo.write( "# Each state below should have information separated by spaces like:\n")
      fo.write( "# states = GS 6 -6 7 -7 8 -8 0.00\n" )

   elif( "states" in line and ".append" in line ) : 
      state_obj = re.search( ".append *\((.*)\)", line )
      state = re.sub( r'[[\],"]', " ", state_obj.group(1) )
      #state = re.sub( r'\[\]\"\,', " ", state_obj.group(1) )
      fo.write( "states = " + state + '\n')

   elif( "=" in line ) : 

      line = re.sub( r' ', "", line)     # Remove spaces
      param_obj = re.search( r'\S+[\[]+(\S+)[\]]+=([^$]+)', line ) # Get key and value
      if( param_obj ) :
         key   = re.sub( r'\"', "", param_obj.group(1) )
         value = re.sub( r'\"', "", param_obj.group(2) )
         value = re.sub( r'\S+\+', "", value)         # Remove basedir+ for Ham and Hprime
         value = re.sub( r'[\[\],]', " ", value)      # Delimit with spaces

         if( "iconds" in key ) :
            fo.write( "# NOTE: Set icond_max and nmicrost variables below\n")
            fo.write( "# NOTE: and the C++ code will loop to set up icond\n")

         else :
            fo.write( key + " = " + value + '\n' )

      else :    # Non param variable assignment
         line = re.sub( r'\"', "", line )
         line = re.sub( r'=', " = ", line)
         fo.write( line + '\n' )

   if( "pyxaid_core.namd" in line ) : break       # Exit build of the input file

 


fi.close()
fo.close()


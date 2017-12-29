'''
*
* A script to scrape cryptocurrency market cap and ranking on daily basis
*
* VERSION: 1.2
*   - ADDED   : Compares cryptocurrencies based on market cap and change in rank.
*               In addition, store that into a log file
*
* ROADMAP:
*   - Determine which coin has the highest change for a given day.
*   - Create a plot on demand for COI or whatever coin chosen.
*   - Streamline code and clean up redundencies + create functions.
*   - Store [DIFF] as a table instead of an ugly ass looking list (maybe).
*   - Automate code to run on more regular intervals instead of manually once a day.
*
* AUTHORED    : MOHAMMAD ODEH
* DATE        : Dec. 26th, 2017 Year of Our Lord
*
* MODIFIED    : Dec. 29th, 2017 Year of Our Lord
*
'''

# Import modules
from    bs4                 import  BeautifulSoup   as  bs
from    datetime            import  datetime, timedelta
import  requests, re, os, platform, getpass

# ************************************************************************
# ===========================> READ CONFIG FILE <========================*
# ************************************************************************

sampleConfig =  ( "# Write down ticker of coins of special interest.\n"
                  "# Lines starting with a hashtag (#) will be ignored.\n"
                  "\n"
                  "# Ethereum\n"
                  "ETH\n"
                  "\n"
                  "# Ripple\n"
                  "XRP\n"
                  "\n"
                  "# Golem\n"
                  "GNT")

COI = []                                        # Start an empty list for Coins of Interest (COI)

configFile = 'config.ini'                       # Define name of config file

if( os.path.isfile(configFile) == False ):      # Check whether config.ini exists or not
    print( "config.ini DNE. Creating sample..." ) ,
    with open( configFile, 'w' ) as f:          # Open file for writing
        f.write( sampleConfig )                 # Write sample config.ini file
    print( "Success!" )

# Extract COI from config.ini file
with open( configFile, 'r' ) as f:              # Open file for reading
    for line in f:                              # Read line-by-line
        if not line.strip(): continue           # Skip empty lines
        else:
            if( line[0] == '#' ): continue      # Skip comments
            else: COI.append( line.strip() )    # Append COI to list

print( COI )

# ************************************************************************
# =====================> PREPARE LOGGING ENVIRONMENT <===================*
# ************************************************************************

# Store logfile under today's date dd-mm-yyy
now = datetime.now()
logFile = "%d-%d-%d.txt" %( now.day, now.month, now.year )

# Prepare log file and folder
if( platform.system() == 'Linux' ):

    # Define useful paths
    homeDir = "/home/" + getpass.getuser()      # Home directory    
    dst = homeDir + "/cryptoScrapper_logs"      # Destination (where log files are to be saved)

    # Directory check
    if( os.path.exists( dst ) == False ):       # Check if directory exist ...
        os.makedirs( dst )                      # ... if NOT, create it!
    else: pass

    # Logfile check
    if( os.path.isfile(dst + "/" + logFile) ):  # Check whether a logfile with today's date exists
        print( "Log exists. Overwrite?" )       # ...
        print( "1. (Y)es" )                     # Prompt to overwrite
        print( "2. (N)o\n" )                      # ...
        
        overwrite = raw_input( "$:>\ " )        # Store choice

        if( overwrite != 'y' ): quit()          # If No, quit
        else: pass                              # If Yes, overwrite!
        

# Directory/logfile setup done. Switch to working directory.
os.chdir( dst )                                 # Change working directory to dst
print( ">\ Log stored under: %s\n" %logFile )   # Inform logfile name


# ************************************************************************
# =====================> SETUP SCRAPPING PARAMETERS <====================*
# ************************************************************************

URL = 'http://coinmarketcap.com/'

print( ">\ Accessing %s..." %URL ) ,

# Define URL of webpage to scrape
request = requests.get( URL )
content = request.content

# Parse webpage
soup = bs(content, 'html.parser')  

# Look for the data of interest
table = soup.findChildren('table')[0]
rows = table.findChildren('tr')

# Extract data and print to screen
headers = [x.getText() for x in rows[0].findChildren('th')]

print( "Success!" )

# ************************************************************************
# =====================> PRINT & STORE SCRAPPED DATA  <==================*
# ************************************************************************

print( ">\ Storing logfile..." ) ,

# Write to file / Print to screen
with open( logFile, 'w+' ) as f:
    j = 0                                       # Counter to print headers
    for row in rows:
        cells = row.findChildren('td')
        for i in range( 0, len(cells) ):
            cell_content = cells[i].getText()
            stripped_content = re.sub( '\s+', ' ',
                                       cell_content).strip()
            
            if( j != 7 ):                       # 8th header is useless, no need to print it
##                print( headers[j] + ' :') ,
                f.write( "%s :" %headers[j] )
                j += 1                          # Increment j index by 1
                
            else:
                j = 0                           # if j is equal to 7, reset counter & do NOT print
                
##            print( stripped_content )           # Print content
            f.write( "%s\n" %stripped_content )

print( "Success!" )

# ************************************************************************
# =============================> ANALYZE DATA  <=========================*
# ************************************************************************
today = []                                          # List to store today's data
ayer  = []                                          # List to store yesterday's data
delta = []                                          # List to store analyzed data

print( ">\ Performing data analysis..." ) ,

# Open today's logfile
with open( logFile, 'r' ) as f:                     # Open file for reading
    for line in f:                                  # Read line-by-line
        
        if( line[0] == '#' ):                       # Store coin's ranking
            delimeter = " :"
            
            startPos = line.find( delimeter )       # Find delimeter position
            today.append( line[startPos+2:-1] )     # Append to list

        elif( line[0] == 'N' ):                     # Store coin's name
            delimeter = " :"
            
            startPos = line.find( delimeter )       # Find delimeter position
            today.append( line[startPos+2:-1] )     # Append to list

        elif( line[0] == 'M' ):                     # Store coin's market cap
            delimeter = " :$"
            
            startPos = line.find( delimeter )       # Find delimeter position
            val = line[startPos+3:-1]               # Read value
            val = val.replace( ',', '' )            # Convert to integer
            today.append( val )                     # Append to list
     
# Open yesterday's logfile
now = now - timedelta(1)
logFile = "%d-%d-%d.txt" %( now.day, now.month, now.year )
with open( logFile, 'r' ) as f:                     # Open file for reading
    for line in f:                                  # Read line-by-line
        
        if( line[0] == '#' ):                       # Store coin's ranking
            delimeter = " :"
            
            startPos = line.find( delimeter )       # Find delimeter position
            ayer.append( line[startPos+2:-1] )      # Append to list

        elif( line[0] == 'N' ):                     # Store coin's name
            delimeter = " :"
            
            startPos = line.find( delimeter )       # Find delimeter position
            ayer.append( line[startPos+2:-1] )      # Append to list

        elif( line[0] == 'M' ):                     # Store coin's market cap
            delimeter = " :$"
            
            startPos = line.find( delimeter )       # Find delimeter position
            val = line[startPos+3:-1]               # Read value
            val = val.replace( ',', '' )            # Convert to integer
            ayer.append( val )                      # Append to list

# Find difference accrued in one day
# i == Ranking
# j == Name
# k == Market Cap
for j in range( 1, len(today), 3 ):                 # Loop over all crypocurrencies
    if( today[j] in ayer ):                         # Check if coin is still in first 100 coins

        ndx = ayer.index( today[j] )                # Get index of coin in yesterday's list
        
        # Find difference in ranking
        i = int( ayer[ndx-1] ) - int( today[j-1] )  # Calculate difference in ranking
        if( i > 0 )  : rankDiff = ( "+%r" %i )      # If it moved up in ranking
        elif( i < 0 ): rankDiff = ( " %r" %i )      # If it moved down in ranking
        else         : rankDiff = ( " %r" %i )      # If it stayed the same

        # Find difference in market cap
        k = int( today[j+1] ) - int( ayer[ndx+1] )  # Calculate difference in market cap
        if( k > 0 )  : capDiff = ( "+%r" %k )       # If it moved up in market cap
        elif( k < 0 ): capDiff = ( " %r" %k )       # If it moved down in market cap
        else         : capDiff = ( " %r" %k )       # If it stayed the same

        delta.append( rankDiff )                    # Append rank difference to list
        delta.append( today[j] )                    # Append crypto name to list
        delta.append( capDiff  )                    # Append market cap difference to list
        delta.append( '\n'     )                    # Append a newline for aesthetics

print( "Success!" )

now = datetime.now()
updateLogFile = ( '[DIFF]_%d-%d-%d' %(now.day,
                                      now.month,
                                      now.year) )

print( ">\ Storing under %s..." %updateLogFile ) ,
                        
with open( updateLogFile, 'w' ) as f:               # Open file for writing
    for item in delta:
        if( item == '\n'): f.write( item )          # Write spaces for ease of reading
        else             : f.write( "%s\n" %item )  # Write computed differences

print( "Success!" )

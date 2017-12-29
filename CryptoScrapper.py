'''
*
* A script to scrape cryptocurrency market cap and ranking on daily basis
*
* VERSION: 1.1.1
*   - ADDED   : Store logfile under a folder for later data analysis
*   - ADDED   : Create a config.ini file for COI (will implement data analysis
*               and pay close attention to COI found in config.ini in later update)
*
* AUTHORED  : MOHAMMAD ODEH
* DATE      : Dec. 26th, 2017 Year of Our Lord
*
* MODIFIED  : Dec. 29th, 2017 Year of Our Lord
*
'''

# Import modules
from    bs4                 import  BeautifulSoup   as  bs
from    datetime            import  datetime
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
logFile = "[LOG]_%d-%d-%d.txt" %( now.day, now.month, now.year )

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
    mode = 'w+'
    if( os.path.isfile(dst + "/" + logFile) ):  # Check whether a logfile with today's date exists
        print( "Log exists. Overwrite?" )       # ...
        print( "1. Yes" )                       # Prompt to overwrite
        print( "2. No" )                        # ...
        
        overwrite = raw_input( ">\ " )          # Store choice

        if( overwrite != '1' ): quit()          # If No, quit
        else: print( "OVERWRITTING!!!" )        # If Yes, overwrite!
        

# Directory/logfile setup done. Switch to working directory.
os.chdir( dst )                                 # Change working directory to dst
print( ">\ Log stored under: %s" %logFile )     # Inform logfile name


# ************************************************************************
# =====================> SETUP SCRAPPING PARAMETERS <====================*
# ************************************************************************

# Define URL of webpage to scrape
request = requests.get( 'http://coinmarketcap.com/' )
content = request.content

# Parse webpage
soup = bs(content, 'html.parser')  

# Look for the data of interest
table = soup.findChildren('table')[0]
rows = table.findChildren('tr')

# Extract data and print to screen
headers = [x.getText() for x in rows[0].findChildren('th')]


# ************************************************************************
# =====================> PRINT & STORE SCRAPPED DATA  <==================*
# ************************************************************************

# Write to file / Print to screen
with open( logFile, mode ) as f:
    j = 0                                       # Counter to print headers
    for row in rows:
        cells = row.findChildren('td')
        for i in range( 0, len(cells) ):
            cell_content = cells[i].getText()
            stripped_content = re.sub( '\s+', ' ',
                                       cell_content).strip()
            
            if( j != 7 ):                       # 8th header is useless, no need to print it
                print( headers[j] + ' :') ,
                f.write( "%s :" %headers[j] )
                j += 1                          # Increment j index by 1
                
            else:
                j = 0                           # if j is equal to 7, reset counter & do NOT print
                
            print( stripped_content )           # Print content
            f.write( "%s\n" %stripped_content )

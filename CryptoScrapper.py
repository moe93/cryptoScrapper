'''
*
* A script to scrape cryptocurrency market cap and ranking on daily basis
*
* VERSION: 1.1
*   - ADDED   : Store logfile under a folder for later data analysis
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
# =======================> DEFINE GLOBAL VARIABLES <=====================*
# ************************************************************************

##overwrite = 0                                   # Overwrite or nah!
##mode = ''                                       # What mode to open logfile under

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

### Print to screen
##j = 0                                       # Counter to print headers
##for row in rows:
##    cells = row.findChildren('td')
##    for i in range( 0, len(cells) ):
##        cell_content = cells[i].getText()
##        stripped_content = re.sub( '\s+', ' ',
##                                   cell_content).strip()
##        
##        if( j != 7 ):                       # 8th header is useless, no need to print it
##            print( headers[j] + ' :') ,
##            j += 1                          # Increment j index by 1
##            
##        else:
##            j = 0                           # if j is equal to 7, reset counter & do NOT print
##            
##        print( stripped_content )           # Print content

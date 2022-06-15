import requests
from requests import get
from requests.exceptions import RequestException

print("Finding Criminals...")

# included in everyweb search
url = "http://media.graytvinc.com/documents/"

#file extension we are trying to hunt for
extention = ".pdf"

#possiable file seperators in the document we are hunting
seperator = [ "-", "_" ]
#seperator_rare = [ "/", "_", ".", "," ]

#possiable constant strings that preceed unique identifiers
#in the file we are hunting.
booking_report = [ "Booking+Report+", "LCSO+Booking+Report+",
                    "LCSO+Daily+Booking+Report+", "Daily+Booking+Report+",
                    "LCSO+Daily+Booking+Report1+" ]

# Various permuations of the years 2000 - 2020
#years = [ "12", "13", "14", "15", "16", "17", "18", "19", "20" ]
years = [ "2000", "2001", "2002", "2003", "2004", "2005",
          "2006", "2007", "2008", "2009", "2010", "2011",
          "2012", "2013", "2014", "2015", "2016", "2017",
          "2018", "2019", "2020",
          "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
          "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
          "11", "12", "13", "14", "15", "16", "17", "18", "19", "20" ]
#years_short = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]

# Various permuations of the 12 months of the calender
months = [ "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
           "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
           "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
           "Sep", "Sept", "Oct", "Nov", "Dec", "jan", "feb", "mar", "apr",
           "may", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec" ]


# Varoius permuations of the values days of a month can hold.
# --Dont worry about some months having less than 31 days,
# its actually faster to just get told by the http that it
# dosent exist rather than try and parse days. also this catches
# any miss-typings by the publisher.
days = [ "01", "02", "03", "04", "05", "06", "07", "08", "09",
         "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
         "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
         "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
         "31" ]


def Grab(prefix, formatted_date):
    image_url = url + prefix + formatted_date + extention
    saved_file = formatted_date + extention

    # URL of the image to be downloaded is defined as image_url
    r = requests.get(image_url) # create HTTP response object
    was_found = r.status_code

    if was_found == 200:
        # send a HTTP request to the server and save the HTTP response in a response object called r
        with open(saved_file,'wb') as f:
            # Save as png file in binary format write the contents of the response (r.content) to a new file in binary mode.
            f.write(r.content)
            print("        " + formatted_date + "    [X]")
            return;
    else:
        #print("        " + formatted_date + "    [ ]")
        return;


def Assemble(pref, a, b, c):
    for s in seperator:
        result = a + s + b + s + c
        Grab(pref, result)


def Setformat(prefix, month, day, year):
    Assemble(prefix, month, day, year)
    Assemble(prefix, year, month, day)
    Assemble(prefix, day, month, year)


for a in booking_report:
    print("------------------------------------------------")
    for z in years:

        for x in months:

            for y in days:
                Setformat(a, x, y, z)

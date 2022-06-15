entry point:

    ./run.sh <-X>

  where X is any of the following commands:

    1)   -n
    This means run a new pdf parse and generate a new sorted
    list from the results of the pdf breakdowns. This is a lengthy
    operation (3 min for 20,000 pdf's). This will not take into account
    previous correct entry's, this will delete all previous
    text files and start new.


    2)   -u
    This means update. this will check the log and determine
    the last date an arrest record was scraped from the internet
    and check for all new records up until today's date.


    3)   -gui
    Just launch the gui feature. this assumes the current records
    have been inserted already or this is for offline use where the
    user does not need to find more current records or lastly for
    maintenance procedures by the maintainer.

    4)   -log
    Show contents of LOG.d file.

    5)   -grab
    Will do a massive search over all iterations through all years. you
    should modify the "getpdfs.py" file if you want to make a search
    other than my parameters, i.e. go to a different website. This is mostly
    just a tool to launch the python script. This could also be used to
    get every pdf from every year if you accidentally deleted them.


From the GUI menu:
    - Update will update the arrest records to the most current release.
    - View Log will display all actions saved in the master log associated
      with this application.
    - Clear will clear the current screen.
    - Exit will close this program.


Tips:
     - You can always just type a name or date into the
       search bar and start looking for dirt-bags.
     - Don't worry about capitalization.
     - If you think you don't know how to spell the name
       then type the portion you do know. 

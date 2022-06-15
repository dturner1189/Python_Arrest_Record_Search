#!/bin/bash

clear

update_use_log() {
    #echo "Updating log file..."
    timestamp=$(date "+%Y%m%d, %H%M%S")
    echo "$1 $timestamp" >> LOG.d
}

escape_prog() {
    echo -e "\n\n"
    read -p "Press any key to exit:  " DONE
    exit 0
}

if [ "$#" -eq 0 ]; then
    echo -e "How to use:\n"
    more ./help.d
    escape_prog
fi



if [ ! -e "LOG.d" ]; then
    echo "Generating new log..."
    touch LOG.d
    chmod 755 ./LOG.d
    update_use_log "First use: "
    update_use_log "Last arrest record: 01012019"
fi


#####
if [ "$1" == "-n" ]; then

    rm ./*.txt

    echo "#!/bin/bash" > to_text.sh

    ls -l *.pdf | awk '{print "pdftotext " $9}' >> to_text.sh

    chmod 755 ./to_text.sh

    ./to_text.sh


    ######


    echo "#!/bin/bash" > commands.sh

    ls -l *.txt | awk '{print "./getnames.sh " $9}' >> commands.sh

    chmod 755 ./commands.sh

    ./commands.sh

    rm ./to_text.sh
    rm ./commands.sh

    rm ./*.txt

    cat names.d | sort -n -k 1,1 > sorted.txt

    rm ./names.d

    clear
    echo "All done..."
    echo "Launching GUI..."

    update_use_log "completed pdf scrape and sorting operation: "
    update_use_log "Launched gui:"

    python gui.py

    exit 0
fi

if [ "$1" == "-u" ]; then

    today_md=$(date "+%-m-%-d-")
    year=$(date "+%Y" | cut -c 3-)
    today="$today_md$year"
    echo "$today"

    todays_pdf="$today.pdf"
    if [ -e "$todays_pdf" ]; then
        echo "Todays arrest record has been found in your archive..."
        echo "Looks like your up to date."
        update_use_log "Last arrest record: $todays_pdf  "
        escape_prog
    fi

    # still need to fix ranges when using the python script
    # as it still searches every day in the year 2019
    if [ ! -e "$todays_pdf" ]; then
        echo "No pdf found for today in your database, lets find it."

        python getpdfspecific.py
    fi

    update_use_log "updated pdf directory: "

    exit 0
fi

if [ "$1" == "-gui" ]; then
    update_use_log "Launched gui: "
    python gui.py

    exit 0

fi

if [ "$1" == "-log" ]; then
    update_use_log "viewed log: "
    more LOG.d

    escape_prog
fi

if [ "$1" == "-grab" ]; then
    update_use_log "Massive web scrape: "
    echo "begining web scrape..."
    python getpdfs.py
    echo "Done web scrape..."
    update_use_log "Completed Massive web scrape: "
    escape_prog
fi

#!/bin/bash
# This script is used as a one time function.
# this code is called many times over and over
# by another generating script. So this means that
# files are handled here one at a time.
clear

# input file is the output file generated by the
# calling script. This is the result of pdftotext linux
# command. This will be the name of the pdf, with a
# .txt extention.
input_file="$1"

# this is a log that gets appended to by each file passing
# through this script. Do not delete this file, only append to.
output_file="names.d"

# regex the date of arrest found on the txt file gend from the pdf.
date_of_arrest=$(grep -o -m 1 "[0-9]\{2\}/[0-9]\{2\}/[0-9]\{4\}" $input_file | sort --unique)

# if the pdftotext command was a success then this file will exist...
if [ -e "$input_file" ]; then

    # grep all unique names found on the txt file.
    # saved on a temp file for later sorting.
    names_of_arrested=$(grep [a-zA-Z], "$1" > tmp.d)

    # desired name of data text file with / seperators (invalid)
    txt_name="$date_of_arrest.txt"
    # replacing / with -
    replace="-"
    # regex replacement
    new_txt=${txt_name//\//$replace}
    #rename the text file to dd-mm-yyyy.txt
    mv "$input_file" "$new_txt"

    # take the name of the text file (due to bad formatting
    # from the sourced pdf website) and replace the double
    # extension .txt with pdf to get the actual saved pdf name.
    tainted_pdf_name="$input_file"
    # replace
    replace_with=".pdf"
    # this is now the original name of the pdf we are minipulating.
    old_pdf_name=${tainted_pdf_name//.txt/$replace_with}

    # desired pdf name with  / seperator
    pdf_date="$date_of_arrest.pdf"
    # replace all / with -
    replace2="-"
    # regex replacement
    new_pdf_name=${pdf_date//\//$replace}
    # rename the pdf to dd-mm-yyyy.pdf for easier handling later.
    mv "$old_pdf_name" "$new_pdf_name"
fi

# regex the name of both pdf and txt, so at this point
# its really just the date in dd-mm-yyyy format.
file_found_on=$(echo "$new_txt" | cut -f 1 -d '.')

# append the master records log with all the new people
# found on the input text file.
awk -v file="$file_found_on" '{print $1 " " $2 " "$3 " " file}' tmp.d >> $output_file

# remove temp file with unsorted names.
rm ./tmp.d

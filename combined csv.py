# csv: day, comments, and sentiments on that day
import csv

HEADERS_TO_COPY = ['num_comments', 'mean_compound', 'num_positive', 'mean_positive', 'mean_positive', 'num_negative', 'mean_negative', 'num_neutral', 'mean_neutral']

CSV_FILE = "KeepBritainInEurope_facebook"
ROOT = "/Users/Tara/Desktop/C/Writing/sentiment analysis"
INPUT_FILE1 = ROOT + "/sentiment/" + "sentiment_" +  CSV_FILE + "_statuses.csv"
INPUT_FILE2 = ROOT + "/sentiment/" + "sentiment_" +  CSV_FILE + "_comments.csv"

OUTPUT_FILE = ROOT + "/sentiment/" + "sentiment_" + CSV_FILE + "_combined.csv"

#
def dict_maker(file):
    dict = {}
    with open(file, 'rb') as csvFile:
        reader1 = csv.DictReader(csvFile)
        for row in reader1:
            dict[row["date"]] = {}

            for header in HEADERS_TO_COPY:
                dict[row["date"]][header] = row[header]
    return dict

writer = csv.writer(open(OUTPUT_FILE, "wb"), delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)

# write headers
def prefix_headers(prefix):
    array = []
    for header in HEADERS_TO_COPY:
        array.append(prefix + header)
    return array

headers = []
headers.append("date")
headers.extend(prefix_headers("status_"))
headers.extend(prefix_headers("comment_"))
writer.writerow(headers)

# write rows
file1 = dict_maker(INPUT_FILE1)
file2 = dict_maker(INPUT_FILE2)

dates = set(file1.keys() + file2.keys())

for date in sorted(dates):
    row = []
    row.append(date)

    if file1.has_key(date):
        for header in HEADERS_TO_COPY:
            row.append(file1[date][header])
    else:
        for header in HEADERS_TO_COPY:
            row.append("")

    if file2.has_key(date):
        for header in HEADERS_TO_COPY:
            row.append(file2[date][header])
    else:
        for header in HEADERS_TO_COPY:
            row.append("")

    writer.writerow(row)
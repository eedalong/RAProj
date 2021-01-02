import csv
def isCompanyName(name):
    tokens = ["CORP", "LTD", "INC", "FUND", "CO", "LLC", "BANK", "PARTNERSHIP", "PARTNERS"]
    name = name.upper()
    for token in tokens:
        if token in name:
            return True
    return False


cleaned_file = open("cleaned_activist_list.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(cleaned_file)
file_path = r"activist_list.csv"
input_file = open(file_path)
csv_reader = csv.reader(input_file)
data = next(csv_reader)
csv_writer.writerow(data)
filtered = list(filter(lambda x: isCompanyName(x[1]),csv_reader))
print("all company number ", len(filtered))
csv_writer.writerows(filtered)





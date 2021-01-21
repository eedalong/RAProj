import csv
import os
import match_module
def commonToken(res, namePos=1):
    nameList = []
    for item in res:
        if len(item) > namePos:
            nameList.append(item[namePos])

    # extract removed token
    removedToken = match_module.commonToken(nameList)

    return removedToken

def getReverseIndex(res, indexPos, removedToken):
        # create reverse index
        reverseIndex = match_module.reverseIndex(res, indexPos, removedToken)
        return reverseIndex

def match_name(names, index_dict, removed_token):
    currentScore = 0
    currentItem = None
    for name in names:
        name = name.upper()
        tmp_data = name.replace(".", "").replace(",", '').split()
        for token in tmp_data:
            score, tmp_item = match_module.fuzzy_match(name, index_dict.get(token, []), 1, removed_token,60)
            if score > currentScore:
                currentScore = score
                currentItem = tmp_item
    return currentItem
processed_files = ["indivs{0:02d}.txt".format(index) for index in range(00, 20, 2)] + ["indivs{0:02d}.txt".format(index) for index in range(90, 100, 2)]
#processed_files = ["indivs16.txt"]

print(processed_files)
activist_file = open("cleaned_activist.csv")
activist_reader = list(csv.reader(activist_file))


removed_token = commonToken(activist_reader, 1)
index_dict = getReverseIndex(activist_reader, 1, removed_token)
print("check keys", len(index_dict))

res_file = open("res_file_temp", "w")
matched_count = 0
total_count = 0
for file in processed_files:
    if not os.path.exists(file):
        continue
    print("check processing file", file)

    with open(file, encoding="utf8") as input_file:
        while True:
            try:
                line = next(input_file)
            except StopIteration:
                break
            except Exception as e:
                print(e)
                continue
            data = line.split("|")
            data = list(filter(lambda x: x!="," and x!='\n', data))
            if len(data) < 20:
                continue
            if data[0] == "":
                data = data[1:]

            candidate = match_name([data[5],data[6], data[-2]], removed_token=removed_token, index_dict=index_dict)
            if candidate:
                line += f",|{candidate[0]}|{candidate[1]}\n"
                res_file.write(line)
                matched_count += 1
            total_count += 1
            if total_count % 1000 == 0:
                print(f"process {total_count}, matched {matched_count}")

        print(f"matched_count is {matched_count}, totla_count is {total_count}, matched_rate = {matched_count*1.0/total_count}")

os.rename("res_file_temp", "res_file_all")








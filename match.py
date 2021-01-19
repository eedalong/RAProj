import csv
import os
def ngram(string, n):
    return [string[start:start+n] for start in range(0, len(string), n)]

def find_meaningless_token(all_data, k = 20):
    count = {}
    for item in all_data:
        data = item[1].upper().replace("/", " ").replace(",", " ").split()
        for token in data:
            count[token] = count.get(token, 0) + 1
    sorted_token = sorted(count, key=lambda x: count[x])
    return set(sorted_token[:k])

def build_index(all_data, removed_token):
    index_dict = {}
    for item in all_data:
        data = set(item[1].upper().replace("/", " ").replace(",", " ").split())
        indexed_token = data - removed_token
        for token  in indexed_token:
            if index_dict.get(token, None) is None:
                index_dict[token] = []
            index_dict[token].append(item)
    return index_dict
def company_name_match(name_a, name_b, removed_token):

    name_a = name_a.replace(".", "").replace(",","")
    name_b = name_b.replace(".", "").replace(",","")

    token_a = set(name_a.upper().split())
    token_b = set(name_b.upper().split())
    token_a -= removed_token
    token_b -= removed_token

    if len(token_a.union(token_b)) == 0:
        return 0

    score = (len(token_a.intersection(token_b)) * 1.0 / len(token_a.union(token_b))) * 100

    return score > 60
def sameCompany(name1, name2, removed_token):
    item1 = set(name1.upper().replace("/", " ").replace(",", " ").split())
    item2 = set(name2.upper().replace("/", " ").replace(",", " ").split())
    item1 -= removed_token
    item2 -= removed_token
    return len(item1.intersection(item2)) * 1.0/ len(item2.union(item1)) > 0.8
def match_name(name, index_dict, removed_token):
    item = set(name.upper().replace("/", " ").replace(",", " ").split())
    item -= removed_token
    for token in item:
        candidates = index_dict.get(token, [])
        for candidate in candidates:
            if company_name_match(name, candidate[1], removed_token):
                return candidate
    return None
processed_files = ["indivs{0:02d}.txt".format(index) for index in range(00, 20, 2)] + ["indivs{0:02d}.txt".format(index) for index in range(90, 100, 2)]
print(processed_files)
activist_file = open("cleaned_activist_list.csv")
activist_reader = list(csv.reader(activist_file))
removed_token = find_meaningless_token(activist_reader)
index_dict = build_index(activist_reader, removed_token)
print("check keys", len(index_dict))

res_file = open("res_file", "w")
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
            candidate = match_name(data[5].upper(), index_dict=index_dict, removed_token=removed_token) or \
                        match_name(data[6].upper(), index_dict=index_dict, removed_token=removed_token) or \
                        match_name(data[-2].upper(), index_dict=index_dict, removed_token=removed_token)

            if candidate:
                line += f",|{candidate[0]}|{candidate[1]}\n"
                res_file.write(line)
                matched_count += 1
            total_count += 1
            if total_count % 1000 == 0:
                pass

        print(f"check for file {file} , matched_count is {matched_count}, totla_count is {total_count}, matched_rate = {matched_count*1.0/total_count}")










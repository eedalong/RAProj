import csv
def isCompanyName(name):
    tokens = ["CORP", "LTD", "INC", "FUND", "CO", "LLC", "BANK", "PARTNERSHIP", "PARTNERS"]
    name = name.upper()
    for token in tokens:
        if token in name:
            return True
    return False

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

def match_name(name, index_dict, removed_token):
    item = set(name.upper().replace("/", " ").replace(",", " ").split())
    item -= removed_token
    for token in item:
        candidates = index_dict.get(token, [])
        for candidate in candidates:
            if company_name_match(name, candidate[1], removed_token):
                return candidate
    return None


if __name__ == "__main__":
    company_name_file = open("company_list.csv")
    csv_reader = csv.reader(company_name_file)
    all_companys = list(csv_reader)
    index_dict = build_index(all_companys, set([]))
    out_file = open("matched_company.csv", newline="", mode="w")
    csv_writer = csv.writer(out_file)

    activist_reader = csv.reader(open('activist_list.csv'))
    index = 0
    title = next(activist_reader)
    title += ["is_company", "gv_key", "company_name"]
    csv_writer.writerow(title)

    for line in activist_reader:
        res = match_name(line[1], index_dict, removed_token=set([]))
        if res:
            data = line + [1] + res
        elif isCompanyName(line[1]):
            data = line + [1] + ["", ""]
        else:
            data = line + [0] + ["", ""]
        csv_writer.writerow(data)
        if index % 10 == 0:
            print(index)

        index += 1
    out_file.close()



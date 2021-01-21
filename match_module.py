import csv
tokens = ["CORP", "LTD", "INC", "FUND", "CO", "LLC", "BANK", "PARTNERSHIP", "PARTNERS",
              "LP", "L.P", "LLP", "TRUST", "TRUSTEE", "FUND", "PLC","ADVISOR", "GROUP",
              "INVESTMENT", "INVEST", "VENTURES", "BANK", "VC", "SPA", "COM", "/",
              "HOLDINGS", "ESTATE", "EQUITY", "FOUNDATION", "HOMIES", "CAPITAL",
              "INDUSTRIES", "COMMITTEE", "KEEPING", "AVV", "CONSORTIUM", "ASSET ",
              "MANAGEMENT","ACQUISITION","ENTERPRISES","AKTIENGESELLSCHAFT",
              "COMPUTER","INNOVATION","TECHNOLOGIES","SA", "AG", "&", "S A", "A G",
              "L.L.C", "INSURANCE", "ASSOCIATION", "L P", "L L C", "S.A.", "-", "S.A",
              "Interactive","Resources", "Reserve","Global","Cross","Federal","Financial",
              "Association","Enterprise","Pharmaceuticals","Establishment","Center",
              "N.V.","Research","TEL","TEST","THERAPEUTICS","ASSOCIATES","Portfolios",
              "CREDIT","CREDITS","Venture","Holding","Energy","Health","Plan","Mutual",
              "S.p.A.","Financial","Family","Debt","Insurance","International","FINANCE","REPUBLIC",
              "PENSION","MHC","G.P.","L.L.C.","S.A.","tech",
              "S.a.r.l.","Bhd","LABORATORIES","BNP","TECHNOLOGY","ELECTRONICS","PROPERTIES",
              "SYSTEM","MEDICAL"
              ]
def commonToken(nameList):
    all_words = {}
    for name in nameList:
        company_name = name.replace(".", "").replace(",", "").split()
        for word in company_name:
            word = word.upper()
            all_words[word] = all_words.get(word, 0) + 1

    removed_token = set(sorted(all_words.keys(), key=lambda x: all_words[x], reverse=True)[:20])
    removed_token = removed_token.union(set(["CORP", "LTD", "INC", "FUND", "CO", "LLC", "BANK", "PARTNERSHIP", "PARTNERS"]))
    print(removed_token)

    return removed_token

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

    return score


def fuzzy_match(name, company_list, namePos, removedToken, threshold):
    highest_score = threshold
    highest_item = None
    #print(f"threshold is {highest_score}")
    for item in company_list:

        score = company_name_match(name, item[namePos], removedToken)
        if score >= highest_score:
            highest_score = score
            highest_item = item
            #print(f"{name} && {highest_item} score is {highest_score}")

    return highest_score, highest_item

def reverseIndex(data, indexPos, removedToken):

    all_companys = {}
    for index, line in enumerate(data):
        name = line[indexPos]
        items = name.replace(".", "").replace(",","").split()
        for item in items:
            item = item.upper()
            if item in removedToken:
                continue
            if not all_companys.get(item, None):
                all_companys[item] = []
            all_companys[item].append(line)
    # some statistics
    totalLength = 0
    for key in all_companys:
        totalLength += len(all_companys[key])
    print(f"TOTAL KEYS LENGTH IS {len(all_companys)}, AVERAGE LENGTH IS {totalLength / len(all_companys)}")
    return all_companys
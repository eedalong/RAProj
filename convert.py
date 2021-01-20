import csv
input_file = open("res_file")
res_file = open("convert_res_08.csv", "w", newline='')
csv_writer = csv.writer(res_file)
while(True):
    try:
        line1 = next(input_file)
        line2 = next(input_file)
    except StopIteration:
        break
    data = line1.split("|")
    data = list(filter(lambda x: x != "," and x != '\n', data))[1:]
    tmp = data[8].split(",")
    try:
        assert len(tmp) == 4
    except:
        continue
    data[8] = tmp[1]

    if len(tmp) > 1:
        data.insert(9, tmp[2])
    data2 = line2[1:].split("|")[1:]

    data2[-1] = data2[-1][:-1]
    data.extend(data2)

    csv_writer.writerow(data)

res_file.close()


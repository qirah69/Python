import csv
with open('penguins.csv', mode='r') as penguins, open("penguins_data.csv", mode='w', newline='') as outfile:
    reader = csv.reader(penguins)
    writer = csv.writer(outfile)

    next(reader)
    writer.writerow(['species', 'flipper_length_mm', 'culmen_length_mm', 'culmen_depth_mm', 'body_mass_g', 'island', 'sex'])
        
    for row in reader:
        selected_row = [row[2], row[11], row[9], row[10], row[12], row[4], row[13]]
        if '' not in selected_row and 'NA' not in selected_row:
            writer.writerow(selected_row)
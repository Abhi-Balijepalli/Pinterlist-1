import string_to_object
import csv
from collections import OrderedDict

with open("Pin_list_examples.csv") as csv_file:
    

    csv_reader = csv.DictReader(csv_file)

    with open('Pin_list_output.csv', 'w') as new_file:
        # fieldnames = ['Name', 'Cleaned']
        fieldnames = OrderedDict([('\ufeffName',None),('Cleaned',None)])
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

        csv_writer.writeheader()

        for line in csv_reader:
            clean_string = string_to_object.user_view_recipe_item(line['\ufeffName'])
            line['Cleaned'] = clean_string
            csv_writer.writerow(line)
            print(line)

    print("done")
  
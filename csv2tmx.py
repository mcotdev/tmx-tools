# Convert CSV to TMX as a CLI command (danish to english). Customise to suit needs.
# python script.py --input input2tmx.csv --output pcat.tmx
# python script.py -i input2tmx.csv -o pcat.tmx

import argparse
import csv

class TmxFile:
    def __init__(self):
        self.translation_units = []
    
    def add_translation(self, srclang, translation, translang, datatype):
        tu = {
            'srclang': srclang,
            'translation': translation,
            'translang': translang,
            'datatype': datatype
        }
        self.translation_units.append(tu)
    
    def write_to_file(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write('<tmx version="1.4">\n')
            file.write('  <header/>\n')
            file.write('  <body>\n')
            
            for tu in self.translation_units:
                file.write('    <tu>\n')
                file.write(f'      <tuv xml:lang="{tu["srclang"]}">\n')
                file.write(f'        <seg>{tu["srclang"]}</seg>\n')
                file.write('      </tuv>\n')
                file.write(f'      <tuv xml:lang="{tu["translang"]}">\n')
                file.write(f'        <seg>{tu["translation"]}</seg>\n')
                file.write('      </tuv>\n')
                file.write('    </tu>\n')
            
            file.write('  </body>\n')
            file.write('</tmx>\n')

def convert_csv_to_tmx(input_file, output_file):
    tmx_file = TmxFile()

    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                danish_translation = row['Danish']
                english_translation = row['English']
                
                tmx_file.add_translation('da', danish_translation, 'en', 'text')
                tmx_file.add_translation('en', english_translation, 'da', 'text')

        tmx_file.write_to_file(output_file)
        print("TMX file created successfully.")
    except FileNotFoundError:
        print("CSV file not found.")
    except KeyError as e:
        print(f"Column header not found: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Convert CSV file to TMX file.')
parser.add_argument('--input', '-i', type=str, help='Input CSV file path', required=True)
parser.add_argument('--output', '-o', type=str, help='Output TMX file path', required=True)
args = parser.parse_args()

# Convert CSV to TMX
convert_csv_to_tmx(args.input, args.output)

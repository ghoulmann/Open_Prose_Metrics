import shelve
from input.read_document import Sample
import pathlib, os
launch_script = os.path.abspath(__file__)
directory = os.path.dirname(launch_script)
shelve_file = 'shelve.db'
save_path = os.path.join(directory, shelve_file)


document = 'util/12thGrade-informationExplanatory.txt'
report = Sample(document)

db = shelve.open(save_path)
db['example'] = report

db.close()

import shelve
from input.read_document import Sample
import pathlib, os
path = pathlib.Path(__file__).parent.absolute()
print("Working Direcory" + str(path))
document = 'util/12thGrade-informationExplanatory.txt'

report = Sample(document)

db = shelve.open(os.path.join(path, 'shelve.db'))
Print("Writing shelve.db to " + str(os.path.join(path, 'shelve.db'))
db['example'] = report

db.close()

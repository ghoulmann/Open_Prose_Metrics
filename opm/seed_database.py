import shelve
from input.read_document import Sample
import pathlib, os, sys

path = pathlib.Path(__file__).parent.absolute()
document = 'util/12thGrade-informationExplanatory.txt'

report = Sample(document)
db = shelve.open(os.path.join(path, 'shelve.db'))

db['example'] = report

db.close()


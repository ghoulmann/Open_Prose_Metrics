import shelve
from input.read_document import Sample

document = 'util/12thGrade-informationExplanatory.txt'

report = Sample(document)
db = shelve.open('shelve.db')

db['example'] = report

db.close()


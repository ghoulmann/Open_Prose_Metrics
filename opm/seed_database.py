import shelve
from input.read_document import Sample

document = 'util/12thGrade-informationExplanatory.txt'

report = Sample(document)
db = shelve.open('shelve')

db['example'] = report

db.close()


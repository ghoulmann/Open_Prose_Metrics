Env
---------
* Python 3.7 now 3.8
* with apache and mod wsgi 3
* with virtualenv
* tmp for audio does not delete files yet (?_
* [x] default on scraper and paste forms is still to ask for external
* Im production, the shelve file is in wsgi home directory

To Do
------

[ ] Adapt nested for loops for traversing values to rely on list comprehension

[ ] At least document summary of each module

[X] Change default begaviour on upload/import forms

[ ] 2to3 textgain module

[ ] 2to3 passive module

[ ] Instead of using placeholders for app directories, create them if missing on run

[ ] perhaps move list constants to a single file

[ ] now that tts and txtToHTML work on proofread endpoint, work to delete mp3s

[ ] integrate proofreading tools better

[ ] catch divide by zero and other arithmetic problems

[ ] modals for reading indexes, or some other [i]nformation

[ ] quotes for front page

[ ] List sections on front page

[ ] [i]nformation for each section on the feedback page

[ ] app.config to be sourced from another file

[ ] change environment changes app.log, error.log, tmp folder, audio folder

[ ] fork google-search for python, see if it can be modified for urllib3

[ ] pull navy code for feedback out of template and into new_feedback

[ ] Adjust logo (or scaling on the templates)

[ ] Clean modules and files no longer used

[x] change extraeyes to *Open Prose Metrics*

[ ] Find a way to determine template components with variables (appname, logo, theme)

[ ] Write comprehensive install

[ ] Add vagrantfile

[ ] add dockerfile

[ ] set application paths with vars, relative or absolute

[ ] Add footer

[ ] clean/merge/unify requirements.txt

[ ] Credit for influential code

[ ] catch ZeroDivisionErrors for ratios and adjust templates

[ ] clean up *weak verb* count mechanisms
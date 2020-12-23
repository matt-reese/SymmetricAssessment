# SymmetricAssessment

To run this project:

Make sure Python 3 is installed, then, using a command line, enter these commands:
1. git clone https://github.com/matt-reese/SymmetricAssessment.git
2. cd SymmetricAssessment
3. python generate_datasets.py -- this will generate three CSV files (GUDID data, MDALL data, and their aligned data)

Then, you can choose to run the command:\
python overlap.py -- which will give the count of GUDID-only catalog numbers, the count of MDALL-only catalog numbers, and the count of catalog numbers in both

Or:\
python search.py -- which will allow you to input a catalog number and see the item descriptions from both the GUDID and MDALL datasets.

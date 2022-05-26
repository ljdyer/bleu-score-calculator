# BLEU score calculator

A web app for calculating BLEU scores

:warning: **Currently in prototype stage and easily breakable!**

:warning: **Security of host not verified. Do not upload proprietary data!**

## How to use

Drag and drop the file containing your language data into the dropzone on the landing page to see BLEU score information.

Files must be in .xlsx format. The first cell in each column will be interpreted as the column header.

Your file should include the following column headers:

- A single reference column, whose header begins with the word 'reference' (Examples of permissible reference column headers: 'reference', 'Reference sentences')
- One or more hypothesis columns, whose headers begin with the word 'hypothesis' (Examples of permissible reference column headers: 'hypothesis', 'Hypothesis 1: Google MT')

Your file may also include any number of other columns (e.g. the source text for the translations). These will be ignored when calculating the BLEU scores.

You can try it out using the sample data [here](app/test_files/ja_en_test.xlsx)

# Credits

https://flask-dropzone.readthedocs.io/en/latest/
https://github.com/Manav1918/drag-drop-file-flask
https://www.dropzone.dev/js/
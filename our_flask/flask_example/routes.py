# Here, we import the forms, since they are used for routing.
# We also add routing to the registration and the login pages.

from flask import render_template, redirect
from flask_example import app
from flask_example.forms import SubmitForm
import gspread

@app.route('/', methods=['GET', 'POST'])
def loginform():
    form = SubmitForm()
    is_submitted = form.validate_on_submit()

    if not is_submitted:
        return render_template('submit.html', form=form)
    else:
        url = form.spread_sheet_url.data
        account = gspread.service_account("credentials.json")
        spreadsheet = account.open_by_url(url)

        input = spreadsheet.worksheet("Input")
        output = spreadsheet.worksheet("Output")

        input_list = [{'bins': int(bins), 'items': [int(item) for item in items.split(',')]}
                      for bins, items in input.get_all_values()[1:]]

        from prtpy.partitioning.snp import snp
        from prtpy.partitioning import partition

        output_rows = []
        for row in input_list:
            bins, items = row['bins'], row['items']
            part = partition(algorithm=snp, numbins=bins, items=items)
            output_rows.append([bins, str(items), str(part)])

        range_to_update = "A2:C" + str(len(input_list) + 1)

        output.update(range_to_update, output_rows)

        return redirect("https://docs.google.com/spreadsheets/d/10jSIOFba6vjk1U-C7N6p-8LHTXeFFch8Ui68MOXoUa4/edit#gid=238297537")


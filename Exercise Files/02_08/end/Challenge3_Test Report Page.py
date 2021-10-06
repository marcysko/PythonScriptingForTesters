import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#read in the data from the spreadsheet
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('TestRunData').sheet1

spreadsheet_data = sheet.get_all_values()
run_times = []
for row in spreadsheet_data:
    #we remove the first 2 items from the row since we are not 
    #interested in the Test Name or Avg Run time
    del row[0]
    del row[1]

    run_times.append(row)

#read in csv data
csv_data = []
with open('LatestTestRunData.csv') as csv_file:
    file_reader = csv.reader(csv_file)
    for row in file_reader:
        csv_data.append(row)

#for the sake of simplicity we are going to assume a few things:
# 1. All of the tests in the csv data were run on the same date
# 2. The test are in the same order in the csv file as they are in the 
#    spreadsheet data

#get the run date from the third item of the second row of the csv_data
run_date = csv_data[1][2]
spreadsheet_header_row = run_times[0]
spreadsheet_header_row.append(run_date)
del spreadsheet_header_row[0]
#add the data from each run to the end of the same row in the spreadsheet data
for spreadsheet_row,csv_row in zip(run_times[1:],csv_data[1:]):
    new_value = csv_row[1] #second column in the csv data is the new run time
    spreadsheet_row.append(new_value)
    del spreadsheet_row[0]

#write the new spreadsheet data back into the spreadsheet
for row_index, row in enumerate(run_times):
    for col_index, cell in enumerate(row):
        sheet.update_cell(row_index+1,col_index+3,cell)

#create a chart

#read in the average data from the spreadsheet
avg_data = sheet.col_values(2)

chart_data = [["Test Name","Diff From Avg"]]
for avg,current in zip(avg_data[1:],csv_data[1:]):
    diff = float(avg)-float(current[1])
    chart_data.append([current[0],diff])

from string import Template
#first substitution is the header, the res is the data
htmlString = Template("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
  google.charts.load('current', {packages: ['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  
  function drawChart(){
      var data = google.visualization.arrayToDataTable([
      $labels,
      $data
      ],
      false);

      var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
      chart.draw(data);
  }
</script>
</head>
<body>
<div id = 'chart_div' style='width:800; height:600'><div>
</body>

</html>""")

chart_data_str = ''
for row in chart_data[1:]:
    chart_data_str += '%s,\n'%row
    
completedHtml = htmlString.substitute(labels=chart_data[0],data=chart_data_str)

with open('Chart.html','w') as f:
    f.write (completedHtml)
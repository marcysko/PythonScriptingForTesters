import csv

#final desired data formats:
# - Charts:         [["Test Name",<NumberOfAsserts>,<NumberOfFailedAsserts>],...]

#read in the data from file

data_list = []
with open('TestAnalysisData.csv') as csv_file:
    file_reader = csv.reader(csv_file)
    for row in file_reader:
        data_list.append(row)

#convert the data so that the asserts and fails are integers

#initialize the new list with the headers
chart_data = [data_list[0]]
for row in data_list[1:]:
    num_asserts = int(row[1])
    num_failed_asserts = int(row[2])
    chart_data.append([row[0],num_asserts,num_failed_asserts])


#create the html for the chart
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
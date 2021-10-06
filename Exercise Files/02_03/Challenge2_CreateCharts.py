import csv

#final desired data formats:
# - Charts:         [["Test Name",<NumberOfAsserts>,<NumberOfFailedAsserts>],...]

#read in the data from file

data_list = []
with open('TestAnalysisData.csv') as csv_file:
    #read in data using csv reader

#new list is initialized with headers
chart_data = [data_list[0]]
for row in data_list[1:]:
    #format each row of the data_list and add to chart_data


#create the html for the chart
from string import Template
#first substitution is the header, the rest is the data
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
    #create the data string
    
#substitute the data into the template

with open('Chart.html','w') as f:
    #write the html string you've create to a file
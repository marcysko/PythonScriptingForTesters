import json

json_data = open('jiraJsonData.json').read()
data = json.loads(json_data)

status_counts = {}

for project in data['projects']:
    for issue in project['issues']:
        status = issue['status']
        if not status in status_counts.keys():
            status_counts[status] = 1
        else:
            status_counts[status] = status_counts[status] + 1

from string import Template

template_string = Template("""<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Status', 'Number of Issues'],
          $my_data
        ]);

        var options = {
          title: 'Issues by Status'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart" style="width: 900px; height: 500px;"></div>
  </body>
</html>""")

formatted_data = ''

for stat in status_counts.keys():
    formatted_data += "['%s',%s],\n"%(stat,status_counts[stat])

html_string = template_string.substitute(my_data=formatted_data)

with open('PieChart.html','w') as f:
    f.write(html_string)
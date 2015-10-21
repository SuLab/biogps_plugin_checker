import urllib2      #To open url
import json         #To load json data
import requests     #To get status code

human_gene_id_list = [1017,7157,695,3702,5599,3558,1743,65220,132,3485]
mouse_gene_id_list = [12566,22059,12229,16428,26419,16183,78920,192185,11534,16008]
rat_gene_id_list = [362817,24842,367901,363577,116554,116562,299201,100125370,25368,25662]
url = "http://biogps.org/plugin/all/?format=json&limit=381"

#Function 1: Give plugin_id list
def ExtractPluginId(url):     
    plugin_id_list = []    
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json1 = json.load(f)
    
    for item in json1:
        id1 = item.get('id')
        plugin_id_list.append(id1)   
    return plugin_id_list

    
#Function 2:Get status code of url
def getCode(main_url):
    data = urllib2.urlopen(main_url)
    for lines in data:           
        data1 = json.loads(lines)                    
        try:            
            data2 = data1['url']
            if data2.startswith('/'):
                data3 = "http://biogps.org/"+data2
            else:
                data3 = data2
            r = requests.get(data3,timeout=30)
            d1 = r.status_code
        except:
            d1 = "Error"            
    return d1

#Function 3: Give html table of status code with sorting feature
def get_html_table(url,gene_id_list):
    #local variables
    html = []
    plugin_id_list = []    
    plugin_id_list = ExtractPluginId(url)
    
    # Create a head and provide jquery tablesorter plugin
    html1 = """
    <head>
    <script src="http://tablesorter.com/jquery-latest.js" type="text/javascript"></script>
    <script src="http://tablesorter.com/__jquery.tablesorter.min.js" type="text/javascript"></script>
    <script type="text/javascript"></script>   
    
    <script>
        $(document).ready(function(){
        $(function(){
        $("#Biogps_plugins").tablesorter();
        });
        });
    </script>
    
    <style>
    p{
    display: block;
    align: bottom;
    }    
    caption{    
    display: table-caption;
    text-align: center;
    font-size: 30;
    font-style: italic;
    color: #CD5C5C;
    }
    table {
    border-radius: 10px;
    border: 2px solid #FFDAB9;
    padding: 5px;
    width: 100px;
    height: 100px;
    }
    td {    
    background-color: #F5F5DC;
    padding: 15px;
    height: 15px;
    vertical-align: bottom;
    }
    th {    
    background-color: #FFDAB9;    
    height: 15px;
    padding: 15px;
    }    
    </style>
    
    </head>
    <body>
    <table id="Biogps_plugins" class="tablesorter" border="2" cellspacing="5"cellpadding="12">
    <caption>Biogps Plugins Checker</caption>
    <thead>
    """
    html.append(html1)    
   
    # Create column for gene_id_list, keep first column void to match rows indentation.
    headerlist = list(gene_id_list)
    headerlist.append('Number of Pluginid not having "200" statuscode')
    headerlist.insert(0,"geneid/pluginid")
    if headerlist:
        html.append("<tr>")
        for header in headerlist:
            html.append("<th>%s</th>" % header)
        html.append("</tr>")
    html.append("</thead>")

    # Create body
    html.append("<tbody>")
    
    # Scan and generate status code (row=pluginid, col=geneid)
    for j in plugin_id_list:
        count = 0       #count for Not having 200 status code
        plugin_url = "http://biogps.org/plugin/"+str(j)+"/"
        html.append("<tr>")
        html.append('<td><a href=%s>%s</a>'%(plugin_url,j))
        html.append('</td>')
        for i in gene_id_list:
            main_url = "http://biogps.org/plugin/"+str(j)+"/renderurl/?geneid="+str(i)
            sub_url  = main_url+"&redirect=true"
            status = getCode(main_url)            
            html.append('<td><a href=%s>%s</a>'%(sub_url,status))
            if status !=200:
                count += 1
            html.append('</td>')
        html.append('<td>%s</td>'%count)
        html.append("</tr>")
    html.append("</tbody")
    html2 = '''
    <p>
    Notes:<br>
    First row = gene-ids<br>
    First column = plugin-ids<br>
    Each cell represents status code of related gene-id and plugin-id.<br>
    Click anywhere in the First row for sorting. <br>   
    Click on any cell to open corresponding url.<br>    
    </p>
    '''
    
    html.append(html2)    
    html.append("</table")     
    html.append('</body>')
    html_table=  "\n".join(html)    
    html_file = open("output_human_gene_id.html","w")
    html_file.write(html_table)
    html_file.close()
    return html_file
print get_html_table(url,human_gene_id_list)



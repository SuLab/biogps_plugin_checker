import urllib2
import json
import csv
import httplib2

human_gene_id_list = [1017,7157,695,3702,5599,3558,1743,65220,132,3485]
mouse_gene_id_list = [12566,12229,16428,26419,16183,78920,192185,11534,16008]
rat_gene_id_list = [362817,24842,367901,363577,116554,116562,299201,100125370,25368,25662]
url = "http://biogps.org/plugin/all/?format=json&limit=381"


# Function 1 - should open the input url, parse it to prepare url_list
# input  = url
# output = url_list

'''def ExtractUrl(url,gene_id_list):
    
    url_list = []
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json1 = json.load(f)
    
    for j in gene_id_list:
        for item in json1:
            url1 = item.get('url')
            url_list.append(url1)
    return url_list
'''

# Function 2 - should open the input url, parse it to plugin_id_list
# input = url
# output = plugin_id_list

def ExtractPluginId(url):
    plugin_id_list = []
    
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json1 = json.load(f)
    
    for item in json1:
        id1 = item.get('id')
        plugin_id_list.append(id1)
    #print "PLUGIN_IDS' : ", plugin_id_list
    return plugin_id_list

    
# Function 3 - should create new_url_list using input plugin_id_list and human_gene_id_list
# input = plugin_id_list
# input = human_gene_id_list
# output = new_url_list

def UrlList(plugin_id_list,gene_id_list):
    
    new_url_list = []
    for x in gene_id_list:
        for y in plugin_id_list:
            new_url = "http://biogps.org/plugin/"+str(y)+"/renderurl/?geneid="+str(x)
            new_url_list.append(new_url)
    return new_url_list


# Function 4
# input  new_url_list
# output status_code_list or a dictonary whose key=new_url_list elements and value=status_code

def StatusCode(new_url_list):
    dictionary = dict()
    l1 = []
    
    #sock=socket.socket()
    #sock.settimeout(60)
    for i in new_url_list:
        #print "key: ",i
        data = urllib2.urlopen(i)
        for lines in data:
            data1 = json.loads(lines)            
            #print "EXTRACTED_URL: ",data2          
            try:
                data2 = data1['url']
                h = httplib2.Http(timeout=30)
                resp,content = h.request(data2)
                d1 = resp.status
                #print i, d1
                #print "STATUS_CODE: ",d1
                dictionary[i] = d1
                #print dictionary
                
            except:
                dictionary[i] = "error"
                #print "Error"
                    #print dictionary
                        
    return dictionary



# Function 5
# - declare inputs 
# - Call function 1 and get url_list
# - call function 2 and get plugin_id_list
# - call function 3 to get new_url_list
# - call function 4 to get dictonary (where key = new_url_list (not the url from which we get status code), value = statuscode
# - Create a CSV/html file either using dictory or (url_list + plugin_id_list)

def StatusCodeInCsv(url,gene_id_list):
    # Open text file and add header
    f = open("myfile_mouse_genes.txt",'w')
    f.write("\t")    
    for m in gene_id_list:
        string = str(m) + "\t"
        f.write(str(string))
    f.write("\n")
    #print " ----------- Created header in text file -----------"

    # Create dictionary whose key=URL and value is status code
    plugin_id_list = []
    urllist = []
    dictionary = dict()
    plugin_id_list = ExtractPluginId(url)
    #print " ----------- Extracted plugin id from url ---------- "
    urllist = UrlList(plugin_id_list,gene_id_list)
    #print " ----------- Created URL list to find out status code -------- "
    dictionary = StatusCode(urllist)
    #print " ----------- Created dictionary for URL and Status code ------- "

    # Create a table in text file    
    for j in plugin_id_list:
        string = str(j)+"\t"
        f.write(str(string))
        col=1;
        for i in gene_id_list:
            mykey = "http://biogps.org/plugin/"+str(j)+"/renderurl/?geneid="+str(i)
            string = str(dictionary[mykey])+"\t"
            f.write(str(string))
        f.write("\n")
    f.close()

    #Generate csv from text file
    c=open("output_mouse_genes.csv","wb")
    writer = csv.writer(c)
    f = open("myfile_mouse_genes.txt",'r')
    data = f.readlines()
    for line in data:
        words = line.split("\t")
        #print "----------"
        #print words
        writer.writerow(words)

    f.close()
    c.close()
    return f

print StatusCodeInCsv(url,mouse_gene_id_list)


import string, os, sys, getopt
from xml.dom import minidom


# Author :  Jain Basil Aliyas <jainbasil@gmail.com>
# Homepage : http://jainbasil.net


def convert(infile):
    """
	    Convert Wordpress Export File to multiple html files.
    """
    
    
    # First we parse the XML file into a list of posts.
    # Each post is a dictionary
    
    dom = minidom.parse(infile)

    blog = [] # list that will contain all posts

    for node in dom.getElementsByTagName('item'):
    	post = dict()

    	post["title"] = node.getElementsByTagName('title')[0].firstChild.data
    	post["date"] = node.getElementsByTagName('pubDate')[0].firstChild.data
    	post["postname"] = node.getElementsByTagName('wp:post_name')[0].firstChild.data
    	post["postdate"] =''.join(node.getElementsByTagName('wp:post_date')[0].firstChild.data.split(' ')[0])
    	post["posttype"] = node.getElementsByTagName('wp:post_type')[0].firstChild.data
	if node.getElementsByTagName('content:encoded')[0].firstChild != None:
    	    post["text"] = node.getElementsByTagName('content:encoded')[0].firstChild.data
    	else:
    	    post["text"] = ""
    	
    	# Get the categories and tags
    	tempCategories = []
	tempTags=[]
    	for subnode in node.getElementsByTagName('category'):
		if subnode.getAttribute('domain') == "category":
			tempCategories.append(subnode.firstChild.data)
		if subnode.getAttribute('domain') == "tag":
			tempTags.append(subnode.firstChild.data)
	
	# I got all the tags twice in the list, so I am just removing the duplicates by following line. I don't know whether this is found in all the xml files.
	tempTags = list(set(tempTags))
    	
	# My category list had one named Tips &amp; Tricks. It will create an error if we give & in the category name. So, I am replaving that with ''
	Categories = []
	for c in tempCategories:
		c = c.replace(' &amp; ','-')
		c = c.replace(' ','-')
		Categories.append(c)
	
	categories = [x for x in Categories if x != '']
	tags = [x for x in tempTags if x != '']
    	post["categories"] = categories 
	post["tags"] = tags

    	# Add post to the list of all posts
    	blog.append(post)
    	
    
    # Then we create the directories and HTML files from the list of posts.
    
    for post in blog:
    	if post["posttype"].encode('utf-8') != 'attachment': 
        	# Jekyll recognize html file as yyyy-mm-dd-title-of-the-post.html
        	title = post["title"].encode('utf-8')
		postname = post["postname"].encode('utf-8')
		postdate = post["postdate"].encode('utf-8')
        	filename = postdate+ '-' + postname + '.html'
        
        	# Add a meta tag to specify charset (UTF-8) in the HTML file
        	meta = """<META http-equiv="Content-Type" content="text/html; charset=UTF-8">"""
		filename = filename.replace('/',' ')
        	f = open(filename, 'w')
		titletemp = title.replace(':',' ')
		fileTitle = "---\nlayout: post\ntitle: "+titletemp + "\n"
		
		f.write(fileTitle)

		#Adding categories into file
		if post["categories"]:
			Category = "categories:\n"
			for c in post["categories"]:
				c = c.encode('utf-8')
				Category = Category + '- '+ c +"\n"
			f.write(Category)

		# Adding Tags into file
		if post["tags"]:
			Tags = "tags:\n"
			for t in post["tags"]:
				t = t.encode('utf-8')
				Tags = Tags + '- ' + t + "\n"
			f.write(Tags)

		footer = "---\n"
		f.write(footer)
		
		f.write(meta+"\n")
        	
        	# Add "HTML header"
        	start = "<html>\n<head>\n<title>"+ title +"</title>\n</head>\n<body>\n"
        	f.write(start)
        	
        	# Convert the unicode object to a string that can be written to a file
        	# with the proper encoding (UTF-8)
        	text = post["text"].encode('utf-8')
        	
        	# Replace simple newlines with <br/> + newline so that the HTML file
        	# represents the original post more accuratelly
        	text = text.replace("\n", "<br/>\n")
        
        
        	f.write(text)
        
        	# Finalize HTML
        	end = "\n</body>\n</html>"
        	f.write(end)
        
        	f.close()
	else:
		pass

def main(argv):

    infile = sys.argv[1]
    if infile == "":
	    print "Error: Missing Argument: missing wordpress export file."
	    usage(argv[0])
	    sys.exit(3)

    convert(infile)
	

if __name__ == "__main__":
	main(sys.argv)

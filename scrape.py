from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import csv



#Returns the number of occurences of searchText on a given web page
def countOccurence(webAddress, searchText):
    url = urllib.urlopen(webAddress)
    soup = BeautifulSoup(url, "html.parser")
	#convert to upper for easy search
    cleanSoup = soup.text.upper()
    searchText = searchText.upper()
    #print(cleanSoup)
    #print(searchText)
    occurence = [m.start() for m in re.finditer(searchText, cleanSoup)]
    count = len(occurence)
    return count


print(countOccurence('http://www.cnn.com/','bitcoin'))

#imports
from website import create_website

#creating an instance of website
website = create_website()

#initiating
if __name__ == '__main__':
    #run instance of website
    website.run(host="192.168.2.40",port=8080,debug=True)
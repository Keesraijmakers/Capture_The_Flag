#imports
from website import create_website

#creating an instance of website
website = create_website()

#initiating
if __name__ == '__main__':
    #run instance of website
    website.run(debug=True)
# Import Needed libraries
import requests
from bs4 import BeautifulSoup
import time
import csv

# create function to Extract the data we want from the website


def job_scraper():
    # variable of the job a user want to extract
    Job_search = 'python'
    # create the variable base_url and give the url of the website so we can request to access that url
    base_url = f'https://wuzzuf.net/search/jobs/?a=navbl&q={Job_search}&start='
    # here i created a results variable and assigned to it and empty list to gather the data i extracted in one list
    results = []
    # This For Loop is to loop on every page and extract the Information i want
    for page in range(0, 10):
        # Here i make the request using requests library to get the url and then add the page number
        # page number is added because when i extract the data there will be multiple pages not extracted so i add the str(page) to add a number at the end of the url to loop over the pages of the job_search value
        response = requests.get(base_url + str(page))
        # Create a soup object and give it the .Content attribute to display the webpage content and for the parser i had to choose lxml due to it's speed
        soup = BeautifulSoup(response.content, 'lxml')
        # Here Each job has a card of its own but with the same classname for each one
        # so this code returns a list of all the job cards the page have without getting any unwanted cards
        job_lists = soup.find_all('div', {'class': 'css-1gatmva e1v1l3u10'})
        # This For Loop is to loop on every tag inside the div of the job_lists list
        for job_list in job_lists:
            # Here I have created a dictionary so that i would assign every data to its parent name
            job = {}
            # Here i Extracted the a tags that has that class name below and add the .text to extract the text only and assigned it to the 'Title' key
            # I have the same thing for the rest with using replace and text attributes
            job['Title'] = job_list.find('a', {'class': 'css-o171kl'}).text
            job['Company'] = job_list.find(
                'a', {'class': 'css-17s97q8'}).text.replace('-', "")
            job['Location'] = job_list.find(
                'span', {'class': 'css-5wys0k'}).text
            # check wether the job is part time or full time
            job['Time'] = job_list.find(
                'span', {'class': 'css-1ve4b75 eoyjyou0'}).text
            # extract the post date and because there is the new one and old one
            # i have made a condition to print the new post if its there and if it's not then the post the old one
            job_post_new = job_list.find('div', {'class': 'css-4c4ojb'})
            job_post_old = job_list.find('div', {'class': 'css-do6t5g'})
            job['Post'] = job_post_new.text if job_post_new else job_post_old.text
            # Here for the description i have declared ana empty list to save all the description in it
            # Because the description of the job is split into two sentences each have its own classname and its inside a div in the job_lists
            # so as the job_lists return a list, i can see the place of the div i want and then index it from that list and then extract the text out of all the elements within that div
            job['description'] = []
            des = job_list.find_all('div')
            for tag in des[6]:
                if tag.text:
                    cleaned_text = tag.text.replace("Â", "").replace("·", "").replace(
                        ".css-5x9pm1{-webkit-text-decoration:none;text-decoration:none;color:inherit;max-width:calc(100vw / 2 - 32px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:-webkit-inline-box;display:-webkit-inline-flex;display:-ms-inline-flexbox;display:inline-flex;}", "").strip()
                    if cleaned_text:
                        # This returns a list of the texts extracted from the des and append it to the job dictionary under the key description
                        job['description'].append(cleaned_text)
            # I used the join to concatenate the list items into one single list item
            job['description'] = ' '.join(job['description'])

            # This appends the results into the results list above in line 16
            results.append(job)
            # For this code i have imported the time library so that between every page there will be a delay of 1 second
            time.sleep(1)
    return results

# explanation for the Code below #
# Here I have created a function for the csv file that reads the data extracted which in this case is the results list
# the second parameter carries the file name


def save_to_csv(data, Jobs):

    try:
        with open(Jobs, 'w', newline='', encoding='utf-8') as file:
            # This code to create(Write) the csv File
            writer = csv.writer(file)
            # This code is to write the headers of the csv file
            writer.writerow(['Title', 'Company', 'Location',
                            'Time', 'Post', 'Description'])
            # created a for loop to loop on every item in the results list and assign it to the key it belongs to
            for job in data:
                writer.writerow([job['Title'], job['Company'], job['Location'], job['Time'],
                                job['Post'], job['description']])
        return True
    # The Exception as e try to catch any exception in the try code and then assign it to the variable e and then execute the except block
    except Exception as e:
        print(f"Error saving data to CSV file: {e}")
        return False


# explanation for the Code below #
# Checks if the program is being run as standalone program or imported as a module in another program
# if it's being run as a stand alone program then the if block is executed and
# if it's imported as a module in another program the if block wont be executed
if __name__ == "__main__":

    results = job_scraper()
    # this condition is here to ensure that the functions is called by returning a boolean value(True or False) then execute the if block
    if save_to_csv(results, 'jobs.csv'):
        print('CSV File Created')
    else:
        print('Error Occurred While Creating The File')

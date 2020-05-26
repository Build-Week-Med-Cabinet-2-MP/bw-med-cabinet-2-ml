import requests
import time
from random import randint
import pandas as pd


URL = "https://api-g.weedmaps.com/wm/v1/strains?page_size=150&page={}"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


class WeedmapsStrains():
  """Save Weedmaps.com cannabis strain database to file
  FOR EDUCATIONAL PURPOSES ONLY"""


  def __init__(self, url=URL, headers=HEADERS):
    """Initialize class with optional parameters
    
    Args:
      url: Optional, default url points to Weedmaps Strains API, page_size sest to 150 strains per page
      headers: Optional, default HTTP headers to specify user-agent during data requests
    
    Returns:
      Initialized WeedmapsStrains class"""

    self.url = url
    self.headers = headers


  def scrape_to_csv(self, output_filename):
    """Scrape Weedmaps Strain API and save to file
    
    Args:
      output_filename: path to save csv file with strain data
      
    Returns:
      CSV file saved at output_filename"""

    self.output_filename = output_filename
    self.list_of_requests = []
    self.page_number = 1

    while len(requests.get(self.url.format(self.page_number), 
                           headers=self.headers).json()["data"]) != 0:
      self.response = requests.get(self.url.format(self.page_number), 
                                   headers=self.headers)
      self.list_of_requests.append(self.response)
      self.page_number += 1
      time.sleep(randint(1,5))

    self.list_of_dataframes = []

    for i in range(len(self.list_of_requests)):
      self.list_of_dataframes.append(pd.DataFrame.from_records(pd.DataFrame.from_records(self.list_of_requests[i].json()["data"])["attributes"]))

    self.strains = pd.concat(self.list_of_dataframes, ignore_index=True)
    self.strains.to_csv(self.output_filename, index=False)

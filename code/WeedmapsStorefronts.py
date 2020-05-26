import requests
import pandas as pd
import time
from random import randint


URL = "https://api-g.weedmaps.com/discovery/v1/listings?sort_by=position_distance&filter%5Bany_retailer_services%5D%5B%5D=storefront&page_size=100&page={}"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


class WeedmapsStorefronts():
  """Save Weedmaps.com cannabis storefronts database to file
  FOR EDUCATIONAL PURPOSES ONLY"""

  def __init__(self, url=URL, headers=HEADERS):
    """Initialize class with optional parameters
    
    Args:
        url: Optional, defaults to weedmaps storefront API (URL)
        headers: Optional, defaults to provided HTTP header
    
    Returns:
        Initialized WeedmapsStorefronts class"""

    self.url = url
    self.headers = headers


  def scrape_to_csv(self, output_file):
    """Scrape Weedmaps Storefront API and save to file
    
    Args:
        output_file: path to save csv file with storefront data
        
    Returns:
        CSV file saved at output_filename"""

    self.output_file = output_file
    self.list_of_requests = []
    self.page_number = 1

    while len(requests.get(self.url.format(self.page_number), headers=self.headers).json()["data"]["listings"]) != 0:
      self.response = requests.get(self.url.format(self.page_number), headers=self.headers)
      self.list_of_requests.append(self.response)
      self.page_number += 1
      time.sleep(randint(1,5))
      
    self.list_of_dataframes = []
    
    for i in range(len(self.list_of_requests)):
      self.list_of_dataframes.append(pd.DataFrame.from_records(pd.DataFrame.from_records(self.list_of_requests[i].json()["data"])["listings"]))
      
    self.storefronts_df = pd.concat(self.list_of_dataframes, ignore_index=True)
    self.storefronts_df.to_csv(self.output_file)



Python 3 code to extract, clean, and analyze cannabis strain data from weedmaps.com

### Usage

**Extract Data**

```python

# Scrape data and save locally
WeedmapsStrains().scrape_to_csv("LOCAL_FILE_PATH.csv")

# Cleaned local copy of scraped data, subset for strains with effects and flavors
CleanedStrains("LOCAL_FILE_PATH.csv").clean_crop_save("CLEAN_LOCAL_FILE_PATH.csv")

# Scrape storefront data and save locally
WeedmapsStorefronts().scrape_to_csv("ANOTHER_LOCAL_FILE_PATH.csv")

# Scrape delivery data and save locally
WeedmapsDeliveries().scrape_to_csv("YET_ANOTHER_LOCAL_FILE_PATH.csv")

```



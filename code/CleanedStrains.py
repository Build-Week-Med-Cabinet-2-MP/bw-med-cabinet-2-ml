import ast 
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


class CleanedStrains():
  """Clean output of WeedmapsStrains class"""

  def __init__(self, filepath):
    """Initialize CleanedStrains class
    
    Args:
        filepath: Output from WeedmapsStrains `scrape_to_csv` method
    """

    self.filepath = filepath
    self.df = pd.read_csv(self.filepath)

  def clean_crop_save(self, output_filepath):
    """Clean, crop, and save output from WeedmapsStrains `scrape_to_csv` method
    
    Args:
        output_filepath: path to save csv file with cleaned and cropped data
    
    Returns: 
        Cleaned and cropped data at output_filepath
    """

    self.output_filepath = output_filepath

    def cleaning_function(cell_contents):
      if type(cell_contents) == dict:
        return cell_contents["name"]
      return "No data"

    def remove_no_data_from_tuple_series(cellcontents):
      intermediate = list(cellcontents)
      if "No data" in intermediate:
        return intermediate[:].remove("No data")
      return intermediate

    self.effects_df = pd.DataFrame.from_records(self.df["effects"].apply(ast.literal_eval))
    self.null_dict = {"name":"no data"}
    self.effects_df.replace([None], self.null_dict, inplace=True)
    self.effects_result = list(zip(self.effects_df[0].apply(cleaning_function).tolist(), 
                                   self.effects_df[1].apply(cleaning_function).tolist(), 
                                   self.effects_df[2].apply(cleaning_function).tolist()))
    self.df["effects_cleaned"] = pd.Series(self.effects_result)

    self.flavors_df = pd.DataFrame.from_records(self.df["flavors"].apply(ast.literal_eval))
    self.flavors_df.replace([None], self.null_dict, inplace=True)
    self.flavors_result = list(zip(self.flavors_df[0].apply(cleaning_function).tolist(), 
                                   self.flavors_df[1].apply(cleaning_function).tolist(), 
                                   self.flavors_df[2].apply(cleaning_function).tolist()))
    self.df["flavors_cleaned"] = pd.Series(self.flavors_result)

    self.df["effects_cleaned"] = self.df["effects_cleaned"].apply(remove_no_data_from_tuple_series)
    self.df["flavors_cleaned"] = self.df["flavors_cleaned"].apply(remove_no_data_from_tuple_series)

    self.cropped_df = self.df[(self.df["effects_cleaned"].notna()) & (self.df["flavors_cleaned"].notna())]

    self.cropped_df_effects = self.cropped_df['effects_cleaned'].str.join('|').str.get_dummies()
    self.cropped_df_effects["name"] = self.cropped_df["name"].copy()

    self.cropped_df_flavors = self.cropped_df['flavors_cleaned'].str.join('|').str.get_dummies()
    self.cropped_df_flavors["name"] = self.cropped_df["name"].copy()

    self.intermediate_merge_df = pd.merge(self.cropped_df, self.cropped_df_flavors, on='name')
    self.merged_results = pd.merge(self.intermediate_merge_df, self.cropped_df_effects, on="name")

    self.columns_to_drop = ["slug","genetic_cultivation_description","references","hero_image_attribution","lab_data_attribution",
                            "thc_min","thc_max","cbd_min","cbd_max","featured_position","featured","avatar_image_url",
                            "hero_image_url","aliases","effects","flavors","effects_cleaned","flavors_cleaned"]

    self.dropped_df = self.merged_results.drop(columns=self.columns_to_drop)

    self.species_df = pd.DataFrame(OneHotEncoder().fit_transform(self.dropped_df["species"].values.reshape(-1,1)).toarray())
    self.species_df.columns = self.dropped_df["species"].value_counts().index.tolist()
    self.species_df.columns = [column.title() for column in self.species_df.columns]
    self.species_df = self.species_df.astype(int)
    self.species_df["name"] = self.dropped_df["name"].copy()

    self.merged_df = pd.merge(self.dropped_df.drop(columns="species"), self.species_df, on="name")

    self.merged_df.to_csv(self.output_filepath, index=False)

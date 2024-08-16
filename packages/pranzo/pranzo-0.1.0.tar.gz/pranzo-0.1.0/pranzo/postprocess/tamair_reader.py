import pandas as pd

class TamAirReader:

    def __init__(self, sdir, file_id):
        self.sdir = sdir
        self.file_id = file_id
        self.calo_file = f"{sdir}/calo_{file_id}.csv"


    def get_data(self) -> dict:
        """get calo data in a dictionary"""
        df_raw = self.calofile_in_df()
        df = self.rename_columns(df_raw)
        df_data = self.reaction_start_to_ampoule_removed(df)
        dict_calo_data = self.get_dict_calo_data(df_data)

        return dict_calo_data



    def calofile_in_df(self) -> pd.DataFrame:
        """reads the calo csv and puts it in a pandas dataframe"""
        df = pd.read_csv(self.calo_file)

        return df
    
    def rename_columns(self, df_raw) -> pd.DataFrame:
        """remove capital letters and spaces from column headers"""
        df = df_raw.rename(columns={'Time': 'time', 
                                'Temperature': 'temperature', 
                                'Heat flow': 'heat_flow', 'Heat': 'heat', 
                                'Normalized heat': 'normalized_heat', 
                                'Normalized heat flow': 'normalized_heat_flow', 
                                'Time markers': 'time_markers'})
        return df

    def reaction_start_to_ampoule_removed(self, df) -> pd.DataFrame:
        """Extract df without data from baseline before and after measurement"""
        # Find the indices of the time markers
        reaction_start_idx = df[df['time_markers'] == "Reaction start"].index[0]
        ampoule_removed_idx = df[df['time_markers'] == "Ampoule removed"].index[0]

        # Slice the DataFrame between these indices
        df_subset = df.loc[reaction_start_idx:ampoule_removed_idx]

        return df_subset

    def get_dict_calo_data(self, df) -> dict:
        """get dictionary of calo data"""
        dict_calo_data = {'time_s': df.time.to_numpy(),
                        'temperature_degC': df.temperature.to_numpy(),
                        'heat_flow_W': df.heat_flow.to_numpy(),
                        'heat_J': df.heat.to_numpy(),
                        'norm_heat_flow_Wpgbinder': df.normalized_heat_flow.to_numpy(),
                        'norm_heat_Jpgbinder': df.normalized_heat.to_numpy()}
        
        return dict_calo_data
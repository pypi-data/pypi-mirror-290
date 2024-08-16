import csv
import re
import numpy as np
import pandas as pd


class AntonPaarReader:

    def __init__(self, sdir, file_id):
        self.sdir = sdir
        self.file_id = file_id
        self.rheo_file = f"{sdir}/rheo_{file_id}.csv"

    def get_data(self) -> dict:
        """get the rheo data and phase tags in dictionaries"""

        df_raw = self.rheofile_in_df()
        df = self.set_df_headers(df_raw)

        data = self.get_dict_rheo_data(df)
        tags = self.get_dict_pstart_pend(df)

        return data, tags

    def get_rheofile_corrected_lines(self) -> list:
        """returs a list of all lines of the rheo file corrected (lenght, i acute)"""
        raw_lines = self.read_csv_line_by_line()
        filled_lines = self.add_empty_columns(raw_lines)
        corrected_lines = self.rm_i_acute(filled_lines)

        return corrected_lines

    def read_csv_line_by_line(self) -> list:
        """The rheo csv has varying column numbers.
        The first line of the csv has only 1 column but the last line has e.g. 16 columns.
        This function stores each line of the rheo file in a list lines"""

        with open(self.rheo_file, "r", encoding="latin-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            lines = []
            for line in csv_reader:
                lines.append(line)
        return lines

    def add_empty_columns(self, lines) -> list:
        """add (empty) column elements s.t. all lines have same length"""
        len_last_line = len(lines[-1])
        empty_array = ""
        for line in lines:
            while len(line) != len_last_line:
                line.append(empty_array)
        return lines

    def rm_i_acute(self, lines) -> list:
        """RheoPlus software adds a weird format for big numbers
        this removes characters unknown to pandas"""
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = re.sub(r"\x92", "", lines[i][j])
        return lines

    def rheofile_in_df(self) -> pd.DataFrame:
        """from a list of lines, create a pandas dataframe of the rheofile"""
        lines = self.get_rheofile_corrected_lines()
        df = pd.DataFrame(lines)
        return df

    def locate_variable_names(self, df) -> pd.core.indexes.base.Index:
        """locate the lines which contain variable names (Deformation, Sherrate...)
        look for indices where Messpkt. appears"""

        search_string = "Messpkt."
        idces_rows_dataheaders = df[df.eq(search_string).any(axis=1)].index
        return idces_rows_dataheaders

    def translate_variable_names(self, df) -> list:
        """translate variable names from german to hdf field names"""
        dict_translate = {
            "Messpkt.": "messpkt",
            "Abschnittszeit": "phase_time_s",
            "Zeit": "time_s",
            "Speichermodul": "storage_modulus_Pa",
            "Verhältnis": "ratio_pc",
            "Schubspannung": "shear_stress_Pa",
            "Deformation": "shear_strain_pc",
            "Scherrate": "strain_rate_1ps",
            "Normalkraft": "normal_force_N",
            "Verlustmodul": "loss_modulus_Pa",
            "Verlustfaktor": "loss_factor",
            "Betrag(Viskosität)": "betrag_viskositaet_Pas",
            "Auslenkwinkel": "auslenkwinkel_mrad",
            "Moment": "moment_Nm",
            "Status": "status",
            "Verlustwinkel": "verlustwinkel_deg",
            "Viskosität": "viskositaet_Pas",
            "Winkelgeschwindigkeit": "winkelgeschwindigkeit_radps",
            "Temperatur": "temperature_degC",
            "Zugspannung": "zugspannung_Pa",
            "Frequenz":"frequency_Hz",
            "var_n_german": "var_n_english",
            "var_np1_german": "var_np1_english",
            "var_np2_german": "var_np2_english",
        }

        idces_varnames = self.locate_variable_names(df)

        # the variable names appear before each phase of the rheo, so only look at idces_varnames[0]
        german_headers = df.iloc[idces_varnames[0]]
        new_headers = []
        for header in german_headers:
            new_headers.append(dict_translate[header])

        return new_headers

    def set_df_headers(self, df) -> pd.DataFrame:
        """add hdf5 field names as column headers of rheofile_df"""

        new_headers = self.translate_variable_names(df)
        df.columns = new_headers

        return df

    def locate_col_with_expinfo(self, df) -> str:
        """locate column with experimental info by finding C:\\Users
        this column contains the value of e.g. Anzahl Messpkt for each rheo phase"""
        headers = self.translate_variable_names(df)
        col_with_expinfo = ""
        idx = 0
        # look for C:\
        for header in headers:
            if "C:\\Users" in df[header][1]:  # python reads \\ as \
                col_with_expinfo = headers[idx]
                break
            idx += 1
        if col_with_expinfo == "":
            raise ValueError(
                f"""Could not locate string C:\\ in {self.rheo_file}
                            Maybe you exported the wrong window of RheoPlus data?"""
            )

        return col_with_expinfo

    def get_num_measurement_pts(self, df) -> np.array:
        """get number of measurement points for each rheo phase"""
        search_string = "Anzahl Messpunkte:"
        idces_rows_anzahl_messpkt = df[df.eq(search_string).any(axis=1)].index
        col_expinfo = self.locate_col_with_expinfo(df)
        num_measurement_points = df[col_expinfo][idces_rows_anzahl_messpkt]

        return np.array(num_measurement_points)

    def get_idces_start_measurement(self, df) -> np.array:
        """get the index in df at which the rheo phases start"""
        indces_start_measurements = df[df["time_s"] == "[s]"].index.tolist()
        for i in range(len(indces_start_measurements)):
            indces_start_measurements[
                i
            ] += 1  # the line at which phase data starts is one below the header
        return np.array(indces_start_measurements)

    def get_idces_end_measurement(self, df) -> np.array:
        idx_start_measurement = self.get_idces_start_measurement(df)
        num_measurement_pts = self.get_num_measurement_pts(df)
        indces_end_measurements = []
        for i in range(len(idx_start_measurement)):
            indces_end_measurements.append(
                int(idx_start_measurement[i]) + int(num_measurement_pts[i])
            )
        return np.array(indces_end_measurements)

    def get_messpktdauers(self, df) -> np.array:
        """messpunkdauer is needed for the butter lowpass filtering"""
        # messpunnktdauer is one line below zeitvorgabe
        search_string = "Zeitvorgabe:"
        idces_rows_zeitvorgabe = df[df.eq(search_string).any(axis=1)].index
        idces_messpktdauer = []
        for index in idces_rows_zeitvorgabe:
            idces_messpktdauer.append(
                index + 1
            )  # messpunktdauer is one line below zeitvorgabe

        # extract messpunktdauer as a string, e.g. 'Messpunktdauer 1 s'
        messpktdauers = []
        col_expinfo = self.locate_col_with_expinfo(df)
        for index in idces_messpktdauer:
            messpktdauer_str = df[col_expinfo].iloc[
                index
            ]  # format = Messpunktdauer 2 s
            messpktdauers.append(
                int("".join(x for x in messpktdauer_str if x.isdigit()))
            )

        return np.array(messpktdauers)

    def get_dict_rheo_data(self, df) -> dict:
        """from a df, get a dictionary of the raw rheo data
        without the non-numerical info from the rheo csv"""
        headers = df.columns.values
        start_indices = self.get_idces_start_measurement(df)
        end_indices = self.get_idces_end_measurement(df)
        dict_rheo_data = {}

        annoying_elems_list = [
            "******",
            "Dy_auto",
            "ME-,MV-",
            "MV-,WMa",
            "WMa,DSO",
            "WMa,taD",
            "WMa,taD",
            "ME-,WMa",
            "M- ,ME-",
            "M- ,MV-",
            "M- ,WMa",
            "viskositaet_Pas"
        ]

        for i in range(len(headers)):
            dummy_list = []  # for a given variable, recover all data in on list
            for j in range(len(start_indices)):
                start = start_indices[j]
                end = end_indices[j]
                phase_data = df[headers[i]][start:end]
                for elem in phase_data:
                    # sometimes rheo values = ******
                    if elem in annoying_elems_list:
                        dummy_list.append(0)
                    else:
                        dummy_list.append(float(elem))
            
            # dummy_list contains all the data. fill dictionary with it
            dict_rheo_data[headers[i]] = np.array(dummy_list).astype(float)

        return dict_rheo_data

    def get_pstart(self, df) -> list:
        """locate p.start in dict_rheo_data"""
        start = [0]
        num_measurement_pts = self.get_num_measurement_pts(df)
        for i in range(len(num_measurement_pts)):
            start.append(start[i] + int(num_measurement_pts[i]))
        start = start[:-1]
        return start

    def get_pend(self, df) -> list:
        """locate p.end in dict_rheo_data"""
        # if phase 0 has len 45 then p0.start = 0 and p0.end = 44
        num_measurement_pts = self.get_num_measurement_pts(df)
        end = [int(num_measurement_pts[0]) - 1]
        for i in range(len(num_measurement_pts) - 1):
            end.append(end[i] + int(num_measurement_pts[i + 1]))

        return end

    def get_dict_pstart_pend(self, df) -> dict:
        """get dictionary containing p.start and p.end for each phase
        valid for raw rheo data (not rsmpl)"""
        start = self.get_pstart(df)
        end = self.get_pend(df)
        messpktdauers = self.get_messpktdauers(df)

        dict_indices = {}
        for i, val in enumerate(start):
            dict_indices["p" + str(i) + ".start"] = val
        for i, val in enumerate(end):
            dict_indices["p" + str(i) + ".end"] = val

        # to be able to access all data
        dict_indices["all.start"] = start[0]
        dict_indices["all.end"] = end[-1]

        for i, val in enumerate(messpktdauers):
            dict_indices["p" + str(i) + ".sampling_period"] = val

        # to be able to filter all data
        dict_indices["all.sampling_period"] = 2

        return dict_indices

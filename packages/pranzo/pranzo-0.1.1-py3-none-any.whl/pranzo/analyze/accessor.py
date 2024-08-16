from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt
from scipy.interpolate import interp1d

from bamboost.common.hdf_pointer import MutableGroup, Dataset
from bamboost.common.file_handler import FileHandler


class Accessor:

    def __init__(self, sim, timeshift_watercontact: dict = {}):

        # recover time shift between water contact and data acquisition start
        timeshift_rheo = timeshift_watercontact.get(
            "rheo",
            sim.parameters.get("rheo", {}).get("start_time_s_from_watercontact", 0),
        )
        timeshift_rheo = float(timeshift_rheo)

        if "rheo" in sim.userdata.keys():
            self.rheo = MyRheo(
                file_handler=sim._file,
                path_to_data="userdata/rheo",
                dt_watercontact=timeshift_rheo,
            )

        # recover time shift between water contact and data acquisition start
        timeshift_calo = timeshift_watercontact.get(
            "calo",
            sim.parameters.get("calo", {}).get("start_time_s_from_watercontact", 0),
        )
        timeshift_calo = float(timeshift_calo)

        # recover characteristic time of device to compute corrected heat, default is 0
        calo_chartime = float(sim.parameters.get("calo", {}).get("chartime_s", "0"))

        if "calo" in sim.userdata.keys():
            self.calo = MyCalo(
                file_handler=sim._file,
                path_to_data="userdata/calo",
                dt_watercontact=timeshift_calo,
                chartime=calo_chartime,
            )


class MyCalo(MutableGroup):

    def __init__(
        self,
        file_handler: FileHandler,
        path_to_data: str,
        dt_watercontact: float,
        chartime: float,
    ) -> None:
        super().__init__(file_handler, path_to_data)

        self.dt_watercontact = dt_watercontact
        self.chartime = chartime

    @property
    def real_time_s(self):
        return self["time_s"][:] + self.dt_watercontact

    @property
    def corrected_heat_Jpg(self):
        return (
            self["norm_heat_Jpgbinder"][:]
            + self.chartime * self["norm_heat_flow_Wpgbinder"][:]
        )

    def __getitem__(self, key) -> CaloField:
        return CaloField(
            file_handler=self._file, path_to_data=f"{self.path_to_data}/{key}"
        )

    def interpolate(self, field: str, x_array: np.ndarray) -> np.ndarray:
        interpolator = interp1d(self.real_time_s, self[field][:], bounds_error=False)
        return interpolator(x_array)


class CaloField(Dataset):

    def __init__(self, file_handler: FileHandler, path_to_data: str) -> None:
        super().__init__(file_handler, path_to_data)


class MyRheo(MutableGroup):

    def __init__(
        self,
        file_handler: FileHandler,
        path_to_data: str,
        dt_watercontact: float = 0,
        phase: str = "all",
    ) -> None:
        super().__init__(file_handler, path_to_data)

        self.dt_watercontact = dt_watercontact
        self._phase = phase
        self.data_slice = slice(
            self.attrs[f"{phase}.start"], self.attrs[f"{phase}.end"]
        )
        self.sampling_period = self.attrs[f"{phase}.sampling_period"]

    @property
    def real_time_s(self):
        return self["time_s"][:] + self.dt_watercontact

    def __getitem__(self, key: str) -> RheoField:

        return RheoField(
            file_handler=self._file,
            path_to_data=f"{self.path_to_data}/{key}",
            data_slice=self.data_slice,
            sampling_period=self.sampling_period,
        )

    def phase(self, phase: str):
        self._phase = phase
        self.data_slice = slice(
            self.attrs[f"{phase}.start"], self.attrs[f"{phase}.end"]
        )
        return self

    def interpolate(self, field: str, x_array: np.ndarray, cutoff=None) -> np.ndarray:

        if cutoff is None:
            interpolator = interp1d(
                self.real_time_s, self[field][:], bounds_error=False
            )
        else:
            interpolator = interp1d(
                self.real_time_s, self[field].filter(cutoff=cutoff), bounds_error=False
            )
        return interpolator(x_array)


class RheoField(Dataset):

    def __init__(
        self,
        file_handler: FileHandler,
        path_to_data: str,
        data_slice,
        sampling_period,
    ) -> None:

        super().__init__(file_handler, path_to_data)

        self.data_slice = data_slice
        self.sampling_period = sampling_period

    def __getitem__(self, slice):
        return super().__getitem__(self.data_slice)[slice]

    def filter(self, cutoff):

        # Filter requirements.
        fs = 1 / self.sampling_period  # sample rate, Hz
        nyq = 0.5 * fs  # Nyquist Frequency
        order = 1  # take first order approx

        def butter_lowpass_filter(data, cutoff, order):
            normal_cutoff = cutoff / nyq
            # Get the filter coefficients
            b, a = butter(order, normal_cutoff, btype="low", analog=False)
            y = filtfilt(b, a, data)
            return y

        filtered_field = butter_lowpass_filter(self[:], cutoff, order)

        return filtered_field

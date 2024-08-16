import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from pranzo.analyze import Accessor, CaloFields, RheoFields


class Analyzer(Accessor):

    def __init__(self, sim):

        # define normalization factors
        self.nft = 1 / 3600
        self.nfh = 1e3
        self.nfG = 1e-6
        self.nfH = 1

        # define unit labels
        self.ut = "h"
        self.uh = "mW/g"
        self.uH = "J/g"
        self.uG = "MPa"

        super().__init__(sim)

        self.sim = sim

    def myplot(
        self,
        ax=None,
        x=[0, 1],
        y=[0, 1],
        xlbl="xlbl",
        ylbl="ylbl",
        type="lin",
        s=0,
        e=-1,
        normx=1,
        normy=1,
        lbl=True,
        **kwargs,
    ):
        if ax is None:
            fig, ax = plt.subplots()

        if type == "lin":
            ax.plot(x[s:e] * normx, y[s:e] * normy, **kwargs)
        elif type == "semilogy":
            ax.semilogy(x[s:e] * normx, y[s:e] * normy, **kwargs)

        if lbl:
            ax.set_xlabel(xlbl)
            ax.set_ylabel(ylbl)

    def plot_ht(self, ax=None, lbl=True, **kwargs):
        """
        plots heat flow vs. time for calo data

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
        """

        t = self.calo.real_time_s
        h = self.calo[CaloFields.NORMHEATFLOW.value][:]

        self.myplot(
            ax=ax,
            x=t * self.nft,
            y=h * self.nfh,
            xlbl=rf"time [{self.ut}]",
            ylbl=rf"h [{self.uh}]",
            lbl=lbl,
            **kwargs,
        )

    def plot_Ht(self, ax=None, lbl=True, **kwargs):
        """
        plots cumulative heat vs. time for calo data

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
        """

        t = self.calo.real_time_s
        H = self.calo[CaloFields.NORMHEAT.value][:]

        self.myplot(
            ax=ax,
            x=t * self.nft,
            y=H * self.nfH,
            xlbl=rf"time [{self.ut}]",
            ylbl=rf"H [{self.uH}]",
            lbl=lbl,
            **kwargs,
        )

    def plot_Gt(self, ax=None, lbl=True, phase="all", cutoff=0.012, **kwargs):
        """
        plots storage modulu vs. time for rheo data

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            phase: custom rheo phase, default is all
            cutoff: custom filter cutoff, default is 0.012
        """

        rheo = self.rheo.phase(phase=phase)

        t = rheo.real_time_s
        G = rheo[RheoFields.G.value].filter(cutoff=cutoff)

        self.myplot(
            ax=ax,
            x=t * self.nft,
            y=G * self.nfG,
            xlbl=rf"time [{self.ut}]",
            ylbl=rf"G [{self.uG}]",
            lbl=lbl,
            **kwargs,
        )

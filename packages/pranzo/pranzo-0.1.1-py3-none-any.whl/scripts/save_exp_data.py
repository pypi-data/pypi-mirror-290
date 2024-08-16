#!/usr/bin/env python

import argparse
import os

os.environ["BAMBOOST_NO_MPI"] = "1"
import bamboost

from pranzo.postprocess import MetaReader, AntonPaarReader, TamAirReader


def add_data(db_name: str, sdir: str, file_id: str):
    """Add data to a bamboost database.

    Args:
        db_name: name of the database
        sdir: directory containing raw csv datafiles
        file_id: id of experiment, e.g. 220513_prelim_opc525r_wc0p4

    """

    db = bamboost.Manager(db_name)

    # if meta data exists, add meta data
    if os.path.exists(f"{sdir}/meta_{file_id}.toml"):
        meta = MetaReader(sdir=sdir, file_id=file_id)
        meta_dict = meta.get_meta_dict()
        print(f"got meta data for {file_id}")
    else:
        print(
            f"Warning: Empty parameters dict. The file meta_{file_id}.toml does not exist. It is recommended to create one."
        )
        meta_dict = {}

    # create empty simulation
    writer = db.create_simulation(
        file_id, parameters=meta_dict, skip_duplicate_check=True
    )

    # if rheo data exists, add rheo data
    if os.path.exists(f"{sdir}/rheo_{file_id}.csv"):
        rheo = AntonPaarReader(sdir=sdir, file_id=file_id)
        data, tags = rheo.get_data()

        writer = db.sim(file_id, return_writer=True)
        exp = writer.userdata.require_group("rheo")

        for key, value in data.items():
            exp[key] = value

        # add phases start and end as attributes of the rheo group
        exp = db.sim(file_id)
        exp.userdata["rheo"].update_attrs(tags)

        print(f"added rheo data for {file_id}")

    # if calo data exists, add calo data
    if os.path.exists(f"{sdir}/calo_{file_id}.csv"):
        calo = TamAirReader(sdir=sdir, file_id=file_id)
        data = calo.get_data()

        writer = db.sim(file_id, return_writer=True)
        exp = writer.userdata.require_group("calo")

        for key, value in data.items():
            exp[key] = value

        print(f"added calo data for {file_id}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("db_name", help="name of bamboost database")
    parser.add_argument("sdir", help="directory containing raw csv files")
    parser.add_argument("file_id", help="e.g. 220513_prelim_opc525r_wc0p4")

    args = parser.parse_args()

    db_name = args.db_name
    sdir = args.sdir
    file_id = args.file_id

    add_data(db_name=db_name, sdir=sdir, file_id=file_id)


if __name__ == "__main__":
    main()

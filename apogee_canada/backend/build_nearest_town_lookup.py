import argparse
import zipfile
import io
from pathlib import Path

import requests
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
RAW_DIR = DATA_DIR / "_raw_cgndb"
RAW_DIR.mkdir(exist_ok=True)

PROVINCE_FILES = {
    "AB": "cgn_ab_csv_eng.zip", "BC": "cgn_bc_csv_eng.zip", "MB": "cgn_mb_csv_eng.zip",
    "NB": "cgn_nb_csv_eng.zip", "NL": "cgn_nl_csv_eng.zip", "NT": "cgn_nt_csv_eng.zip",
    "NS": "cgn_ns_csv_eng.zip", "NU": "cgn_nu_csv_eng.zip", "ON": "cgn_on_csv_eng.zip",
    "PE": "cgn_pe_csv_eng.zip", "QC": "cgn_qc_csv_eng.zip", "SK": "cgn_sk_csv_eng.zip",
    "YT": "cgn_yt_csv_eng.zip",
}
BASE_URL = "https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_cgn_toponyme/prov_csv_eng/"


def download_all():
    for code, fname in PROVINCE_FILES.items():
        out_zip = RAW_DIR / fname
        if out_zip.exists():
            print(f"{code}: already downloaded, skipping")
            continue
        print(f"Downloading {code} ({fname}) ...")
        resp = requests.get(BASE_URL + fname, timeout=60)
        resp.raise_for_status()
        out_zip.write_bytes(resp.content)


def load_province_csv(code: str) -> pd.DataFrame:
    fname = PROVINCE_FILES[code]
    zip_path = RAW_DIR / fname
    with zipfile.ZipFile(zip_path) as z:
        csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        with z.open(csv_names[0]) as f:
            df = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"))
    df["_province_code"] = code
    return df


def inspect_all():
    download_all()
    for code in PROVINCE_FILES:
        df = load_province_csv(code)
        print(f"\n=== {code} === ({len(df)} rows)")
        print(f"Columns: {list(df.columns)}")
        # print unique values of any column that looks like a feature-type field
        for col in df.columns:
            if any(k in col.lower() for k in ["generic", "concise", "type", "feature"]):
                print(f"  {col} unique values (sample): {df[col].dropna().unique()[:15]}")
        print(df.head(2).to_string())
        break  # just inspect one province first, structure should be identical across all


def build_lookup():
    download_all()
    all_places = []
    for code in PROVINCE_FILES:
        df = load_province_csv(code)
        all_places.append(df)
    places = pd.concat(all_places, ignore_index=True)

    # NOTE: adjust these column names after running --inspect and seeing the
    # real headers. CGNDB files typically include columns similar to:
    # GEONAME_ID, NAME, GENERIC (feature type), LATITUDE, LONGITUDE, PROVINCE
    # Populated place feature types in CGNDB are typically listed as
    # something like "Populated Place" in a GENERIC/CONCISE column.
    name_col = "Geographical Name"
    lat_col = "Latitude"
    lon_col = "Longitude"
    feature_col = "Generic Category"
    populated_place_values = ["Populated Place"]

    places = places[places[feature_col].isin(populated_place_values)].copy()
    places = places.dropna(subset=[lat_col, lon_col, name_col])
    print(f"Filtered to {len(places)} real populated places across all provinces.")

    places.to_csv(DATA_DIR / "cgndb_populated_places.csv", index=False)

    # Build nearest-neighbor lookup against DA centroids
    from scipy.spatial import cKDTree

    da_df = pd.read_csv(DATA_DIR / "da_working_dataset.csv")

    place_coords = places[[lat_col, lon_col]].to_numpy()
    tree = cKDTree(place_coords)

    da_coords = da_df[["y", "x"]].to_numpy()  # matches existing DA schema (y=lat, x=lon)
    distances, indices = tree.query(da_coords, k=1)

    da_df["nearest_town"] = places.iloc[indices][name_col].to_numpy()
    da_df["nearest_town_distance_km"] = distances * 111  # rough deg-to-km conversion

    da_df.to_csv(DATA_DIR / "da_working_dataset.csv", index=False)
    print(f"Wrote real nearest_town values for {len(da_df)} DAs to da_working_dataset.csv")
    print(da_df[["DAUID", "nearest_town", "nearest_town_distance_km"]].head(10).to_string())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()

    if args.inspect:
        inspect_all()
        print("\nConfirm the real column names above (name_col, lat_col, lon_col, "
              "feature_col, populated_place_values), update the TODOs in build_lookup(), "
              "then re-run without --inspect.")
        return

    build_lookup()


if __name__ == "__main__":
    main()

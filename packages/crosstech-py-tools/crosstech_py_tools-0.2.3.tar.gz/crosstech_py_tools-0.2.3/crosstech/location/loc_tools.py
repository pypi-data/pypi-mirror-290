from abc import ABC, abstractmethod
from shapely import Point
import geopandas as gpd
import pandas as pd
import numpy as np
import pickle
import os


# ELRBase is an abstract class that defines the interface for all ELR classes.
#
# This interface will allow one to expand how exacly we get the ELR data.
# Perhaps in the future we will want to get the ELR data from a pd.DataFrame or a dict.
class ELRBase(ABC):
    @abstractmethod
    def get(self) -> gpd.GeoDataFrame:
        pass


class StringELR(ELRBase):
    def __init__(self, **kwargs):
        self.elr = kwargs.get("elr")

    def get(self) -> gpd.GeoDataFrame:
        # Get the directory of the current script
        current_dir = os.path.dirname(__file__)
        # Construct the path to the elrs.pkl file
        elrs_path = os.path.join(current_dir, "data", "elrs.pkl")

        with open(elrs_path, "rb") as f:
            elrs: gpd.GeoDataFrame = pickle.load(f)

        elr: gpd.GeoDataFrame = elrs[elrs["elr"] == self.elr].reset_index(drop=True)
        return elr


class GeoDataFrameELR(ELRBase):
    def __init__(self, **kwargs):
        self.elr: gpd.GeoDataFrame = kwargs.get("elr")
        self._validate_columns()

    def get(self) -> gpd.GeoDataFrame:
        if self.elr.crs != 27700:
            self.elr = self.elr.to_crs(27700)
        if "L_M_FROM" in self.elr.columns:
            self.elr.rename(columns={"L_M_FROM": "start_mileage"}, inplace=True)
        if len(self.elr) > 1:
            raise ValueError("Please provide a GeoDataFrame with only 1 row.")
        return self.elr

    def _validate_columns(self) -> None:
        if "geometry" not in self.elr.columns:
            raise ValueError("Please provide a GeoDataFrame with a 'geometry' column.")
        if "elr" not in self.elr.columns:
            raise ValueError("Please provide a GeoDataFrame with an 'elr' column.")
        if (
            "start_mileage" not in self.elr.columns
            and "L_M_FROM" not in self.elr.columns
        ):
            raise ValueError(
                "Please provide a GeoDataFrame with a 'start_mileage' OR 'L_M_FROM' column."
            )


class ELRFactory:
    @staticmethod
    def create_elr(**kwargs) -> type[ELRBase]:
        elr = kwargs.get("elr")
        if elr is None:
            raise ValueError("Please provide an ELR.")
        elif isinstance(elr, str):
            return StringELR(**kwargs)
        elif isinstance(elr, gpd.GeoDataFrame):
            return GeoDataFrameELR(**kwargs)
        else:
            raise ValueError("Please provide a valid ELR.")


class LocTools:
    """
    A class providing tools for location-based operations.

    Methods
    -------
    to_point(lat: float, lon: float, **kwargs) -> Point
        Converts latitude and longitude to a Point object, optionally transforming CRS.
    to_coords(point: Point, **kwargs) -> tuple[float, float] | float
        Extracts latitude or longitude or both from a Point object based on provided keyword arguments.
    point_from_mileage(mileage: float, **kwargs) -> Point
        Interpolates a Point on a GeoDataFrame geometry based on a given mileage.
    """

    @classmethod
    def to_point(cls, lat: float, lon: float, **kwargs) -> Point:
        """
        Converts latitude and longitude to a Point object, optionally transforming CRS.

        Parameters
        ----------
        lat : float
            Latitude of the point.
        lon : float
            Longitude of the point.
        **kwargs : dict
            Optional keyword arguments:
        - crs : str or int
            - The current coordinate reference system of the point.
        - to_crs : str or int
            - The target coordinate reference system to transform the point.

        NOTE: 'crs' and 'to_crs' must be provided together.

        Returns
        -------
        Point
            A shapely.geometry.Point object representing the location.

        Raises
        ------
        Exception
            If only one of 'crs' or 'to_crs' is provided.
        """
        crs = kwargs.get("crs")
        to_crs = kwargs.get("to_crs")

        if crs and to_crs:
            return (
                gpd.GeoDataFrame({"geometry": [Point(lon, lat)]}, crs=crs)
                .to_crs(to_crs)
                .iloc[0]["geometry"]
            )
        elif (crs and not to_crs) or (to_crs and not crs):
            raise Exception(
                "Please provide both 'crs' and 'to_crs' as keyword arguments."
            )

        return Point(lon, lat)

    @classmethod
    def to_coords(cls, point: Point, **kwargs) -> tuple[float, float] | float:
        """
        Extracts latitude or longitude or both from a Point object based on provided keyword arguments.
        Optionally transforming CRS, by default CRS agnostic.

        Parameters
        ----------
        point : Point
            A shapely.geometry.Point object.
        **kwargs : dict
            Optional keyword arguments:
        - lat : bool
            - If True, returns the latitude of the point.
        - lon : bool
            - If True, returns the longitude of the point.
        - crs : str or int
            - The current coordinate reference system of the point.
        - to_crs : str or int
            - The target coordinate reference system to transform the point.

        NOTE: 'crs' and 'to_crs' must be provided together.
        NOTE: 'lat' and 'lon' cannot be provided together.

        Returns
        -------
        tuple[float, float] or float
            - A tuple of (latitude, longitude) if neither 'lat' nor 'lon' is specified.
            - A single float representing latitude if 'lat' is True.
            - A single float representing longitude if 'lon' is True.

        Raises
        ------
        Exception
            If both 'lat' and 'lon' are provided.
        Exception
            If only one of 'crs' or 'to_crs' is provided.
        """
        lat, lon = kwargs.get("lat"), kwargs.get("lon")
        crs, to_crs = kwargs.get("crs"), kwargs.get("to_crs")

        if crs and to_crs:
            point = (
                gpd.GeoDataFrame({"geometry": [point]}, crs=crs)
                .to_crs(to_crs)
                .iloc[0]["geometry"]
            )
        elif (crs and not to_crs) or (to_crs and not crs):
            raise Exception(
                "Please provide both 'crs' and 'to_crs' as keyword arguments."
            )

        if lat and lon:
            raise Exception(
                "Please provide either 'lat' or 'lon' as a keyword argument."
            )
        elif lat:
            return point.coords.xy[1][0]
        elif lon:
            return point.coords.xy[0][0]

        return point.coords.xy[1][0], point.coords.xy[0][0]

    @classmethod
    def point_from_mileage(
        cls,
        mileage: float,
        **kwargs,
    ) -> Point:
        """
        Interpolates a Point on a GeoDataFrame geometry based on a given mileage.
        Naturally input mileage is in miles. Return point is in meters of crs 27700.

        Parameters
        ----------
        mileage : float
            The mileage to interpolate the point.
        **kwargs : dict
            Additional keyword arguments to pass to the ELRFactory.create_elr method.
        - elr : str or GeoDataFrame
            - The ELR (Engineer's Line Reference) code or a single-row GeoDataFrame with ELR data.

        Returns
        -------
        Point
            A shapely.geometry.Point object representing the interpolated location.

        Notes
        -----
        The ELRFactory handles the creation and retrieval of ELR data. It supports two types of inputs:
        - A string representing the ELR code, which retrieves the corresponding GeoDataFrame from a predefined file.
        - A GeoDataFrame containing ELR data, which must include columns for 'geometry' and either 'start_mileage' or 'L_M_FROM'.

        The ELR data is assumed to be in EPSG:27700 CRS. If not, it is transformed accordingly.
        """
        elr_handler = ELRFactory.create_elr(**kwargs)
        elr: gpd.GeoDataFrame = elr_handler.get()

        meterage = float((mileage - elr.start_mileage.values[0]) * 1609.34)
        return elr.geometry.values[0].interpolate(meterage)

from datetime import date, datetime
import json
import requests
from datetime import date
from typing import List, Literal, Optional, Union
from uuid import UUID

from d2spy import models, schemas
from d2spy.api_client import APIClient
from d2spy.extras.utils import pretty_print_response
from d2spy.schemas.geojson import GeoJSON


class Project:
    def __init__(self, client: APIClient, **kwargs):
        self.client = client
        # project attributes returned from API
        self.__dict__.update(kwargs)

    def __repr__(self):
        return (
            f"Project(title={self.title!r}, description={self.description!r}, "
            f"centroid={self.centroid!r})"
        )

    def add_flight(
        self,
        acquisition_date: date,
        altitude: float,
        side_overlap: float,
        forward_overlap: float,
        sensor: Literal["RGB", "Multispectral", "LiDAR", "Other"],
        platform: Union[Literal["Phantom_4", "M300", "M350", "Other"], str],
        name: Optional[str] = None,
        pilot_id: Optional[UUID] = None,
    ) -> models.Flight:
        """Create new flight in a project.

        Args:
            name (Optional[str]): Name of flight.
            acquisition_date (date): Date of flight.
            altitude (float): Flight altitude.
            side_overlap (float): Flight side overlap %.
            forward_overlap (float): Flight forward overlap %.
            sensor (Literal["RGB", "Multispectral", "LiDAR", "Other"]): Sensor used for collecting data on flight.
            platform (Union[Literal["Phantom_4", "M300", "M350"], str]): Platform used for flight.
            pilot_id (Optional[UUID]): ID of the flight's pilot. Defaults to None.

        Returns:
            models.Flight: Newly created flight.
        """
        endpoint = f"/api/v1/projects/{self.id}/flights"

        # if pilot id not provided, use current user's id
        if not pilot_id:
            response = self.client.make_get_request("/api/v1/users/current")
            if response.status_code == 200:
                user = response.json()
                pilot_id = user["id"]

        # Check if we need to serialize the acquisition date
        if isinstance(acquisition_date, date):
            acquisition_date = acquisition_date.strftime("%Y-%m-%d")

        # form data for flight creation
        data = {
            "name": name,
            "acquisition_date": acquisition_date,
            "altitude": altitude,
            "side_overlap": side_overlap,
            "forward_overlap": forward_overlap,
            "sensor": sensor,
            "platform": platform,
            "pilot_id": pilot_id,
        }

        # post form data
        response = self.client.make_post_request(endpoint, json=data)

        # if successful, return flight model
        if response.status_code == 201:
            response_data: Optional[schemas.Flight] = response.json()
            if response_data:
                flight = models.Flight(
                    self.client, **schemas.Flight.from_dict(response_data).__dict__
                )
                return flight

        pretty_print_response(response)
        return None

    def get_flight(self, flight_id: str) -> Optional[models.Flight]:
        """Request single flight by ID. Flight must be active and viewable by user.

        Args:
            flight_id (str): Flight ID.

        Returns:
            Optional[models.Flight]: Flight matching ID or None.
        """
        endpoint = f"/api/v1/projects/{self.id}/flights/{flight_id}"
        response = self.client.make_get_request(endpoint)

        if response.status_code == 200:
            response_data: schemas.Flight = response.json()
            if response_data:
                flight = schemas.Flight.from_dict(response_data)
                return models.Flight(self.client, **flight.__dict__)

        return None

    def get_flights(self, has_raster: Optional[bool] = False) -> List[models.Flight]:
        """Return list of all active flights in project.

        Args:
            has_raster (Optional[bool], optional): Only return flights with active raster data products. Excludes non-raster data products. Defaults to False.

        Returns:
            List[models.Flight]: List of flights.
        """
        endpoint = f"/api/v1/projects/{self.id}/flights"
        response = self.client.make_get_request(
            endpoint, params={"has_raster": has_raster}
        )

        if response.status_code == 200:
            response_data: List[schemas.Flight] = response.json()
            if len(response_data) > 0:
                flights = [
                    models.Flight(
                        self.client, **schemas.Flight.from_dict(flight).__dict__
                    )
                    for flight in response_data
                ]
                return flights

        pretty_print_response(response)
        return []

    def get_project_boundary(self) -> Optional[GeoJSON]:
        """Return project boundary in GeoJSON format.

        Returns:
            GeoJSON: Project boundary in GeoJSON format.
        """
        endpoint = f"/api/v1/projects/{self.id}"
        response = self.client.make_get_request(endpoint)

        if response.status_code == 200:
            response_data: Union[dict, None] = response.json()
            if response_data:
                project = schemas.Project.from_dict(response_data)
                return project.field

        return None

    def update(self, **kwargs) -> None:
        """Update project attributes."""
        endpoint = f"/api/v1/projects/{self.id}"
        response = self.client.make_put_request(
            endpoint, json=json.loads(json.dumps(kwargs, default=str))
        )

        if response.status_code == 200:
            response_data: Optional[schemas.Project] = response.json()
            if response_data:
                updated_project = schemas.Project.from_dict(response_data).__dict__
                for key, value in updated_project.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        print(f"Warning: Attribute '{key}' not found in Project class.")
                return None

        pretty_print_response(response)
        return None

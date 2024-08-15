import aiohttp
from aiohttp import ClientConnectionError, ClientResponse, ClientResponseError, ClientSession

import logging

from typing import List, Optional, Dict, Any


from mbta_route import MBTARoute
from mbta_stop import MBTAStop
from mbta_schedule import MBTASchedule
from mbta_prediction import MBTAPrediction
from mbta_trip import MBTATrip
from mbta_alert import MBTAAlert

MBTA_DEFAULT_HOST = "api-v3.mbta.com"

ENDPOINTS = {
    'STOPS': 'stops',
    'ROUTES': 'routes',
    'PREDICTIONS': 'predictions',
    'SCHEDULES': 'schedules',
    'TRIPS': 'trips',
    'ALERTS': 'alerts'
}

class MBTAClient:
    """Class to interact with the MBTA v3 API."""

    def __init__(self, session: aiohttp.ClientSession, api_key: Optional[str] = None) -> None:
        self._session = session
        self._api_key = api_key

    
    async def get_route(self, id: str, params: Optional[Dict[str, Any]] = None) -> MBTARoute:
        """Get a route by its ID."""
        route_data = await self._fetch_data(f'{ENDPOINTS["ROUTES"]}/{id}', params)
        return MBTARoute(route_data['data'])
    
    async def get_stop(self, id: str, params: Optional[Dict[str, Any]] = None) -> MBTAStop:
        """Get a stop by its ID."""
        stop_data = await self._fetch_data(f'{ENDPOINTS["STOPS"]}/{id}', params)
        return MBTAStop(stop_data['data'])
    
    async def get_trip(self, id: str, params: Optional[Dict[str, Any]] = None) -> MBTATrip:
        """Get a trip by its ID."""
        trip_data = await self._fetch_data(f'{ENDPOINTS["TRIPS"]}/{id}', params)
        return MBTATrip(trip_data['data'])
        
    async def list_routes(self, params: Optional[Dict[str, Any]] = None) -> List[MBTARoute]:
        """List all routes."""
        route_data = await self._fetch_data(ENDPOINTS['ROUTES'], params)
        return [MBTARoute(item) for item in route_data['data']]

    async def list_stops(self, params: Optional[Dict[str, Any]] = None) -> List[MBTAStop]:
        """List all stops."""
        stop_data = await self._fetch_data(ENDPOINTS['STOPS'], params)
        return [MBTAStop(item) for item in stop_data['data']]

    async def list_schedules(self, params: Optional[Dict[str, Any]] = None) -> List[MBTASchedule]:
        """List all schedules."""
        schedule_data = await self._fetch_data(ENDPOINTS['SCHEDULES'], params)
        return [MBTASchedule(item) for item in schedule_data['data']]
    
    async def list_predictions(self, params: Optional[Dict[str, Any]] = None) -> List[MBTAPrediction]:
        """List all predictions."""
        prediction_data = await self._fetch_data(ENDPOINTS['PREDICTIONS'], params)
        return [MBTAPrediction(item) for item in prediction_data['data']]

    async def list_alerts(self, params: Optional[Dict[str, Any]] = None) -> List[MBTAAlert]:
        """List all predictions."""
        alert_data = await self._fetch_data(ENDPOINTS['ALERTS'], params)
        return [MBTAAlert(item) for item in alert_data['data']]
    
    async def _fetch_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to fetch data from the MBTA API."""
        try:
            response = await self.request("get", endpoint, params)
            data = await response.json()  # Await the JSON response
            if 'data' not in data:
                raise ValueError("Unexpected response format")
            return data
        except Exception as error:
            logging.error(f"Error fetching data: {error}")
            raise
        
    async def request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> ClientResponse:
        """Make an HTTP request with optional query parameters and JSON body."""
        
        if params is None:
            params = {}
        if self._api_key:
            params['api_key'] = self._api_key
        
        try:
            response = await self._session.request(
                method,
                f'https://{MBTA_DEFAULT_HOST}/{path}',
                params=params
            )
            
            # Ensure response has a valid status code
            response.raise_for_status()
            
            return response
            
        except ClientConnectionError as error:
            logging.error(f"Connection error: {error}")
            raise
        except ClientResponseError as error:
            logging.error(f"Client response error: {error.status} - {str(error)}")
            raise
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}")
            raise        




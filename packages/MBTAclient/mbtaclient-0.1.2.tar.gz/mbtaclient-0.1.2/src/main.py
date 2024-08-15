import aiohttp

from mbta_client import MBTAClient
from mbta_stop import MBTAStop
from mbta_route import MBTARoute
from mbta_journeys import MBTAJourneys

from typing import Dict, List, Any

API_KEY = None
MAX_JOURNEYS = 2

# ROUTE = 'Framingham/Worcester Line'
# ARRIVE_AT = 'Wellesley Square'
# DEPART_FROM = 'South Station'

ROUTE = 'Framingham/Worcester Line'
DEPART_FROM = 'Wellesley Square'
ARRIVE_AT = 'South Station'

# ROUTE = 'Red'
# DEPART_FROM = 'South Station'
# ARRIVE_AT = 'Alewife'

# ROUTE = None
# DEPART_FROM = 'Copley'
# ARRIVE_AT = 'Park Street'

# ROUTE = None
# DEPART_FROM = 'North Station'
# ARRIVE_AT = 'Swampscott'

# ROUTE = 'Wakefield Avenue & Truman Parkway - Ashmont Station'
# DEPART_FROM = 'Dorchester Ave @ Valley Rd'
# ARRIVE_AT = 'River St @ Standard St'

# ROUTE = 'Forest Hills Station - Back Bay Station'
# DEPART_FROM = 'Back Bay'
# ARRIVE_AT = 'Huntington Ave @ Opera Pl'

# DEPART_FROM = 'Charlestown Navy Yard'
# ARRIVE_AT = 'Long Wharf (South)'
# ROUTE = 'Charlestown Ferry'

# ROUTE = None
# DEPART_FROM = 'North Billerica'
# ARRIVE_AT = 'North Station'

# ROUTE = None
# DEPART_FROM = 'Back Bay'
# ARRIVE_AT = 'South Station'

# ROUTE = None
# DEPART_FROM = 'Pemberton Point'
# ARRIVE_AT = 'Summer St from Cushing Way to Water St (FLAG)'



async def main():
    async with aiohttp.ClientSession() as session:
        
        if API_KEY:
            mbta_client = MBTAClient(session, API_KEY)
        else:
            mbta_client = MBTAClient(session)
            

        params = {
            'filter[location_type]' :'0'
        }
        
        stops = await mbta_client.list_stops(params)
        
       
        depart_from_stops = MBTAStop.get_stops_by_name(stops,DEPART_FROM )
        arrive_at_stops = MBTAStop.get_stops_by_name(stops,ARRIVE_AT )
        
        del stops
        
        if ROUTE:
            routes = await mbta_client.list_routes()
            journey_route = None

            for route in routes:
                if route.long_name == ROUTE:
                    journey_route: MBTARoute = route
                    break  # Found the route, no need to continue the loop

            if journey_route:
                journeys = MBTAJourneys(mbta_client, MAX_JOURNEYS, depart_from_stops, arrive_at_stops, journey_route)
                del route
            else:
                journeys = MBTAJourneys(mbta_client, MAX_JOURNEYS, depart_from_stops, arrive_at_stops)
        else:
            journeys = MBTAJourneys(mbta_client, MAX_JOURNEYS, depart_from_stops, arrive_at_stops)
        
        await journeys.populate()
        
        for journey in journeys.journeys.values():
            
                route_type = journey.get_route_type()
            
                # if subway or ferry
                if route_type == 0 or route_type == 1 or route_type == 4:
                    
                    print("###########")
                    print("Line:", journey.get_route_long_name())  
                    print("Type:", journey.get_route_description())        
                    print("Color:", journey.get_route_color())
                    print() 
                    print("Direction:", journey.get_trip_direction()+" to "+journey.get_trip_destination())
                    print("Destination:", journey.get_trip_headsign())
                    print() 
                    for i in range(len(journey.journey_stops)):
                        print("Station:", journey.get_stop_name(i))
                        print("Platform:", journey.get_platform_name(i))
                        print("Time:", journey.get_stop_time( i))
                        print("Delay:", journey.get_stop_delay( i))
                        print("Time To:", journey.get_stop_time_to(i))
                        print() 
                    for j in range(len(journey.alerts)):
                        print("Alert:" , journey.get_alert_header(j))
                        print() 
                
                # if train
                elif route_type == 2:    
                                                      
                    print("###########")
                    print("Line:", journey.get_route_long_name())  
                    print("Type:", journey.get_route_description())        
                    print("Color:", journey.get_route_color())
                    print() 
                    print("Train Number:", journey.get_trip_name())
                    print("Direction:", journey.get_trip_direction()+" to "+journey.get_trip_destination())
                    print("Destination:", journey.get_trip_headsign())
                    print() 
                    for i in range(len(journey.journey_stops)):
                        print("Station:", journey.get_stop_name(i))
                        print("Platform:", journey.get_platform_name(i))
                        print("Time:", journey.get_stop_time(i))
                        print("Delay:", journey.get_stop_delay(i))
                        print("Time To:", journey.get_stop_time_to(i))
                        print() 
                        
                    for j in range(len(journey.alerts)):
                        print("Alert:" , journey.get_alert_header(j))
                        print() 
                
                #if bus
                elif route_type == 3:

                    print("###########")
                    print("Line:", journey.get_route_short_name())  
                    print("Type:", journey.get_route_description())        
                    print("Color:", journey.get_route_color())
                    print() 
                    print("Direction:", journey.get_trip_direction()+" to "+journey.get_trip_destination())
                    print("Destination:", journey.get_trip_headsign())
                    print() 
                    for i in range(len(journey.journey_stops)):
                        print("Stop:", journey.get_stop_name(i))
                        print("Time:", journey.get_stop_time(i))
                        print("Delay:", journey.get_stop_delay(i))
                        print("Time To:", journey.get_stop_time_to(i))
                        print() 
                        
                    for j in range(len(journey.alerts)):
                        print("Alert:" , journey.get_alert_header(j))
                        print() 
                                    
                else:
                    
                     print('ARGH!') 
                                
# Run the main function
import asyncio
asyncio.run(main())

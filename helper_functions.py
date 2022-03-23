import pandas as pd
import zipfile

#helper functions
def check_routes(route_list, routes):
    wrong_names = []
    for route in route_list:
        if route not in routes.route_short_name.unique():
            wrong_names.append(route)

    if len(wrong_names) >= 1:
        print("Routes " + str(wrong_names)[1:-1] + ' Not Found.')
        route_choices = input('Please enter a new route list: ')
        route_list = route_choices.upper().replace(' ', '').split(",")

        #recursively call check routes with the new list until it's good
        check_routes(route_list, routes)

    return route_list

#function to get the service ids for selected day type
def filter_dates(selected_day, GTFS):
    calendar = None
    dates = None
    
    with zipfile.ZipFile('./feeds/' + GTFS) as myzip:
        try: 
            myzip.extract('calendar.txt')
            calendar = pd.read_csv('calendar.txt')

        except:
            myzip.extract("calendar_dates.txt")
            dates = pd.read_csv('calendar_dates.txt')

    if calendar is not None: 
        if selected_day == 'weekday': 
            conditions = (calendar.monday == 1) & (calendar.tuesday == 1) & (calendar.wednesday == 1) & (calendar.thursday == 1) & (calendar.friday == 1)
            service_ids = calendar[conditions].service_id
        elif selected_day == 'weekend':
            conditions = (calendar.saturday == 1) | (calendar.sunday == 1)
            service_ids = calendar[conditions].service_id
        else:
            service_ids = calendar.service_id.unique()


    if dates is not None:
        dates['day_type'] = pd.to_datetime(dates.date, format='%Y%m%d').dt.dayofweek

        if selected_day == 'weekday':
            condition = (dates.day_type.isin([5,6]) == False)
        elif selected_day == 'weekend':
            condition = (dates.day_type.isin([5,6]))
        else: 
            condition = dates.day_type.isin([0,1,2,3,4,5,6])

        #Convert to string for comparison with the trips
        service_ids = dates[condition].service_id.unique()
        
    return service_ids.astype(str)
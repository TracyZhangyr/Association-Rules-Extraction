import csv
# our data source: @ NYC OPEN DATA
# link to original data: https://data.cityofnewyork.us/NYC-BigApps/NYPD-Motor-Vehicle-Collisions-Summary/m666-sf2m

def is_recent(row):
    year = int(row[0].split('/')[2])
    # return year >= 2022 # For quick check
    return year >= 2020

def get_crush_season(row):
    month = int(row[0].split('/')[0])
    if month >= 3 and month <=5:
        return 'spring'
    elif month >=6 and month <= 8:
        return 'summer'
    elif month >=9 and month <= 11:
        return 'autumn'
    else:
        return 'winter'

def get_crush_time(row):
    hour = int(row[1].split(':')[0])
    if hour >= 3 and hour <= 6:
        return 'dawn'
    elif hour >= 7 and hour <= 10:
        return 'morning'
    elif hour >= 11 and hour <= 14:
        return 'noon'
    elif hour >= 15 and hour <= 18:
        return 'afternoon'
    elif hour >= 19 and hour <= 22:
        return 'night'
    elif hour >= 23 or hour <= 2:
        return 'midnight'

def get_crush_borough(row):
    borough = row[2].strip()
    if borough != '':
        return borough.lower().replace(' ', '_').replace('/', '_')
    else:
        return 'unspecified_borough'

# def getZip(row):
#     row[3] = row[3].strip()
#     if row[3] != '':
#         return row[3].strip()
#     else:
#         return None

def get_crush_street(row):
    on_street = row[7].strip()
    if on_street != '':
        return on_street.lower().replace(' ', '_')
    else:
        return 'unspecified_street'

def get_person_status(row):
    data = []

    if int(row[12])>0 or int(row[14])>0 or int(row[16])>0:
        data.append('injured')

    if int(row[13])>0 or int(row[15])>0 or int(row[17])>0:
        data.append('killed')

    if len(data) == 0:
        data.append('safe')

    return data

def get_crush_reason(row):
    data = set()
    is_unspecified = 1
    r1 = row[18].strip()
    r2 = row[19].strip()
    r3 = row[20].strip()
    if r1 != 'Unspecified' and r1 != '':
        is_unspecified = 0
        data.add(r1.lower().replace(' ', '_').replace('/', '_').replace('-', '_')) 
    if r2 != 'Unspecified' and r2 != '':
        is_unspecified = 0
        data.add(r2.lower().replace(' ', '_').replace('/', '_').replace('-', '_')) 
    if r3 != 'Unspecified' and r3 != '':
        is_unspecified = 0
        data.add(r3.lower().replace(' ', '_').replace('/', '_').replace('-', '_')) 
    if is_unspecified == 1:
        data.add('unspecified_reason')

def get_vehicle_type(row):
    data = set()
    if row[24] != '':
        data.add(row[24].strip().lower().replace(' ', '_'))
        if row[25] != '':
            data.add(row[25].strip().lower().replace(' ', '_'))
            if row[26] != '':
                data.add(row[26].strip().lower().replace(' ', '_'))
                if row[27] != '':
                    data.add(row[27].strip().lower().replace(' ', '_'))
    else:
        data.add('unspecified_vehicle')
        return list(data)

    type_data = list(data)
    type_data = ['truck' if 'truck' in item or 'dump' in item else item for item in type_data]
    type_data = ['suv' if 'station_wagon' in item or 'sport_utility_vehicle' in item else item for item in type_data]

    return type_data


# Please replace the absolute path here when you try in your local space
with open('/Users/test/Desktop/6111/Motor_Vehicle_Collisions_-_Crashes.csv', newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    next(datareader)
    filtered_data = []
    recent_line = 0
    scanned_line = 0
    for row in datareader:
        scanned_line += 1
        if is_recent(row):
            recent_line += 1
            data = []

            crush_season = get_crush_season(row)
            data.append(crush_season)

            crush_time = get_crush_time(row)
            data.append(crush_time)

            crush_borough = get_crush_borough(row)
            data.append(crush_borough)

            # zip = getZip(row)
            # if zip is not None:
            #     data.append(zip)

            person_status_list = get_person_status(row)
            data.extend(person_status_list)

            crush_reason = get_crush_reason(row)
            data.append(crush_reason)

            vehicle_list = get_vehicle_type(row)
            data.extend(vehicle_list)

            filtered_data.append(data)


with open('PROCESSED_CRUSH_DATA.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    writer.writerows(filtered_data)
    print("Finished data preprocessing.")
    print("Scanned ", scanned_line, " lines")
    print("Recent ", recent_line, " lines")

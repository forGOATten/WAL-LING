import json
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone

data = []
with open('TLE_data.json') as file:
    contents = file.read()
    data = json.loads(contents)

# types = []
# for type in [a['OBJECT_TYPE'] for a in data]:
#     if type not in types:
#         types.append(type)
# types.sort()
# print(types)
# ['DEBRIS', 'PAYLOAD', 'ROCKET BODY']
now = datetime.now(timezone.utc)

debris = []
rocketbody = []
payload = []

for obj in data:
    space_obj = EarthSatellite(obj['TLE_LINE1'], obj['TLE_LINE2'], obj['INTLDES'], load.timescale())
    t = space_obj.epoch
    position = space_obj.at(t).position.km  # (x, y, z) in km
    data[data.index(obj)]["XYZ"] = tuple(position.tolist())
    match(obj['OBJECT_TYPE']):
        case "DEBRIS":
            debris.append(tuple(position.tolist()))
        case "ROCKET BODY":
            rocketbody.append(tuple(position.tolist()))
        case "PAYLOAD":
            payload.append(tuple(position.tolist()))






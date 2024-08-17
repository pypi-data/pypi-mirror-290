you can import function as below

from .arial_distance import get_distance, check_distance_within

get_distance - this function will return integer value of distance betn 2 coordinate

source = 19.207084243604214, 73.12916639835512
distination = 19.210002125062804, 73.11869505407905
get_distance(source, distination)

check_distance_within - it cheks if dist betn  source and distination falls within radius in KM and return json

radius = 20
check_distance_within(source, distination, radius)
from pdb import set_trace
from datetime import datetime



def parse_date_from_filename(filename: str, /) -> datetime:
     """Parse the date and time from a filename.

     Args:
         filename (str): The filename to parse. FORMAT TYPES:
        R16A0612.014930 | RM2280811.114579 | RM04B1019.582

     Returns:
         datetime: The datetime object parsed from the filename.
     """

     #Split the filename in name and extension
     name = filename.split(".")[0]
     extension = filename.split(".")[1]

     #Get the date and hour from the name
     date = f"{name[-7:-5]}-{int(name[-5], base = 16):02d}-{name[-4:-2]}"
     extension = extension + "000"

     #Get the hour and microseconds from the extension
     hour = f"{name[-2:]}:{extension[0:2]}:{extension[2:4]}"
     microseconds = f"{int(extension[4:6])*10000:06d}"

     return datetime.strptime(f"{date}T{hour}.{microseconds}", r"%y-%m-%dT%H:%M:%S.%f")
    
    
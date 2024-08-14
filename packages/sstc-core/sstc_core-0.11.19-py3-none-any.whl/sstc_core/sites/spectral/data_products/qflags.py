from sstc_core.sites.spectral import utils


def compute_qflag(
    latitude_dd: float,
    longitude_dd: float, 
    records_dict: dict,
    has_snow_presence: bool = False,
    timezone_str: str = 'Europe/Stockholm', 
    default_temporal_resolution: bool = True,  # default temporal resolution is 30 min, else 1 hr or more
    ) -> int:
    """
    Computes the Quality Flag (QFLAG) for a set of records based on their temporal resolution, solar elevation, and environmental conditions.

    This function calculates a QFLAG value for a set of records, considering factors such as the sun's elevation angle, 
    the presence of snow, and the number of records within a given temporal resolution. The QFLAG indicates the quality 
    or suitability of the records for further processing.

    Parameters:
        latitude_dd (float): The latitude of the location in decimal degrees.
        longitude_dd (float): The longitude of the location in decimal degrees.
        records_dict (dict): A dictionary of records, where keys are record identifiers and values are dictionaries 
                             containing record data. Each record must include a 'creation_date' field.
        has_snow_presence (bool, optional): Indicates whether snow is present in the records. Defaults to False.
        timezone_str (str, optional): The timezone string to use for the location. Defaults to 'Europe/Stockholm'.
        default_temporal_resolution (bool, optional): If True, assumes a default temporal resolution of 30 minutes; 
                                                      otherwise, assumes a resolution of 1 hour or more. Defaults to True.

    Returns:
        int: The computed QFLAG value, which indicates the quality of the records.

    Example:
        ```python
        records_dict = {
            'record1': {'creation_date': '2024-06-07 08:17:23'},
            'record2': {'creation_date': '2024-06-07 08:47:23'},
            'record3': {'creation_date': '2024-06-07 09:17:23'}
        }
        qflag = compute_qflag(
            latitude_dd=68.35,
            longitude_dd=18.82,
            records_dict=records_dict,
            has_snow_presence=False,
            timezone_str='Europe/Stockholm',
            default_temporal_resolution=True
        )
        print(qflag)
        # Output might be 231, depending on the number of records and solar elevation class.
        ```

    Raises:
        ValueError: If there is an issue with calculating the sun position or determining the solar elevation class.

    Notes:
        - The function first calculates the mean datetime of all the records.
        - The sun's position is determined based on the mean datetime and the location's latitude and longitude.
        - The `default_temporal_resolution` parameter controls whether the function uses a 30-minute or 1-hour (or more) 
          temporal resolution when computing the QFLAG.
        - The function uses specific rules based on the number of records and the solar elevation class to assign a QFLAG value.
        - A QFLAG of 100 indicates snow presence, regardless of other conditions.

    Dependencies:
        - This function depends on external utility functions such as `utils.mean_datetime_str`, `utils.calculate_sun_position`, 
          and `utils.get_solar_elevation_class`, which are assumed to be defined elsewhere in the codebase.
    """
    
    datetime_list = [v['creation_date'] for k, v in records_dict.items()]
    
    mean_datetime_str = utils.mean_datetime_str(datetime_list=datetime_list)
    sun_position = utils.calculate_sun_position(
        datetime_str=mean_datetime_str, 
        latitude_dd=latitude_dd, 
        longitude_dd=longitude_dd, 
        timezone_str=timezone_str
    )
    
    sun_elevation_angle = sun_position['sun_elevation_angle']
    solar_elevation_class = utils.get_solar_elevation_class(sun_elevation=sun_elevation_angle)
   
    n_records = len(records_dict)
    
    if default_temporal_resolution:
        if has_snow_presence:
            QFLAG = 100
        
        elif (n_records < 3) and (solar_elevation_class == 1):
            QFLAG = 211
            
        elif (n_records < 3) and (solar_elevation_class == 2):
            QFLAG = 212
        
        elif (n_records < 3) and (solar_elevation_class == 3):
            QFLAG = 213
        
        elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 1):
            QFLAG = 221
        
        elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 2):
            QFLAG = 222
            
        elif ((n_records >= 3) and (n_records < 6)) and (solar_elevation_class == 3):
            QFLAG = 223
            
        elif (n_records >= 6) and (solar_elevation_class == 1):
            QFLAG = 231
        
        elif (n_records >= 6) and (solar_elevation_class == 2):
            QFLAG = 232     
        
        elif (n_records >= 6) and (solar_elevation_class == 3):
            QFLAG = 233 
        
        return QFLAG
    
    else:
        # Valid only for hourly/bi-hourly temporal resolution
        if has_snow_presence:
            QFLAG = 100
        
        elif (n_records < 2) and (solar_elevation_class == 1):
            QFLAG = 211
            
        elif (n_records < 2) and (solar_elevation_class == 2):
            QFLAG = 212
        
        elif (n_records < 2) and (n_records < 2) and (solar_elevation_class == 3):
            QFLAG = 213
        
        elif ((n_records >= 2) and (n_records < 4)) and (solar_elevation_class == 1):
            QFLAG = 221
        
        elif ((n_records >= 2) and (n_records < 4)) and (solar_elevation_class == 2):
            QFLAG = 222
            
        elif ((n_records >= 2) and (n_records < 4)) and (solar_elevation_class == 3):
            QFLAG = 223
            
        elif (n_records >= 4) and (solar_elevation_class == 1):
            QFLAG = 231
        
        elif (n_records >= 4) and (solar_elevation_class == 2):
            QFLAG = 232     
        
        elif (n_records >= 4) and (solar_elevation_class == 3):
            QFLAG = 233 
        
        return QFLAG

        
        
'''
This file contains the loaders for the EV City environment.
'''

import numpy as np
import pandas as pd
import datetime
import math
import pkg_resources

from ..models.ev_charger import EV_Charger
from ..models.ev import EV
from ..models.transformer import Transformer


def load_ev_spawn_scenarios(env):
    '''Loads the EV spawn scenarios of the simulation'''

    df_arrival_week_file = pkg_resources.resource_filename(
        'EVsSimulator', 'data/distribution-of-arrival.csv')
    df_arrival_weekend_file = pkg_resources.resource_filename(
        'EVsSimulator', 'data/distribution-of-arrival-weekend.csv')
    df_connection_time_file = pkg_resources.resource_filename(
        'EVsSimulator', 'data/distribution-of-connection-time.csv')
    df_energy_demand_file = pkg_resources.resource_filename(
        'EVsSimulator', 'data/distribution-of-energy-demand.csv')
    time_of_connection_vs_hour_file = pkg_resources.resource_filename(
        'EVsSimulator', 'data/time_of_connection_vs_hour.npy')
    
    env.df_arrival_week = pd.read_csv(df_arrival_week_file)  # weekdays
    env.df_arrival_weekend = pd.read_csv(df_arrival_weekend_file)  # weekends
    env.df_connection_time = pd.read_csv(df_connection_time_file)  # connection time
    env.df_energy_demand = pd.read_csv(df_energy_demand_file)  # energy demand
    env.time_of_connection_vs_hour = np.load(time_of_connection_vs_hour_file)  # time of connection vs hour


def load_power_setpoints(env, randomly):
    '''
    Loads the power setpoints of the simulation based on the day-ahead prices'''

    # It is necessary to run the simulation first in order to get the ev_load_potential
    if not randomly and env.load_from_replay_path is None:
        raise ValueError(
            'Cannot load power setpoints from day-ahead prices if load_from_replay_path is None')

    power_setpoints = np.ones(env.simulation_length)

    if env.load_from_replay_path:
        return env.replay.power_setpoints

    if randomly:
        inverse_prices = 1/abs(env.charge_prices[0, :]+0.001)

        if env.cs == 1:
            cs = env.charging_stations[0]
            power_setpoints = power_setpoints * cs.max_charge_current * \
                cs.voltage * math.sqrt(cs.phases)/1000
            power_setpoints = power_setpoints * \
                np.random.randint(2, size=env.simulation_length)
            return power_setpoints

        return power_setpoints*(inverse_prices*env.cs)*np.random.uniform(0.08, 0.09, 1)
    else:
        raise NotImplementedError(
            'Loading power setpoints from is not implemented yet')


def load_transformers(env):
    '''Loads the transformers of the simulation
    If load_from_replay_path is None, then the transformers are created randomly

    Returns:
        - transformers: a list of transformer objects'''

    transformers = []
    if env.load_from_replay_path is not None:
        transformers = env.replay.transformers

    elif env.charging_network_topology:
        # parse the topology file and create the transformers
        cs_counter = 0
        for i, tr in enumerate(env.charging_network_topology):
            cs_ids = []
            for cs in env.charging_network_topology[tr]['charging_stations']:
                cs_ids.append(cs_counter)
                cs_counter += 1
            transformer = Transformer(id=i,
                                      cs_ids=cs_ids,
                                      min_current=env.charging_network_topology[tr]['min_current'],
                                      max_current=env.charging_network_topology[tr]['max_current'],
                                      timescale=env.timescale,
                                      simulation_length=env.simulation_length,
                                      standard_transformer_loading=np.zeros(
                                          env.simulation_length),
                                      )
            transformers.append(transformer)

    else:
        if env.number_of_transformers > env.cs:
            raise ValueError(
                'The number of transformers cannot be greater than the number of charging stations')
        for i in range(env.number_of_transformers):
            # get indexes where the transformer is connected
            transformer = Transformer(id=i,
                                      cs_ids=np.where(
                                          np.array(env.cs_transformers) == i)[0],
                                      timescale=env.timescale,)
            transformers.append(transformer)
        env.n_transformers = len(transformers)
    return transformers


def load_ev_charger_profiles(env):
    '''Loads the EV charger profiles of the simulation
    If load_from_replay_path is None, then the EV charger profiles are created randomly

    Returns:
        - ev_charger_profiles: a list of ev_charger_profile objects'''

    charging_stations = []
    if env.load_from_replay_path is not None:
        return env.replay.charging_stations
    elif env.charging_network_topology:
        # parse the topology file and create the charging stations
        cs_counter = 0
        for i, tr in enumerate(env.charging_network_topology):
            for cs in env.charging_network_topology[tr]['charging_stations']:
                ev_charger = EV_Charger(id=cs_counter,
                                        connected_bus=0,
                                        connected_transformer=i,
                                        min_charge_current=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['min_charge_current'],
                                        max_charge_current=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['max_charge_current'],
                                        min_discharge_current=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['min_discharge_current'],
                                        max_discharge_current=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['max_discharge_current'],
                                        voltage=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['voltage'],
                                        n_ports=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['n_ports'],
                                        charger_type=env.charging_network_topology[tr][
                                            'charging_stations'][cs]['charger_type'],
                                        phases=env.charging_network_topology[tr]['charging_stations'][cs]['phases'],
                                        timescale=env.timescale,
                                        verbose=env.verbose,)
                cs_counter += 1
                charging_stations.append(ev_charger)
        env.cs = len(charging_stations)
        return charging_stations

    else:
        for i in range(env.cs):
            ev_charger = EV_Charger(id=i,
                                    connected_bus=0,  # env.cs_buses[i],
                                    connected_transformer=env.cs_transformers[i],
                                    n_ports=env.number_of_ports_per_cs,
                                    timescale=env.timescale,
                                    verbose=env.verbose,)

            charging_stations.append(ev_charger)
        return charging_stations


def load_ev_profiles(env):
    '''Loads the EV profiles of the simulation
    If load_from_replay_path is None, then the EV profiles are created randomly

    Returns:
        - ev_profiles: a list of ev_profile objects'''

    if env.load_from_replay_path is None:
        return None
    else:
        return env.replay.EVs


def load_electricity_prices(env):
    '''Loads the electricity prices of the simulation
    If load_from_replay_path is None, then the electricity prices are created randomly

    Returns:
        - charge_prices: a matrix of size (number of charging stations, simulation length) with the charge prices
        - discharge_prices: a matrix of size (number of charging stations, simulation length) with the discharge prices'''

    if env.load_from_replay_path is not None:
        return env.replay.charge_prices, env.replay.discharge_prices

    # else load historical prices
    file_path = pkg_resources.resource_filename(
        'EVsSimulator', 'data/Netherlands_day-ahead-2015-2023.csv')
    data = pd.read_csv(file_path, sep=',', header=0)
    drop_columns = ['Country', 'Datetime (Local)']
    data.drop(drop_columns, inplace=True, axis=1)
    data['year'] = pd.DatetimeIndex(data['Datetime (UTC)']).year
    data['month'] = pd.DatetimeIndex(data['Datetime (UTC)']).month
    data['day'] = pd.DatetimeIndex(data['Datetime (UTC)']).day
    data['hour'] = pd.DatetimeIndex(data['Datetime (UTC)']).hour

    # assume charge and discharge prices are the same
    # assume prices are the same for all charging stations

    charge_prices = np.zeros((env.cs, env.simulation_length))
    discharge_prices = np.zeros((env.cs, env.simulation_length))
    # for every simulation step, take the price of the corresponding hour
    sim_temp_date = env.sim_starting_date
    for i in range(env.simulation_length):

        year = sim_temp_date.year
        month = sim_temp_date.month
        day = sim_temp_date.day
        hour = sim_temp_date.hour
        # find the corresponding price
        try:
            charge_prices[:, i] = -data.loc[(data['year'] == year) & (data['month'] == month) & (data['day'] == day) & (data['hour'] == hour),
                                            'Price (EUR/MWhe)'].iloc[0]/1000  # €/kWh
            discharge_prices[:, i] = data.loc[(data['year'] == year) & (data['month'] == month) & (data['day'] == day) & (data['hour'] == hour),
                                              'Price (EUR/MWhe)'].iloc[0]/1000  # €/kWh
        except:
            print(
                'Error: no price found for the given date and hour. Using 2022 prices instead.')

            year = 2022
            if day > 28:
                day -= 1
            print("Debug:", year, month, day, hour)
            charge_prices[:, i] = -data.loc[(data['year'] == year) & (data['month'] == month) & (data['day'] == day) & (data['hour'] == hour),
                                            'Price (EUR/MWhe)'].iloc[0]/1000  # €/kWh
            discharge_prices[:, i] = data.loc[(data['year'] == year) & (data['month'] == month) & (data['day'] == day) & (data['hour'] == hour),
                                              'Price (EUR/MWhe)'].iloc[0]/1000  # €/kWh

        # step to next
        sim_temp_date = sim_temp_date + \
            datetime.timedelta(minutes=env.timescale)
    return charge_prices, discharge_prices

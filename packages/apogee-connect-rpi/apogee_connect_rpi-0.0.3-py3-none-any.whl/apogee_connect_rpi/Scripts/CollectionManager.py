import bleak
import struct
import asyncio  
import os
import csv
import datetime
import re
from crontab import CronTab

from apogee_connect_rpi.Scripts.SensorClasses import *
from apogee_connect_rpi.Helpers.liveDataTypes import liveDataTypes
from apogee_connect_rpi.Helpers.ApogeeUuids import *
from apogee_connect_rpi.Scripts.AppConfig import AppConfig
from apogee_connect_rpi.Scripts.SensorManager import SensorManager


class CollectionManager:
    def __init__(self, address: str, filename: str):
        self.address = address
        self.filename = filename

        self.sensor = None
        self.bleak_client = None 

        self.sensorManager = SensorManager()
        config = AppConfig()
        self.precision = config.get_precision()

    #
    # SENSOR CONNECTION
    #
    async def connect(self):
        if not self.bleak_client:
            try: 
                print(f"Connecting to sensor {self.address}")
                self.bleak_client = bleak.BleakClient(self.address)
                await self.bleak_client.connect()

            except asyncio.TimeoutError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

            except bleak.BleakError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

    async def disconnect(self):
        if self.bleak_client:
            try:
                await self.bleak_client.disconnect()
                self.bleak_client = None
            
            except bleak.BleakError as e:
                print(f"Could not disconnect from sensor {self.address}. {e}")
                exit(1)

    #
    # INITIATE COLLECTION
    #
    async def collect_live_data(self, interval: int, start_time, end_time):
        await self.connect()
        await self.populate_sensor_info()
        await self.check_sensor_time()

        if self.sensor is None:
            print("Error retrieving sensor information")
            return

        self.create_csv()
 
        if self.sensor.type == "Guardian":
            await self.collect_guardian_data(interval, start_time, end_time)
        else:
            await self.collect_microcache_data(interval, start_time, end_time)

        await self.disconnect()
    
    async def collect_guardian_data(self, interval: int, start_time, end_time):
        try:            
            # Set last timestamp transferred to current time to avoid getting old data
            await self.set_last_timestamp_transferred()

            # Configure data logging settings and turn logging on 
            bytearray_data = self.get_logging_bytearray(interval, start_time, end_time)
            await self.initiate_logging(bytearray_data)

            # Add sensor to list of currently collecting sensors
            self.sensorManager.add_sensor(self.sensor.address, self.sensor.sensorID, interval, start_time, end_time, self.filename)

            self.setup_crontab_command(interval, start_time, end_time)

        except bleak.BleakError as e:
            print(f"Error retrieving sensor data: {e}")

    async def collect_microcache_data(self, interval: int, start_time, end_time):
        print("Not yet implemented")

    async def set_last_timestamp_transferred(self):
        current_time_epoch = int(datetime.datetime.now().timestamp())
        await self.bleak_client.write_gatt_char(lastTransferredTimestampUUID, bytearray(struct.pack('<I', current_time_epoch)), True)

    def get_logging_bytearray(self, interval: int, start_time, end_time):
        logging_interval = interval * 60 # Convert to minutes
        sampling_interval = 15 # Just keep sampling interval at 15 seconds
        data_array = [sampling_interval, logging_interval]

        # Determine need to set a custom start/end time
        if start_time:
            data_array.append(start_time)
        if end_time:
            if not start_time:
                data_array.append(0) # Add a 0 for start time if there is an end time but no start time
            data_array.append(end_time)

        # Convert array to bytearray for gatt characteristic
        bytearray_data = bytearray()
        for num in data_array:
            bytearray_data.extend(struct.pack('<I', num)) 
        
        return bytearray_data

    async def check_sensor_time(self):
        data = await self.bleak_client.read_gatt_char(currentTimeUUID)
        data_packet = bytes(data)
        sensor_time = struct.unpack('<I', data_packet[:4])[0]

        current_time_epoch = int(datetime.datetime.now().timestamp())

        # Update time on sensor if more than a minute off
        time_difference = abs(current_time_epoch - sensor_time)
        if time_difference > 60:
            print("Updating time on sensor")
            await self.bleak_client.write_gatt_char(currentTimeUUID, bytearray(struct.pack('<I', current_time_epoch)), True)      

    async def initiate_logging(self, bytearray_data):
        # Start data logging
        print("Starting data collection...")
        await self.bleak_client.write_gatt_char(dataLoggingIntervalsUUID, bytearray_data, True)
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([1]), True)

    def setup_crontab_command(self, interval: int, start_time, end_time):
        if not start_time:
            start_time = 0
        if not end_time:
            end_time = 4294967295

        cron = CronTab(user=True)

        # Check that sensor with address doesn't already have a cron job
        for job in cron:
            if self.address in job.command:
                print("A task is already scheduled for a sensor with the given address. Run the 'stop' command to remove that job.")
                exit(0)

        # Setup crontab command
        home_dir = os.path.expanduser("~")
        log_dir = os.path.join(home_dir, "Apogee", "apogee_connect_rpi", "logs")
        os.makedirs(log_dir, exist_ok=True)

        command = f"{home_dir}/.local/bin/apogee run_data_collection {self.address} --file {self.filename} --id {self.sensor.sensorID} --start {start_time} --end {end_time} >> {log_dir}/cron.log 2>&1"
        job = cron.new(command=command)
        job.minute.every(interval)
        cron.write()

        print(f"Data collection continuing in background. Logs will be collected at {self.filename}. \nThis terminal may be closed.")

    async def populate_sensor_info(self):
        await self.connect()

        try:
            print("Getting sensor info")
            sensorID_data = await self.bleak_client.read_gatt_char(sensorIDUUID)
            hw_data = await self.bleak_client.read_gatt_char(hardwareVersionUUID)
            fw_data = await self.bleak_client.read_gatt_char(firmwareVersionUUID)

            sensorID = int.from_bytes(sensorID_data, byteorder='little', signed=False)           
            hw = int(hw_data.decode('utf-8'))
            fw = int(fw_data.decode('utf-8'))

            self.sensor = get_sensor_class_from_ID(sensorID, self.address)

            if not self.sensor.compatibleFirmware(int(hw), int(fw)):
                print("Firmware needs to be updated in order to be compatible with this application")
                exit(1)
        
        except bleak.BleakError as e:
            print(f"Error getting sensor info, {e}")
            exit(1)

    #
    # DATA COLLECTION
    #
    async def run_data_collection(self, sensorID):
        await self.connect()
        self.sensor = get_sensor_class_from_ID(sensorID, self.address)

        print('Collecting data' )
        try:
            data = await self.bleak_client.read_gatt_char(dataLogTransferUUID)
            self.handle_live_data(data)

        except asyncio.TimeoutError as e:
                print(f"Could not connect to sensor {self.address}. {e}")
                exit(1)

        except bleak.BleakError as e:
            print(f"Could not connect to sensor {self.address}. {e}")
            exit(1)

        finally:
            await self.disconnect()

    def handle_live_data(self, data):
        data_packet = bytes(data)
        hex_representation = data_packet.hex()
        print(f"Received packet: {hex_representation}")

        # Ensure the data packet is complete or if it is just all "FF" indicating no data to collect
        if len(data_packet) < 8:
            print("No data to collect")
            return
        
        # Get packet header information
        timestamp = struct.unpack('<I', data_packet[:4])[0]
        intervalBetweenTimestamps = struct.unpack('<H', data_packet[4:6])[0]
        measurementsPerInterval = struct.unpack('<B', data_packet[6:7])[0]
                
        data = []
        # This loop should usually only run once, but just in case a collection is missed and there are multiple sets in packet
        # Separate packet into groups based on timestamp (e.g., groups of 5 datapoints for the Guardian, groups of 1 datapoint for microcache)
        for startIndex in range(8, len(data_packet) - 1, 4 * measurementsPerInterval):
            endIndex = min(startIndex + (4 * measurementsPerInterval), len(data_packet))
            groupedArray = data_packet[startIndex:endIndex]

            # Get each datapoint within the current timestamp
            data = []
            for i in range(0, len(groupedArray), 4):
                raw = struct.unpack('<I', groupedArray[i:(i + 4)])[0]

                # Divide by 10,000 to scale from ten-thousandths to ones
                dataValue = raw / 10000.0

                data.append(dataValue)

            # Calculate all live data based on specific sensor class
            live_data = self.sensor.calculate_live_data(data)

            self.write_to_csv(timestamp, live_data)
            self.sensorManager.increment_collected_logs(self.address)

            # Increment timestamp in case there are multiple logs in a single packet
            timestamp += intervalBetweenTimestamps

        return
    
    # 
    # STOP COLLECTION
    #
    async def stop_data_collection(self):
        await self.connect()

        self.remove_crontab_job()
            
        print("Removing sensor from list")
        self.sensorManager.remove_sensor(self.address)

        print("Stopping Live Data")
        await self.bleak_client.write_gatt_char(dataLoggingControlUUID, bytearray([0]), True)

    async def delayed_stop_data_collection(self, end_time: int):
        print("Updating data collection end time")
        cron = CronTab(user=True)

        job_found = False
        for job in cron:
            if self.address in job.command:
                job_found = True
                command = job.command

                # Find and replace the command's end time
                new_command = re.sub(r'--end \d+', f'--end {end_time}', command)
                job.set_command(new_command)
                cron.write()

        if job_found:
            print(f"Data collection end time successfully updated to: {end_time}")
        else:
            print(f"Error setting data collection end time. Please check address and try again.")

    def remove_crontab_job(self):
        print("Removing scheduled data collection")
        cron = CronTab(user=True)
        for job in cron:
            # Add the 'run_data_collection' before the address to avoid the one-in-a-million chance that the address string is found in something like a filepath for a different sensor
            if f"run_data_collection {self.address}" in job.command:
                cron.remove(job)
        cron.write()

    #
    # CSV MANAGEMENT 
    #
    def write_to_csv(self, timestamp, live_data):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        file_exists = os.path.isfile(self.filename)

        if not file_exists:
            self.create_csv()

        with open(self.filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            datetime = self.convert_timestamp_dattime(timestamp)
            truncated_values = [datetime] + [self.truncate_float(value, self.precision) for value in live_data]
            writer.writerow(truncated_values)
    
    def create_csv(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        file_exists = os.path.isfile(self.filename)

        if file_exists:
            overwrite = input(f"\nThe file '{self.filename}' already exists. Do you want to overwrite it? [Y/N]: ")
            if overwrite.lower() != 'y':
                print("File not overwritten. Exiting function.")
                exit(1)
            else:
                print("Overwriting file")
            
        with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            labels_with_units = ["Timestamp"] + [self.format_label_with_units(label) for label in self.sensor.live_data_labels]
            writer.writerow(labels_with_units)

    #
    # HELPERS
    #        
    def format_label_with_units(self, label):
        if label in liveDataTypes:
            units = liveDataTypes[label]["units"]
            return f"{label} ({units})"
        else:
            return label
    
    def truncate_float(self, value, precision=2):
        return f"{value:.{precision}f}"
    
    def convert_timestamp_dattime(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%c')


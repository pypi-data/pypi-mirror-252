import time
import pyvisa
import logging
from typing import Literal

RANGE = 'AUTO'


class KeySight34465A:
    """
    ``Base class for the Keysight 34465A DMM``
    """
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.dmm = None
        self.resource_manager = None

    def open_connection(self):
        """
        ``Opens a TCP/IP connection to connect to the Keysight DMM 34465A`` \n
        """
        self.resource_manager = pyvisa.ResourceManager()
        try:
            logging.info(f": Opening KeysightDMM 34465A Resource at {self.connection_string}")
            self.dmm = self.resource_manager.open_resource(self.connection_string)
            self.dmm.read_termination = '\n'
            self.dmm.write_termination = '\n'
            time.sleep(3)
        except Exception as err:
            raise Exception(f": ERROR {err}: Could not open connection! ")

    def close_connection(self):
        """
        ``Closes the TCP/IP connection to the Keysight DMM 34465A`` \n
        """
        self.resource_manager.close()

    def self_test(self):
        """
        ``Performs the self-test and checks for system errors`` \n
        :return: `bool` : True or Error
        """
        sys_err = self.dmm.query(f'SYST:ERR?', delay=1)
        if sys_err == '+0,"No error"':
            try:
                selftest = self.dmm.query(f'TEST:ALL?', delay=1)
                if selftest == "+0":
                    logging.info("PASS: SELF-TEST PASSED!")
                    return True
                else:
                    logging.error(f"Self-test FAILED")
                    return False
            except Exception as e:
                raise Exception(f": ERROR: {e} One or more self-test has FAILED")
        else:
            logging.error(f": SYSTEM_ERROR: {sys_err}")
            raise Exception(f": {sys_err}")

    def id_number(self):
        """
        ``This function returns the ID number on query in string`` \n
        :return: `str` : ID number
        """
        time.sleep(5)
        idn = self.dmm.query(f'*IDN?', delay=1)
        logging.info(f": IDN: {idn} \n")
        return str(idn)

    def reset(self):
        """
        ``This function resets the system for remote operation `` \n
        """
        self.dmm.write("*RST")

    def system_version(self):
        """
        ``This function gets System Version for the Keysight DMM 34465A`` \n
        :return: `str`: System Version
        """
        sys_ver = self.dmm.query(f'SYST:VERS?', delay=1)
        logging.info(f": System Version: {sys_ver}")
        return str(sys_ver)

    def dhcp(self):
        """
        ``This function gets DHCP for the Keysight DMM 34465A`` \n
        :return: `str`: DHCP Setting
        """
        is_dhcp = self.dmm.query(f'SYST:COMM:LAN:DHCP?', delay=1)
        logging.info(f": DHCP Setting: {is_dhcp} \n")
        return str(is_dhcp)

    def ip_address(self):
        """
        ``This function gets IP Address for the Keysight DMM 34465A`` \n
        :return: `str`: IP Address
        """
        ip_address = self.dmm.query(f'SYST:COMM:LAN:IPAD?', delay=1)
        logging.info(f": IP Address: {ip_address} \n")
        return str(ip_address)

    def mac_address(self):
        """
        ``This function gets MAC address for the Keysight DMM 34465A`` \n
        :return: `str`: MAC Address
        """
        mac_address = self.dmm.query(f'SYST:COMM:LAN:MAC?', delay=1)
        logging.info(f": MAC Address: {mac_address} \n")
        return str(mac_address)

    def hostname(self):
        """
        ``This function gets the Hostname for the Keysight DMM 34465A`` \n
        :return: `str`: Hostname
        """
        host_name = self.dmm.query(f'SYST:COMM:LAN:HOST?', delay=1)
        logging.info(f": DNS Hostname: {host_name} \n")
        return str(host_name)

    def subnet_mask(self):
        """
        ``This function gets Subnet Mask for the Keysight DMM 34465A`` \n
        :return: `str`: Subnet mask
        """
        subnet_mask = self.dmm.query(f'SYST:COMM:LAN:SMASK?', delay=1)
        logging.info(f": Subnet Mask: {subnet_mask} \n")
        return str(subnet_mask)

    def dns(self):
        """
        ``This function gets teh DNS setting for the Keysight DMM 34465A`` \n
        :return: `str`: DNS Setting
        """
        dns_setting = self.dmm.query(f'SYST:COMM:LAN:DNS?', delay=1)
        logging.info(f": DNS Setting: {dns_setting} \n")
        return str(dns_setting)

    def gateway(self):
        """
        ``This function gets the Gateway for the Keysight DMM 34465A`` \n
        :return: `str`: Gateway
        """
        gateway = self.dmm.query(f'SYST:COMM:LAN:GAT?', delay=1)
        logging.info(f": Default Gateway: {gateway} \n")
        return str(gateway)

    def get_current(self, test_mode):
        """
        ``This function reads a current measurement`` \n
        :param test_mode: `str` : AC/DC \n
        :return: `float` : Current in Amps
        """
        current = self.dmm.query(f'MEAS:CURR:{test_mode}?', delay=1)
        logging.info(f": {str(test_mode)} Current: {current} Amps \n")
        return float(current)

    def eel_configure_voltage(self, test_mode: Literal["AC", "DC"] = "DC", ranges: str = "0.1", resolution: str = "0.000001"):
        """
        ``This function sets all the measurement parameters and trigger parameters to their default values with specified
        range and resolution`` \n
        :param: `str` :  test_mode: AC/DC \n
        :param: ranges: {100 mV | 1 V | 10 V | 100 V | 1000 V}. Default: AUTO \n
        :param: resolution: AC: optional and ignored, fixed to 6 1/2 digits; DC default 10 PLC \n
        :return: Success or failure
        """
        self.reset()
        sys_err = self.dmm.query(f'SYST:ERR?')
        if sys_err == '+0,"No error"':
            self.dmm.write(f'CONF:VOLT:{str(test_mode).upper()} {ranges}, {float(resolution)}')
            self.dmm.write("TRIG:SOUR IMM")
            self.dmm.write("SAMP:COUN 1")
            self.dmm.write("CALC:SMO:RESP SLOW")
            self.dmm.write("CALC:SMO:STAT ON")
            return True
        else:
            logging.info(f" SYSTEM ERROR: {sys_err}")
            raise Exception(f": ERROR: {sys_err}")

    def eel_null(self, n_aver: int = 10):
        """
        ``Null readings`` \n
        """
        self.dmm.write("VOLT:DC:NULL:STAT ON;VAL 0")
        # Unfortunately the DMM only allows 1000 average samples, so we need more of them
        aver = 0.0
        for i in range(n_aver):
            aver += self.get_average(1000)
        self.dmm.write(f"VOLT:DC:NULL:STAT ON;VAL {(aver / n_aver):.2e}")


    def get_average(self, n_samples: int):
        """
        ``Averaging the DMM output`` \n
        :return: `float` : calculated average
        """
        num_samples = str(min(n_samples, 1000))  # it has to be limited, since DMM only allows 1000 aver samples

        self.dmm.write("SAMP:COUN " + num_samples)
        self.dmm.write("CALC:AVER:STAT ON")
        self.dmm.write("INIT")
        self.dmm.write("*WAI")
        ret = self.dmm.query("CALC:AVER:AVER?")
        self.dmm.write("CALC:AVER:CLE")
        self.dmm.write("CALC:AVER:STAT OFF")
        self.dmm.write("SAMP:COUN 1")

        try:
            return float(ret.strip())
        except ValueError:
            return None

    def get_voltage(self, test_mode):
        """
        ``This function reads a voltage measurement`` \n
        :param test_mode: `str` : AC/DC \n
        :return: `float` : Current in Amps
        """
        voltage = self.dmm.query(f'MEAS:VOLT:{test_mode}?', delay=1)
        logging.info(f": {str(test_mode)} Voltage: {voltage} Volts \n")
        return float(voltage)

    def read_dc_voltage(self):
        """
        ``Function reads DC voltage as previously configured``
        :return: `float` : Voltage in Volts, (9.9E37 if out of range) or None if other measurement error
        """
        ret = self.dmm.query("READ?")

        try:
            return float(ret.strip())
        except ValueError:
            return None

    def fetch_measurement_results(self):
        """
        ``Fetch results from previous measurement series`` \n
        :return: `list` : List of float measurement samples
        """
        ret = self.dmm.query("FETC?")
        ret = ret.strip("\n")
        return [float(x) for x in ret.split(",")]

    def measure_frequency(self):
        """
        ``This function measures frequency of the DMM`` \n
        :return: `str` : Frequency in Hz
        """
        frequency = self.dmm.query(f'MEAS:FREQ?', delay=1)
        logging.info(f": Frequency: {frequency} \n")
        return str(frequency)

    def measure_period(self):
        """
        ``This function measures period of the DMM`` \n
        :return: `str` : Period
        """
        period = self.dmm.query(f'MEAS:PER?', delay=1)
        logging.info(f": Period: {period} \n")
        return str(period)

        # If the input signal is greater than can be measured on the specified manual range, the instrument displays
        # the word Overload on front panel and returns "9.9E37" from the remote interface.

    def measure_diode(self):
        """
        ``This function measures diode of the DMM`` \n
        :return: `str` : Diode value
        """
        diode = self.dmm.query(f'MEAS:DIOD?', delay=1)
        if diode > '+9.8E+37':
            logging.info(f": Check Diode value for Overload of measurement!")
            return ValueError
        else:
            logging.info(f": Diode value: {diode} \n")
            return str(diode)

    def measure_resistance(self):
        """
        ``This function measures resistance of the DMM`` \n
        :return: `str` : Resistance
        """
        resistance = self.dmm.query(f'MEAS:RES?', delay=1)
        if resistance > '+9.80000000E+37':
            logging.info(f": Check Resistance value for Overload of measurement!")
            return ValueError
        else:
            logging.info(f": Resistance value: {resistance} \n")
            return str(resistance)

    def measure_capacitance(self):
        """
        ``This function measures capacitance of the DMM`` \n
        :return: `str` : Capacitance
        """
        capacitance = self.dmm.query(f'MEAS:CAP?', delay=1)
        if capacitance > '+9.80000000E+37':
            logging.info(f": Check Capacitance value for Overload of measurement!")
            return ValueError
        else:
            logging.info(f": Capacitance: {capacitance} \n")
            return str(capacitance)

    # def configure_current(self):
    #     """
    #     ``This function sets all the measurement parameters and trigger parameters to their default values with specified
    #     range and resolution`` \n
    #     :param: `str` : test_mode: AC/DC \n
    #     :param: ranges: {100µA | 1mA | 10mA | 100mA | 1A | 3A | 10A }. Default: AUTO \n
    #     :param: `str` : resolution: AC: optional and ignored, fixed to 6 1/2 digits; DC default 10 PLC \n
    #     :return: `bool` : Success or failure
    #     """
    #     sys_err = self.dmm.query(f'SYST:ERR?')
    #     time.sleep(2)
    #     if sys_err == '+0,"No error"':
    #         time.sleep(2)
    #         self.dmm.write(f'CONF:CURR:DC AUTO')
    #         self.dmm.write(f'TRIG:SOUR EXT;SLOP POS')
    #         self.dmm.write(f'INIT')
    #         time.sleep(3)
    #         curr = self.dmm.query(f'FETC?')
    #
    #         logging.info(f": DC Current: {curr} Amps \n")
    #         return True
    #     else:
    #         logging.info(f" SYSTEM ERROR: {sys_err}")
    #         raise Exception(f": ERROR: {sys_err}")

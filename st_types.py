'''
Class types for ST Nodeserver
'''

import requests, grequests
from st_nodedef import LINKS
from polyglot.nodeserver_api import Node

def myfloat(value, prec=6):
    """ round and return float """
    return round(float(value), prec)

class STControl(Node):

    def __init__(self, *args, **kwargs):
        super(STControl, self).__init__(*args, **kwargs)

    def _discover(self, *args, **kwargs):
        manifest = self.parent.config.get('manifest', {})
        try:
            r = requests.get('http://' + str(self.parent.address) + ':' + str(self.parent.port) + '/api/clients')
            for endpoint in r.json():
                if endpoint['endpoint'].lower()[:7] == 'st-mems':
                    address = endpoint['endpoint'].lower()[-9:]
                    self.logger.info('Found ST Mems IPSO Sensor. Proceeding to check objectLinks.')
                    for objectLink in endpoint['objectLinks']:
                        self.logger.info('ObjectLink Found: ' + objectLink['url'])
                        if objectLink['url'] == '3200/0':
                            naddress = 'di_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(DigitalInput(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Digital Input', objectLink, manifest))
                        elif objectLink['url'] == '3303/0':
                            naddress = 'tp_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(Temperature(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Temperature', objectLink, manifest))
                        elif objectLink['url'] == '3304/0':
                            naddress = 'hu_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(Humidity(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Humidity', objectLink, manifest))
                        elif objectLink['url'] == '3313/0':
                            naddress = 'ac_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(Accelerometer(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Accelerometer', objectLink, manifest))
                        elif objectLink['url'] == '3314/0':
                            naddress = 'ma_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(Magnetometer(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Magnetometer', objectLink, manifest))
                        elif objectLink['url'] == '3315/0':
                            naddress = 'ba_' + address
                            lnode = self.parent.get_node(naddress)
                            if not lnode:
                                self.parent.sensors.append(Barometer(self.parent, self.parent.get_node('stcontrol'), endpoint['endpoint'], naddress, 'IPSO Barometer', objectLink, manifest))
                            
        except (requests.exceptions.ConnectionError, ValueError) as ex:
            self.logger.error('Could not get clients from Leshan Server. {}'.format(ex))
        return True

    def query(self, **kwargs):
        self.parent.report_drivers()
        return True

    _drivers = {}

    _commands = {'DISCOVER': _discover}

    node_def_id = 'stcontrol'

class DigitalInput(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(DigitalInput, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3', 'GV4', 'GV5')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True

    _drivers = {'GV1': [0, 2, int], 'GV2': [0, 56, int],
                            'GV3': [0, 2, int], 'GV4': [0, 56, int],
                            'GV5': [0, 56, int]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsodi'

class Temperature(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(Temperature, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True

    _drivers = {'GV1': [0, 4, myfloat], 'GV2': [0, 4, myfloat],
                            'GV3': [0, 4, myfloat]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsotemp'

class Humidity(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(Humidity, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True
        
    _drivers = {'GV1': [0, 22, myfloat], 'GV2': [0, 22, myfloat],
                            'GV3': [0, 22, myfloat]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsohum'

class Accelerometer(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(Accelerometer, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3', 'GV4', 'GV5')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True
        
    _drivers = {'GV1': [0, 56, myfloat], 'GV2': [0, 56, myfloat],
                            'GV3': [0, 56, myfloat], 'GV4': [0, 56, myfloat], 'GV5': [0, 56, myfloat]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsoacel'
    
class Magnetometer(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(Magnetometer, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True
        
    _drivers = {'GV1': [0, 56, myfloat], 'GV2': [0, 56, myfloat],
                            'GV3': [0, 56, myfloat]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsomagn'

class Barometer(Node):
    def __init__(self, parent, primary, endpoint, address, name, object, manifest=None):
        self.endpoint = endpoint
        self.parent = parent
        self.address = address
        self.name = name
        self.object = object
        self.links = LINKS[int(self.object['url'].split('/')[0])]
        self.num_links = len(self.links)
        self.values = [None]*self.num_links
        super(Barometer, self).__init__(parent, address, self.name, primary, manifest)
        self.query()

    def update_info(self):
        for index, link in enumerate(self.links):
            self.values[index] = getValue(self.parent.address, self.parent.port, self.endpoint, self.object['url'], link)
        for index, driver in enumerate(('GV1', 'GV2', 'GV3')):
            try:
                self.set_driver(driver, self.values[index])
            except TypeError: pass
        return True

    def query(self, **kwargs):
        self.update_info()
        self.report_driver()
        return True
        
    _drivers = {'GV1': [0, 56, myfloat], 'GV2': [0, 56, myfloat],
                            'GV3': [0, 56, myfloat]}

    _commands = { 'QUERY': query }

    node_def_id = 'ipsobaro'
    
def getValue(address, port, endpoint, prefix, link):
    value = None
    try:
        r = requests.get('http://' + str(address) + ':' + str(port) + '/api/clients/' + endpoint + '/' + prefix + '/' + str(link))
        value = r.json()['content']['value']
    except (requests.exceptions.ConnectionError, ValueError) as ex:
        pass
    return value if not None else False
    
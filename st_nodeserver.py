#!/usr/bin/python
''' 
ST Micro Node Server for Polyglot
by Einstein.42(James Milne)
milne.james@gmail.com
'''

import sys
from polyglot.nodeserver_api import SimpleNodeServer, PolyglotConnector
from st_types import STControl
      
VERSION = "0.0.1"

class STNodeServer(SimpleNodeServer):
    ''' ST Micro Node Server '''
    sensors = []
    
    def setup(self):
        self.logger = self.poly.logger
        self.logger.info('Config File param: %s', self.poly.configfile)
        try:
            self.address = self.poly.nodeserver_config['server']['address']
            self.port = self.poly.nodeserver_config['server']['port']
        except (KeyError, ValueError) as ex:
            self.logger.error('Could not find address or port value in config file. Exiting...')
            sys.exit()
        self.logger.info('Using Leshan Server: {} Port: {}'.format(self.address, self.port))
        manifest = self.config.get('manifest', {})
        self.controller = STControl(self, 'stcontrol', 'ST Control', True, manifest)
        self.controller._discover()
        self.update_config()

    def poll(self):
        if len(self.sensors) >= 1:
            for i in self.sensors:
                i.update_info()
        
    def long_poll(self):
        pass
        
    def report_drivers(self):
        if len(self.sensors) >= 1:
            for i in self.sensors:
                i.report_driver()


def main():
    # Setup connection, node server, and nodes
    poly = PolyglotConnector()
    # Override shortpoll and longpoll timers to 5/30, once per second is unnessesary
    nserver = STNodeServer(poly, 30, 60)
    poly.connect()
    poly.wait_for_config()
    poly.logger.info("ST NodeServer Interface version " + VERSION + " created. Initiating setup.")
    nserver.setup()
    poly.logger.info("Setup completed. Running Server.")
    nserver.run()

if __name__ == "__main__":
    main()
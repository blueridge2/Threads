
import random
import threading
import time


class GpsLockLocation(object):
    """
    A class to contain common data for the lock class and locatin
    """
    def __init__(self):
        """
        The init class for the lock and location
        """
        self._lock = threading.Lock()
        self.gps_location = None

    @property
    def gps_location(self):
        """
        a function to lock the location, read it unlock the data and return with the location
        :return a string with the gps location
        """
        print('called get location')
        self._lock.acquire()
        location = self.__gps_location
        self._lock.release()
        return location

    @gps_location.setter
    def gps_location(self, location):
        """
        a function to set the gps locattion
        :param location: the gps location
        :return: None
        """
        print("called set location")
        self._lock.acquire()
        self.__gps_location = location
        self._lock.release()
        print('ended gps location')

gps_lock_location = GpsLockLocation()

class RadioThread(threading.Thread):
    def __init__(self, name, *args, **kwargs):
        """
        this is the init class for the thread
        :param name: The name of the thread
        :param args: The args, it must be a tupple consistin go the lock variable, the shared data, shold be a string
        :param kwargs: Not used
        """
        super(RadioThread, self).__init__(name=name, args=args, kwargs=kwargs)
        self.name = name
        self.kwargs = kwargs
        self.args = args
        print('args={}'.format(args))
        if args is None:
            raise ValueError()
        self.lock_location_class = args[0]

    def run(self):
        while True:
            self.lock_location_class.gps_location = (str(random.randint(0, 1999)) + str(random.randint(5000,10000)))
            print('A location={}'.format(self.lock_location_class.gps_location))
            time.sleep(1)

class BluetoothThread(threading.Thread):
    """
    this is a thread class for the bluetooth radio

    """
    def __init__(self, name, *args, **kwargs):
        """
        this is the init class for the thread
        :param name: The name of the thread
        :param args: The args, it must be a tupple consistin go the lock variable, the shared data, shold be a string
        :param kwargs: Noe used
        """
        super(BluetoothThread, self).__init__(name=name, args=args, kwargs=kwargs)

        if args is None:
            raise ValueError('Args cannot be None')

        if args is None:
            raise ValueError()
        self.lock_location_class = args[0]
        self.name = name


    def run(self):
        """
        This overrides run on the threading class
        :return:
        """
        while True:
            print('B location = {}'.format(self.lock_location_class.gps_location))
            time.sleep(1)


a = RadioThread("Radio Thread", gps_lock_location,  )
b = BluetoothThread("Bluetooth Thread", gps_lock_location)

b.start()
a.start()

a.join()
b.join()
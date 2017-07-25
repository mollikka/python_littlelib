from time import localtime

class Logger:

    def __init__(self, filename):
        self.logfile = open(filename, "w+")

    def __call__(self, eventstring, identifier):
        t = localtime()
        timestr = "{}-{}-{} {}:{}:{}".format(
                            t.tm_year, t.tm_mon, t.tm_mday,
                            t.tm_hour, t.tm_min, t.tm_sec)
        self.logfile.write("{} {} {}\n".format(timestr,eventstring,identifier))
        self.logfile.flush()


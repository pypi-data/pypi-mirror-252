"""MINimal MONitor - write and graph: date, time, memory, CPU, temperature, disk i/o and net i/o

MINMON  writes  on  standard  output  at  fixed time intervals a line built
according to the characters in -f --format argument:

    • 'y': Date as 'YYYY-mm-dd'
    • 'h': Time as 'HH:MM:SS'
    • 'm':  Memory  and  Swap  %  usage as two 2-characters decimal numbers
      ('**' = 100)
    • 'M':  Memory  and  Swap  % usage as a 21-characters '0-50-100' linear
      graph ('M' = Memory, 'S' = Swap, 'X' = both)
    • 'c':   CPU  %  usage  and  Temperature  °C  (Celsius  degrees)as  two
      2-characters decimal numbers ('**' = 100)
    • 'C':  CPU  %  usage  and Temperature °C as a 21-characters '0-50-100'
      linear graph ('C' = CPU, 'T' = temperature, 'X' = both)
    • 'r': disk Read and Write B/s (bytes per second) as two human-readable
      5-characters  numbers  ('K' = 2 ** 10 = 1024, 'M' = 2 ** 20 = 1024 **
      2, 'G' = 2 ** 30 = 1024 ** 3, 'T' = 2 ** 40 = 1024 ** 4)
    • 'R':  disk  Read  and Write B/s (bytes per second) as a 19-characters
      '1-K-M-G' logarithmic graph ('R' = Read, 'W' = write, 'X' = both)
    • 'd':  network  Download  and  Upload in B/s (bytes per second) as two
      human-readable 5-characters numbers
    • 'D':  network  Download  and  Upload  in  B/s (bytes per second) as a
      19-characters  '1-K-M-G'  logarithmic  graph  ('D'  = Download, 'U' =
      Upload, 'X' = both)

MINMON is minimal as it has a minimal RAM (6 MB) and CPU footprint.

To stop the program press Ctrl-C.

"""

__version__ = "0.9.9"

__requires__ = ["psutil"]

def int2human(num, length=5):
    if not isinstance(num, int):
        raise TypeError(f'int2human: num {num!r} is not an integer')
    if not isinstance(length, int):
        raise TypeError(f'int2human: length {length!r} is not an integer')
    min_length = 6 if num < 0 else 5
    if not (min_length <= length <= 15):
        raise ValueError(f'int2human: length {length} is not between {min_length} and 15')
    if abs(num) < 1024:
        return f'{num:{length}}'
    else:
        for char in 'KMGTPEZY':
            num /= 1024
            if abs(num) < 1024 or char == 'Y':
                buf = str(num)
                if buf.endswith('.0'):
                    buf = buf[:-2]
                buf = buf[:length-1]
                if buf.endswith('.'):
                    buf = ' ' + buf[:-1]
                return buf.rjust(length-1)[:length-1] + char
                
def human2int(hum):
    if not isinstance(hum, str):
        raise TypeError(f'int2human: {hum!r} is not a string')
    try:
        return int(hum)
    except ValueError:
        try:
            buf = hum.strip()
            return round(float(buf[:-1]) * 1024 ** ('KMGTPEZY'.index(buf[-1].upper()) + 1))
        except ValueError:
            raise ValueError(f'human2int: string {hum!r} is not a correct human literal')

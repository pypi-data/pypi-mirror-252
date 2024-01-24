```
usage: minmon [-h] [-V] [-s SECONDS] [-f FORMAT] [-t]

MINimal MONitor - write and graph: date, time, memory, CPU, temperature, disk i/o and net i/o

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

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -s SECONDS, --seconds SECONDS
                        interval in seconds as an integer greater than 0
                        (default: '1')
  -f FORMAT, --format FORMAT
                        output format (default: 'yhmMcCrRdD')
  -t, --tera-byte       extended 25-characters '1-K-M-G-T' logarithmic scale
                        (default: 19-characters '1-K-M-G')
```

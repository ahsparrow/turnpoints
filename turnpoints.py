import argparse
import csv
import sys

def parse_latlon(str):
    if str[-1] in "NS":
        deg = int(str[:2])
        min = float(str[2:-1])
        sign = 1 if str[-1] == "N" else -1
    else:
        deg = int(str[:3])
        min = float(str[3:-1])
        sign = 1 if str[-1] == "E" else -1

    return sign * (deg + min / 60)

def turnpoints(reader):
    out = []
    for tp in reader:
        name, code, cat, point, elev, lat_lon, freq = tp

        if "!" in cat:
            # Non-competition TP
            continue

        if int(lat_lon[:2]) >= 54:
            # Too far North
            continue

        lat = "".join(lat_lon.split(" ")[:2])
        lon = "".join(lat_lon.split(" ")[2:])

        out.append([name, code, "UK", lat, lon, elev, "1", "", "", "", point])

    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", nargs="?",
                         help="CSV turnpoint file",
                         type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("out_file", nargs="?",
                         help="CUP output file",
                         type=argparse.FileType("wt"), default=sys.stdout)

    args = parser.parse_args()

    reader = csv.reader(args.in_file)
    tps = turnpoints(reader)

    writer = csv.writer(args.out_file)
    writer.writerow(["name","code","country","lat","lon","elev","style","rwydir","rwylen","freq","desc"])
    for tp in tps:
        writer.writerow(tp)

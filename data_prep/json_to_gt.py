import os
import glob
import argparse
import json
from math import cos, sin, pi

# Usage: python xml_to_gt.py in_dir out_dir


def rotate_rect(xmin, ymin, xmax, ymax, theta):
    theta = theta * pi / 180

    w = xmax - xmin
    h = ymax - ymin

    yc = ymin + h/2
    xc = xmin + w/2

    xmax_rot = cos(theta) * (xmax-xc) - sin(theta) * (ymax-yc) + xc
    xmin_rot = cos(theta) * (xmin-xc) - sin(theta) * (ymin-yc) + xc
    ymax_rot = sin(theta) * (xmax-xc) + cos(theta) * (ymax-yc) + yc
    ymin_rot = sin(theta) * (xmin-xc) + cos(theta) * (ymin-yc) + yc

    return int(xmin_rot), int(ymin_rot), int(xmax_rot), int(ymax_rot)


def pts_to_box(pts):
    """In the form [x0, y0, x1, y1, x2, y2, x3, y3]"""

    x0, y0 = pts[0][0], pts[0][1]
    x1, y1 = pts[1][0], pts[1][1]
    x2, y2 = pts[2][0], pts[2][1]
    x3, y3 = pts[3][0], pts[3][1]

    l = [x0, y0, x1, y1, x2, y2, x3, y3]
    l = [int(x) for x in l]
    return l


def json_to_txt(json_dir, output_dir, rotation=0):

    for json_file in glob.glob(os.path.join(json_dir, '*.json')):
        with open(json_file, 'r') as f:
            d = json.load(f)
        filename = json_file.split("/")[-1]
        filename = filename.replace(".json", "")
        filename = 'gt_' + filename + '.txt'
        text = "TEXT"
        lines = []
        for shape in d.get('shapes', []):
            points = shape['points']
            pts = pts_to_box(points)
            line = ""
            for pt in pts:
                line += str(pt) + ","
            line += text
            lines.append(line)

        for i in range(len(lines) - 1):
            lines[i] += "\n"

        with open(os.path.join(output_dir, filename), 'w') as outfile:
            outfile.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = 'Reads all json files, generated by labelme, from a directory and generates IDCAR compliant gt_*.txt files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'input',
        metavar='input',
        type=str,
        help=
        'Directory containing the json files generated by labelme'
    )
    parser.add_argument('output',
                        metavar='output',
                        type=str,
                        help='Path where the output folder is.')

    args = parser.parse_args()

    json_to_txt(args.input, args.output)
from tempfile import TemporaryDirectory
import re
from datetime import datetime
import cv2
import pytesseract as ocr
import io

import whatimage
import pyheif
from PIL import Image

from API.core.receiptControl.imageUploading import upload_image_to_drive


def format_ocr_data(lines):
    tin = lines[0].split(" ")[-1]
    tin = tin.replace("H", '4')
    tin = tin.replace("S", "5")
    tin = tin.replace("G", "6")
    lines.pop(0)

    business_place = ""
    for line in lines:
        business_place += line
        if line.startswith("TEL"):
            business_place += line
            break
        business_place += " "

    fs = ""
    date = ""
    time = ""
    date_found = False
    row = 0
    for line in lines:
        row += 1
        if "FS No." in line or "PS No." in line or "FS Ho." in line or "PS Ho." in line:
            fs += line.split(" ")[2]
            if "Date:" in line:
                x = line.split(" ")
                index = x.index("Date:")
                date = x[index + 1]
                time = x[index + 2]
                date_found = False
                pass
            break

    if not date_found:
        date_row = lines[row].split(" ")
    date_string = date_row[0].split("/")
    year = date_string[2]
    if int(date_string[0]) <= 30:
        day = date_string[0]
    else:
        day = date_string[0][1:]
    if int(date_string[1]) <= 12:
        month = date_string[1]
    else:
        month = date_string[1][1:]
    date = day + "/" + month + "/" + year

    if len(date_row[1]) == 5:
        time = date_row[1][:2] + ":" + date_row[1][3:5]

    total = ""
    for line in lines:
        if "TOTAL" in line or "TDTAL" in line:
            total_row = line.split(" ")
            for i in total_row:
                if "*" in i:
                    index_total = total_row.index(i)
            total += " ".join(line.split(" ")[index_total:])[1:].replace(" ", ".")
    date_time = date + " " + time
    items = []
    items_found = False
    items_row = 0
    for line in lines:
        if "Description" in line:
            items_row = lines.index(line) + 1
            items_found = True
    if items_found:
        if "----" in lines[items_row] \
                or "===" in lines[items_row] \
                or "___" in lines[items_row] or "..." in lines[items_row]:
            items_row += 1

        for line in lines[items_row:]:
            if re.search('[a-zA-Z]', line):
                # item = line.split(" ")[0]
                # price = line.split(" ")[1]

                items.append([line.split(" ")[0], line.split(" ")[-1]])
            if "TXBLI" in line:
                break
    else:
        for line in lines[row - 1:]:
            line_row = line.split(" ")
            if len(line_row) > 2:
                if re.search('[a-zA-Z]', line_row[0]) and re.search('[0-9]', line_row[-1]):
                    items.append([" ".join(line_row[:-1]), 1, line_row[-1][1:]])
            if "TXBLI" in line:
                break

    register = ""
    register_found = False
    for line in lines:
        if "ERCA" in line:
            index_re = lines.index(line)
            register = lines[index_re].split(" ")[-1]
            register_found = True
            break
    if row != 0:
        for line in lines[row:]:
            for i in line.split(" "):
                if re.search("[a-zA-Z]{3}$[0-9]", line):
                    register = i
                    register_found = True
    if not register_found:
        register = "000000000"

    items_data = []
    for item in items:
        x = {
            "name": item[0],
            "quantity": float(item[1]),
            "item_price": float(item[2])
        }
        items_data.append(x)
    data = {
        "tin_number": tin,
        "fs_number": fs,
        "issued_date": datetime.strptime(date_time, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S"),
        "business_place_name": business_place,
        "register_id": register,
        "total_price": float(total),
        "Items": items_data

    }

    return data


def scanner(file, filename, mimetype):
    with TemporaryDirectory(prefix='image') as tempdir:
        fmt = whatimage.identify_image(file)
        if fmt in ['heic', 'avif']:
            i = pyheif.read(file)

            # Convert to other file format like jpeg
            s = io.BytesIO()
            pi = Image.frombytes(
                mode=i.mode, size=i.size, data=i.data)

            pi.save(s, format="jpeg")
            image = cv2.imread(pi)
        else:
            image = cv2.imread(file)

        custom_config = r'-l  font0 font1 font2 font3 --oem 3 --psm 4'
        text = ocr.image_to_string(image, config=custom_config)

        with open(tempdir + "/data.txt", 'w') as f:
            f.write(str(text))

        lines = []
        with open(tempdir + "/data.txt") as file:
            for line in file:
                lines.append(line.rstrip())

        return format_ocr_data(lines)

import cv2
import numpy as np
import pytesseract
import os
import natsort
import sqlite3


conn = sqlite3.connect("LCT.db")
cursor = conn.cursor()


def delete_images(*directories):
    for directory in directories:
        files = os.listdir(directory)
        for file in files:
            os.remove(directory + str(file))


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    return (cnts, boundingBoxes)


def find_kernel_length(basic_image):
    img = cv2.imread(basic_image, 0)
    (thresh, img_bin) = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin
    kernel_length = np.array(img).shape[1] // 95
    return img_bin, kernel_length


def verticle_lines(image_bin, length_of_kernel):
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length_of_kernel))
    img_temp1 = cv2.erode(image_bin, verticle_kernel, iterations=2)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=2)
    cv2.imwrite('lines/vertical_lines.png', verticle_lines_img)


def horizontally_lines(image_bin, length_of_kernel):
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length_of_kernel, 1))
    img_temp2 = cv2.erode(image_bin, hori_kernel, iterations=2)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
    cv2.imwrite('lines/horizontal_lines.png', horizontal_lines_img)


def merge_lines():
    alpha = 0.5
    beta = 1.0 - alpha
    img1 = cv2.imread('lines/vertical_lines.png')
    img2 = cv2.imread('lines/horizontal_lines.png')
    img_cv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img_cv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img_final_bin = cv2.addWeighted(img_cv1, alpha, img_cv2, beta, 0.0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite('lines/all_lines.png', img_final_bin)
    return img_final_bin


def find_need_cells(basic_image, img_final_bin):
    # img_final_bin = cv2.imread('lines/all_lines.png')
    img = cv2.imread(basic_image)
    im2, contours, hierarchy = cv2.findContours(
        img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0
    coordinates = []
    arr_location = []
    arr_coordinates = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        coordinates.append(w)
        arr_coordinates.append([x, y, w, h])
        arr_location.append(x+y+x + w+y + h)
    for i in range(len(arr_location)):
        try:
            if arr_location[i] - 6 < arr_location[i + 1] < arr_location[i] + 6:
                pass
            else:
                if sorted(coordinates)[-3]-15< arr_coordinates[i][2] <=sorted(coordinates)[-3] and arr_coordinates[i][3] > 13:
                    new_img = img[arr_coordinates[i][1]:arr_coordinates[i][1] + arr_coordinates[i][3],
                              arr_coordinates[i][0]:arr_coordinates[i][0] + arr_coordinates[i][2]]

                    if idx == 5:
                        break
                    else:
                        cv2.imwrite('resize_cells/'+str(idx) + '.jpg', new_img)
                        idx += 1
        except IndexError:
            pass

def extract_text():
    resize_cells_directory = 'resize_cells/'
    arr_text = []
    for image_cell in natsort.natsorted(os.listdir(resize_cells_directory)):
        image_cell = cv2.imread(resize_cells_directory+image_cell)
        text = pytesseract.image_to_string(image_cell, lang='rus')

        if text.strip() == '':
            x, y, _ = image_cell.shape
            image_cell = cv2.resize(image_cell, (y * 2, x * 2))
            text = pytesseract.image_to_string(image_cell, lang='rus')
            arr_text.append(text.strip().replace('\n', ' '))

        else:
            arr_text.append(text.strip().replace('\n', ' '))

    return arr_text


def find_number(basic_image):
    img = cv2.imread(basic_image)
    y, x, _ = img.shape
    arr_text = []
    res_img = img[0:int(y/3.5), 0:int(x/1.5)]
    text = pytesseract.image_to_string(res_img, lang='rus', config='--psm 6')
    arr_text.append(text.strip())
    res = arr_text[0].split(' ')
    try:
        number = ' '.join(res[res.index('№') + 1:])
        return number.split('\n')[0]
    except ValueError:
        try:
            number = ' '.join(res[res.index('№:') + 1:])
            return number.split('\n')[0]
        except ValueError:
            number = ''
            return number


def add_in_bd(registration_number, path_to_image, need_attributes):
    try:
        cursor.execute("INSERT INTO class1 (number, imagepath,"
                   "district, region, address , objectname, "
                   "objectpurpose) VALUES (?,?,?,?,?,?,?)",
                       (registration_number, path_to_image, need_attributes[0], need_attributes[1], need_attributes[2],
                        need_attributes[3], need_attributes[4]))
        conn.commit()
    except IndexError:
        print("Данный документ не удалось распознать: "+str(path_to_image))



main_directory = '/home/wb_08/PycharmProjects/hakaton/documents/dataset_img/class_1/'


for img in os.listdir(main_directory):
    delete_images('resize_cells/', 'lines/')
    main_image = main_directory + img
    img_bin, kernel_length = find_kernel_length(main_image)
    verticle_lines(img_bin, kernel_length)
    horizontally_lines(img_bin, kernel_length)
    erode_final_image = merge_lines()
    find_need_cells(main_image, erode_final_image)
    need_attributes = extract_text()
    registration_number = find_number(main_image)
    add_in_bd(registration_number, 'documents/dataset_img/class_1/'+ img, need_attributes)

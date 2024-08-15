import os
import cv2
import csv
import math
import numpy as np
import tifffile
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PyQt5.QtWidgets import QMessageBox
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import warnings
warnings.filterwarnings('ignore')


def bw_correction(image, rectangle, color):
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    if color == 'black':
        image = 255 - image
        
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

        image_patch = image[x0:x1, y0:y1]
    else:
        image_patch = image
    image_max = (image*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)
    image_max = np.asarray(image_max*255).astype('uint8')
    
    if color == 'black':
        image_max = 255 - image_max

    return image_max


def rgb_correction(image, rectangle, color):
    if color == 'red':
        index = 0
    elif color == 'green':
        index = 1
    elif color == 'blue':
        index = 2
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

        image_patch = image[x0:x1, y0:y1, index]
    else:
        image_patch = image[:,:,index]
    image_max = (image[:,:,index]*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)

    im_res = np.zeros(image.shape, dtype=np.uint8)
    for i in range(3):
        if i == index:
            im_res[:,:,i] = np.asarray(image_max*255).astype('uint8')
        else:
            im_res[:,:,i] = image[:,:,i]
    return im_res


def cmy_correction(image, rectangle, color):
    if color == 'yellow':
        indexes = [0, 1]
    elif color == 'magenta':
        indexes = [0, 2]
    elif color == 'cyan':
        indexes = [1, 2]
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    
    if rectangle != None:
        rectangle = rectangle.data
        x0 = int(rectangle[0][0][0])
        y0 = int(rectangle[0][0][1])
        x1 = int(rectangle[0][2][0])
        y1 = int(rectangle[0][2][1])

    im_res = np.zeros(image.shape, dtype=np.uint8)
    for index in indexes:
        image_copy = image.copy()
        if rectangle != None:
            image_patch = image[x0:x1, y0:y1, index]
        else:
            image_patch = image[:,:,index]
        image_max = (image_copy[:,:,index]*1.0 / image_patch.max(axis=(0, 1))).clip(0, 1)
        
        for i in range(3):
            if i == index:
                im_res[:,:,i] = np.asarray(image_max*255).astype('uint8')
    
    for i in range(3):
        if i not in indexes:
            im_res[:,:,i] = image[:,:,i]
        
    return im_res

################################################################

def set_cm_scale(line):
    d = math.dist(line[0][0],line[0][1])
    # Message pop-up when analysis is finished
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Information)
    msg.setText("Scale saved!")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_() 
    return d

################################################################

def color_analysis(image, mask_init, output_path, image_name, scale):
    support_dir = os.path.join(output_path, 'support_images')
    if not os.path.exists(support_dir):
        os.mkdir(support_dir)

    # Read the image and the mask correctly and find contour
    if np.max(image) <= 1:
        image = np.asarray(image*255).astype('uint8')
    mask_init = mask_init.astype('uint8')

    # Keep only the bigger contour found
    cnts, _ = cv2.findContours(mask_init, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cnts, key=cv2.contourArea)
    out = np.zeros(mask_init.shape, np.uint8)
    mask = cv2.drawContours(out, [cnt], -1, 255, cv2.FILLED)
    masktosave = cv2.drawContours(out, [cnt], -1, 255, cv2.FILLED)
    # Save support-composite image
    composite = np.zeros((2, image.shape[0], image.shape[1], image.shape[2]), dtype=np.uint8)
    composite[0] = image
    composite[1,:,:,0] = masktosave
    composite[1,:,:,1] = masktosave
    composite[1,:,:,2] = masktosave
    tifffile.imwrite(os.path.join(support_dir, image_name+'.tif'), composite, imagej=True)

    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)

    # Mask the image with the mask
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)

    # Find lenght of the fish if the scale was set
    fish_len_px, masked_image, rotated_mask = measure_fish(cnt, masked_image, mask)
    if scale:
        fish_len_cm = fish_len_px/scale # scale = pixels per cm
    else:
        fish_len_cm = None

    # Crop the image around the fish mask
    masked_cropped = masked_image[y:y+h,x:x+w]
    
    # Color analysis which autom^nomsly save figures
    n_black_outofmask = (mask[y:y+h,x:x+w].shape[0]*mask[y:y+h,x:x+w].shape[1]) - np.count_nonzero(mask[y:y+h,x:x+w])
    try: colors_plot(masked_cropped, output_path, image_name, n_black_outofmask)
    except: pass
    try: colors_distribution_pie(masked_cropped, rotated_mask[y:y+h,x:x+w], output_path, image_name, n_black_outofmask, fish_len_px, fish_len_cm)
    except: pass

    # Message pop-up when analysis is finished
    msg = QMessageBox() 
    msg.setIcon(QMessageBox.Information)
    msg.setText("Analysis saved!")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_() 


def measure_fish(contour, masked_image, mask):
    hh, ww = masked_image.shape[:2]
    rotrect = cv2.minAreaRect(contour)
    (center), (width,height), angle = rotrect
    # Draw over the imagr the rectangle
    #box = cv2.boxPoints(rotrect)
    #boxpts = np.int0(box)
    #cv2.drawContours(masked_image,[boxpts],0,(255,0,255),10)
    if angle < -45:
        angle = -angle
    # otherwise, check width vs height
    else:
        if width > height:
            angle = -angle
        
        else:
            angle = -(90 + angle)
            
    # Get rotation matrix
    M = cv2.getRotationMatrix2D(center, -angle, scale=1.0)

    # Rotate image
    #masked_image = cv2.warpAffine(masked_image, M, (ww, hh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #mask = cv2.warpAffine(mask, M, (ww, hh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return np.max([width,height]), masked_image, mask


def colors_plot(masked_cropped, output_path, image_name, n_black_outofmask):
    def find_minimum_color(colors):
        # Function to calculate the sum of RGB components
        def rgb_sum(color):
            return sum(color)

        # Use the min function with a key parameter to find the color with the smallest sum of components
        min_color = min(colors, key=rgb_sum)
        return min_color
    
    # Preprocess the image
    masked_cropped = masked_cropped.reshape((masked_cropped.shape[0] * masked_cropped.shape[1], 3))
    # Apply K-means clustering
    num_colors = 5  # Number of colors to extract
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(masked_cropped)

    # Get the colors
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Create a histogram of the color labels
    label_counts = np.bincount(labels)
    
    # Sort colors by frequency
    sorted_indices = np.argsort(label_counts)[::-1]
    colors = colors[sorted_indices]
    label_counts = label_counts[sorted_indices]
    
    # Create a figure
    plt.figure(figsize=(8, 6))
    
    # Plot each color as a bar
    black = find_minimum_color(colors)
    tosave_colors = []
    for i, color in enumerate(colors):
        tosave_colors.append([int(c) for c in color])
        color = [abs(c) for c in color]
        if np.sum(color) == np.sum(black):
            plt.barh(i, label_counts[i]-n_black_outofmask, color=np.array(color)/255, edgecolor='black')
        else:
            plt.barh(i, label_counts[i], color=np.array(color)/255, edgecolor='black')
    
    
    plt.xlabel('Pixel Count')
    plt.ylabel('Color')
    plt.title('Colors in Image')
    plt.yticks(np.arange(0, num_colors), tosave_colors)
    plt.savefig(os.path.join(output_path, image_name+'_colors_plot'), bbox_inches='tight', dpi=200)
    plt.close()


def colors_distribution_pie(masked_image, cropped_mask, output_path, image_name, n_black_outofmask, fish_len_px, fish_len_cm):
    def classify_color(pixel):
        # Define thresholds for black, white, and orange in RGB
        black_threshold = 100
        white_threshold = 200
        white_lower = np.array([0, 100, 200]) # which is almost blue becuase most of the time the background is light blue
        orange_lower = np.array([100, 40, 0])
        orange_upper = np.array([255, 230, 65])
        
        if np.all(pixel <= black_threshold):
            return 'black'
        elif np.all(pixel >= white_threshold):
            return 'white'
        elif np.all(pixel >= orange_lower) and np.all(pixel <= orange_upper):
            return 'orange'
        else:
            if np.all(pixel >= white_lower):
                return 'white'
            return 'black'

    # Classify each pixel in the image
    black_count = 0
    white_count = 0
    orange_count = 0

    masked_image_copy = masked_image.copy()
    res_image = masked_image.copy()

    for x in range(masked_image_copy.shape[1]):
        for y in range(masked_image_copy.shape[0]):
            pixel = masked_image_copy[y,x,:]
            color_class = classify_color(pixel)
            if color_class == 'black':
                res_image[y,x,:] = (0,0,0)
                black_count += 1
            elif color_class == 'white':
                res_image[y,x,:] = (255,255,255)
                white_count += 1
            elif color_class == 'orange':
                res_image[y,x,:] = (255,140,0)
                orange_count += 1
            elif color_class == 'other':
                res_image[y,x,:] = (0,140,255)
                orange_count += 1
    
    n_black = black_count-n_black_outofmask
    tot_px = n_black + white_count + orange_count
    if ('colors.csv' in os.listdir(output_path)):
        with open(os.path.join(output_path, 'colors.csv'), "a") as file:
            writer = csv.writer(file)
            writer.writerow([image_name, n_black, white_count, orange_count, round((n_black)/tot_px, 2)*100, round((white_count)/tot_px, 2)*100, round((orange_count)/tot_px, 2)*100, fish_len_px, fish_len_cm])
    else:
        with open(os.path.join(output_path, 'colors.csv'), "w") as file:
            writer = csv.writer(file)
            writer.writerow(['Image', '#black [px]', '#white [px]', '#orange [px]', 'black[%]', 'white[%]', 'orange[%]', 'len fish [px]', 'len fish [cm]'])
            writer.writerow([image_name, n_black, white_count, orange_count, round((n_black)/tot_px, 2)*100, round((white_count)/tot_px, 2)*100, round((orange_count)/tot_px, 2)*100, fish_len_px, fish_len_cm])


    # Step 4: Plot the results as a donut chart
    labels = ['Black', 'White', 'Orange']
    sizes = [black_count-n_black_outofmask, white_count, orange_count]
    colors = ['#000000', '#FFFFFF', '#FF8C00']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='gray'))
    # Draw a circle at the center to make it look like a donut
    center_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(center_circle)

    contours, _ = cv2.findContours(cropped_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(res_image, contours, -1, (50,50,50), 2)

    # Add the image to the center of the donut
    res_image[cropped_mask == 0] = (255,255,255)
    imagebox = OffsetImage(res_image, zoom=0.05)
    ab = AnnotationBbox(imagebox, (0, 0), frameon=False)
    ax.add_artist(ab)

    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Dominant Colors Distribution')
    plt.savefig(os.path.join(output_path, image_name+'_colors_distribution'), bbox_inches='tight', dpi=200)
    plt.close()

################################################################

def lock_controls(layer, viewer, widget_list, locked=True):
    qctrl = viewer.window.qt_viewer.controls.widgets[layer]
    for wdg in widget_list:
        getattr(qctrl, wdg).setEnabled(not locked)
        # or setVisible() if you want to just hide them completely

################################################################

"""#image = tifffile.imread('/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/prova.tif')
image = np.asarray(Image.open('/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/res/Corrected_Apo1_4_colors.png'))
mask = np.asarray(Image.open('/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/res/mask_Apo1_4.png'))

masked_image = cv2.bitwise_and(image, image, mask=mask)
contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
x,y,w,h = cv2.boundingRect(cnt)
n_black_outofmask = (mask[y:y+h,x:x+w].shape[0]*mask[y:y+h,x:x+w].shape[1]) - np.count_nonzero(mask[y:y+h,x:x+w])
color_analysis(image, mask, '/Users/aravera/Documents/PROJECTS/DSB_Salamin/Lucy_s35/res/', 'a', 5)"""
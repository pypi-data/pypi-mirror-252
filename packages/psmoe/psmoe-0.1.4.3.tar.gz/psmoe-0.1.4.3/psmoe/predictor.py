import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import cv2
import time
import nibabel as nib
from nyul import nyul_apply_standard_scale
import gdown
import networks


def model_downloader():
    
    try:
        os.makedirs("modelsh5")
        print(f"Folder created: modelsh5")
    except FileExistsError:
        print(f"Folder already exists: modelsh5")
        return
    
    pf = os.path.join(os.getcwd(),"modelsh5")

    gdown.download("https://drive.google.com/file/d/1bNIWg5OOhCMMY2e-0K-JVgKxzcj1LUbM/view?usp=sharing", 
                   os.path.join(pf,"attunet_final.h5"), 
                   quiet=False,
                   fuzzy=True)
    gdown.download("https://drive.google.com/file/d/1fiLNAW70bwqRGB0t_QjmVEYXjRFIPrZe/view?usp=sharing", 
                   os.path.join(pf,"classicunet_final.h5"), 
                   quiet=False,
                   fuzzy=True)
    gdown.download("https://drive.google.com/file/d/1r0ektmVG2UBhuiNNWYc_mL_b8iiVERdo/view?usp=sharing", 
                   os.path.join(pf,"sunet_final.h5"), 
                   quiet=False,
                   fuzzy=True)
    gdown.download("https://drive.google.com/file/d/1bWcbIhaDlWSmJyN7XERiQ7mD-RTEUCCE/view?usp=sharing", 
                   os.path.join(pf,"unet3_final.h5"), 
                   quiet=False,
                   fuzzy=True)
    
    print("-- Finished downloading models --")

    return

def load_example():
    
    try:
        os.makedirs("test_images")
        print(f"Folder created: test_images")
    except FileExistsError:
        print(f"Folder already exists: test_images")
        return
    
    pf = os.path.join(os.getcwd(),"test_images")

    gdown.download("https://drive.google.com/file/d/1bUl8uM5nOUPJCkGRwf1cWlrXqM5hBuDb/view?usp=sharing", 
                   os.path.join(pf,"sujeto_006.nii"), 
                   quiet=False,
                   fuzzy=True)
    
    print("-- Finished downloading example --")

    return


def model_loading():
    
    attunet = networks.AttUnet(input_size=(256,256,1),activation="selu",initializer="lecun_normal",num_filters=64)
    attunet.load_weights("modelsh5/attunet_final.h5")
    unet3 = networks.unet3plus(input_size=(256,256,1))
    unet3.load_weights("modelsh5/unet3_final.h5")
    sunet = networks.UNet(input_size=(256,256,1),activation="relu",initializer="he_uniform",num_filters=32)
    sunet.load_weights("modelsh5/sunet_final.h5")
    classicunet = networks.classicUNet(input_size=(256,256,1),activation="selu",initializer="lecun_normal",num_filters=64)
    classicunet.load_weights("modelsh5/classicunet_final.h5")
    
    return [attunet,unet3,sunet,classicunet]
    
def predict(path,nets,moe_th=0.4,thresholds=[0.95,0.45,0.65,0.95],coeff=[169, 201, 228, 161]):
    
    standard_path = 'nyul_landmarks.npy'
    nyul_media = 3.54715519304951
    nyul_var = 42.85355462071623
    volumen = 0
    x = nib.load(path)
    y = x.get_fdata()
    y = nyul_apply_standard_scale(y, standard_path)
    
    orig_img = []
    predicted = []
    heatmaps = []
    start = time.time()
    for slices in range(np.size(y,2)):
        img = y[63:319,63:319,slices]
        img = (img-nyul_media)/nyul_var                           
        test_img_input = np.expand_dims(img, 0)
        prediction = np.zeros(shape=(1,256,256,256))
        for i,net in enumerate(nets):
            prediction += ((net(test_img_input).numpy()) > thresholds[i])*coeff[i]/sum(coeff)
        predicted_img_th = (prediction[0,:,:,0] > moe_th)*1
        volumen += np.sum(predicted_img_th)*(x.header["pixdim"][1]*x.header["pixdim"][2]*x.header["pixdim"][3])
        orig_img.append(test_img_input)
        heatmaps.append(prediction)
        predicted.append(predicted_img_th)
    end = time.time()
    
    inference_time = end-start
    volumen = round(volumen/1000,2)
    
    return {
        "volume":volumen,
        "heatmap":heatmaps,
        "prediction":predicted,
        "inference_time": inference_time,
        "processed": orig_img
        }

  
def seg_plot(path,nets,moe=0.4):
    
    results = predict(path,nets,moe)
    test_img = results["processed"][int(len(results["processed"])/2)]
    prediction = results["prediction"][int(len(results["processed"])/2)]
    heatmap = results["heatmap"][int(len(results["processed"])/2)]

    contours, _ = cv2.findContours(prediction.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bordes = np.zeros_like(prediction, dtype=np.uint8)
    for contour in contours:
        bordes = cv2.drawContours(bordes, [contour], 0, (255, 0, 0), 1)
    bordes2 = cv2.cvtColor(bordes.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    bordes2[bordes == 255] = [255, 0, 0]
    
    reshaped_arr = test_img.reshape((256, 256, 1))
    rgb_arr = np.repeat(reshaped_arr, 3, axis=2)
    n = Normalize()(rgb_arr)

    plt.figure(figsize=(20, 10))
    plt.subplot(1,3,1)
    plt.title('Prediction Heatmap')
    plt.imshow(heatmap[0, :, :, 0],cmap='hot')
    plt.axis("off")
    plt.subplot(1,3,2)
    plt.title(f'Predicted Mask')
    plt.imshow(prediction, cmap='gray')
    plt.axis("off")
    plt.subplot(1,3,3)
    plt.title(f'Final View')
    plt.imshow(n + bordes2, cmap='gray')
    plt.axis("off")
    plt.subplots_adjust(wspace=0.01, hspace=0.1)
    plt.show()
    
    return
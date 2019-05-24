import os
import cv2 as cv
import numpy as np
import scipy.signal as filtering
import openslide as ops

import keras
import til_quantification as tq

# loading saved model from the disk
with keras.utils.generic_utils.CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,
                        'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
    model = keras.models.load_model('../models/MobileNet.hdf5')

# name and path of a whole slide image
wsi_image_path = '../whole_slide_images/'
wsi_name = 'sample.svs'

# this code support all the whole slide images readable with openslide library
wsiObj = ops.OpenSlide(os.path.join(wsi_image_path, wsi_name))
level = 1 # level should represent 20X magnification or scan resolution of ~0.50 micron/pixel
rows, cols = wsiObj.level_dimensions[level][1], wsiObj.level_dimensions[level][0]
dsf = wsiObj.level_downsamples[level] # down_sampling_factor with respect to level zero

patch_size = 128 # we used a 128x128 patch at 20X which is then upsampled to 224x224 for training
batch_size = 128 # number of image patch in a batch

batch = []
batch_counter = 0
patch_prob = np.zeros((0, 4))

for i in range(0, rows-patch_size+1, patch_size):
    for j in range(0, cols-patch_size+1, patch_size):
        patch = wsiObj.read_region((np.int64(j*dsf),np.int64(i*dsf)), level, (patch_size, patch_size))
        r, g, b, _ = cv.split(np.array(patch)) # ignoring alpha channel
        patch = cv.merge([r, g, b]) # constructing rgb patch

        # image preprocessing
        patch = cv.resize(patch, (224, 224), cv.INTER_LINEAR) # patch resizing to make it compatible with the trained model
        patch = ((np.float64(patch)/255)-0.5)*2 # only do if it's done while training otherwise comment this line

        batch.append(patch)
        batch_counter += 1
        if batch_counter == batch_size:
            probs = model.predict(np.array(batch))
            patch_prob = np.vstack([patch_prob, probs])
            batch_counter = 0
            batch = []

if batch_counter > 0: # process the remaining patches
    probs = model.predict(np.array(batch))
    patch_prob = np.vstack([patch_prob, probs])

# coverting patch_probs into prob_map where third dimension represents the probabilities of four classes
prob_map = np.reshape(patch_prob, (np.int64(np.floor(rows/patch_size)), np.int64(np.floor(cols/patch_size)),4))

# wsi name without extension
wsi_name, _ = os.path.splitext(wsi_name)

# saving prob_maps as npy for future use
np.save('../results/%s_prob_map.npy' % wsi_name, prob_map)

# saving prob_maps as png images for ease of visualization
cv.imwrite('../results/%s_stroma.png' % wsi_name, np.uint8(prob_map[:, :, 0] * 100))
cv.imwrite('../results/%s_non_roi.png' % wsi_name, np.uint8(prob_map[:, :, 1] * 100))
cv.imwrite('../results/%s_tumour.png' % wsi_name, np.uint8(prob_map[:, :, 2] * 100))
cv.imwrite('../results/%s_lymphocyte.png' % wsi_name, np.uint8(prob_map[:, :, 3] * 100))

# TIL quantification through TILAb score using given neighbourhood
tilab_score = tq.TILAb_Score(prob_map, cell_size=16) # cell sizes used in the paper are: 4, 6, 8 ,10, 12, 14, 16, and 18
print('TILAb Score: %0.04f' % tilab_score)

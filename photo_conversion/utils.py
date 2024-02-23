import cv2
import numpy as np
from skimage.color import rgb2lab,lab2rgb
from keras.models import model_from_json
import os
from django.conf import settings
import matplotlib.pyplot as plt
# sharred task from celery

DEF_PATH = "/mnt/e/colormemoir"

def model():
# Load the model architecture from JSON file
    json_file = open(f"{DEF_PATH}/photo_conversion/models/model1.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # Load the weights into the model
    loaded_model.load_weights(f"{DEF_PATH}/photo_conversion/models/model.h5")
    
    return loaded_model
    
def initiate_conversion(photo_conversion):
    input_image_url = f"{DEF_PATH}{photo_conversion.input_image.url}"
    print(input_image_url)
    output_image_path = os.path.join(settings.MEDIA_ROOT, 'output_images', photo_conversion.reference_id + '.jpg')
    print(output_image_path)
     
    # Read image
    img = cv2.imread(input_image_url)

    # Convert image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize image to 256x256
    img_resized = cv2.resize(img, (256, 256))

    # Preprocess image for colorization
    colorize = np.array([img_resized], dtype=float)
    colorize = rgb2lab(1.0/255 * colorize)[:, :, :, 0]
    colorize = colorize.reshape(colorize.shape + (1,))

    # Perform colorization using the model
    loaded_model = model()
    output = loaded_model.predict(colorize)
    output *= 128

    # Create resulting image
    res_image = np.zeros((256, 256, 3))
    res_image[:, :, 0] = colorize[0][:, :, 0]
    res_image[:, :, 1:] = output[0]
    res_image = lab2rgb(res_image)
    # plt.imshow(res_image)

    # Convert res_image to uint8 data type before saving
    res_image_uint8 = (res_image * 255).astype(np.uint8)

    # Save resulting image
    if cv2.imwrite(output_image_path, cv2.cvtColor(res_image_uint8, cv2.COLOR_RGB2BGR)):
        # timro kaam ends
        photo_conversion.status = 'completed'
        photo_conversion.output_image = output_image_path
        photo_conversion.save()
    
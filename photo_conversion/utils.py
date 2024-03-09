import cv2
import numpy as np
from skimage.color import rgb2lab, lab2rgb
from keras.models import model_from_json
import os
from django.conf import settings
from pathlib import Path

if os.name == 'nt':
    DEF_PATH = Path(__file__).resolve().parent
else:
    # if virtual terminal
    DEF_PATH = "/mnt/d/Non-Windows/Projects and Works/colormemoir/colormemoir/"


def model():
    # Load the model architecture from JSON file
    json_file = open(os.path.join(
        DEF_PATH, 'models', 'model_350opt.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # Load the weights into the model
    loaded_model.load_weights(os.path.join(
        DEF_PATH, 'models', 'model_350opt.h5'))
    return loaded_model


def convert(input_image_url, output_image_path, resolution=None):
    img = cv2.imread(input_image_url)

    # Convert image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize image to 256x256
    img_resized = cv2.resize(img, (256, 256))

    # Preprocess image for colorization
    colorize_array = np.array([img_resized], dtype=float)
    colorize_l = rgb2lab(1.0/255 * colorize_array)[:, :, :, 0]
    colorize_ab = rgb2lab(1.0/255 * colorize_array)[:, :, :, 1:]
    colorize = colorize_l.reshape(colorize_l.shape + (1,))

    # Perform colorization using the model
    loaded_model = model()
    output = loaded_model.predict(colorize)
    output *= 128

    # Create resulting image
    res_image = np.zeros((256, 256, 3))
    res_image[:, :, 0] = colorize[0][:, :, 0]
    res_image[:, :, 1:] = output[0]
    res_image = lab2rgb(res_image)

    # Convert res_image to uint8 data type before saving
    res_image_uint8 = (res_image * 255).astype(np.uint8)
    loaded_model.compile(optimizer='rmsprop', loss='mse', metrics=['accuracy'])
    loss, accuracy = loaded_model.evaluate(colorize, colorize_ab/128)

    try:
        w, h = resolution.split('x')
        w, h = int(w), int(h)
        print(w, h)
        res_image_uint8 = cv2.resize(res_image_uint8, (w, h))
    except:
        print("Failed to resize image")
        pass

    # Save resulting image
    return (cv2.imwrite(output_image_path, cv2.cvtColor(res_image_uint8, cv2.COLOR_RGB2BGR)), loss,  accuracy)


def initiate_conversion(photo_conversion):
    input_image_url = os.path.join(
        settings.MEDIA_ROOT, photo_conversion.input_image.name)  # .replace("/", "\\")
    output_image_path = os.path.join(
        settings.MEDIA_ROOT, 'output_images', photo_conversion.reference_id + '.jpg')  # .replace("/", "\\")
    converted, loss, accuracy = convert(
        input_image_url, output_image_path, photo_conversion.resolution)
    if converted:
        photo_conversion.status = 'completed'
        photo_conversion.output_image = "/output_images/" + \
            photo_conversion.reference_id + ".jpg"
        photo_conversion.accuracy = accuracy
        photo_conversion.loss = loss
        photo_conversion.save()


def convert_all(from_dir, to_dir):
    files = os.listdir(from_dir)
    # print(files)
    for f in files:
        from_path = os.path.join(from_dir, f)
        to_path = os.path.join(to_dir, f)
        # if os.path.isfile(f):
        convert(from_path, to_path)
        # print(f"converting {from_path} to {to_path}")
        # else:
        #     print(
        #         f"Skipping {from_path} | {to_path} because it is not a file.")

import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from utils import convert_all
import sys
import os


def compare_images(colorized_img_path, ground_truth_img_path):
    colorized_img = cv2.imread(colorized_img_path)
    ground_truth_img = cv2.imread(ground_truth_img_path)
    ground_truth_img = cv2.resize(ground_truth_img, (256, 256))
    ssim_score = ssim(colorized_img, ground_truth_img,
                      multichannel=True, win_size=3)
    mse_score = mse(colorized_img, ground_truth_img)
    return (ssim_score, mse_score)


def log_metrics():
    print("Logging metrics...")
    ssim_score, mse_score = compare_images(
        '../media/testing/colored/pSNiGUiLvU.jpg', '../media/testing/groundtruth/_MG_4258.jpg')
    print(f"(SSIM: {ssim_score:.4f}, MSE: {mse_score:.4f})")


def log_to_json(from_dir, to_dir):
    metrics = []
    for f in os.listdir(from_dir):
        ssim_score, mse_score = compare_images(
            os.path.join(from_dir, f), os.path.join(to_dir, f))
        metrics.append({
            'file': f,
            'ssim': ssim_score,
            'mse': mse_score
        })

    import json
    with open('./metrics/real_metrics.json', 'w') as outfile:
        json.dump(metrics, outfile)


def calculate_average_metrics(json_file_path='./metrics/real_metrics.json'):
    import json
    import numpy as np
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    # find mean of ssim and mse
    ssim_scores = np.array([d['ssim'] for d in data])
    mse_scores = np.array([d['mse'] for d in data])

    mean_ssim_score = np.mean(ssim_scores)

    min_ssim_score = np.min(ssim_scores)
    fq_ssim_score = np.percentile(ssim_scores, 25)
    md_ssim_score = np.percentile(ssim_scores, 50)
    thq_ssim_score = np.percentile(ssim_scores, 75)
    max_ssim_score = np.max(ssim_scores)

    sd_ssim_score = np.std(ssim_scores)

    mean_mse_score = np.mean(mse_scores)

    min_mse_score = np.min(mse_scores)
    fq_mse_score = np.percentile(mse_scores, 25)
    md_mse_score = np.percentile(mse_scores, 50)
    thq_mse_score = np.percentile(mse_scores, 75)
    max_mse_score = np.max(mse_scores)

    sd_mse_score = np.std(mse_scores)

    print(f"Mean SSIM: {mean_ssim_score:.4f}")
    print(f"({min_ssim_score, fq_ssim_score, md_ssim_score, thq_ssim_score, max_ssim_score})")
    print(f"SD SSIM: {sd_ssim_score:.4f}")

    print(f"Mean MSE: {mean_mse_score:.4f}")
    print(
        f"({min_mse_score, fq_mse_score, md_mse_score, thq_mse_score, max_mse_score})")
    print(f"SD MSE: {sd_mse_score:.4f}")

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    ax.plot(np.random.normal(1, 0.02, len(ssim_scores)),
            ssim_scores, 'ro', alpha=0.5)  # Red circles for SSIM

    box1 = ax.boxplot([ssim_scores], positions=[1], patch_artist=True,
                      widths=0.2, showfliers=False)  # SSIM box plot

    colors = ['lightcoral', 'lightblue']
    for box, color in zip([box1], colors):
        for patch in box['boxes']:
            patch.set_facecolor(color)

    # Set labels and save the plot
    ax.set_xticklabels(['SSIM'])
    plt.savefig('./metrics/real_metrics_ssim.png')

    fig, ax = plt.subplots()
    ax.plot(np.random.normal(2, 0.02, len(mse_scores)),
            mse_scores, 'bo', alpha=0.5)    # Blue circles for MSE
    box2 = ax.boxplot([mse_scores], positions=[2], patch_artist=True,
                      widths=0.2, showfliers=False)    # MSE box plot

    colors = ['lightblue']
    for box, color in zip([box2], colors):
        for patch in box['boxes']:
            patch.set_facecolor(color)

    # Set labels and save the plot
    ax.set_xticklabels(['MSE'])
    plt.savefig('./metrics/real_metrics_mse.png')

    plt.close()


def convert_to_bandw(from_dir, to_dir):
    from PIL import Image
    import os

    # Define input and output folders
    input_folder = from_dir
    output_folder = to_dir

    print("Converting images to black and white...")
    print(input_folder, output_folder)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(
        input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(image_files)

    # Process each image
    for image_file in image_files:
        # Open the image
        input_path = os.path.join(input_folder, image_file)
        img = Image.open(input_path)

        # Convert the image to grayscale
        bw_img = img.convert('L')

        # Save the black and white image with the same name in the output folder
        output_path = os.path.join(output_folder, image_file)
        bw_img.save(output_path)

        print(f"Converted {image_file} to black and white.")


if __name__ == '__main__':
    args = sys.argv
    if "--json" in args:
        log_to_json('../media/test_test_set/colored/',
                    '../media/test_test_set/groundtruth/')
    elif "--bandw" in args:
        convert_to_bandw('../media/new_test_set/',
                         '../media/new_test_set_bandw/')
    elif "--convert" in args:
        convert_all('../media/test_test_set/bandw/',
                    '../media/test_test_set/colored/')
    elif "--calc" in args:
        calculate_average_metrics()
    else:
        log_metrics()

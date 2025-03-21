import cv2

def get_figure_hocr_bbox_only(fig):
    fig_hocr = f"<img bbox=\"{fig[0]} {fig[1]} {fig[2]} {fig[3]}\">\n"
    return fig_hocr

def get_figure_hocr(image_path, outputDirectory, pagenumber, bbox, count):
    image = cv2.imread(image_path)
    cropped_image = image[bbox[1]: bbox[3], bbox[0]: bbox[2]]
    image_file_name = '/Cropped_Images/figure_' + str(pagenumber) + '_' + str(count) + '.jpg'
    cv2.imwrite(outputDirectory + image_file_name, cropped_image)
    fig_hocr = f'<img src=\"..{image_file_name}\" bbox=\"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\">\n'
    return fig_hocr
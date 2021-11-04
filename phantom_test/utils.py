from nilearn import image, masking

def read_nifti(niftiFilename, get_data=True):

    if get_data: 
        output_file = image.load_img(niftiFilename).get_fdata()
    else: 
        output_file = image.load_img(niftiFilename)
    return output_file

def applymask(niftiFilename, mask):

    masked_array = masking.apply_mask(niftiFilename, mask)
    return masked_array

def check_dimension(image_path1, image_path2):

    sameShape = False
    image1_shape = image.load_img(image_path1).get_fdata().shape
    print(image1_shape)
    image2_shape = image.load_img(image_path2).get_fdata().shape
    print(image2_shape)

    if image1_shape == image2_shape: 
        sameShape = True
    return sameShape 

def resample_image(image_path1, image_path2):

    roi_image = image.load_img(image_path1)
    ref_image = image.load_img(image_path2)

    roi_resampled = image.resample_to_img(roi_image, ref_image, interpolation='nearest')
    
    return roi_resampled 

def getOutputFilename(runId, TRindex):
	""""Return station classification filename"""
	filename = "AverageAct_run-{0:02d}_TR-{1:03d}.txt".format(runId, TRindex)
	return filename

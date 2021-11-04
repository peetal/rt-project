import os, glob, time, shutil

def main():

    currPath = os.path.dirname(os.path.realpath(__file__))
    bridgePath = '/Users/peetal/Desktop/Bridge_test/'

    # existing DICOM files directory 
    test_dicom_dir = os.path.join(currPath, 'dicomDir', '20190219.0219191_faceMatching.0219191_faceMatching')
    test_bridge_dir = os.path.join(bridgePath, 'dicomDir', '20190219.0219191_faceMatching.0219191_faceMatching')

    if not os.path.isdir(test_bridge_dir): # if not a directory, make one
        os.makedirs(test_bridge_dir)
    elif len(glob.glob(os.path.join(test_bridge_dir, '*'))) > 0: # remove all the files in the dir 
        for dicom in glob.glob(os.path.join(test_bridge_dir, '*')):
            os.remove(dicom)
            

    # all DICOM files
    all_dicoms = sorted(glob.glob(os.path.join(test_dicom_dir, '*')))

    for idx, dicom in enumerate(all_dicoms):
        if idx == 0:
            time.sleep(20) 
        shutil.copy(dicom, test_bridge_dir)
        time.sleep(3)
    
    return

if __name__ == "__main__":

    main()




import os
import requests

# List of URLs to download
urls = [
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/4hr_avr',
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/6hr_avr',
    
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/9hr_avr',
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/mock',
    
    # Add more URLs as needed
]

# Specify the directory to save the downloaded files
download_directory = os.path.join('data','segmentations')

# Ensure the download directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)


for url in urls:
    cell_stats = url + '/segmentation_' + os.path.basename(url)+ '_cell_stats.csv'
    counts = url + '/segmentation_' + os.path.basename(url)+ '_counts.tsv'

    # Specify the directory to save the downloaded files
    download_directory = os.path.join('data','segmentations', os.path.basename(url))
    print(download_directory)
    # Ensure the download directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    for subfile in [cell_stats, counts]:

        response = requests.get(subfile)
        # Extract the filename from the URL
        filename = os.path.join(download_directory,subfile.split('/')[-1])

        # Save the file to the specified directory
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')

additional_urls = ['http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/avrrpt24/segmentation2_cell_stats.csv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/avrrpt24/segmentation2_counts.tsv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/kt56/segmentation_kt_cell_stats.csv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/Baysor_segmentations/kt56/segmentation_kt_counts.tsv']

for url in additional_urls:
    download_directory = os.path.join('data','segmentations', os.path.basename(os.path.dirname(url)))
    print(download_directory)
    # Ensure the download directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    response = requests.get(url)
    filename = os.path.join(download_directory,url.split('/')[-1])

    # Save the file to the specified directory
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Downloaded {filename}')


smFISH_folders = ['http://neomorph.salk.edu/download/Nobori_etal_merfish/smFISH/mock_9h', 
                  'http://neomorph.salk.edu/download/Nobori_etal_merfish/smFISH/avr_9h',
                  'http://neomorph.salk.edu/download/Nobori_etal_merfish/smFISH/avr_24h',
                  'http://neomorph.salk.edu/download/Nobori_etal_merfish/smFISH/dc3000_24h']

for url in smFISH_folders:
    for fl in ['mosaic_sid_z'+str(i)+'.tif' for i in range(0,7)]:
        url_temp = url + '/' + fl
        download_directory = os.path.join('data','smFISH_images', os.path.basename(os.path.dirname(url_temp)))
        print(download_directory)
        # Ensure the download directory exists
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        response = requests.get(url_temp)
        filename = os.path.join(download_directory,url_temp.split('/')[-1])

        # Save the file to the specified directory
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')
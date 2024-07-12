import os
import requests

# segmentation urls
urls = [
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/4hr_avr',
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/6hr_avr',
    
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/9hr_avr',
    'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/mock',
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

additional_urls = ['http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/avrrpt24/segmentation2_cell_stats.csv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/avrrpt24/segmentation2_counts.tsv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/kt56/segmentation_kt_cell_stats.csv',
'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/Baysor_segmentations/kt56/segmentation_kt_counts.tsv']

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


# downloading a useful file
useful_file = 'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/_Misc/geneID_to_geneName_MERSCOPE_panel1.txt'

download_directory = os.path.join('data','useful_files')

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

response = requests.get(url)
filename = os.path.join(download_directory,useful_file.split('/')[-1])

# Save the file to the specified directory
with open(filename, 'wb') as f:
    f.write(response.content)
print(f'Downloaded {filename}')


#downloading objects
useful_files = ['http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/DC3000_alone.rds', 'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/AvrRpt2_alone.rds', 'http://neomorph.salk.edu/download/Nobori_etal_merfish/MERFISH/AvrRpt2_alone2.rds']
for useful_file in useful_files:
    download_directory = os.path.join('data')

    response = requests.get(url)
    filename = os.path.join(download_directory,useful_file.split('/')[-1])

    # Save the file to the specified directory
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Downloaded {filename}')

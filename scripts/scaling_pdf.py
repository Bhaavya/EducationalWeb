from PyPDF2 import PdfFileMerger,PdfFileWriter,PdfFileReader
import re
def sort_slide_names(l):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key) ]
    sl = sorted(l, key = alphanum_key)
    return sl

import os

folder_name = input('Input course name')
scale = float(input('Input scale factor'))
path = "/Users/richameherwal/Desktop/UIUC/research/eduweb/EducationalWeb/pdf.js/static/slides/"+folder_name
#path = "/Users/richameherwal/Desktop/UIUC/research/eduweb/ECE_486_trial"
dirs = os.listdir( path )
dirs.remove('.DS_Store')
    

# 1. Read page 0 from Pdf File Reader
# 2. Add that page to a writer of the lecture
# 3. Write the writer to a new lecture path 

for lecture in dirs:
    lec_folder= os.listdir(os.path.join(path, lecture))
    sorted_file_list = sort_slide_names(lec_folder)
    writer = PdfFileWriter()
    for slide in sorted_file_list:
        pdf_file_path=os.path.join(path,lecture,slide)
        pdf = PdfFileReader(pdf_file_path)
        page0 = pdf.getPage(0)
        page0.scaleBy(scale)
        writer.add_page(page0)
    pdf_out = path+'/'+lecture+'.pdf'   
    with open(pdf_out, "wb+") as f:
        writer.write(pdf_out)

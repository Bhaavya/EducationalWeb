from PyPDF2 import PdfFileMerger
import re
def sort_slide_names(l): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key) ] 
    sl = sorted(l, key = alphanum_key)
#     try:
#         sl.remove('.DS_Store')
#     except:
#         pass
    return sl 

import os

folder_name = input('Input course name')
path = "/Users/richameherwal/Desktop/UIUC/research/eduweb/EducationalWeb/pdf.js/static/slides/"+folder_name
dirs = os.listdir( path )
# dirs.remove('.DS_Store')

for lecture in dirs:
    lec_folder= os.listdir(os.path.join(path, lecture))
    sorted_file_list = sort_slide_names(lec_folder)
#     print(sorted_file_list)
    merger = PdfFileMerger()
    for slide in sorted_file_list:
        pdf_file_path=os.path.join(path,lecture,slide)
#         print(pdf_file_path)
        merger.append(pdf_file_path)
    merger.write(path+'/'+lecture+'.pdf')
    merger.close()

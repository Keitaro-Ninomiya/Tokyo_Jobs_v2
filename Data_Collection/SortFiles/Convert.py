import pypdfium2 as pdfium
import os
def PDFtoPNG(origin,path,Page):    
    image_name =f"Page"+str(Page)+".pdf"
    pdfpath=os.path.join(origin,path,image_name)
    pdf = pdfium.PdfDocument(pdfpath)
    page = pdf.get_page(0)
    pil_image = page.render(scale = 300/72).to_pil()
    image_name =f"Page"+'{:03d}'.format(Page)+".png"
    pil_image.save(os.path.join(origin,path,image_name))
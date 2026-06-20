import fitz


class PDFProcessor:

    def extract_text(self, pdf_path):

        doc = fitz.open(pdf_path)

        paragraphs = []

        for page_num, page in enumerate(doc, start=1):

            text = page.get_text()
            paras = text.split("\n\n")

            for para_num, para in enumerate(paras, start=1):

                para = para.strip()

                if len(para) < 20:
                    continue

                paragraphs.append({
                    "text": para,
                    "page": page_num,
                    "para": para_num
                })

        doc.close()
        return paragraphs
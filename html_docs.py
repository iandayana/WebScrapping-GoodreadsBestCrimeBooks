import requests


class HTMLDocs:
    def __init__(self, main_url, my_title,  queryable_object):
        self.main_url = main_url
        self.title = my_title
        self.queryable_object = queryable_object
        self.text = ""

    def get_doc(self, page_number):
        url = self.main_url
        if page_number > 1:
            url += f"{self.queryable_object}{page_number}"

        page = requests.get(url)
        self.text = page.text

    def save_doc(self, page_number):
        self.get_doc(page_number)

        with open(f"{self.title}_{page_number}.html", "w") as doc:
            doc.write(self.text)
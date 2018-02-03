import mosspy
from bs4 import BeautifulSoup
from django.utils import timezone
from django.conf import settings


class PlagiarismResult:
    """
    Class for storing detected plagiarism
    """
    def __init__(self, file_1, percentage_1, file_2, percentage_2, lines):
        self.file_1 = file_1
        self.percentage_1 = percentage_1
        self.file_2 = file_2
        self.percentage_2 = percentage_2
        self.lines = lines


def create_moss_report(files, folder):
    """
    Send request to MOSS and parse response
    """
    lic_file = open(settings.MEDIA_URL + "license.txt")
    user_id = int(lic_file.read())
    lic_file.close()

    m = mosspy.Moss(user_id, "python")
    for this_file in files:
        m.addFile(this_file)

    url = m.send()

    creation_time = timezone.now()
    file_name = "report_" + str(creation_time.day) + str(creation_time.month) + str(creation_time.year) + "_" + \
                str(creation_time.hour) + str(creation_time.minute) + str(creation_time.second) + ".html"
    file_path = folder + file_name

    m.saveWebPage(url, file_path)

    detected = check_results(file_path)
    return detected, file_path


def has_results(html):
    """
    Return True if given HTML contains result
    """
    return "No matches were found" not in str(html)


def check_results(file_path):
    """
    Check if downloaded report contains plagiarsm
    """
    f = open(file_path)
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'html.parser')
    return has_results(soup)


def extract_results(file_path):
    """
    Extract results from given report
    """
    f = open(file_path)
    html = f.read()
    f.close()

    plagiarisms = []

    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.findAll("tr")
    del table_rows[0]
    for row in table_rows:
        content = list(row.get_text().split("\n"))
        plagiarisms.append(extract_row_result(content))
    return plagiarisms


def extract_row_result(row_content):
    """
    Extract data from report's table row
    """
    file_1, percentage_1 = get_file_data(row_content[0])
    file_2, percentage_2 = get_file_data(row_content[1])
    lines = int(row_content[2])
    return PlagiarismResult(file_1, percentage_1, file_2, percentage_2, lines)


def get_file_data(file_html):
    """
    Extract file name and file matching percentage
    """
    file_text = file_html.split(" ")[0]
    file_percentage_text = file_html.split(" ")[1]
    file_percentage = float(file_percentage_text[1:-2])
    return file_text, file_percentage

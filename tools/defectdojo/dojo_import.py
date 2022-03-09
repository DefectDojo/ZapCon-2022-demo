import os
import requests
import shutil
import argparse
from datetime import datetime


# --- Helper Functions ---
# ------------------------
def log(message, name=None, item_id=None, file_path=None, scan_type=None, fails=None):
    """
    Log status messages for completion of requests, error messages, and consistent formatting

    :message: The body of the statement
    :name: Name of the object logged, if applicable
    :item_id: The ID of the object logged, if applicable
    :file_path: Path of the file that was imported, if applicable
    :scan_type: Type of scan that was imported, if applicable
    :fails: List of failed imports to be logged, if applicable
    """
    form = ''
    if name and item_id:
        form = name + ':' + str(item_id)
    elif file_path and scan_type:
        form = scan_type + ' at: ' + file_path
    elif item_id:
        form = '(' + str(item_id) + ')'
    elif fails:
        form = ': ' + str(len(fails)) + '\n'
        for index in range(0, len(fails)):
            form += str(index + 1) + '\t' + str(fails[index])

    print(message, form)


def post(api_url, token, payload, files=None):
    """
    POST API call to DefectDojo to create and edit objects

    :api_url: Url that points to a specific endpoint of the api
    :token: Used for authentication
    :payload: Contains the information of the object to be creates
    :files: Files to be attached to the request and uploaded (Default to None)
    """
    headers = {'Authorization': token}
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    data = response.json()
    if response.status_code not in range(400, 600):
        obj_id = data.get('test') if files else data.get('id')
        return obj_id
    log(data)
    return None


def get(api_url, token):
    """
    GET API call to DefectDojo to retrieve objects

    :api_url: Url that points to a specific endpoint of the api
    :token: Used for authentication
    """
    headers = {'Authorization': token}
    response = requests.request("GET", api_url, headers=headers)
    data = response.json()
    if response.status_code not in range(400, 600):
        return data.get('results')
    log(data)
    return None


def make_dir(base, scan_type):
    """
    Creates the completed and failed scan directories for processed reports to be filed
    into. If these directories already exists, then this function does nothing

    :base: The base directory of this project. Generally where this very python file is located
    :scan_type: The type of scan that was imported
    """
    complete = os.path.join(base + '/completed/' + scan_type)
    failed = os.path.join(base + '/failed/' + scan_type)

    try:
        os.makedirs(complete)
        log('Created dir ' + complete)
    except FileExistsError:
        log(complete + 'already exsists')

    try:
        os.makedirs(failed)
        log('Created dir ' + failed)
    except FileExistsError:
        log(failed + 'already exsists')


# --- Action functions ---
# ------------------------
def import_scan(api_url, token, product_name, engagement_name, scan_type, abs_file):
    """
    Import the scan with the given file_path

    :api_url: Url that points to a specific endpoint of the api
    :token: Used for authentication
    :engagement_id: ID of the engagement found or created
    :scan_type: The type of scan that is to be imported
    :abs_file: Absolute path of the report to be imported
    """
    log('Trying to import the file', scan_type=scan_type, file_path=abs_file)
    payload = {
        'scan_type': scan_type,
        'verified': False,
        'active': True,
        'auto_create_context': True,
        'product_type_name': 'Research and Development',
        'product_name': product_name,
        'engagement_name': engagement_name
    }
    files = [
        ('file', ('file', open(abs_file, 'rb'), 'application/octet-stream'))
    ]

    test_id = post(api_url, token, payload, files)
    if test_id:
        log('Imported successfully', item_id=test_id)
    else:
        log('The file could not be imported. Please check DefectDojo logs for more information')
    return test_id


def directory_crawl(api_url, token, product_name, engagement_name):
    """
    Crawl through the 'imports' directory to import all files and then move
    them to the appropriate ending directory

    :api_url: Url that points to a specific endpoint of the api
    :token: Used for authentication
    :engagement_id: ID of the engagement found or created
    """
    import_scan_url = api_url + 'import-scan/'
    base_dir = os.path.abspath('imports')
    fail_list = []
    log('importing the files in the imports directory...')

    to_do_dir = base_dir + '/to_do'
    for scan_type in os.listdir(to_do_dir):
        scan_dir = os.path.join(to_do_dir, scan_type)
        for file in os.listdir(scan_dir):
            # Attempt to import
            abs_file = os.path.abspath(os.path.join(scan_dir, file))
            test_id = import_scan(import_scan_url, token, product_name, engagement_name, scan_type, abs_file)
            # Determine where the results should go after import
            # Make sure there is already a directory for the scans to go into
            make_dir(base_dir, scan_type)
            if test_id:  # Success
                dest = base_dir + '/completed/' + scan_type + '/' + file
            else:  # Failed
                dest = base_dir + '/failed/' + scan_type + '/' + file
                fail_list.append(str(abs_file))
            shutil.move(abs_file, dest)

    if len(fail_list):
        log('Some reports failed to import', fails=fail_list)
    else:
        log('Imported all reports successfully')


# --- Main ---
# Import all files in the /path/to/import_<scan_type> directory
if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="DefectDojo url as follows http(s)://dojo-url.com'")
    parser.add_argument("--project_name", required=True, help="Matches the name of the Azure DevOps project")
    parser.add_argument("--token", required=True, help="Just the token without \"Token\"")
    args = parser.parse_args()
    # Set the "globals" tp be used throughout the project
    api_url = str(args.url).strip('/') + '/api/v2/'
    project_name = str(args.project_name)
    token = 'Token ' + str(args.token)
    # Import all the available scans
    directory_crawl(api_url, token, project_name, datetime.today().strftime("%Y/%m/%d - %H:%M"))

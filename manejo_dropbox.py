import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

def update_dropbox_file(nombre_file):
    access_token = 'zp_ELfFzrVAAAAAAAAAAEdGOto9N9D1ADJtPpYbG9lqfYD6WTN6IXFmqJwEC1V0s'
    transferData = TransferData(access_token)
    file_from = '{}'.format(nombre_file)
    file_to = '/{}'.format(nombre_file)  # The full path to upload the file to, including the file name
    # API v2
    transferData.upload_file(file_from, file_to)


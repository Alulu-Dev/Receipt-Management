

def validate_attached_file(request):
    supported_formats = ['image/jpg', 'image/bmp', 'image/gif', 'image/heic',
                         'image/heif', 'image/jpeg', 'image/png', 'image/webp'
                         ]

    if 'file' not in request.files:
        raise CustomFileValidationException('No File Found')
    file = request.files['file']

    if file.filename == '':
        raise CustomFileValidationException('No File Found')
    if file.mimetype in supported_formats:
        return True
    raise CustomFileValidationException("File Format not supported! File must be an Image")


class CustomFileValidationException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message

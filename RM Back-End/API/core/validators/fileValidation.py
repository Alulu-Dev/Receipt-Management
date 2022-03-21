def validate_attached_file(request):
    supported_formats = ['image/avif', 'image/bmp', 'image/gif', 'image/heic',
                         'image/heif', 'image/jpeg', 'image/png', 'image/webp'
                         ]

    if 'file' not in request.files:
        return 'No File Found', 400
    file = request.files['file']

    if file.filename == '':
        return 'No File Found', 400
    if file.mimetype in supported_formats:
        return True
    return False

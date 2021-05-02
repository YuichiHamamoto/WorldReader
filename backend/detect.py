from google.cloud import vision
import io, json
from google.protobuf.json_format import MessageToJson

def detect(path):
    """Detects labels in the file."""
    
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    retData = {
        'labelAnnotations': list(),
        'logoAnnotations': list(),
        'localizedObjectAnnotations': list()
    }

    response = client.label_detection(image=image)
    tmp = json.loads(MessageToJson(response))
    retData['labelAnnotations'] = tmp['labelAnnotations'] if 'labelAnnotations' in tmp else []
    
    response = client.logo_detection(image=image)
    tmp = json.loads(MessageToJson(response))
    retData['logoAnnotations'] = tmp['logoAnnotations'] if 'logoAnnotations' in tmp else []

    response = client.object_localization(image=image)
    tmp = json.loads(MessageToJson(response))
    retData['localizedObjectAnnotations'] = tmp['localizedObjectAnnotations'] if 'localizedObjectAnnotations' in tmp else []

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return retData

# [START vision_logo_detection]
def detect_logos(path):
    """Detects logos in the file."""

    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_logo_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_logo_detection]
# [END vision_logo_detection]

# [START vision_localize_objects]
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
# [END vision_localize_objects]



if __name__ == '__main__':
    print(detect('uploads/your_image.png'))
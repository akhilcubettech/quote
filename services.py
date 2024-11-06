import boto3

def extract_image(image_path):
    textract_client = boto3.client('textract', region_name='us-west-2')

    with open(image_path, 'rb') as document:
        response = textract_client.detect_document_text(Document={'Bytes': document.read()})

    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])
    return "\n".join(extracted_text)

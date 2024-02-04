import boto3
import base64
import json

emotions_translate = {
    "ANGRY": "nervoso",
    "DISGUSTED": "enjoado",
    "FEAR": "medo",
    "CALM": "calmo",
    "SAD": "triste",
    "SURPRISED": "surpreso",
    "CONFUSED": "confuso",
    "HAPPY": "feliz"
}

def obter_maior_confianca(lista):
    # inicializa a maior confiança e o dicionário com maior confiança como None
    maior_confianca = None
    dicionario_maior_confianca = None

    # percorre cada dicionário na lista
    for dicionario in lista:
        confianca = dicionario["Confidence"]

        # verifica se é a maior confiança encontrada até o momento
        if maior_confianca is None or confianca > maior_confianca:
            maior_confianca = confianca
            dicionario_maior_confianca = dicionario

    return dicionario_maior_confianca

def lambda_handler(event, context):

    # Verificando se o request veio de URL
    if "headers" in event:
        event = event["body"]

        # Remove as barras invertidas de escape e caracteres adicionais
        event = event.replace("\\", "")
        event = event.strip('"')

        # Converte a string para um dicionário Python
        event = json.loads(event)

    print(event)

    # Verifica se o evento contém a imagem em base64
    if 'image_base64' in event:
        # Decodifica a imagem base64
        image_base64 = event['image_base64']
        image_bytes = base64.b64decode(image_base64)
        
        # Define o caminho e o nome do arquivo temporário
        temp_image_path = '/tmp/temp_image.png'
        
        # Salva a imagem em um arquivo temporário
        with open(temp_image_path, 'wb') as f:
            f.write(image_bytes)
        
        # Inicializa o cliente para a AWS Rekognition
        rekognition_client = boto3.client('rekognition')
        
        # Chama a API de análise facial da AWS Rekognition
        with open(temp_image_path, 'rb') as f:
            response = rekognition_client.detect_faces(
                Image={
                    'Bytes': f.read()
                },
                Attributes=['ALL']
            )
        
        # Processa a resposta da API
        if 'FaceDetails' in response:
            face_details = response['FaceDetails']

            if len(face_details) > 1:
                
                return {
                    'statusCode': 400,
                    'body': "Há mais de uma face neste rosto."
                }
            
            # Realizar validação se alguma emoção tem maior que 70% de confiança

            emotions = response['FaceDetails'][0]["Emotions"]
            emotion_max = obter_maior_confianca(emotions)

            if emotion_max["Confidence"] > 0.7 and emotion_max["Type"] != "CALM":
                return {
                    'statusCode': 400,
                    'body': "Rosto com emoção predominante (" + emotions_translate[emotion_max["Type"]] + ")."
                }

            return {
                'statusCode': 200,
                'body': {"boundingBox": response['FaceDetails'][0]["BoundingBox"], "reason":  "Face validada com sucesso."}
            }
        else:
            return {
                'statusCode': 400,
                'body': 'Não foram encontrados detalhes faciais na imagem.'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Por favor, forneça a imagem em base64.'
        }
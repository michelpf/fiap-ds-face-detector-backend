# Serviço de Backend Preparação de Foto para Documentos

Este serviço (backend) fornece uma camada de entrada para avaliação de fotos como medida de segurança para on-boarding de aplicações bancárias ou afins.

Os seguintes requisitos precisam estar presentes para a foto ser aceita:

* Uma única foto na imagem
* Ausência de emoções

Após a análise de emoções, a imagem deve ser recortada somente para a região onde se encontra a face.

O serviço requer um paylod com a imagem em formato base 64.
Exemplo de payload:

```json
{
    "image_base64": "imagem_em_base_64"
       
}

```

## Componentes utilizados:

* Serverless backend (AWS Lambda)[https://aws.amazon.com/pt/lambda/]

## Implantação

Para implantar, compacte todas bibliotecas das dependências.

```
mkdir deploy
pip install -r .\requirements.txt -t deploy
copy app.py deploy
cd deploy
zip -r function.zip .
```

Com o arquivo ```function.zip``` via Console da AWS você pode enviar o pacote para atualizar.
Ou pode optar por enviar diretamente pelo comando AWS CLI, deste que tenha as permissões necessárias para implantar um Lambda.

```
aws lambda update-function-code --function-name detectar-face --zip-file fileb://function.zip
```

## Uso

Realize um request simples do tipo "post" enviando o payload citado.
Os retornos seguem o padrão de status de API Rest. Código 200 indica sucesso para o processamento da imagem. Códigos de erro, como 400 indicam restrições que precisam ser verificadas (no "body" contém o detalhamento).
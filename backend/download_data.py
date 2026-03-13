from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")
access_key = os.getenv("ACCESS_KEY")
secret_access_key = os.getenv("SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")

FILES = [
    "cosine_sim.npy",
    "ids_tmdb.pkl",
    "indices.pkl",
    "movies_info.parquet",
]

def get_data():

    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    #Cria a pasta data se não existir
    os.makedirs("artifacts", exist_ok=True)


    for file in FILES:

        local_path = f"artifacts/{file}"

        try:
            #Verifica a última atualização no bucket
            remote = s3.head_object(Bucket=bucket_name, Key=file)["LastModified"].timestamp()

        except ClientError as e:
            print(f"Erro ao verificar {file}: {e}")
            continue
        
        #Se o arquivo local não existir, cria
        if not os.path.exists(local_path):
            print(f"{file} não existe localmente. Baixando...")
            s3.download_file(bucket_name, file, local_path)
            continue
        
        #Verifica a última atualização do arquivo local
        local = os.path.getmtime(local_path)

        #Se estiver desatualizado, atualiza
        if remote > local:
            print(f"{file} desatualizado. Baixando nova versão...")
            s3.download_file(bucket_name, file, local_path)

        else:
            print(f"{file} já está atualizado.")

get_data()

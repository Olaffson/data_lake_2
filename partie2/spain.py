from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

def load_environment_variables():
    """Charger les variables d'environnement depuis le fichier .env."""
    load_dotenv()

def create_service_principal_credential(tenant_id, client_id, client_secret):
    """
    Créer un objet Credential pour un service principal.

    :param tenant_id: ID du locataire Azure
    :param client_id: ID du client (Service Principal)
    :param client_secret: Secret du client (Service Principal)
    :return: Objet ClientSecretCredential
    """
    try:
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        print("Connexion réussie au Service Principal !")
        return credential
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        raise

def get_key_vault_secret(tenant_id, client_id, client_secret, key_vault_name, secret_name):
    """
    Connexion à Azure Key Vault et récupération d'un secret.

    :param tenant_id: ID du locataire Azure
    :param client_id: ID du client (Service Principal)
    :param client_secret: Secret du client (Service Principal)
    :param key_vault_name: Nom du Key Vault
    :param secret_name: Nom du secret à récupérer
    :return: Valeur du secret récupéré
    """
    try:
        key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
        credential = create_service_principal_credential(tenant_id, client_id, client_secret)
        secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
        retrieved_secret = secret_client.get_secret(secret_name)
        print(f"Secret récupéré depuis Key Vault : {retrieved_secret.value}")
        return retrieved_secret.value
    except Exception as e:
        print(f"Erreur lors de l'accès au Key Vault : {e}")
        raise

def generate_container_sas_token(account_name, container_name, credential):
    """
    Générer un SAS token pour un conteneur.

    :param account_name: Nom du compte de stockage
    :param container_name: Nom du conteneur
    :param credential: Objet ClientSecretCredential
    :return: SAS Token pour le conteneur
    """
    try:
        blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net/", credential=credential)

        # Obtenir une User Delegation Key
        delegation_key = blob_service_client.get_user_delegation_key(
            key_start_time=datetime.utcnow(),
            key_expiry_time=datetime.utcnow() + timedelta(hours=1)
        )

        # Générer le SAS Token
        sas_token = generate_container_sas(
            account_name=account_name,
            container_name=container_name,
            user_delegation_key=delegation_key,
            permission=ContainerSasPermissions(read=True, write=True, list=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        print(f"SAS Token généré pour le conteneur '{container_name}'")
        return sas_token
    except Exception as e:
        print(f"Erreur lors de la génération du SAS Token : {e}")
        raise

def upload_file_to_blob(account_name, container_name, sas_token, file_url, blob_name):
    """
    Télécharger un fichier depuis une URL et le charger dans Azure Blob Storage.

    :param account_name: Nom du compte de stockage
    :param container_name: Nom du conteneur
    :param sas_token: SAS token généré pour le conteneur
    :param file_url: URL du fichier à télécharger
    :param blob_name: Nom du blob cible
    """
    try:
        # Télécharger le fichier depuis l'URL
        response = requests.get(file_url, timeout=10)
        response.raise_for_status()

        # Charger le fichier dans Azure Blob Storage
        container_url = f"https://{account_name}.blob.core.windows.net/{container_name}"
        blob_url = f"{container_url}/{blob_name}?{sas_token}"

        headers = {"x-ms-blob-type": "BlockBlob"}
        upload_response = requests.put(blob_url, headers=headers, data=response.content)

        if upload_response.status_code == 201:
            print(f"Fichier chargé avec succès dans '{blob_name}'")
        else:
            print(f"Erreur lors du chargement : {upload_response.status_code} - {upload_response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement du fichier depuis '{file_url}': {e}")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier '{file_url}' dans Azure : {e}")

def extract_spain_urls():
    """Récupérer toutes les URL contenant le mot 'spain' depuis la page."""
    url = "https://insideairbnb.com/get-the-data/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        html_content = response.text

        # Analyser le contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Trouver toutes les balises <a> contenant 'spain'
        links = soup.find_all("a", href=True)  # Trouve toutes les balises <a> avec un href
        spain_urls = [link["href"] for link in links if "spain" in link["href"].lower()]

        return spain_urls

    except Exception as e:
        print(f"Erreur lors de la récupération des URLs : {e}")
        return []

def main():
    # Charger les variables d'environnement
    load_environment_variables()

    # Récupérer les informations d'identification pour le Service Principal 2
    tenant_id2 = os.getenv("TENANT_ID2")
    client_id2 = os.getenv("CLIENT_ID2")
    client_secret2 = os.getenv("CLIENT_SECRET2")
    key_vault_name = os.getenv("KEY_VAULT_NAME")
    secret_name = "CLIENTSECRET1"

    # Récupérer le client_secret1 depuis Key Vault via le Service Principal 2
    client_secret1 = get_key_vault_secret(tenant_id2, client_id2, client_secret2, key_vault_name, secret_name)

    # Récupérer les informations d'identification pour le Service Principal 1
    tenant_id1 = os.getenv("TENANT_ID1")
    client_id1 = os.getenv("CLIENT_ID1")

    # Créer l'objet Credential pour le Service Principal 1
    credential = create_service_principal_credential(tenant_id1, client_id1, client_secret1)

    # Générer un SAS Token pour le conteneur
    account_name = "okdatalakestoragegen2"
    container_name = "ok-container-part2"
    sas_token = generate_container_sas_token(account_name, container_name, credential)

    # Extraire les URL contenant "spain"
    spain_urls = extract_spain_urls()

    # Charger chaque fichier dans le conteneur
    for file_url in spain_urls:
        blob_name = file_url.split("/")[-1]  # Nom du fichier depuis l'URL
        print(f"Traitement de l'URL : {file_url}")
        upload_file_to_blob(account_name, container_name, sas_token, file_url, blob_name)

if __name__ == "__main__":
    main()

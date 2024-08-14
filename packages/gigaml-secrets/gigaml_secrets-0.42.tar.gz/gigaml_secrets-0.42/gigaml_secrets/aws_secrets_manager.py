import os
import time
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from gigaml_secrets.secrets_manager import SecretsManager  # Absolute import

class CachedSecretsManager:
    def __init__(self, env, ttl=10):
        self.env = env
        self.secrets_manager = SecretsManager()
        self.ttl = ttl
        self.cache = {}

    def get_secret(self, secret_name):
        prefixed_secret_name = f"{self.env}/{secret_name}"
        current_time = time.time()
        if prefixed_secret_name in self.cache:
            secret, timestamp = self.cache[prefixed_secret_name]
            if current_time - timestamp < self.ttl:
                print(f"Fetching {secret_name} from cache")
                return secret

        print(f"Fetching {secret_name} from API call")
        secret = self.secrets_manager.get_secret(prefixed_secret_name)
        self.cache[prefixed_secret_name] = (secret, current_time)
        os.environ[secret_name] = secret  # Store without the prefix in environment variables
        return secret

def load_secrets(env, secret_names):
    """
    Load secrets from AWS Secrets Manager and set them as environment variables.
    """
    client = boto3.client('secretsmanager')

    for secret_name in secret_names:
        try:
            get_secret_value_response = client.get_secret_value(SecretId=f"{env}/{secret_name}")
            secret = get_secret_value_response['SecretString']
            os.environ[secret_name] = secret
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
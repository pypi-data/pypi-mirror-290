# My Secrets Manager

A library to manage AWS secrets with caching and environment variable integration.

## Setup

Follow these steps to set up the environment and install the dependencies:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/my_secrets_manager.git
    cd my_secrets_manager
    ```

2. **Run the setup script**:
    ```sh
    ./setup_and_run.sh
    ```

This script will:
- Create a virtual environment named `myenv`.
- Activate the virtual environment.
- Upgrade `pip` to the latest version.
- Install the package and its dependencies (`boto3` and `botocore`).
- Deactivate the virtual environment.

## Usage

After setting up the environment, you can activate the virtual environment and use the library in your scripts:

1. **Activate the virtual environment**:
    ```sh
    source myenv/bin/activate
    ```

2. **Use the library in your script**:
    ```python
    from aws_secrets_manager import load_secrets
    import os

    # Specify the environment and list of secrets to load
    env = 'dev'
    secret_names = ['ADMIN_API_KEY', 'BACKEND_API']
    load_secrets(env, secret_names)

    # Now you can access the secrets from environment variables
    admin_api_key = os.getenv('ADMIN_API_KEY')
    backend_api = os.getenv('BACKEND_API')

    print(admin_api_key)
    print(backend_api)
    ```

3. **Deactivate the virtual environment when done**:
    ```sh
    deactivate
    ```

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
import os
import subprocess
import json
import click
import boto3

def is_sourced():
    return os.getenv('__IS_SOURCED__') == '1'

def list_profiles():
    config_file = os.path.expanduser("~/.aws/config")
    if not os.path.exists(config_file):
        click.echo("AWS config file not found.")
        return

    with open(config_file, 'r') as f:
        lines = f.readlines()

    profiles = [line.split()[1][:-1] for line in lines if line.startswith('[profile')]
    click.echo("The following are configured profiles in ~/.aws/config:")
    for profile in profiles:
        click.echo(profile)

def get_aws_credentials(profile_name, save=False):
    session = boto3.Session(profile_name=profile_name)
    sso_client = session.client('sso')

    aws_account_id = session.get_config_variable('sso_account_id')
    aws_role_name = session.get_config_variable('sso_role_name')
    aws_region = session.get_config_variable('sso_region')

    sso_cache_dir = os.path.expanduser("~/.aws/sso/cache")
    sso_cache_files = [os.path.join(sso_cache_dir, f) for f in os.listdir(sso_cache_dir)]
    if not sso_cache_files:
        click.echo("No SSO cache files found. Please login first.")
        return

    with open(sso_cache_files[0], 'r') as f:
        access_token = json.load(f).get('accessToken')

    if not access_token:
        click.echo("Failed to retrieve the access token from the SSO cache file.")
        return

    response = sso_client.get_role_credentials(
        accountId=aws_account_id,
        roleName=aws_role_name,
        accessToken=access_token,
    )

    credentials = response['roleCredentials']
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['accessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['secretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['sessionToken']
    os.environ['AWS_PROFILE'] = profile_name

    if save:
        with open(os.path.expanduser("~/.aws/credentials"), 'w') as cred_file:
            cred_file.write(f"[default]\n")
            cred_file.write(f"aws_access_key_id = {credentials['accessKeyId']}\n")
            cred_file.write(f"aws_secret_access_key = {credentials['secretAccessKey']}\n")
            cred_file.write(f"aws_session_token = {credentials['sessionToken']}\n")

@click.command()
@click.argument('profile_name', required=False)
@click.option('--list', 'list_profiles_flag', is_flag=True, help="List all profiles in ~/.aws/config")
@click.option('--save', is_flag=True, help="Save credentials to ~/.aws/credentials")
def main(profile_name, list_profiles_flag, save):
    if list_profiles_flag:
        list_profiles()
        return

    if not profile_name:
        click.echo(main.__doc__)
        return

    get_aws_credentials(profile_name, save)

if __name__ == '__main__':
    main()

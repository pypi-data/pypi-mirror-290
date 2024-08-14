import subprocess
import os
import sys
from deploybot.utils.config import get_config
from deploybot.utils.parser import extract_stack_name

def git_command(command, cwd, capture_output=True, check=True):
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if capture_output:
        print(result.stdout)
    if result.returncode != 0 and check:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)
    return result

def pull_latest_changes(base_path):
    try:
        git_command(['git', 'pull'], cwd=base_path)
        print("Git pull successful.")
    except subprocess.CalledProcessError as e:
        print("Git pull failed: {}".format(e))
        print("Detailed error log: {}".format(e.stderr))
        print("Please resolve the conflicts manually or stash your changes and clean untracked files before retrying.")
        return False
    return True

def switch_branch(base_path, target_branch):
    try:
        git_command(['git', 'checkout', target_branch], cwd=base_path)
        print("Switched to branch: {}".format(target_branch))
    except subprocess.CalledProcessError as e:
        print("Failed to switch to branch: {}. Stashing changes and retrying...".format(target_branch))
        git_command(['git', 'stash'], cwd=base_path)
        try:
            git_command(['git', 'checkout', target_branch], cwd=base_path)
            print("Switched to branch: {} after stashing changes.".format(target_branch))
        except subprocess.CalledProcessError as retry_e:
            print("Failed to switch to branch after stashing: {}".format(retry_e))
            print("Detailed error log: {}".format(retry_e.stderr))
            return False

    return pull_latest_changes(base_path)

def check_and_switch_branch(environment, base_path):
    try:
        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=base_path, universal_newlines=True).strip()
        target_branch = 'dev' if environment == 'staging' else 'master'

        print("Environment: {}".format(environment))
        print("Current Branch: {}".format(current_branch))

        if current_branch != target_branch:
            if not switch_branch(base_path, target_branch):
                return False
            current_branch = target_branch
        else:
            if not pull_latest_changes(base_path):
                return False

        if (environment == 'staging' and current_branch != 'dev') or (environment == 'production' and current_branch != 'master'):
            print("Warning: {} environment selected but branch is {}. Exiting.".format(environment, current_branch))
            return False

        print("Branch check passed for environment {} and branch {}".format(environment, current_branch))
        os.environ['BUILDKITE_BRANCH'] = current_branch
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to determine current branch: {}".format(e))
        return False

def run_script(script_path, env_vars, base_path):
    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    env_vars['LC_ALL'] = 'en_US.UTF-8'
    env_vars['LANG'] = 'en_US.UTF-8'
    env_vars['ENV'] = env_vars['ENVIRONMENT']
    try:
        process = subprocess.Popen(
            ['bash', '-c', 'cd {} && bash {}/{}'.format(base_path, script_dir, script_name)],
            env=env_vars,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        process.communicate()
        return process.returncode
    except KeyboardInterrupt:
        print("\nScript execution cancelled by user.")
        sys.exit(0)

def set_environment_variables(config):
    environment = config['DEFAULT']['environment']
    aws_account_id = config['DEFAULT']['aws_account_id']
    sam_deployment_bucket = config['DEFAULT']['sam_deployment_bucket']
    buildkite_org_slug = config['DEFAULT']['buildkite_org_slug']
    buildkite_pipeline_slug = config['DEFAULT']['buildkite_pipeline_slug']

    if not environment or not aws_account_id or not sam_deployment_bucket or not buildkite_org_slug or not buildkite_pipeline_slug:
        print("Configuration not found. Please run 'deploybot configure' first.")
        sys.exit(1)

    os.environ['ENVIRONMENT'] = environment
    os.environ['AWS_ACCOUNT_ID'] = aws_account_id
    os.environ['SAM_DEPLOYMENT_BUCKET'] = sam_deployment_bucket
    os.environ['BUILDKITE_ORG_SLUG'] = buildkite_org_slug
    os.environ['BUILDKITE_PIPELINE_SLUG'] = buildkite_pipeline_slug

def remove_node_modules(base_path):
    try:
        # Step 1: Delete all node_modules except the ones under ./service/lambda/*/layers/*/nodejs/node_modules
        command_keep = 'find . -name "node_modules" -type d -prune ! -path "./service/lambda/*/layers/*/nodejs/node_modules" -exec rm -rf \'{}\' +'
        subprocess.run(command_keep, shell=True, cwd=base_path, check=True)
        
        # Step 2: Delete any node_modules deeper inside ./service/lambda/*/layers/*/nodejs/node_modules/*
        command_delete_deep = 'find ./service/lambda/*/layers/*/nodejs/node_modules/* -name "node_modules" -type d -prune -exec rm -rf \'{}\' +'
        subprocess.run(command_delete_deep, shell=True, cwd=base_path, check=True)
        
        print("Removed specified node_modules directories.")
    except subprocess.CalledProcessError as e:
        print("Failed to remove node_modules: {}".format(e))

def deploy(service_type, action, service_name):
    print("Starting deploy function with action: {}, service_type: {}, service_name: {}".format(action, service_type, service_name))
    
    if action not in ['deploy']:
        print("Invalid action. Only 'deploy' is supported.")
        return
    
    config = get_config()
    set_environment_variables(config)
    environment = config['DEFAULT']['environment']
    base_path = config['DEFAULT']['base_path']

    # Remove node_modules directories
    remove_node_modules(base_path)

    if environment not in ['production', 'staging']:
        print("Invalid environment.")
        return

    env_path = "{}/service".format(base_path)
    
    if service_type == 'ecs':
        if service_name == 'auth':
            build_script_path = '{}/auth/api/.buildkite/scripts/docker-build'.format(env_path)
            deploy_script_path = '{}/auth/api/.buildkite/scripts/deploy'.format(env_path)
        else:
            build_script_path = '{}/{}/.buildkite/scripts/docker-build'.format(env_path, service_name)
            deploy_script_path = '{}/{}/.buildkite/scripts/deploy'.format(env_path, service_name)

    elif service_type == 'lambda':
        if service_name == 'auth':
            lambda_path = 'auth/lambda'
            deploy_script_name = 'deploy-lambdas'
        elif service_name.startswith('echo-auth-channels'):
            lambda_path = 'auth/{}'.format(service_name)
            deploy_script_name = 'deploy-lambdas'
        else:
            lambda_path = 'lambda/{}'.format(service_name)
            deploy_script_name = 'deploy'

        deploy_script_path = "{}/{}/.buildkite/scripts/{}".format(env_path, lambda_path, deploy_script_name)
        check_versioning_script_path = "{}/{}/.buildkite/scripts/check-versioning".format(env_path, lambda_path)
        
        stack_name = extract_stack_name("{}/{}/template.yaml".format(env_path, lambda_path), environment)
        if not stack_name:
            print("Stack name not found in the template.")
            return
        os.environ['STACK_NAME'] = stack_name
        
        # Run S3 copy command before executing the deploy script
        s3_command = ("aws s3 cp s3://{}/{}/buildkite/sam/config/{}/{}/{}/samconfig.toml {}/{}/samconfig.toml".format(
            os.environ['SAM_DEPLOYMENT_BUCKET'], environment, os.environ['BUILDKITE_ORG_SLUG'], os.environ['BUILDKITE_PIPELINE_SLUG'], stack_name, env_path, lambda_path))
        try:
            subprocess.run(s3_command, shell=True, check=True)
            print("SAM config copied successfully.")
        except subprocess.CalledProcessError as e:
            print("Failed to copy SAM config: {}".format(e))
            return
    else:
        print("Invalid service type. Only 'ecs' or 'lambda' are supported.")
        return

    if not check_and_switch_branch(environment, base_path):
        print("Branch check failed. Exiting action.")
        return

    if service_type == 'ecs':
        if not os.path.exists(build_script_path):
            print("Build script not found at {}. Skipping build step.".format(build_script_path))
            build_script_path = None

        if not os.path.exists(deploy_script_path):
            print("Deploy script not found at {}. Please provide the correct service name.".format(deploy_script_path))
            return

        if build_script_path:
            print("Running build script: {}".format(build_script_path))
            run_script(build_script_path, os.environ, base_path)
        
        print("Running deploy script: {}".format(deploy_script_path))
        run_script(deploy_script_path, os.environ, base_path)

    elif service_type == 'lambda':
        if not os.path.exists(deploy_script_path):
            print("Deploy script not found at {}. Please provide the correct service name.".format(deploy_script_path))
            return

        print("Running deploy script: {}".format(deploy_script_path))
        run_script(deploy_script_path, os.environ, base_path)

        if os.path.exists(check_versioning_script_path):
            print("Running check versioning script: {}".format(check_versioning_script_path))
            run_script(check_versioning_script_path, os.environ, base_path)
        else:
            print("Check versioning script not found at {}.".format(check_versioning_script_path))

def migrate(db_type):
    config = get_config()
    set_environment_variables(config)
    environment = config['DEFAULT']['environment']
    base_path = config['DEFAULT']['base_path']

    # Remove node_modules directories
    remove_node_modules(base_path)
    
    if not check_and_switch_branch(environment, base_path):
        print("Branch check failed. Exiting action.")
        return

    script_path = '{}/.support/deploybot/migrate'.format(base_path)
    if db_type == 'mysql':
        if not os.path.exists(script_path):
            print("Migration script not found at: {}".format(script_path))
            return
        print("Running migration script for MySQL: {}".format(script_path))
        env_vars = os.environ.copy()
        run_script(script_path, env_vars, base_path)
    else:
        print("Invalid database type. Only 'mysql' is supported.")

def main_ecs(args):
    if args.action == 'deploy':
        deploy('ecs', args.action, args.service_name)
    else:
        print("Invalid action. Only 'deploy' is supported for ECS.")

def main_lambda(args):
    if args.action == 'deploy':
        deploy('lambda', args.action, args.service_name)
    else:
        print("Invalid action. Only 'deploy' is supported for Lambda.")

def main_migrate(args):
    migrate(args.db_type)

import boto3
import base64
import sys

from hgext.fsmonitor.watchmanclient import client
try :
    repository_name = sys.argv[1]
    branch_name =sys.argv[2]
    file_path = sys.argv[3]
    buildNumber=sys.argv[4]

    client = boto3.client('codecommit')

    response = client.get_file(
        repositoryName=repository_name,
        commitSpecifier=branch_name,
        filePath=file_path
    )

    file_content =response['fileContent'].decode()
    comitId=response['commitId']

    new_first_line = "dockerTag: "+buildNumber

    # Replace the first line in the file content
    lines = file_content.split('\n')
    lines[0] = new_first_line
    updated_content = '\n'.join(lines)

    # Push the updated file back to the repository
    client.put_file(
        repositoryName=repository_name,
        branchName=branch_name,
        fileContent=updated_content,
        filePath=file_path,
        fileMode='NORMAL',  # or 'EXECUTABLE' if needed
        parentCommitId=comitId,
        commitMessage="updated value.yaml with = "+updated_content,
        name="jenkins-script",
        email="jenkins-script@ss"
    )
except Exception as e:
    print(f"HelmUpdator script failed with:- {e}")

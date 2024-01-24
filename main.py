import csv
import requests
from requests.auth import HTTPBasicAuth

''' Intial Setup '''
username = '<Add Here>' # Navigate to your Profile Image -> Account Settings -> Username
appPassword = '<Add Here>' # Navigate to your Profile Image -> App Passwords -> Create App Password (Admin and Read for all permissions)
team = '<Add Here>'

respositoriesURL = 'https://api.bitbucket.org/2.0/repositories/%s?pagelen=10&fields=next,values.links.clone.href,values.slug' % team

''' Create CSV report structure for reporting '''
file =  open('results.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(["Repository Name", "Repository Link", "Branch Restrictions", "Group Access", "User Access"])

while respositoriesURL is not None:
    ''' Fetching list of all the repositories under workspace '''
    response = requests.get(respositoriesURL, auth=HTTPBasicAuth(username, appPassword))
    page_json = response.json()

    for repo in page_json['values']:
        repositoryName = repo['slug']
        repositoryLink = repo['links']['clone'][0]['href']
        repositoryBranchRestrictions = []
        repositoryGroupAccess = []
        repositoryUserAccess = []

        print("Repository Name: " + repo['slug'])
        # print("Repository Link: " + repo['links']['clone'][0]['href'])

        ''' Fetch branch restrictions per repository '''
        branchRestrictionURL = 'https://api.bitbucket.org/2.0/repositories/<Add Here>/%s/branch-restrictions' % repositoryName
        response = requests.get(branchRestrictionURL, auth=HTTPBasicAuth(username, appPassword))
        results = response.json()
        if results['values'] == []:
            repositoryBranchRestrictions.append("None")
            # print("Repository Branch Restrictions: None")
        else:
            for repo in results['values']:
                repositoryBranchRestrictions.append('Branch Name: ' + repo['pattern'] + ' , Restriction Name: ' + repo['kind'])
                # print("Repository Branch Restriction: " + '(Branch Name: ' + repo['pattern'] + ' , Restriction Name: ' + repo['kind'] + ')')

        ''' Fetch branch group access per repository '''
        groupAccessURL = 'https://api.bitbucket.org/2.0/repositories/<Add Here>/%s/permissions-config/groups' % repositoryName
        response = requests.get(groupAccessURL, auth=HTTPBasicAuth(username, appPassword))
        results = response.json()
        if results['values'] == []:
            repositoryGroupAccess.append("None")
            # print("Repository Group Access: None")
        else:
            for repo in results['values']:
                repositoryGroupAccess.append(repo['group']['slug'])
                # print("Repository Group Access: " + repo['group']['slug'])

        ''' Fetch branch user access per repository '''
        userAccessURL = 'https://api.bitbucket.org/2.0/repositories/<Add Here>/%s/permissions-config/users' % repositoryName
        response = requests.get(userAccessURL, auth=HTTPBasicAuth(username, appPassword))
        results = response.json()
        if results['values'] == []:
            repositoryUserAccess.append("None")
            # print("Repository User Access: None")
        else:
            for repo in results['values']:
                repositoryUserAccess.append(repo['user']['display_name'] + ' , ' + repo['permission'])
                # print('Repository User Access: ' + repo['user']['display_name'] + ' , Permissions: ' + repo['permission'])

        ''' Dump results in a CSV file '''
        # "Repository Name", "Repository Link", "Branch Restrictions", "Group Access", "User Access"
        writer.writerow([repositoryName, repositoryLink, repositoryBranchRestrictions, repositoryGroupAccess, repositoryUserAccess])

    respositoriesURL = page_json.get('next', None)

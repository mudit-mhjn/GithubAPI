from django.http import HttpResponse, JsonResponse
import requests
from github import Github
#from github import InputGitTreeElement
import json
import base64


def git_get(request):
	username = request.GET.get('username')
	repo_name = request.GET.get('repository')
	branch = request.GET.get('branch')
	address = request.GET.get('address')
	file_name = request.GET.get('file')
	if address == None:
		raw_url = 'https://raw.githubusercontent.com/{}/{}/{}/{}'.format(username, repo_name, branch, file_name)
	else:
		raw_url = 'https://raw.githubusercontent.com/{}/{}/{}/{}/{}'.format(username, repo_name, branch, address, file_name)
	content = requests.get(raw_url)
	print(content.text)
	return JsonResponse({'file_content': content.text})

def git_commit(request):
	username = request.GET.get('username')
	password = request.GET.get('password')
	token = Github(username, password)

	repo_name = request.GET.get('repository')
	file_address = request.GET.get('address')
	file_name = request.GET.get('file_name')
	repo = token.get_repo('{}/{}'.format(username, repo_name))
	branch_name = request.GET.get('branch', 'codeio')
	updated_content = request.GET.get('file_content')
	commit_message = request.GET.get('commit_msg')

	if file_address == None:
		contents = repo.get_contents(file_name)
	else:
		contents = repo.get_contents('{}/{}'.format(address, file_name))
	print(contents.path, contents.sha)
	print(contents)
	commits = repo.update_file(contents.path, commit_message, updated_content, contents.sha, branch=branch_name)
	return JsonResponse(commits)


"""
def git_commit(requesst):
	username = request.GET.get('username')
	password = request.GET.get('password')
	tocken = GitHub(username, password)
	repo_name = requests.GET.get('repository')
	file_name = request.GET.get('file')
	branch = request.GET.get('branch_name', 'codeio')
	commit_message = request.GET.get('commit_msg')
	url_path = "https://api.github.com/repos/{}/branches/{}".format(repository, branch)
	
	r1 = requests.get(url_path, auth=(username, token))
	if not r1:
		return JsonResponse({'Error': 'Error while retriving branches.'
							 'Reason': '{}, {}'.format(r1.text, r1.status_code)})
	r1Json = r1.json()
	treeurl = r1Json['commit']['commit']['tree']['url']

	r2 = requests.get(treeurl, auth=(username, token))
	if not r2:
		return JsonResponse({'Error': 'Error while retriving commits.'
							 'Reason': '{}, {}'.format(r2.text, r2.status_code)})
	r2Json = r2.json()
	sha = None
	for files in r2Json['tree']:
		if files['path']==file_name:
			sha = file['sha']
			break
	if sha==None:
		return JsonResponse({'Error': 'Did not find the file in github'})
"""

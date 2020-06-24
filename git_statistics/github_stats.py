#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv

import requests
from bs4 import BeautifulSoup, Tag

from github import Github
from github_token import GITHUB_TOKEN

def get_num_cs_files(repo_link):

    #link to the search area
    repo_link = repo_link.strip() + '/search?l=C%23'
    
    #get the html
    html = requests.get(repo_link)
    html = html.text

    #read only H3 tag
    soup = BeautifulSoup(html, features="lxml")
    filtered = soup.find_all('h3')

    #token to extract the results
    token = ' code results'

    #get onle the tag that have the target info
    
    cs_classes = 0

    for f in filtered:
        if token in str(f):
            
            (before, token, after) = str(f).partition(token)
            cs_classes = before.split()[1] 
            print('Number of C# classes: {}'.format(cs_classes))

    return cs_classes




def get_repo_information(repo, repo_link):
    
    #Get branches for a repo
    branches = repo.get_branches()
    branches_list = []
    for branch in branches:
        branches_list.append(branch)

    print('Number of branchs: {}'.format(len(branches_list)))

    #Get commits to a repo
    commits = repo.get_commits()
    commits_sha_list = []
    for commit in commits:
        commits_sha_list.append(commit.sha)

    print("Number of commits: {}".format(len(commits_sha_list)))

    #Get contributors to a repo
    contributors = repo.get_contributors()
    contributors_list = []
    for c in contributors:
        contributors_list.append(c)
    print("Number of contributors: {}".format(len(contributors_list)))

    #Get forks for a repo
    forks = repo.get_forks()
    forks_list = []
    for c in forks:
        forks_list.append(c)
    print("Number of forks: {}".format(len(forks_list)))


    #Get subscribers for a repo
    subscribers = repo.get_subscribers()
    subscribers_list = []
    for s in subscribers:
        subscribers_list.append(s)
    print("Number of subscribers: {}".format(len(subscribers_list)))

    #Get watchers of a repo
    watchers = repo.get_watchers()
    watchers_list = []
    for w in watchers:
        watchers_list.append(w)
    print("Number of watchers: {}".format(len(watchers_list)))

    cs_classes = get_num_cs_files(repo_link)

    #Repository, Classes, Branches, Commits, Contributors, Forks, Subscribers, Stars
    return [repo, cs_classes, len(branches_list), len(commits_sha_list), len(contributors_list),  len(forks_list),  len(subscribers_list), len(watchers_list)]
    

if __name__ == "__main__":

    #login via token
    g1 = Github(GITHUB_TOKEN)

    results = []

    with open('nonvr-repos.txt', 'r') as repos_list:

        for repo_link in repos_list:
            
            #split the repository link to get only the name of the repo
            (before, token, after) = repo_link.partition('github.com/')
            
            #get the repository name
            repo_name = after.strip()

            print('Repo Name:', repo_name)
            #feach the repo
            repo = g1.get_repo(repo_name)

            #get the repo info
            r = get_repo_information(repo, repo_link)
            
            #add the results of a repo into a list
            results.append(r)
    
    
    #define the configs of a csv file
    csv.register_dialect('myDialect',
                        delimiter=',',
                        quoting=csv.QUOTE_ALL)

    #write the results into a csv file
    with open('github_stats.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='myDialect')
        writer.writerows(results)
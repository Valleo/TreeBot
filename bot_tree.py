import praw
import yaml
import random


def setOfUsersToInvite(listOfUsers, amountToInvite, element):
    if (amountToInvite <= 0):
        return set()
    if (len(listOfUsers) <= 0):
        return set()
    random.shuffle(listOfUsers)
    selectedUser = listOfUsers.pop(0)
    setOfSelectedUser = setOfUsersToInvite(listOfUsers, amountToInvite-1, selectedUser)
    if (element != None):
        setOfSelectedUser.add(element)
    return setOfSelectedUser

print("Launching if the invitation bot")

with open('../passwords.yml', 'r') as file:
    password_service = yaml.safe_load(file)

reddit = praw.Reddit(
    client_id=password_service['client_id'],
    client_secret=password_service['client_secret'],
    password=password_service['password'],
    user_agent=password_service['user_agent'],
    username=password_service['username'],
)

with open('subs.yml', 'r') as file:
    subs_service = yaml.safe_load(file)

subs = subs_service['subs']



print(reddit.user.me())
for subreddit in reddit.user.subreddits():
    print(subreddit)

setOfUsers = set()


for subToFindPeople in subs:
    print("search users in sub ", subToFindPeople)
    subreddit = reddit.subreddit(subToFindPeople)
    for submission in subreddit.new(limit=25):
        setOfUsers.add(submission.author.name)

mockTreeSubreddit = reddit.subreddit(subs_service['subToInviteIn'])
setOfCurrentMembers = set()

for member in mockTreeSubreddit.contributor():
    setOfCurrentMembers.add(member.name)

setOfCandidats = setOfUsers.difference(setOfCurrentMembers)

listOfCandidats = list(setOfCandidats)

print("selected users to invite : ", setOfUsersToInvite(listOfCandidats, subs_service['invitationAmount'], None))



#mockTreeSubreddit.contributor.add("Valloross")


    
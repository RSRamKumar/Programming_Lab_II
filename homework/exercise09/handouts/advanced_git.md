# [Advanced Git](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

## [Branching](https://git-scm.com/docs/git-checkout)

A branch in Git is essentially a new pointer that no longer follows the primary branch. This is incredibly useful for no only testing new code before modifying a working version of your software, but also a great way to help avoid merge conflicts when pushing your code. Your new branch will no longer be receiving updates from the master branch, but we will show you how to keep your branch up to date in the [Rebasing](#rebasing) section.  

### How to Create a Branch
#### Terminal/Bash
To create a new branch **AND** have it be tracked by your remote repository:
```
git checkout -b <new_branch> --track origin/<new_branch>
```

To go back to the master branch (or any other branch)
```
git checkout <some_other_branch>
```

To see a list of all branches that your **local** machine is tracking:
```
git branch
```
**NOTE**: There may exist more branches in the **remote** repository, but your system has not been setup to track those.  

If you wish to track a branch that is in the remote repository (also known as **origin**):
```
git checkout --track origin/<some_branch>
```

## [Rebasing](https://git-scm.com/docs/git-rebase)

It will get to the point where you want to update your branch with everything that has been pushed to the master branch (or you want to prepare to [merge](#merging)), so you have to **rebase** your branch i.e. apply all the commits on the master branch to your branch. Rebasing helps to ensure a clean project history since you are incorporating all of the master branch's commits into your new branch's history. Typically, you should only rebase if you are working alone on a branch, shared branches should be only use merging. Rebasing may cause [merge conflicts](#merge-conflicts) that you will have to sort out, but this is good practice especially before attempting to merging your branch into master.

**IMPORTANT NOTE**: Never, and I mean NEVER, rebase the master branch onto some other branch. the master branch is meant to be the working branch with finished, tested code. If you rebase the master branch onto your new branch which contains code that hasn't been tested, then the master branch will now contain this unfinished code and may no longer work. the proper way to add your changes from new branch to master is to merge it.

### How to Rebase Your Branch
#### Terminal/Bash
Go to the branch you want to rebase and rebase it on master:
```
git checkout <my_new_branch>
git rebase master
```

## [Merging](https://git-scm.com/docs/git-merge)
At some point you will want to combine all of your great work back into the master branch so that your software can make use of it. To this, you need to **merge** your branch, that is to join the development histories together. This is the *only* proper way to integrate code from your new to branch to the master branch.

**IMPORTANT** We will only go over how to merge branches using the GitLab browser interface. Merging via command line is very difficult and not recommended.

### GitLab
Once you have pushed your changes to your new branch, login into the repository on GitLab.

If you don't see it then on the left side bar in GitLab go to `Repository -> Branches`

Then go to `Merge Request` for your branch    

#### Submitting Your Merge Request
Write a brief merge request title describing what was added/changed/optimized in this set of commits. You can go into more detail in the description. There are a number of other options you can use in the merge request:
* `Assignee`: Assign the merge request to a specific person. This person will be responsible for actually merging the branches.
* `Labels`: Add labels to the merge request for easier filtering later
* `Source branch`: the new branch with the tested changes
* `Target branch`: the branch that the new code will be applied to (usually master)
* `Delete source branch when merge request is accepted`: Deletes the source branch after merging. This is useful when your group names branches for the new features that are being implemented/tested (optional)
* `Squash commits when merge request is accepted`: Applies all of the changes in the merge request as a single commit (optional)

Finally, click `Submit merge request`

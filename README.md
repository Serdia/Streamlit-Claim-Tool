# initilize a Git repository (if not already initialized):
git init
# Link the remote repository (if not already added) This will NOT create a new repository in GitHub:
git remote add origin https://github.com/Serdia/Streamlit-Claim-Tool.git
# Stage your changes:
git add .
# Commit changes:
git commit -m "Your commit message"
# push changes to GitHub:
git push origin main

# switch repository
git checkout main

------------------------------------------
# remove files from index(stopping git from tracking those files without deleting it from local directory):
git rm --cached .gitignore .env
# remove .venv folder from git but make sure its not deleted from local
git rm -r --cached .venv/
# check current branch: 
git branch
# create main branch if it doesnt exits:
git checkout -b main
# push to main:
git push origin main

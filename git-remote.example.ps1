# Fill in your GitHub repository URL, then run this script from the project root.

$RemoteUrl = "https://github.com/<your-username>/<your-repository>.git"

git remote remove origin 2>$null
git remote add origin $RemoteUrl
git branch -M main
git push -u origin main

import time
import os
import utilum
from . import scripts

gitLfsStream = '''
#remote=`echo "git remote -v"`

git lfs install
git lfs track "*.psd"
git lfs track "*.jpeg"
git lfs track "*.jpg"
git lfs track "*.JPG"
git lfs track "*.png"
git lfs track "*.PNG"
git lfs track "*.mp4"
git lfs track "*.webm"
git lfs track "*.mkv"
git lfs track "*.tar.gz"
git lfs track "*.pdf"
git lfs track "*.heic"
git lfs track "*.HEIC"
git lfs track "*.mov"
git lfs track "*.MOV"
git lfs track "*.ipynb"
git lfs track "*.zip"
git lfs track "*.ckpt"
git lfs track "*.db"
git lfs track "*.sql"

git add .gitattributes
#git config lfs.$remote
'''

def gitConfig(name, email, repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''
    utilum.system.shell(wrapperRegular(
        f'git config --local user.name "{name}"'))
    utilum.system.shell(wrapperRegular(
        f'git config --local user.email "{email}"'))


def gitPushDataBase():
    return

def gitInitOrRegular(repoPath, groupRepoPath, tokenFilePath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    # 1/6
    cmd1 = wrapperRegular(f'''git init --initial-branch=main''')
    utilum.system.shell(cmd1)

    # 2/6
    dstToken = utilum.file.readFile(tokenFilePath).replace("\n", "")
    rUrl = f'https://gitlab-ci-token:{dstToken}@gitlab.com/{groupRepoPath}.git'
    cmd2 = wrapperRegular(f'''git remote set-url origin {rUrl}''')
    cmd22 = wrapperRegular(f'''git remote add origin {rUrl}''')
    # print("debug:cmd2: ", cmd2) # :debug:note comment when pushing
    utilum.system.shell(cmd2)
    utilum.system.shell(cmd22)

    # 2.3 git lfs
    cmd23 = wrapperRegular(f'''{gitLfsStream}''')
    utilum.system.shell(cmd23)

    # 3-5/6
    cmd3 = wrapperRegular(f'''git add .''')
    cmd4 = wrapperRegular(f'''git commit -m "Regular Update"''')
    cmd5 = wrapperRegular(f'''git push origin main''')

    utilum.system.shell(cmd3)
    utilum.system.shell(cmd4)
    utilum.system.shell(cmd5)

    # 6/6
    rUrlClean = f'https://gitlab.com/{groupRepoPath}.git'
    cmd6 = wrapperRegular(f'''git remote set-url origin {rUrlClean}''')
    utilum.system.shell(cmd6)

    return None

def manageDatabases(config):
    cmd1 = scripts.showDatabasesDocker(config.CONTAINER_NAME, config.PASSWORD_FILE_PATH)
    (out, err) = utilum.system.shellRead(cmd1)
    decoded = out.decode('utf-8')
    dbs = decoded.split("\n")
    dbs = dbs[1:-1]

    for databaseName in dbs:
        # [0/3] skip for config.skipDatabases
        if(databaseName in config.SKIP_DATABASES):
            print("Skipping ", databaseName)
            continue

        # [1/3]: db-folder and file init
        outputDbFolderPath = os.path.join(config.STAGE_STORAGE_GROUP_PATH, databaseName) + "/"
        utilum.file.createPath(outputDbFolderPath)

        outputDbFilePath = os.path.join(outputDbFolderPath, databaseName + '.sql')
        exportCmd = scripts.exportDatabaseDocker(
            config.CONTAINER_NAME, config.PASSWORD_FILE_PATH, databaseName, outputDbFilePath)
        utilum.system.shell(exportCmd)

        # [2/3]: git config set
        gitConfig(config.GIT_NAME, config.GIT_EMAIL, outputDbFolderPath)

        # [3/3]: Last Function to Commit
        groupRepoPath = f'''{config.PARENT_GROUP_PATH}/{config.GROUP_NAME}/{databaseName}'''
        gitInitOrRegular(outputDbFolderPath, groupRepoPath, config.TOKEN_FILE_PATH)


def flow(config):
    # 1. Basic File/Folder Inits
    utilum.file.createPath(config.STAGE_STORAGE_GROUP_PATH)

    # 2. Mid Function to Transfer DB Files
    manageDatabases(config)


def start(config):
    config.STAGE_STORAGE_GROUP_PATH = os.path.join(config.STAGE_STORAGE_PATH, config.GROUP_NAME) + "/"
    config.GIT_GROUP_PATH = os.path.join(config.PARENT_GROUP_PATH, config.GROUP_NAME)

    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001

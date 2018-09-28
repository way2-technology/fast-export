from subprocess import check_output
import sys, json, os

def getMergedBranches():
    ''' a list of merged branches, not couting the current branch or master '''
    raw_results = check_output('git branch --merged upstream/master', shell=True)
    return [b.strip() for b in raw_results.split('\n')
        if b.strip() and not b.startswith('*') and b.strip() != 'master']

def loadJson(filePath):
        with open(filePath) as json_data:
            jsonData = json.load(json_data)
            json_data.close()
            return jsonData

def deleteBranch(branch):
    return check_output('git push origin :{}'.format(branch), shell=True)

def removeUnusedBranches(list_branches):
    return [deleteBranch(branch) for branch in list_branches['values'] if list_branches['values']]
        
if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    config_json_path = os.path.join(path,'config.json').replace("\\","/")

    dry_run = '--confirm' not in sys.argv
    if dry_run:
        print('*****************************************************************')
        print('Did not actually delete anything yet, pass in --confirm to delete')
        print('*****************************************************************')
    else:
        removeUnusedBranches(loadJson(config_json_path))
       
from subprocess import check_output
import sys, json, os


def get_merged_branches():
    ''' a list of merged branches, not couting the current branch or master '''
    raw_results = check_output('git branch --merged upstream/master', shell=True)
    return [b.strip() for b in raw_results.split('\n')
        if b.strip() and not b.startswith('*') and b.strip() != 'master']

def load_json(filePath):
        with open(filePath) as json_data:
            jsonData = json.load(json_data)
            json_data.close()
            return jsonData

def delete_branch(branch):
    return check_output('git branch -D %s' % branch, shell=True).strip()


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    config_json_path = os.path.join(path,'config.json').replace("\\","/")
    load_json(config_json_path)

    dry_run = '--confirm' not in sys.argv
    for branch in get_merged_branches():
        if dry_run:
            print(branch)
        else:
            print(delete_branch(branch))
    if dry_run:
        print('*****************************************************************')
        print('Did not actually delete anything yet, pass in --confirm to delete')
        print('*****************************************************************')
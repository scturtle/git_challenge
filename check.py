#!/usr/bin/env python3
import sys
from subprocess import check_output

def sh(cmd):
    return check_output(cmd, shell=True).strip().decode()

def get_branch():
    if is_bisecting():
        return 'bisect'
    branch = sh('git rev-parse --abbrev-ref HEAD')
    if branch.endswith('_test'):
        branch = branch[:-5]

def is_bisecting():
    return sh('git bisect log') != 'We are not bisecting.'

def commit_and_messages():
    return [l.split(' ', 1) for l in sh("git log --abbrev-commit --pretty=format:'%h %s'").split('\n')]

def file_content(fn='file'):
    return open(fn).read().strip()

def git_diff():
    return [l for l in sh("git diff HEAD").split('\n')if l and l[0] in '-+']

def git_diff_between(older, newer):
    return [l for l in sh("git diff {} {}".format(older, newer)).split('\n')if l and l[0] in '-+']

def check_pull_diff():
    messages = [m for _, m in commit_and_messages()]
    assert messages == ['d', 'c', 'b', 'a'], messages
    content = file_content()
    assert content == 'a\nb\nc\nd', repr(content)
    assert git_diff() == []

def init_pull_dirty():
    open('file', 'w').write('a\nb\nc\nd')

def check_pull_dirty():
    messages = [m for _, m in commit_and_messages()]
    assert messages == ['c', 'b', 'a'], messages
    content = file_content()
    assert content == 'a\nb\nc\nd', repr(content)
    diff = git_diff()
    assert diff == ['--- a/file', '+++ b/file', '+d'], diff

def check_pick():
    messages = [m for _, m in commit_and_messages()]
    assert messages == ['c', 'a'], messages

def check_squash_and_reorder():
    messages = [m for _, m in commit_and_messages()]
    assert messages == ['b & c', 'd & e', 'a'], messages
    [bc_id, de_id, a_id] = [i for i, _ in commit_and_messages()]
    diff_a_de = git_diff_between(a_id, de_id)
    assert diff_a_de == ['--- a/file', '+++ b/file', '+e', '+d'], diff_a_de
    diff_de_bc = git_diff_between(de_id, bc_id)
    assert diff_de_bc == ['--- a/file', '+++ b/file', '+b', '+c'], diff_de_bc

def check_bisect():
    assert git_diff() == []
    content = file_content()
    if content != '3751248':
        print('This commit is', 'good!' if int(content) < 3751248 else 'bad!')
    else:
        print('You found bad guy!')

def run_init():
    branch = get_branch()
    if branch.endswith('_test'):
        branch = branch[:-5]
    print('init', branch)
    if 'init_' + branch in globals():
        globals()['init_' + branch]()
        print('ok')
    else:
        print('no need')

def run_check():
    branch = get_branch()
    print('checking', branch)
    globals()['check_' + branch]()
    print('ok')

if __name__ == '__main__':
    if any(arg == 'init' for arg in sys.argv):
        run_init()
    else:
        run_check()

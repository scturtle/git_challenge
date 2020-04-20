# Git Challenge

初始化：
```
$ git clone https://github.com/scturtle/git_challenge.git
$ cd git_challenge
$ git branch -a
```

每个 challenge 在各自名字的 branch 下，比如：
```
$ git checkout amend
```

`check.py` 在 master 里，拷贝到当前目录：
```
$ git checkout master check.py
$ git reset check.py
```

有的 challenge 前需执行初始化：
```
$ ./check.py init
```

看是否完成 challenge：
```
$ ./check.py
```

### amend

**初始化**后把当前的修改（`+c`）添加当之前的 commit "b" 里，并修改 message 为 "b & c"。

### uncommit

**初始化**后 undo 之前的 commit "c"。

### pick

当前有 commit "a", `origin/pick_from` 下有 commit "c", "b", "a"。只把 "c" 加到本地，使得本地有 commit "c" 和 "a"。

### squash_and_reorder

本地有五个 commit。合并并重排一些 commit，使得最终历史依次是这三个："b & c"，"d & e"，"a"。

### pull_diff

从 `origin/pull_diff_remote` 合并但不要 merge。使得最终历史是："d"，"c"，"b"，"a"。

### pull_dirty

**初始化**，从 `origin/pull_dirty_remote` 拉取合并并保持现有未 commit 内容。

### bisect

找到第一个 bad commit。

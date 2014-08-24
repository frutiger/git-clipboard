## git-clipboard - Transport git bundles over the clipboard

Simplifies sending and receiving git content via the clipboard.  This is
typically useful for remote desktop interfaces where networking and file
transfer is prohibited.

### Example

Put all changes since `origin/master` onto the clipboard:

    $ git clipboard put origin/master..HEAD

In some other repo, fetch something previously placed in the clipboard to
`FETCH_HEAD`:

    $ git clipboard get

### Installation

Clone the repository and symlink `git-clipboard.py` to `git-clipboard`
somewhere in your `PATH`.

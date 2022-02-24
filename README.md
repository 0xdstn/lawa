# lawa

lawa is a flat-file journaling script written in Python. You can prepend words with a `+` to mark them as "positive", a  `-` to mark them as "negative", and a `~` to mark them as tags.

When viewing a post, it will display the key words in green, red, or blue (+,-,~), and show a count of how positive or negative a post was.

The intent is to journal, but with statistics on how you were feeling that day. The goal isn't to have only positive posts, but instead to assess your mental state over time. It's up to you to determine which words are positive or negative. Sometimes the same word could even be one or the other, depending on the context. It's all about how you feel.

## Etymology

The name lawa comes from the language Toki Pona. It means "head" and felt appropriate since you are documenting your state of mind.

## Data

All data is stored in a single `~/.lawa` file. Each day is prepended to the file and starts with the date. Line breaks are represented with a `/`.

## Timezone

There is a hard coded timezone of `America/Los_Angeles` in the script. You can comment it out to use your system timezone, or specify your own. Just modify the timezone line in the lawa.py file.

## Usage

You can use the following commands (example: `lawa.py add`):

- `help` - Displays the help screen
- `about` - Displays information about this program
- `all` - Display all posts
- `list` - Display a list of all posts
- `today` - Display today's post
- `last` - Display the most recent post
- `view [YYYY-MM-DD]` - Display the specified post
- `tagged [+,-,~][tag]` - Display all posts with the specified tag
- `add` - Create or update today's post
- `edit [YYYY-MM-DD]` - Edit the specified post
- `delete [YYYY-MM-DD]` - Delete the specified post

## Release notes

- `v1.0.0` Initial release

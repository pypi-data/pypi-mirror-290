# Terminal Markup Language (tml)
- A python library to make the output of colored text in the terminal easier and more readable.

## Example
```python
from tml import markup
print(markup("<red>this text is <bold>red</bold></red> and the following is <green>green</green>"))
```

Alternatively, you can use the `mprint()` function, which is a convenient shortcut.
```python
from tml import mprint
mprint("<red>this text is <bold>red</bold></red> and the following is <green>green</green>")
```

You don't need to close the tag explicitly if it is not needed.
```python
print(markup("<on-green><blue>this text has blue foreground on green background colors"))
```

If you would like to print brackets, use them in doubles:
```python
print(markup("<bold>This is <<example>></bold>"))
```

## Available Tags
### Foreground
- `<black>`
- `<red>`
- `<green>`
- `<yellow>`
- `<blue>`
- `<magenta>`
- `<cyan>`
- `<white>`
- `<bright-black>`
- `<light-black>`
- `<bright-red>`
- `<light-red>`
- `<bright-green>`
- `<light-green>`
- `<bright-yellow>`
- `<light-yellow>`
- `<bright-blue>`
- `<light-blue>`
- `<bright-magenta>`
- `<light-magenta>`
- `<bright-cyan>`
- `<light-cyan>`
- `<bright-white>`
- `<light-white>`

### Background
- `<on-black>`
- `<on-red>`
- `<on-green>`
- `<on-yellow>`
- `<on-blue>`
- `<on-magenta>`
- `<on-cyan>`
- `<on-white>`
- `<on-bright-black>`
- `<on-light-black>`
- `<on-bright-red>`
- `<on-light-red>`
- `<on-bright-green>`
- `<on-light-green>`
- `<on-bright-yellow>`
- `<on-light-yellow>`
- `<on-bright-blue>`
- `<on-light-blue>`
- `<on-bright-magenta>`
- `<on-light-magenta>`
- `<on-bright-cyan>`
- `<on-light-cyan>`

### Attributes
- `<bold>`
- `<b>`
- `<dark>`
- `<italic>`
- `<i>`
- `<underline>`
- `<u>`
- `<blink>`
- `<reverse>`
- `<concealed>`
- `<strike>`

## Acknowledgement
- This library is inspired by [tml](https://github.com/liamg/tml)
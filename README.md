## Text Formatting and Editing in the Context Menu
> Available on AnkiWeb: <a href="https://ankiweb.net/shared/info/2143302836">https://ankiweb.net/shared/info/2143302836</a>

> GitHub: <a href="https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu">https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu</a>

This addon aims to format and edit texts by clicking items in the context menu (right-click menu) in Anki.
<img src="https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/raw/main/ContextMenu.JPG">

### Item list

1. Text Styling - Bold / Italic / Underline / Strikethrough / Superscript / Subscript
2. Text Color - Red / Green / Blue / Cyan / Magenta / Yellow / Black / White / backRed / backGreen / backBlue / backCyan / backMagenta / backYellow / backBlack / backWhite
3. Font Size - Size 1 / Size 2 / Size 3 / Size 4 / Size 5 / Size 6 / Size 7
4. Font... (Font Dialog)
5. Alignment / List - Justify Left / Justify Center / Justify Right / Justify Full / Indent / Outdent / Insert Unordered List / Insert Ordered List
6. Word Count
7. Insert - Link / Image / Blockquote / Date and Time / Horizontal Line / Special Characters
8. Edit - Cut / Copy / Paste / Select All / Undo / Redo
9. (Clear Format)
10. User Words: You can register your own words and easily input them from the context menu.

### Config

- General Tab
  - (1) Show 'Format / Edit'
    - Show 'Format / Edit' in Editor context menu.
    - Show 'Format / Edit' in Reviewer context menu. (This option may be useful if you rely on the incredibly wonderful addon '<a href="https://ankiweb.net/shared/info/1020366288">Edit Field During Review</a>' or '<a href="https://ankiweb.net/shared/info/385888438">Edit Field During Review (Cloze)</a>.' This is the reason why I created this addon.)
  - (2) Quick Access Items (as listed in the image below)
  - (3) Display the Quick Access items on the first level of the context menu
<img src="https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/raw/main/ConfigWindowGeneral.JPG">

- User Words Tab
  - Show 'User Words' in Editor and Reviewer context menus.
  - Word list:
    - Add/Edit/Remove a single word.
    - Move selected item up/down.
    - Import/Export a list (Please note that the file needs to have a line break after each word.)
  - Display the added words on the first level of the context menu
<img src="https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/raw/main/ConfigWindowUserWords.JPG">

### Note

- This addon uses a deprecated Javascript function "document.execCommand". Official updates to Javascript may affect this addon in the future.

### Changelog

- 2023-07-27
  - Added config window (after this addon is updated, please restart Anki.)
  - Added Quick Access feature
  - Fixed some bugs
- 2023-07-29
  - Added option to display the Quick Access items on the first level of the context menu
- 2023-08-16
  - Added User Words feature

# AUTOMAT
Web automation software for dummies (like me).
- Powered by Python and Selenium
- Write simple commands to perform common actions
- Record and replay sequences of actions from files
- Store sensitive data in the .secrets file, protected by .gitignore (todo: add password protection / encryption)

## Usage

`automat sequence.mat` to run a stored sequence from a file

The `automat` command alone begins a live session.

## Commands

### Out of Sequence
Out of sequence commands are not saved as part of a sequence but typically modify them.

`save [sequence name]`: Save a sequence as a file.

`play [sequence name]`: Begin running an existing sequence file. Sequences can call sequences.

`quicksave`: Create a checkpoint in the sequence. 

`restart`: Go back to the beginning of a sequence and delete saved actions outside of a checkpoint. Repeat current sequence up to most recent checkpoint.

`reset`: Delete all checkpoints and go back to the beginning of a sequence.

`secret [name] [string]`: Save a value to the .secrets file.

### In Sequence
In sequence actions are saved as part of sequences.

`start [url]`: Begin a sequence at a given url.

`goto [url]`: Jump to a url *without* beginning a new sequence.

`grab [query selector]`: Focus on an element, typically a text field or other text input.

`grab_x [xpath]`: As above but uses an xpath instead of a query selector.

`text [string]`: Enter a string of characters into a text field or similar.

`text_s [secret]`: Enter a value from secrets into a text field or similar.

`text_i`: Enter a series of characters from the user into a text field or similar.

`click [query selector]`: Click an element, typically a button.

`click_x [query selector]`: As above but uses an xpath instead of a query selector.

`enter`: Send a physical enter key, typically used to submit forms.

## Example
A simple example to show how a sequence looks.

```
start https://myurl.com
grab #username
text Riley
grab #password
text_s my_pwd
click 
```
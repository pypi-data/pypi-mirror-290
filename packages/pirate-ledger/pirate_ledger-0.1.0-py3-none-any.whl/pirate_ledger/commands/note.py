import questionary

from pirate_ledger import cli
from pirate_ledger.helpers import input_error
from pirate_ledger.sea_notes.note import NoteRecord
from pirate_ledger.sea_notes.sea_notes import SeaNotes


@input_error
def add_note(notes_list: SeaNotes):
    while True:
        title = questionary.text(
            "Arrr, what be the title of yer new note?",
            validate=cli.validators.RequiredValidator
        ).ask()

        if notes_list.find(title):
            print(f"Avast! A note with the title '{title}' already exists. Choose a different title, matey.")
        else:
            break

    content = questionary.text(
        "What be the content of yer note?",
        validate=cli.validators.RequiredValidator
    ).ask()

    record = NoteRecord(title, content)
    notes_list.add_record(record)

    return f"Note titled '{title}' added to the ship's log."


@input_error
def delete_note(notes_list: SeaNotes):
    title = questionary.text(
        "What be the title of the note ye wish to delete?",
        validate=cli.validators.RequiredValidator
    ).ask()

    record = notes_list.find(title)

    if not record:
        return f"Note titled '{title}' not found in the ship's log."

    notes_list.delete(title)
    return f"Note titled '{title}' has been cast into the deep sea."


@input_error
def update_note(notes_list: SeaNotes):
    title = questionary.text(
        "What be the title of the note ye wish to update?",
        validate=cli.validators.RequiredValidator
    ).ask()
    record = notes_list.find(title)

    if not record:
        return f"Note titled '{title}' not found in the ship's log."

    new_title = questionary.text(
        f"Enter the new title (current: {record.note.title}):",
        default=record.note.title,
        validate=cli.validators.RequiredValidator
    ).ask()

    new_content = questionary.text(
        f"Enter the new content (current: {record.note.content}):",
        default=record.note.content,
        validate=cli.validators.RequiredValidator
    ).ask()

    record.note.edit(new_title, new_content)

    return f"Note titled '{title}' has been updated in the ship's log."


@input_error
def search_notes(notes_list: SeaNotes):
    query = questionary.text(
        "What be the title or content ye seek in the ship's log?",
        validate=cli.validators.RequiredValidator
    ).ask()
    return notes_list.list_notes(query)


@input_error
def show_notes(notes_list: SeaNotes):
    return notes_list.list_notes()
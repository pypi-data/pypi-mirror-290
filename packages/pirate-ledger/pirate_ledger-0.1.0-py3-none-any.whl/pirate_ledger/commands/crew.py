import questionary

from pirate_ledger import cli
from pirate_ledger.crew_roster.crew_roster import CrewRoster, CrewMember
from pirate_ledger.helpers import ContactsError, input_error


@input_error
def add_crew_member(crewRooster: CrewRoster):
    name = questionary.text(
        "Arrr, enter the name of the scallywag:",
        validate=cli.validators.RequiredValidator
    ).ask()
    message = "New mate added to the crew."

    contact = crewRooster.find(name)
    if contact:
        if questionary.confirm('This pirate already sails with us! Do ye wish to update their details?').ask():
            message = "Details of the crew member have been updated."
        else:
            return 'Aborting the addition of the crew member.'

    contact = contact or CrewMember(name)
    crewRooster.add_record(contact)
    form = questionary.form(
        address=questionary.text("[Optional] Where does this buccaneer call home?"),
        phone=questionary.text("[Optional] How can we reach this pirate? (Phone number)", validate=cli.validators.PhoneValidator),
        email=questionary.text("[Optional] Where do the seabirds deliver messages? (email)", validate=cli.validators.EmailValidator),
        birthday=questionary.text("[Optional] When did this pirate first see the sea? (birthday in DD.MM.YYYY)", validate=cli.validators.DateValidator),
    )
    fields = form.ask()

    for field, value in fields.items():
        if value:
            setattr(contact, field, value)

    return message


@input_error
def update_crew_member(crewRooster: CrewRoster) -> str:
    name = cli.prompts.ask_contact_name(crewRooster)
    record = crewRooster.find(name)
    if record is None:
        raise ContactsError("This pirate doesn't sail with us!")

    field = questionary.autocomplete('What detail do ye wish to update, matey?', choices=CrewMember.get_fields()).ask()
    if hasattr(record, field):
        new_value = questionary.text(f"Enter the new value for {field}:",
                                     validate=cli.validators.RequiredValidator).ask()
        setattr(record, field, new_value)

        return f"{field.capitalize()} has been updated for this salty sea dog."
    else:
        raise ContactsError(f"Field '{field}' doesn't exist on this pirate's record.")


@input_error
def delete_crew_member(crewRooster: CrewRoster) -> str:
    name = cli.prompts.ask_contact_name(crewRooster)
    record = crewRooster.find(name)

    if record is None:
        raise ContactsError("This pirate doesn't sail with us!")

    crewRooster.delete(name)

    return f"{name} walks the plank! This crew member has been removed from the roster."


@input_error
def show_crew_member(crewRooster: CrewRoster) -> str:
    name = questionary.autocomplete('Enter the name of the pirate ye wish to see:', choices=[*crewRooster.keys()]).ask()
    contact = crewRooster.find(name)

    if contact is None:
       raise ContactsError(f"Arrr, it seems {name} has recently walked the plank and is no longer on the roster!")

    return str(contact)


@input_error
def all_crew_members(crewRooster: CrewRoster) -> str:
    if not crewRooster:
        raise ContactsError("Arrr, the crew roster be empty! Not a single pirate aboard!")

    command_output = "Here be the list of all the scallywags aboard:\n"

    for name, contact in crewRooster.items():
        command_output += str(contact)

    return command_output

@input_error
def crew_birthdays(crewRooster: CrewRoster) -> str:
    output = f"{"Pirate Name":<{10}}{" | "}{"Birthday":<{10}}\n{"-" * 10:<{10}}{" | "}{"-" * 10:<{10}}\n"


    if not crewRooster:
        raise ContactsError("Arrr, the crew roster be empty! Not a single pirate aboard!")

    try:
        delta_days = int(input("How many days ahead do ye wish to check for upcoming birthdays? "))
        birthdays_list = crewRooster.get_upcoming_birthdays(delta_days)

        if not birthdays_list:
            return f"No pirate birthdays for the next {delta_days} days."

        for contact in birthdays_list:
            output += f"{contact['name']:<{15}}{' | '}{contact['congratulation_date']:<{10}}\n"

        return output

    except ValueError:
        return "Arrr, that's not a proper number! Please enter an integer, matey."


@input_error
def search_crew_member(crewRooster: CrewRoster) -> str:
    if not crewRooster:
        raise ContactsError("Arrr, the crew roster be empty! Not a single pirate aboard!")

    search_input = questionary.text(
       "What be ye searching for among the crew, matey?",
        validate=cli.validators.RequiredValidator
    ).ask()

    return crewRooster.search_crew_members(search_input)
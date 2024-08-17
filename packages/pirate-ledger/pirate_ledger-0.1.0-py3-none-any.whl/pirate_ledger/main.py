from pirate_ledger.data_handler import load_data, save_data
from pirate_ledger import listen_commands, CrewRoster, SeaNotes

def main():
    book = load_data("crewroster.pkl", CrewRoster())
    notes = load_data("seanotes.pkl", SeaNotes())

    def on_exit(book, notes):
        save_data(book, "crewroster.pkl")
        save_data(notes, "seanotes.pkl")

    listen_commands(book, notes, on_exit)

if __name__ == "__main__":
    main()

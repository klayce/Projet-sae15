import icalendar
import csv

def ics_to_csv(ics_file, csv_file):
    # Ouvrir le fichier ICS
    with open(ics_file, 'rb') as ics_file:
        cal = icalendar.Calendar.from_ical(ics_file.read())

    # Ouvrir le fichier CSV pour l'écriture
    with open(csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["DTSTAMP", "DTSTART", "DTEND", "SUMMARY", "LOCATION", "DESCRIPTION", "CREATED", "LAST-MODIFIED", "SEQUENCE"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Écrire l'en-tête CSV
        csv_writer.writeheader()

        # Parcourir les composants du calendrier
        for event in cal.walk('VEVENT'):
            event_data = {}

            for field in fieldnames:
                if field == "DTSTART" or field == "DTEND" or field == "CREATED" or field == "LAST-MODIFIED":
                    # Formater les champs de date
                    event_data[field] = event.get(field).dt.strftime('%Y-%m-%dT%H:%M:%S')
                else:
                    event_data[field] = str(event.get(field, ''))

            # Écrire chaque ligne dans le fichier CSV
            csv_writer.writerow(event_data)

    print(f"La conversion de {ics_file} vers {csv_file} est terminée avec succès.")

# Exemple d'utilisation avec le nom de fichier spécifique
ics_to_csv('ADECal (1).ics', 'ADECal-sea15.csv')

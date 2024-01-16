import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def creneaux_disponibles(nom_fichier_csv, date_danalyse):
    data = pd.read_csv(nom_fichier_csv, parse_dates=['DTSTART', 'DTEND'])

    # Filtrer les données pour les créneaux après la date d'analyse et pour les salles "RT-Labo Informatique"
    creneaux_apres_date = data[(data['DTSTART'] >= date_danalyse) & data['LOCATION'].str.startswith('RT-Labo Informatique')]
    resultats = []

    for salle in creneaux_apres_date['LOCATION'].unique():
        creneaux_salle = creneaux_apres_date[creneaux_apres_date['LOCATION'] == salle].sort_values('DTSTART').head(10)

        for _, creneau in creneaux_salle.iterrows():
            resultat = {
                'Salle': salle,
                'Date de début': creneau['DTSTART'],
                'Date de fin': creneau['DTEND']
            }
            resultats.append(resultat)

    creneaux_disponibles_df = pd.DataFrame(resultats)

    # Afficher les 10 prochains créneaux disponibles
    print("Les 10 prochains créneaux disponibles dans les salles RT-Labo Informatique :")
    print(creneaux_disponibles_df)

    # Sauvegarder les résultats dans un fichier CSV avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_file = f'resultats_creneaux_disponibles_{timestamp}.csv'
    creneaux_disponibles_df.to_csv(output_csv_file, index=False)

    # Créer la frise chronologique
    plot_timeline(creneaux_disponibles_df)

def plot_timeline(data):
    plt.figure(figsize=(10, 6))
    for idx, row in data.iterrows():
        plt.barh(row['Salle'], width=row['Date de fin'] - row['Date de début'], left=row['Date de début'])
    
    plt.xlabel('Heures')
    plt.title('Frise Chronologique des Créneaux Disponibles')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.show()

creneaux_disponibles('ADECalsea15.csv', pd.to_datetime('2022-01-01'))

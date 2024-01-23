import subprocess
from tqdm import tqdm

def retrieve_data():
    print("Suppression des anciens fichiers dans le dossier de données externe...")
    subprocess.run(['powershell', '-Command', 'Remove-Item ../../data/external/* -Recurse -Force'])
    
    print("Téléchargement des fichiers CSV pertinents depuis Kaggle...")
    # Utilisation de tqdm pour afficher une barre de progression
    with tqdm(total=100, unit='B', unit_scale=True, desc="Téléchargement") as pbar:
        subprocess.run(['kaggle', 'competitions', 'download', '-c', 'home-credit-default-risk', '-p', '../../data/external/'],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        pbar.update(100)
    
    print("Extraction des fichiers ZIP dans le dossier de données externe...")
    subprocess.run(['powershell', '-Command',
                    'Expand-Archive ../../data/external/home-credit-default-risk.zip -DestinationPath ../../data/external/'])
    
    print("Suppression du fichier ZIP téléchargé...")
    subprocess.run(['powershell', '-Command', 'rm ../../data/external/home-credit-default-risk.zip'])


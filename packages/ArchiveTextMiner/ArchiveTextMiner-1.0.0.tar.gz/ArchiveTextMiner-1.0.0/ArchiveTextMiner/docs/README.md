![Logo](media\ArchiveTextMiner_logo.png?raw=true "Title")

<a href="#english-text" style="color: grey;">English text below</a>

## ArchiveTextMiner 
### :memo: Overzicht 
ArchiveTextMiner is een tool die specifiek is ontworpen om tekstuele informatie uit PDF-bestanden te halen en metadata te creëren. De tool reinigt en verwerkt de tekst per bestand en genereert gestructureerde XML-bestanden met metadata in MDTO-formaat. Het primaire doel is om ongestructureerde gegevens om te zetten in gestructureerde metadata, waardoor doorzoekbaarheid wordt verbeterd.

### :fire: Kenmerken

1. **Verwerking van meerdere bestanden:** ArchiveTextMiner kan meerdere PDF-bestanden binnen een  gecomprimeerde map verwerken. 

2. **Bestandsextractie en voorbereiding:** De tool begint met het extraheren van bestanden uit de invoermap en creëert een nieuwe mappenstructuur waarin de invoerbestanden en metadatabestanden kunnen worden bewaard.

3. **Metadata-opslag:** De tool creëert een map genaamd ArchiveTextMiner, voor het opslaan van metagegevensbestanden, zodat er een goed georganiseerd opslagsysteem is voor de verwerkte gegevens.

4. **Identificatie van PDF-bestanden:** De tool identificeert alle PDF-bestanden op die zich bevinden binnen de geëxtraheerde bestanden, zodat ze gereed zijn voor verdere verwerking.

5. **Tekstextractie uit PDF's:** De tool haalt tekstinhoud uit elk geïdentificeerd PDF-bestand met behulp van de `extract_text_from_pdf` functie.

6. **Tekst opschonen:** De geëxtraheerde tekst ondergaat een opschoningsproces (`clean_dutch_text`) om het voor te bereiden op verdere analyse.

7. **MDTO Metadata-genereren:** De gegenereerde metadata wordt geplaatst in een MDTO-schema (Metadata voor Duurzame Toegankelijke Overheidsinformatie), waardoor naleving van Nederlandse overheidsrichtlijnen wordt gewaarborgd. Momenteel kunnen de hieronder gespecificeerde metagegevensvelden worden gegenereerd. Als er geen geschikte informatie wordt gevonden in het document, blijft het betreffende gegevensveld leeg.

   - **Genereren van werktitel:** Genereert een werktitel uit de gereinigde tekst (`generate_working_title`).
   - **Herkenning van bestandsgrootte:** De tool berekent de grootte van het PDF-bestand in bytes (`generate_size`).
   - **Taalherkenning:** De tool identificeert de taal van de tekst (`detect_language`).
   - **Samenvatting genereren:** De tool vat de tekstinhoud samen in één zin (`generate_summary`).
   - **Extractie van topzoekwoorden:** De tool haalt topzoekwoorden uit de tekst (`extract_top_keywords`).
   - **KVK-nummerextractie:** Identificeert KVK-nummers binnen de tekst (`extract_kvk_numbers`).
   - **BSN-extractie:** Haalt geldige BSN (Burgerservicenummer) uit de tekst (`extract_valid_bsn_numbers`).
   - **Identificatie van MIME-type:** Bepaalt het MIME-type van het bestand (`get_file_mime_type`).

8. **Creatie van XML-bestanden:** Met behulp van de geëxtraheerde metadata genereert de tool XML-bestanden in MDTO-formaat voor elk PDF-bestand, waarin de afgeleide informatie is opgenomen.

9. **Geschreven in Python:** De tool is flexibel en eenvoudig integreerbaar in bestaande workflows of aanpasbaar volgens individuele vereisten.

### 🖥️ Benodigdheden
```
click==8.1.7
colorama==0.4.6
joblib==1.3.2
langdetect==1.0.9
nltk==3.8.1
numpy==1.26.3
PyPDF2==3.0.1
python-magic-bin==0.4.14
regex==2023.12.25
scikit-learn==1.3.2
scipy==1.11.4
setuptools==69.0.3
six==1.16.0
threadpoolctl==3.2.0
tqdm==4.66.1
```
### 💿 Installatie
1. Kopieer de repository (gehele package opslag).
2. Installeer de benodigde Python bibliotheken met pip:
   
    ```
    pip install ArchiveTextMiner
    ```

### 👩‍💻 Gebruik
1. Voer de tool uit door `ArchiveTextMiner` in de opdrachtprompt te 'runnen' en volg de stappen die op het scherm verschijnen:

- Plaats de bestanden die u wilt verwerken in een nieuwe map. Tip: gebruik bij voorkeur kopieën van de bestanden om verplaatsing te voorkomen.
- Comprimeer de map naar een ZIP-bestand.
- Verplaats het gezipte bestand naar de 'input'-map binnen de ArchiveTextMiner-directory. Hierdoor weet ArchiveTextMiner waar de bestanden zich bevinden.
- Kopieer het pad naar het ZIP-bestand, dat er ongeveer zo uitziet: `input\map.zip` en plak het hieronder.
- Druk op Enter. ArchiveTextMiner begint dan met het genereren van de metagegevensbestanden.

### 👨‍🏫 Voorbeeld 
```
python ArchiveTextMiner


     _             _     _          _____         _   __  __ _
    / \   _ __ ___| |__ (_)_   ____|_   _|____  _| |_|  \/  (_)_ __   ___ _ __
   / _ \ | '__/ __| '_ \| \ \ / / _ \| |/ _ \ \/ / __| |\/| | | '_ \ / _ \ '__|
  / ___ \| | | (__| | | | |\ V /  __/| |  __/>  <| |_| |  | | | | | |  __/ |
 /_/   \_\_|  \___|_| |_|_| \_/ \___||_|\___/_/\_ \__|_|  |_|_|_| |_|\___|_|



Welkom bij ArchiveTextMiner. Volg deze stappen om de tool te gebruiken:

1. Plaats de bestanden die u wilt verwerken in een nieuwe map. Tip: gebruik bij voorkeur kopieën van de bestanden om verplaatsing te voorkomen.
2. Comprimeer de map naar een ZIP-bestand.
3. Verplaats het gezipte bestand naar de 'input'-map binnen de ArchiveTextMiner-directory. Hierdoor weet ArchiveTextMiner waar de bestanden zich bevinden.
4. Kopieer het pad naar het ZIP-bestand, dat er ongeveer zo uitziet: `input\map.zip` en plak het hieronder.
5. Druk op Enter.

Voer de padnaam van het ZIP-bestand in: input\map.zip

ArchiveTextMiner starten...

Let op: De tekst in het veld 'omschrijving' is gegenereerd door kunstmatige intelligentie (AI). De betrouwbaarheid van de inhoud kan niet worden gegarandeerd; deze is enkel bedoeld voor de verrijking van metadata.

Bezig met uitpakken van input\map.zip naar input\map...

Uitpakken afgerond.

PDF-bestanden uitpakken in input\test...

Bestanden ['Bestand-A.pdf', 'Bestand-B.pdf', 'Bestand-C.pdf'] gevonden.
Bezig met creëren metadata bestanden...

Bestand-A.pdf.xml succesvol gecreëerd.
Bestand-B.pdf.xml succesvol gecreëerd.
Bestand-C.pdf.xml succesvol gecreëerd.

Metadatabestanden opgeslagen in inputmap.

ArchiveTextMiner afgerond.

```

### 🔑 Licentie
Deze tool wordt vrijgegeven onder de [European Union Public Licence V. 1.2](license).

### Bijdragen
ArchiveTextMiner is een actief project. Bijdragen van gebruikers zijn daarom welkom.

- **Bugmeldingen:** Als u problemen of bugs tegenkomt tijdens het gebruik van ArchiveTextMiner, open dan een probleem op onze GitHub-repository. Zorg ervoor dat u gedetailleerde informatie over het opgetreden probleem en de stappen om het te reproduceren, opneemt.

- **Functieverzoeken:** Suggesties kunnen worden ingediend via GitHub-issues als u ideeën hebt voor een nieuwe functie of verbetering.

- **Pull-requests:** Bijdragen in de vorm van pull-requests worden op prijs gesteld.

### 🔮 Toekomstige stappen
Om de tool te optimaliseren, werken we aan nieuwe toepassingen en functionaliteiten voor ArchiveTextMiner. We zijn momenteel bezig met:

- Toevoegen van meer MDTO-velden.

In de toekomst staan de volgende stappen gepland:

- Verbetering van functionaliteit om MDTO-velden aan te vullen (niet alleen genereren, maar ook bestaande metagegevens aanvullen).
- Mogelijkheid van het instellen welke MDTO-velden vereist zijn om te genereren.
- Integratie in processen en applicaties.

### ❕ Disclaimer
ArchiveTextMiner maakt gebruik van open-source modellen die zijn samengevoegd voor het extractie- en conversieproces. Hoewel aanzienlijke inspanningen zijn geleverd om nauwkeurigheid te waarborgen, wordt benadrukt dat de prestaties van de tool kunnen variëren op basis van de aard en kwaliteit van de invoergegevens. De nauwkeurigheid en geschiktheid van de geëxtraheerde gegevens zijn de exclusieve verantwoordelijkheid van de gebruikers. De functionaliteit van de tool berust op modellen en algoritmen die open-source zijn en onderhevig zijn aan mogelijke beperkingen, vooroordelen of onnauwkeurigheden die inherent zijn aan dergelijke modellen. Het wordt ten zeerste aanbevolen dat gebruikers de geëxtraheerde gegevens verifiëren en valideren tegen de originele bronmaterialen of door passende middelen om de nauwkeurigheid en geschiktheid voor hun beoogde doeleinden te waarborgen.

De ontwikkelaars en bijdragers van ArchiveTextMiner wijzen alle garanties of garanties met betrekking tot de nauwkeurigheid, volledigheid of betrouwbaarheid van de geëxtraheerde gegevens af. Gebruikers worden aangemoedigd om hun discretie en beoordelingsvermogen te gebruiken bij het gebruik van de tool en de output voor kritieke of gevoelige toepassingen.

### 🖋️ Auteurs
- [Muriël Valckx](https://github.com/murielvalckx)
- [Simon Pouwelse](https://github.com/simonpouwelse)

### 👍 Dankwoord
We uiten onze oprechte dank aan de ontwikkelaars van de open-source modellen en bibliotheken die in ArchiveTextMiner worden gebruikt en aan de bredere open-source gemeenschap, voor het bevorderen van samenwerking en innovatie.

© Zeeuws Archief and Provincie Zeeland - Alle rechten voorbehouden.

<img src="media/ArchiveTextMiner_favicon.png" alt="Favicon" title="Titel" width="40" height="40" />

## <a name="#english-text"></a> ArchiveTextMiner (English)

### :memo: Overview 
ArchiveTextMiner is a tool specifically designed to extract and convert textual information from PDF files contained within a compressed (zipped) folder. This tool automates the extraction of text from PDF files, cleans and processes the text, and generates structured XML files containing metadata in MDTO-format, derived from the extracted content. Its primary objective is to transform unstructured data into structured metadata, enhancing searchability.

### :fire: Features

1.  **Processing multiple files:** ArchiveTextMiner handles multiple PDF files within a single compressed folder, making it convenient for batch processing.

2. **File extraction and preparation:** The tool starts by extracting files from the provided zipped folder and creates a designated folder structure for further processing.

3. **Metadata storage:** It establishes an output folder structure for storing metadata files, ensuring a well-organized storage system for the processed data.

4. **Identification of PDF files:** The tool identifies and lists all PDF files found within the extracted files, preparing them for subsequent processing.

5. **Text extraction from PDFs:** It extracts text content from each identified PDF file using the `extract_text_from_pdf` function.

6. **Text cleaning:** The extracted Dutch text undergoes a cleaning process (`clean_dutch_text`) to prepare it for further analysis.

7. **MDTO Metadata Generation:** The metadata that is generated is placed in an MDTO-schema (Metadata for Sustainable Accessible Government Information), ensuring compliance with Dutch government guidelines. Currently, the metadata fields specified below can be generated. If no suitable information is found in the document, the respective metadata field will remain empty.
   
   - **Working title generation:** It generates a working title from the cleaned text (`generate_working_title`).
   - **File size extraction:** The tool determines the size of the PDF file (`generate_size`).
   - **Language detection:** It identifies the language of the text (`detect_language`).
   - **Summary extraction:** Summarizes the text content (`generate_summary`).
   - **Top keywords extraction:** Extracts top keywords from the text (`extract_top_keywords`).
   - **KVK-numbers extraction:** Identifies KVK numbers within the text (`extract_kvk_numbers`).
   - **BSN extraction:** Extracts valid BSN (Burgerservicenummer) from the text (`extract_valid_bsn_numbers`).
   - **MIME type identification:** Determines the MIME type of the PDF file (`get_file_mime_type`).

8. **XML file creation:** Using the extracted metadata, it generates XML files in MDTO format for each PDF, incorporating the derived information. 

9.  **Python-based:** The tool is flexible and easily integratable into existing workflows or adaptable according to individual requirements.

### 🖥️ Requirements
```
click==8.1.7
colorama==0.4.6
joblib==1.3.2
langdetect==1.0.9
nltk==3.8.1
numpy==1.26.3
PyPDF2==3.0.1
python-magic-bin==0.4.14
regex==2023.12.25
scikit-learn==1.3.2
scipy==1.11.4
setuptools==69.0.3
six==1.16.0
threadpoolctl==3.2.0
tqdm==4.66.1
```

### 💿 Installation
1. Clone the repository.
2. Install the required Python libraries using pip:
    ```
    pip install ArchiveTextMiner
    ```

### 👩‍💻 Usage
1.  Run the tool by executing `ArchiveTextMiner` in the command prompt and follow the steps that appear on the screen:
   
- Place the files you want to process in a new folder. Tip: preferably use copies of the files to prevent accidental movement.
- Compress the folder into a ZIP file.
- Move the zipped file to the 'input' folder within the ArchiveTextMiner directory. This allows ArchiveTextMiner to locate the files.


1. Copy the path to the ZIP file, which should look something like: `input\folder.zip`, and type it into the command prompt. 
2. Press Enter. ArchiveTextMiner will start generating the metadata files. 

### 👨‍🏫 Example (in Dutch)
```
python ArchiveTextMiner


     _             _     _          _____         _   __  __ _
    / \   _ __ ___| |__ (_)_   ____|_   _|____  _| |_|  \/  (_)_ __   ___ _ __
   / _ \ | '__/ __| '_ \| \ \ / / _ \| |/ _ \ \/ / __| |\/| | | '_ \ / _ \ '__|
  / ___ \| | | (__| | | | |\ V /  __/| |  __/>  <| |_| |  | | | | | |  __/ |
 /_/   \_\_|  \___|_| |_|_| \_/ \___||_|\___/_/\_ \__|_|  |_|_|_| |_|\___|_|



Welkom bij ArchiveTextMiner. Volg deze stappen om de tool te gebruiken:

1. Plaats de bestanden die u wilt verwerken in een nieuwe map. Tip: gebruik bij voorkeur kopieën van de bestanden om verplaatsing te voorkomen.
2. Comprimeer de map naar een ZIP-bestand.
3. Verplaats het gezipte bestand naar de 'input'-map binnen de ArchiveTextMiner-directory. Hierdoor weet ArchiveTextMiner waar de bestanden zich bevinden.
4. Kopieer het pad naar het ZIP-bestand, dat er ongeveer zo uitziet: `input\map.zip` en plak het hieronder.
5. Druk op Enter.

Voer de padnaam van het ZIP-bestand in: input\map.zip

ArchiveTextMiner starten...

Let op: De tekst in het veld 'omschrijving' is gegenereerd door kunstmatige intelligentie (AI). De betrouwbaarheid van de inhoud kan niet worden gegarandeerd; deze is enkel bedoeld voor de verrijking van metadata.

Bezig met uitpakken van input\map.zip naar input\map...

Uitpakken afgerond.

PDF-bestanden uitpakken in input\test...

Bestanden ['Bestand-A.pdf', 'Bestand-B.pdf', 'Bestand-C.pdf'] gevonden.
Bezig met creëren metadata bestanden...

Bestand-A.pdf.xml succesvol gecreëerd.
Bestand-B.pdf.xml succesvol gecreëerd.
Bestand-C.pdf.xml succesvol gecreëerd.

Metadatabestanden opgeslagen in inputmap.

ArchiveTextMiner afgerond.

```

### 🔑 License
This tool is released under the [European Union Public Licence V. 1.2](license).

### Contributions
ArchiveTextMiner is an actively evolving project that welcomes contributions from users. 

- **Bug reports:** If you encounter any issues or bugs while using ArchiveTextMiner, please open an issue on our GitHub repository. Be sure to include detailed information about the problem encountered and steps to reproduce it.

- **Feature requests:** Feel free to submit suggestions via GitHub issues if you have an idea for a new feature or enhancement. 

- **Pull requests:** Contributions in the form of pull requests are appreciated. 

### 🔮 Future steps
To optimize the tool, we are working on new applications and functionalities for ArchiveTextMiner. We are currently working on:

- Adding more MDTO fields.

In the future, the following steps are planned:

- Enhancing functionality to supplement MDTO fields (not just generating but also supplementing existing metadata).
- Configuring which MDTO fields are required for completion.
- Integration into processes and applications.

### ❕  Disclaimer
ArchiveTextMiner utilizes open-source models that are concatenated for the extraction and conversion process. While considerable effort has been made to ensure accuracy, users are advised that the tool's performance may vary based on the nature and quality of the input data. The accuracy and suitability of the extracted data are the sole responsibility of the users. The tool's functionality relies on models and algorithms that are open-source and subject to potential limitations, biases, or inaccuracies inherent in such models. It's highly recommended that users verify and validate the extracted data against the original source materials or through appropriate means to ensure its accuracy and suitability for their intended purposes.

The developers and contributors of ArchiveTextMiner disclaim any warranties or guarantees regarding the accuracy, completeness, or reliability of the extracted data. Users are encouraged to exercise their discretion and judgment when utilizing the tool and its output for any critical or sensitive applications.

### 🖋️ Authors
- [Muriël Valckx](https://github.com/murielvalckx)
- [Simon Pouwelse](https://github.com/simonpouwelse)


### 👍 Acknowledgments
We express our sincere gratitude to the developers of the open-source libraries used in ArchiveTextMiner and the broader open-source community for fostering collaboration and innovation.

 © Zeeuws Archief and Provincie Zeeland - All rights reserved. 
 
 <img src="media/ArchiveTextMiner_favicon.png" alt="Favicon" title="Title" width="40" height="40" />


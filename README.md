# Datu struktūras projekts

## Projekta uzdevums

Šī projekta mērķis ir izstrādāt automatizētu risinājumu Sportland pārdevējiem, kas ietver:
1. Web scraper, kas automātiski iegūst aktuālo produktu informāciju no Sportland mājas lapas
2. Datu strukturēšanu un saglabāšanu `.xlsx` formātā
3. Discord botu kā ērtu lietotāja saskarni datu piekļuvei

Risinājums aizstāj manuālu produktu meklēšanu ar automatizētu sistēmu, ievērojami samazinot laiku, kas nepieciešams, lai atrastu informāciju par produktiem.

## Izmantotās bibliotēkas

**Selenium**

Lai izstrādātu "web scraper" es izmantoju *Selenium* bibliotēku, jo
- Sportland mājas lapa izmanto JavaScript, lai dinamiski renderētu saturu
- Selenium spēj simulēt reāla lietotāja darbības (klikšķi, scrolling, u.c.)
- Var gaidīt līdz elementi ielādējas, kas ir būtiski dinamiskām lapām
- Spēj apstrādāt modernās web tehnoloģijas
- Nodrošina iespēju apiet vienkāršas anti-bot aizsardzības

**webdriver-manager**

Automātiski lejupielādē un pārvalda pārlūka draiverus priekš Selenium
- Nodrošina pareizo draiveru versiju atbilstoši pārlūka versijai
- Automātiski atjaunina draiverus, kad nepieciešams
- Darbojas uz visām operētājsistēmām bez papildus konfigurācijas

**openpyxl**

Tiek izmantots, lai ģenerētu `.xlsx` ar produktu informāciju
- Ļauj formatēt šūnas un pielāgot kolonnu platumu
- Saglabā datu tipus un formātus
- Kalpo kā datubāze produktu informācijas glabāšanai

**discord.py**

Tiek izmantots Discord bota izstrādei ar šādām funkcijām
- `/search <produkta_kods>` - meklē konkrētu produktu pēc tā koda
- `/list [lapas_numurs]` - parāda produktu sarakstu (max 20 produkti lapā)
- Formatēti ziņojumi ar embed funkcionalitāti
- Kļūdu apstrāde un lietotājam draudzīgi paziņojumi

**pandas**

Nodrošina efektīvu datu apstrādi Discord botā
- Excel failu lasīšana un datu strukturēšana
- Ātra meklēšana un filtrēšana lielā datu kopā
- Datu manipulācijas operācijas
- Automātiska datu tipu konvertācija

**python-dotenv**

Nodrošina drošu konfigurācijas pārvaldību
- Discord bota token glabāšana ārpus koda
- Viegla vides mainīgo pārvaldība
- Droša izstrādes un produkcijas vides konfigurācija

## Projekta izmantošanas metodes

Šī ideja man radās, jo mans draugs strādā Sportland par pārdevēju un pēdējo reizi, kad tikāmies man stāstīja, ka viņam darbā ir jāiet Sportland mājas lapā un jāmeklē informācija par produktiem manuāli, kas aizņem daudz laiku, tādēļ man radās ideja to automatizēt un pie reizes izpalīdzēt draugam.

Nepieciešamā informācija par produktiem ir tā nosaukums, cena, produkta kods, zīmols un pieejamie izmēri.

Kā arī, lai to padarītu vienkārši izmantojamu tika izstrādāts Discord bots ar divām komandām `/search` , kas ļauj atrast informāciju par produktu pēc produkta koda un `/list` , kas parāda visus pieejamos produktus pēc to produkta koda un nosaukuma.

Projekta izstrādes laikā es konsultējos ar Sportland pārdevēju, lai precizētu kāda informācija ir nepieciešama un kāds būtu viņam ērtākais veids to izmantot.

Šobrīd šis projekts spēj nodrošināt produktu informācijas meklēšanu tikai vīriešu apaviem, bet kods ir izstrādāts tā, lai tas būtu universāls un atbilstošs visai mājas lapas struktūrai, kas nozīmē ka ar šo pašu kodu ievietojot atbilstošās kategorijas saiti ir iespējams arī iegūt informāciju par citām produktu kategorijām.

## Projekta demo

*Ģenerētais `.xlsx` fails*

[https://screen.studio/share/w8N9nY7K](https://screen.studio/share/w8N9nY7K)

*`/search` komanda Discordā*

![search-discord.png](/images/search-discord.png)

*`/list` komanda Discordā*

![list-discord.png](/images/list-discord.png)

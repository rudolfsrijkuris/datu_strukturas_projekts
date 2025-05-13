# Datu struktūras projekts

## Projekta uzdevums

Šī projekta mērķis ir izstrādāt “web scraper”, kas iegūst produktu informāciju no Sportland mājas lapas un saglabā to `.xlsx` failā, lai to varētu izmantot Sportland pārdevēji sava darba atvieglošanai.

## Izmantotās bibliotēkas

**Selenium**

Lai izstrādātu “web scraper” es izmantoju *Selenium* bibliotēku, jo Sportland mājas lapa izmanto JavaScript, lai dinamiski renderētu mājas lapas saturu. Mana izvēle bija par labu Selenium, jo tas izmanto reālu pārlūku un simulē reālu mājas lapas lietotāju, lai veiktu “web scraping”, kas šajā gadījumā nebūtu iespējams ar parastiem HTTP pieprasījumiem.

**webdriver-manager**

Automātiski lejupielādē pareizos pārlūka draiverus priekš Selenium, izvairoties no to manuālas menedžēšanas.

**openpyxl**

Tiek izmantots, lai ģenerētu `.xlsx` ar produktu informāciju. Šajā gadījumā `.xlsx` fails tiek izmantots kā datubāze.

**discord.py**

Tiek izmantots, lai izveidotu Discord botu un nodrošinātu lietotāju saskarni ar datubāzi.

**pandas**

Tiek izmantots iekš Discord bota, lai nodrošinātu datu iegūšanu un apstrādi no `.xlsx` faila.

**python-dotenv**

Tiek izmantots, lai droši glabātu Discord bota token lokālā vidē.

## Projekta izmantošanas metodes

Šī ideja man radās, jo mans draugs strādā Sportland par pārdevēju un pēdējo reizi, kad tikāmies man stāstīja, ka viņam darbā ir jāiet Sportland mājas lapā un jāmeklē informācija par produktiem manuāli, kas aizņem daudz laiku, tādēļ man radās ideja to automatizēt un pie reizes izpalīdzēt draugam.

Nepieciešamā informācija par produktiem ir tā nosaukums, cena, produkta kods, zīmols un pieejamie izmēri.

Kā arī, lai to padarītu vienkārši izmantojamu tika izstrādāts Discord bots ar divām komandām `/search` , kas ļauj atrast informāciju par produktu pēc produkta koda un `/list` , kas parāda visus pieejamos produktus pēc to produkta koda un nosaukuma.

Projekta izstrādes laikā es konsultējos ar Sportland pārdevēju, lai precizētu kāda informācija ir nepieciešama un kāds būtu viņam ērtākais veids to izmantot.

Šobrīd šis projekts spēj nodrošināt produktu informācijas meklēšanu tikai vīriešu apaviem, bet kods ir izstrādāts tā, lai tas būtu universāls un atbilstošs visai mājas lapas struktūrai, kas nozīmē ka ar šo pašu kodu ievietojot atbilstošās kategorijas saiti ir iespējams arī iegūt informāciju par citām produktu kategorijām.

## Projekta demo

*Ģenerētais `.xlsx` fails*

[https://screen.studio/share/w8N9nY7K](https://screen.studio/share/w8N9nY7K)

`*/search` komanda Discordā*

![image.png](Datu%20struktu%CC%84ras%20projekts%201f241c33ee738054b39fd29305b4c511/image.png)

`*/list` komanda Discordā*

![image.png](Datu%20struktu%CC%84ras%20projekts%201f241c33ee738054b39fd29305b4c511/image%201.png)

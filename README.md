# 🤖 Automaattinen hankintaprosessi - Interaktiivinen demo

**Live-demo:** https://jgmikael.github.io/procurement-automation-demo/

Interaktiivinen visualisointi täysin automatisoitavasta julkisten hankintojen prosessista – tarpeesta maksuun ilman manuaalista työtä.

## 🎯 Mitä tämä on?

Tämä demo näyttää miten julkiset hankinnat voivat toimia tulevaisuudessa kun yhdistetään:

- **EU Business Wallet** - Yritysten digitaalinen identiteetti ja todisteet
- **W3C Verifiable Credentials** - Luotettavat, kryptografisesti vahvistetut todistukset
- **Digitaaliset mandaatit** - Selkeät toimivaltuudet ihmisille ja AI-agenteille
- **Semanttiset tietomallit** - Yhteinen kieli hankintojen kaikille osapuolille
- **Deterministiset sääntökoneet** - Läpinäkyvät, auditoitavat automaattiset tarkastukset
- **AI-agentit** - Älykäs orkestrointi ja päätöstuki

## 📋 Prosessin 10 vaihetta

### 1. Hankinnan valmistelu
- AI-agentti analysoi aiemmat hankinnat
- Ehdottaa hankintamenettelyä
- Generoi rakenteisen tarjouspyyntöluonnoksen

### 2. Rakenteinen tarjouspyyntö
- Soveltuvuusvaatimukset koneluettavassa muodossa
- Jokaiselle vaatimukselle määritetty: todiste, myöntäjä, voimassaolo, sääntö
- Vertailuperusteet matemaattisesti ilmaistuna

### 3. Tarjoajan tunnistus ja lompakko
- Tarjoajan agentti löytää sopivat hankinnat HILMA-rajapinnasta
- EU Business Wallet kokoaa todistukset eri myöntäjiltä
- Yritys antaa suostumuksen tietojen esittämiseen

### 4. Todisteiden esitys
- W3C Verifiable Credentials -standardin mukaiset todistukset
- Kryptografinen allekirjoitus ja alkuperän vahvistus
- Mandaattiketju: henkilö → yritys → hankinta

### 5. Koneellinen kelpoisuustarkastus
- Deterministinen sääntökone tarkastaa vaatimukset
- Jokaisesta tarkastuksesta loggautuu: sääntö, data, tulos, aikaleima
- Ei tulkintaa – vain faktoja ja laskentaa

### 6. Tarjousten automaattinen vertailu
- Numeeriset kriteerit lasketaan kaavalla
- Vertailuperusteet: hinta, tekniset ominaisuudet, referenssit
- Selkeä pisteytys ja perustelut

### 7. Hankintapäätös
- Automaattisesti generoitu päätösluonnos
- **Ihmisen päätöspiste** – hankintayksikkö hyväksyy
- Kaikki perustelut jäljitettävissä

### 8. Sopimuksen muodostaminen
- Sopimusagentti kokoaa sopimuksen tarjouksesta ja päätöksestä
- Rakenteinen JSON-LD sopimusdata
- Velvoitteet muutetaan seurattaviksi mittareiksi

### 9. Toteutus, lasku ja maksu
- Tilaus-toimitus-lasku ketju (Peppol/EN 16931)
- Automaattinen kolmitäsmäytys (3-way match)
- Lasku hyväksytään jos kaikki täsmää sopimukseen

### 10. Audit Trail
- Täydellinen jäljitettävyys koko ketjussa
- Jokainen toimenpide: kuka, milloin, millä mandaatilla, millä säännöllä
- Mahdollistaa auditoinnin ja oikeusturvan

## 🔑 Keskeiset periaatteet

### Mandaattipohjainen automaatio
Jokainen toimenpide vaatii **digitaalisen mandaatin**:
- Kenellä on oikeus tehdä tämä?
- Minkä organisaation puolesta?
- Missä rahallisissa/oikeudellisissa rajoissa?
- Mihin päivään asti?

AI-agentti **ei voi** ylittää mandaattiaan.

### Ihmisen päätöspisteet säilyvät
Automaatio ei tarkoita ihmisen syrjäyttämistä. Ihmisen hyväksyntä **pakollinen** vähintään:
- Tarjouspyynnön hyväksyntä
- Hankintapäätös
- Sopimuksen allekirjoitus

Rutiinit (kelpoisuustarkastus, lasku) voidaan automatisoida.

### Deterministinen sääntökone
AI-mallia **ei käytetä** lakisääteisten ehtojen "tulkitsemiseen". Sen sijaan:
- Ehdot ilmaistaan selkeinä sääntöinä
- Sama syöte → aina sama tulos
- Tulos auditoitavissa ilman AI-mallia
- Kaikki perustelut jäljitettävissä

### Täydellinen jäljitettävyys
**Tavoite:** Yksittäinen ostolasku voidaan jäljittää sitä edeltäneeseen:
- Hankintailmoitukseen
- Tarjouspyyntöön
- Tarjoukseen
- Päätökseen
- Sopimukseen
- Tilaukseen
- Toimitukseen

## 🛠️ Teknologiat

- **EBWV** - EU Business Wallet Vocabulary (semanttinen perusta)
- **W3C VC** - Verifiable Credentials (todistukset)
- **DID** - Decentralized Identifiers (myöntäjien tunnistus)
- **JSON-LD** - Linkitetty data (semanttinen yhteentoimivuus)
- **SHACL** - Shapes Constraint Language (validointi)
- **eForms** - EU:n hankintatietojen standardi
- **Peppol** - Eurooppalainen e-laskutusverkko
- **EN 16931** - Eurooppalainen laskustandardi

## 📚 Liittyvät projektit

- **[EBWV Semantic Analysis](https://jgmikael.github.io/ebwv-semantic-analysis/)** - Semanttinen analyysi EU Business Wallet Vocabularystä

## 🚀 Käyttö

**Suora linkki:** https://jgmikael.github.io/procurement-automation-demo/

Demo toimii täysin selaimessa ilman asennuksia. Navigoi 10 vaiheen läpi painikkeilla ja katso miten automaatio toimii käytännössä.

## 📄 Lisenssi

CC BY 4.0 - Vapaasti käytettävissä, mainitse lähde.

## 👤 Tekijä

Mikael - Automatisoinnin ja semanttisten teknologioiden konsultointi

---

**Huom:** Tämä on konseptidemo. Todellinen toteutus vaatisi laajaa yhteistyötä viranomaisten, järjestelmätoimittajien ja EU-instituutioiden kanssa.

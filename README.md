# Astroveljekset – Vihreän meteoriitin mysteeri

Julkaisuvalmis, täysin staattinen HTML-sivusto kirjalle **Astroveljesten seikkailut, osa I: Vihreän meteoriitin mysteeri**. Sivustolla on kansi, alkusivu ja kaikki 25 lukua omilla osoitteillaan. Navigaatio toimii myös puhelimella, ja lukija voi vaihtaa vaalean ja tumman teeman välillä. Sivuilla ei ole ulkoisia skriptejä, evästeitä eikä palvelinpäässä ajettavaa sovellusta.

## Sisältö

- `index.html`: kirjan etusivu ja sisällysluettelo
- `chapters/`: “Lue ensin!” sekä 25 lukua HTML-muodossa
- `assets/`: tyyli, pieni JavaScript, kansikuva ja kuvake
- `source/book.md`: kirjan [alkuperäisen sivuston](https://astroveljekset.fi/) Markdown-vienti
- `build.py`: luo HTML-sivut uudelleen Markdownista

Teksti on ladattu 5.11.2026 julkisesta [kirjan Markdown-viennistä](https://books.yellowmineralindustries.com/2/vihrean-meteoriitin-mysteeri.md). Lukuja on 25, ja alkuperäisessä sisällysluettelossa on niiden lisäksi “Lue ensin!” -sivu. Kannen lähde on sama kirjasivusto. Tekstiä ei ole toimitettu tai lyhennetty HTML-versiota varten.

Kirjan tekijä on Janne K. Jääskeläinen. Sivustolla säilyy alkuperäisen julkaisun **CC BY-NC-ND 4.0** -merkintä. Se koskee kirjan tekstiä ja kantta.

## Esikatsele omalla koneella

Voit avata `index.html`-tiedoston selaimessa suoraan. Paikallisen palvelimen kautta esikatselu toimii näin:

```sh
cd astroveljekset-site
python3 -m http.server 8000
```

Avaa sitten `http://localhost:8000/`.

## Julkaise GitHub Pagesissa

1. Luo GitHubiin uusi repo ja lisää **tämän kansion sisältö** sen juureen. `index.html` pitää olla repon juuressa.
2. GitHubissa avaa **Settings → Pages**. Valitse **Deploy from a branch**, haara `main` ja kansio `/(root)`, sitten **Save**.
3. GitHub julkaisee valmiit HTML-sivut suoraan. `build.py`-skriptiä ei ajeta GitHubissa; sitä tarvitaan vain, jos kirjan lähdeteksti päivitetään.

Ohje vastaa [GitHubin Pages-julkaisuohjetta](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Sivuston linkit ovat suhteellisia, joten se toimii myös repon alihakemistossa (`käyttäjä.github.io/repo/`). `.nojekyll` varmistaa, että tiedostot julkaistaan sellaisinaan.

## Luo sivut uudelleen lähdetekstistä

```sh
python3 -m pip install -r requirements.txt
python3 build.py
```

Skripti tarkistaa, että Markdownissa on 25 lukua, ja luo etusivun sekä kaikki lukusivut uudelleen. Kansikuva on `assets/cover.png`; pienempi WebP-versio on `assets/cover.webp`.

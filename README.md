# Drzewo genealogiczne Bonisławskich

Strona o historii rodziny: Bonisławscy • Murzyńscy • Nowalscy • Adamczyk.
Każda para ma własną stronę, a menu (hamburger) pokazuje kafle od najmłodszego pokolenia do najstarszego.

## Struktura

| Ścieżka | Do czego służy |
| --- | --- |
| `dane/rodzina.json` | Dane wszystkich par (imiona, lata, rodzice, dzieci). Tu dodajesz nowe osoby. |
| `zasoby/styl.css`, `zasoby/strona.js` | Wygląd i działanie (menu, powiększanie zdjęć). |
| `zdjecia/` | Zdjęcia. Kopiowane na stronę jako `zdjecia/…`. |
| `skany/` | Skany aktów i dokumentów. Kopiowane jako `skany/…`. |
| `zbuduj.py` | Generator: z danych i wzoru tworzy wszystkie strony w `_site/`. |
| `.github/workflows/pages.yml` | Po każdym wgraniu zmian na `main` buduje stronę i publikuje na GitHub Pages. |

## Jak dodać parę

1. Dopisz wpis w `dane/rodzina.json` i wskaż `"rodzice"` u dziecka.
2. Wgraj zmiany na `main`. Strona zbuduje się i opublikuje sama (około minuty).

Podgląd lokalny: `python3 zbuduj.py`, potem otwórz `_site/index.html`.

## Ustawienia GitHub Pages (jednorazowo)

Settings → Pages → Build and deployment → Source: **GitHub Actions**.
Adres strony: `https://<login>.github.io/<nazwa-repozytorium>/`.

## Uwagi

- Teksty w nawiasach `[…]` to pola do uzupełnienia, w tym daty i miejsca.
- Daty z drzewa FamilySearch warto potwierdzić w aktach.

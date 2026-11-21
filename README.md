# Drzewo genealogiczne Bonisławskich

Strona o historii rodziny: Bonisławscy • Murzyńscy • Nowalscy • Adamczyk.
Każda para ma własną stronę, a menu (hamburger) pokazuje kafle od najmłodszego pokolenia do najstarszego.

## Struktura

| Ścieżka | Do czego służy |
| --- | --- |
| `dane/rodzina.json` | Dane wszystkich par (imiona, lata, rodzice, dzieci). Tu dodajesz nowe osoby. |
| `zasoby/styl.css`, `zasoby/strona.js` | Wygląd i działanie (menu, powiększanie zdjęć). |
| `zdjecia/` | Zdjęcia. Przy budowaniu kopiowane do `docs/zdjecia/`. |
| `skany/` | Skany aktów i dokumentów. Kopiowane do `docs/skany/`. |
| `zbuduj.py` | Generator: z danych i wzoru tworzy wszystkie strony w folderze `docs/`. |
| `docs/` | **Gotowa strona** (HTML). Tego folderu używa GitHub Pages. Nie edytuj ręcznie, bo zostanie nadpisany. |

## Jak zmienić stronę

1. Zmień dane w `dane/rodzina.json` (albo wygląd w `zasoby/`), dodaj zdjęcia do `zdjecia/` lub skany do `skany/`.
2. Zbuduj stronę lokalnie: `python3 zbuduj.py` (potrzebny tylko Python 3, bez dodatkowych pakietów).
3. Sprawdź wynik, otwierając `docs/index.html` w przeglądarce.
4. Zatwierdź i wypchnij razem ze zmianami w `docs/`:

```
git add -A
git commit -m "Opis zmiany"
git push
```

GitHub Pages odświeży stronę po około minucie.

## Ustawienia GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: **main**, folder: **/docs** → Save.
Adres strony: `https://<login>.github.io/<nazwa-repozytorium>/`.

## Jak dodać parę

Dopisz wpis w `dane/rodzina.json` i wskaż `"rodzice"` u dziecka. Menu i linki uzupełnią się same po zbudowaniu.

## Uwagi

- Teksty w nawiasach `[…]` to pola do uzupełnienia, w tym daty i miejsca.
- Daty z drzewa FamilySearch warto potwierdzić w aktach.

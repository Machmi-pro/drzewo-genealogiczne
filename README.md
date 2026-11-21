# Drzewo genealogiczne Bonisławskich

Strona o historii rodziny: Bonisławscy • Murzyńscy • Nowalscy • Adamczyk.
Każda para ma własną stronę, a menu (hamburger) pokazuje kafle od najmłodszego pokolenia do najstarszego.

## Struktura

Gotowa strona leży w katalogu głównym `main`, a pliki do jej tworzenia w folderze `zrodlo/`.

| Ścieżka | Do czego służy |
| --- | --- |
| `index.html` | Strona główna (Zofia i Bronisław). |
| `*.html` | Strony pozostałych par. Tworzone przez generator, nie edytuj ręcznie. |
| `styl.css`, `strona.js` | Wygląd i działanie strony. Kopiowane z `zrodlo/zasoby/`. |
| `zdjecia/` | Zdjęcia. Wrzucasz tu pliki i wstawiasz je na stronach. |
| `skany/` | Skany aktów i dokumentów. |
| `zrodlo/dane/rodzina.json` | Dane wszystkich par (imiona, lata, rodzice, dzieci). Tu dodajesz nowe osoby. |
| `zrodlo/zasoby/` | Oryginały `styl.css` i `strona.js`. Zmian wyglądu szukaj tutaj. |
| `zrodlo/zbuduj.py` | Generator: z danych i wzoru tworzy strony w katalogu głównym. |

## Jak zmienić stronę

1. Zmień dane w `zrodlo/dane/rodzina.json` (albo wygląd w `zrodlo/zasoby/`).
2. Zbuduj stronę lokalnie: `python3 zrodlo/zbuduj.py` (potrzebny tylko Python 3, bez dodatkowych pakietów).
3. Sprawdź wynik, otwierając `index.html` w przeglądarce.
4. Zatwierdź i wypchnij:

```
git add -A
git commit -m "Opis zmiany"
git push
```

GitHub Pages odświeży stronę po około minucie.

## Ustawienia GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: **main**, folder: **/ (root)** → Save.
Adres strony: `https://<login>.github.io/<nazwa-repozytorium>/`.

## Jak dodać parę

Dopisz wpis w `zrodlo/dane/rodzina.json` i wskaż `"rodzice"` u dziecka. Menu i linki uzupełnią się same po zbudowaniu.

## Jak dodać historię osoby lub pary (jak u Zofii)

Wzorem jest wpis `zofia-i-bronislaw` w `zrodlo/dane/rodzina.json`. Kolejne osoby dodaje się tak samo:

1. **Zdjęcia i skany**: wrzuć pliki do `zdjecia/` i `skany/` (najlepiej do 1600 px dłuższego boku, nazwy bez spacji, np. `jan-portret.jpg`).
2. **Dane osoby** (`"ona"` lub `"on"`): `ur_data`, `ur_miejsce`, `zm_data`, `zm_miejsce` oraz opcjonalnie `portret` (`plik`, `podpis`, `zrodlo`) dla głównego zdjęcia. Osoby bez `portret` nie mają ramki na zdjęcie profilowe (pokazują się tylko imię, lata i dane); same skany aktów i wycinki z gazet dodaje się w `tresc`. Pole `"puste_pomin": true` przy osobie ukrywa wiersze z nieznaną datą i miejscem zamiast pokazywać `[data]` / `[miejscowość]`.
3. **Treść** w polu `"tresc"`: lista rozdziałów (`tytul`, `lata`), a w nich historie (`tytul`, `elementy`). Elementy mogą być: `akapit`, `tekst_zastepczy`, `zdjecie` (`plik`, `podpis`, `zrodlo`, opcjonalnie `szeroko`) i `galeria` (lista zdjęć lub skanów z podpisami). Podpis i źródło pokazują się pod zdjęciem i w powiększeniu.
4. **Dzieci**: lista `"dzieci"`; `"dzieci_komplet": true` wyłącza puste karty do uzupełnienia.
5. Zbuduj (`python3 zrodlo/zbuduj.py`) i wypchnij zmiany.

Pary bez pola `"tresc"` dostają szablon z polami do uzupełnienia.

## Uwagi

- Teksty w nawiasach `[…]` to pola do uzupełnienia, w tym daty i miejsca.
- Daty z drzewa FamilySearch warto potwierdzić w aktach.
